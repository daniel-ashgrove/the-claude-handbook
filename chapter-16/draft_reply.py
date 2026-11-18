import sys
from typing import Literal

import anthropic

from prompts import SYSTEM, user_message

MODEL = "claude-sonnet-5-5"  # change the model here, and only here
Effort = Literal["low", "medium", "high", "xhigh", "max"]
client = anthropic.Anthropic()


def draft(email: str, effort: Effort = "high", show_thinking: bool = False):
    message = client.messages.create(
        model=MODEL,
        max_tokens=4096,  # room for thinking as well as the reply
        system=SYSTEM,
        messages=[user_message(email)],
        output_config={"effort": effort},
        thinking={"type": "adaptive",
                  "display": "summarized" if show_thinking else "omitted"},
    )
    if message.stop_reason != "end_turn":
        raise RuntimeError(f"No usable draft (stop_reason: {message.stop_reason})")
    reply = "".join(b.text for b in message.content if b.type == "text")
    thinking = "".join(b.thinking for b in message.content if b.type == "thinking")
    return reply, thinking


if __name__ == "__main__":
    email = sys.stdin.read().strip()
    reply, thinking = draft(email, show_thinking="--thinking" in sys.argv)
    if thinking:
        print("--- How Claude approached it (summary) ---\n" + thinking + "\n")
    print(reply)
