import json
import sys
from typing import Literal

import anthropic
from anthropic.types import MessageParam, ToolResultBlockParam

from prompts import SYSTEM
from tools import TOOLS, run_tool

MODEL = "claude-sonnet-5-5"
Effort = Literal["low", "medium", "high", "xhigh", "max"]
MAX_ROUNDS = 6  # requests before the program gives up, the final one included
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


def draft(ticket_id: str, effort: Effort = "high"):
    messages: list[MessageParam] = [
        {"role": "user", "content": f"Draft a reply to support ticket {ticket_id}."}
    ]
    calls = []  # every tool call, for the log and the tests
    for _ in range(MAX_ROUNDS):
        message = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM,
            tools=TOOLS,
            messages=messages,
            output_config={"effort": effort, "format": {
                "type": "json_schema", "schema": DRAFT_SCHEMA}},
        )
        if message.stop_reason == "end_turn":
            text = "".join(b.text for b in message.content if b.type == "text")
            return json.loads(text), calls
        if message.stop_reason != "tool_use":
            raise RuntimeError(f"No draft (stop_reason: {message.stop_reason})")
        # Claude's turn goes back exactly as it came, thinking blocks included.
        messages.append({"role": "assistant", "content": message.content})
        results: list[ToolResultBlockParam] = []
        for block in message.content:
            if block.type == "tool_use":
                content, failed = run_tool(block.name, block.input)
                calls.append((block.name, block.input, failed))
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": content, "is_error": failed})
        messages.append({"role": "user", "content": results})  # all results at once
    raise RuntimeError(f"No draft after {MAX_ROUNDS} requests")


if __name__ == "__main__":
    result, calls = draft(sys.argv[1] if len(sys.argv) > 1 else "812")
    for name, args, failed in calls:
        flag = "  (failed)" if failed else ""
        print(f"Tool call: {name} {json.dumps(args)}{flag}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
