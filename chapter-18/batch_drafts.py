import json
import sys
import time

from anthropic.types import MessageParam
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

from draft_reply import MAX_ROUNDS, client, first_message, request, tool_results
from shop_data import TICKETS


def draft_backlog(ticket_ids: list[str]) -> tuple[dict[str, dict], dict[str, str]]:
    """One batch per round of the tool loop, for every ticket still in progress.
    Returns the drafts, and the tickets left for a person with the reason."""
    open_tickets: dict[str, list[MessageParam]] = {
        t: [first_message(t)] for t in ticket_ids}
    drafts: dict[str, dict] = {}
    unresolved: dict[str, str] = {}
    for round_number in range(1, MAX_ROUNDS + 1):
        if not open_tickets:
            break
        batch = client.messages.batches.create(requests=[
            Request(custom_id=f"ticket-{t}", params=MessageCreateParamsNonStreaming(
                **request(messages, cache_ttl="1h")))
            for t, messages in open_tickets.items()])
        print(f"Round {round_number}: {batch.id}, {len(open_tickets)} request(s)")
        while batch.processing_status != "ended":
            time.sleep(60)
            batch = client.messages.batches.retrieve(batch.id)
        for item in client.messages.batches.results(batch.id):
            ticket_id = item.custom_id.removeprefix("ticket-")
            result = item.result
            if result.type == "succeeded":
                message = result.message
                if message.stop_reason == "tool_use":
                    messages = open_tickets[ticket_id]
                    messages.append({"role": "assistant", "content": message.content})
                    messages.append({"role": "user",
                                     "content": tool_results(message, [])})
                    continue
                if message.stop_reason == "end_turn":
                    text = "".join(b.text for b in message.content
                                   if b.type == "text")
                    drafts[ticket_id] = json.loads(text)
                else:
                    unresolved[ticket_id] = f"stopped: {message.stop_reason}"
            elif result.type == "errored":
                error_type = result.error.error.type
                if error_type != "invalid_request_error":
                    continue  # failed on Anthropic's side: send it again next round
                unresolved[ticket_id] = f"errored: {error_type}"
            else:
                unresolved[ticket_id] = result.type  # canceled or expired
            del open_tickets[ticket_id]
    for ticket_id in open_tickets:  # still waiting when the rounds ran out
        unresolved[ticket_id] = f"no draft after {MAX_ROUNDS} rounds"
    return drafts, unresolved


if __name__ == "__main__":
    drafts, unresolved = draft_backlog(sys.argv[1:] or list(TICKETS))
    with open("drafts.json", "w", encoding="utf-8") as f:
        json.dump(drafts, f, indent=2, ensure_ascii=False)
    with open("unresolved.json", "w", encoding="utf-8") as f:
        json.dump(unresolved, f, indent=2)
    print(f"{len(drafts)} drafts saved to drafts.json for the team to review")
    for ticket_id, reason in unresolved.items():
        print(f"  {ticket_id}: {reason}, left for a person")
    sys.exit(1 if unresolved else 0)  # a ticket left over is something to look at
