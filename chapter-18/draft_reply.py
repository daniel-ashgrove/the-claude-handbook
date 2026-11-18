import json
import logging
import sys
from collections import Counter
from typing import Literal

import anthropic
from anthropic.types import Message, MessageParam, ToolResultBlockParam
from anthropic.types.message_create_params import MessageCreateParamsBase

from prompts import SYSTEM
from tools import TOOLS, run_tool

MODEL = "claude-sonnet-5-5"
Effort = Literal["low", "medium", "high", "xhigh", "max"]
MAX_ROUNDS = 6  # requests per ticket before the program gives up
log = logging.getLogger("drafter")
client = anthropic.Anthropic()

DRAFT_SCHEMA = {
    "type": "object",
    "properties": {
        "reply": {"type": "string",
                  "description": "The reply to send, signed The support team"},
        "order_number": {"type": "string",
                         "description": "The order the email is about, or empty"},
        "category": {"type": "string", "enum": [
            "where_is_my_order", "refund_or_return", "compliment", "other"]},
        "needs_person": {"type": "boolean", "description": (
            "True if someone on the team must decide or do something")},
        "note_for_team": {"type": "string", "description": (
            "One sentence for the person sending the reply, or empty")},
    },
    "required": ["reply", "order_number", "category", "needs_person",
                 "note_for_team"],
    "additionalProperties": False,
}


def request(messages: list[MessageParam], effort: Effort = "high",
            cache_ttl: Literal["5m", "1h"] = "5m") -> MessageCreateParamsBase:
    """Everything one request sends. Between requests, only the messages change."""
    return {
        "model": MODEL,
        "max_tokens": 4096,
        "tools": TOOLS,
        # Breakpoint 1: the tools and the system prompt, the same for every ticket.
        "system": [{"type": "text", "text": SYSTEM,
                    "cache_control": {"type": "ephemeral", "ttl": cache_ttl}}],
        "messages": messages,
        "output_config": {"effort": effort, "format": {
            "type": "json_schema", "schema": DRAFT_SCHEMA}},
        # Breakpoint 2: automatic, at the end of the conversation, round by round.
        "cache_control": {"type": "ephemeral", "ttl": cache_ttl},
    }


def first_message(ticket_id: str) -> MessageParam:
    return {"role": "user",
            "content": f"Draft a reply to support ticket {ticket_id}."}


def tool_results(message: Message, calls: list) -> list[ToolResultBlockParam]:
    """Run every tool call in Claude's turn and return the results for one message."""
    results: list[ToolResultBlockParam] = []
    for block in message.content:
        if block.type == "tool_use":
            content, failed = run_tool(block.name, block.input)
            calls.append((block.name, block.input, failed))
            results.append({"type": "tool_result", "tool_use_id": block.id,
                            "content": content, "is_error": failed})
    return results


def record(message: Message, totals: Counter[str]) -> None:
    """Log what one request used, and add it to the running totals."""
    u = message.usage
    used = {"uncached": u.input_tokens,
            "cache_write": u.cache_creation_input_tokens or 0,
            "cache_read": u.cache_read_input_tokens or 0,
            "output": u.output_tokens}
    totals.update(used)
    log.info("%s stop=%s %s", message.id, message.stop_reason,
             " ".join(f"{k}={v}" for k, v in used.items()))


def create(params: MessageCreateParamsBase) -> Message:
    message = client.messages.create(**params)
    log.info("%s request-id %s", message.id, message._request_id)
    return message


def draft(ticket_id: str, effort: Effort = "high",
          totals: Counter[str] | None = None, send=create):
    messages: list[MessageParam] = [first_message(ticket_id)]
    calls = []  # every tool call, for the log and the tests
    totals = Counter() if totals is None else totals
    for _ in range(MAX_ROUNDS):
        message = send(request(messages, effort))
        record(message, totals)
        if message.stop_reason == "end_turn":
            text = "".join(b.text for b in message.content if b.type == "text")
            return json.loads(text), calls
        if message.stop_reason != "tool_use":
            raise RuntimeError(f"No draft (stop_reason: {message.stop_reason})")
        # Claude's turn goes back exactly as it came, thinking blocks included.
        messages.append({"role": "assistant", "content": message.content})
        messages.append({"role": "user", "content": tool_results(message, calls)})
    raise RuntimeError(f"No draft after {MAX_ROUNDS} requests")


if __name__ == "__main__":
    if "--log" in sys.argv:  # show this program's log lines, not the libraries'
        logging.basicConfig(format="%(asctime)s %(name)s %(message)s")
        log.setLevel(logging.INFO)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    totals: Counter[str] = Counter()
    result, calls = draft(args[0] if args else "812", totals=totals)
    for name, tool_input, failed in calls:
        flag = "  (failed)" if failed else ""
        print(f"Tool call: {name} {json.dumps(tool_input)}{flag}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("Input tokens: {uncached} uncached, {cache_write} written to the cache, "
          "{cache_read} read from it. Output tokens: {output}".format(**totals))
