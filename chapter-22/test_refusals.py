from anthropic.types import Message

from refusals import Declined, reply_text

REFUSED = Message.model_validate({
    "id": "msg_test", "type": "message", "role": "assistant",
    "model": "claude-sonnet-5-5", "content": [{"type": "text", "text": "Hello.."}],
    "stop_reason": "refusal", "stop_sequence": None,
    "stop_details": {"type": "refusal", "category": None, "explanation": None},
    "usage": {"input_tokens": 10, "output_tokens": 2},
})


def test_a_refusal_is_never_returned_as_text():
    try:
        reply_text(REFUSED)
    except Declined as error:
        assert error.category is None
        assert str(error) == "The request was declined."
    else:
        raise AssertionError("a refusal came back as an answer")
