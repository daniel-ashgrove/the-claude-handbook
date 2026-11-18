import json
from pathlib import Path

from anthropic.types import MessageParam

# The fixed part: written once, kept in its own file, changed only on purpose.
SYSTEM = Path(__file__).with_name("drafter_system.txt").read_text(encoding="utf-8")


def user_message(email: str) -> MessageParam:
    """The variable part: this one email, labeled and JSON-encoded."""
    payload = json.dumps({"customer_email": email}, ensure_ascii=False)
    return {
        "role": "user",
        "content": (
            "Here is an inbound email from a customer, as JSON:\n"
            f"{payload}\n\n"
            "Draft a reply to it."
        ),
    }
