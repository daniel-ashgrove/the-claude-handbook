import sys

from anthropic.types import Message
from anthropic.types.message_create_params import MessageCreateParamsBase

from draft_reply import client, draft, log


def send_streamed(params: MessageCreateParamsBase) -> Message:
    """Like client.messages.create(), but shows each block as it arrives."""
    with client.messages.stream(**params) as stream:
        for event in stream:
            if event.type == "content_block_start":
                block = event.content_block
                if block.type == "thinking":
                    print("[thinking]", flush=True)
                elif block.type == "tool_use":
                    print(f"[calling {block.name}]", flush=True)
            elif event.type == "text":
                print(event.text, end="", flush=True)
        message = stream.get_final_message()
    if any(b.type == "text" for b in message.content):
        print()  # end the line of streamed text
    log.info("%s request-id %s", message.id, stream.request_id)
    return message


if __name__ == "__main__":
    result, _ = draft(sys.argv[1] if len(sys.argv) > 1 else "812", send=send_streamed)
    print("\nThe reply, parsed from the finished JSON:\n" + result["reply"])
