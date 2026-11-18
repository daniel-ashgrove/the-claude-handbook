"""Handle a reply that Claude's safeguards declined."""
from anthropic.types import Message


class Declined(Exception):
    """A refusal: a normal 200 response, not an API error."""

    def __init__(self, message: Message) -> None:
        details = message.stop_details
        self.category = details.category if details else None  # can be None
        self.explanation = details.explanation if details else None
        super().__init__(self.explanation or "The request was declined.")


def reply_text(message: Message) -> str:
    """The reply's text, or Declined if a safeguard stopped it."""
    if message.stop_reason == "refusal":
        raise Declined(message)  # any partial text is incomplete: discard it
    return "".join(b.text for b in message.content if b.type == "text")
