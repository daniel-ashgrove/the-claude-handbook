import anthropic

MODEL = "claude-sonnet-5-5"  # change the model here, and only here

SYSTEM = (
    "You draft replies for the support team of a small online homeware shop. "
    "Be warm and brief. Never promise a delivery date or a refund; "
    "a person on the team decides those."
)

email = """Hi, I ordered a ceramic teapot (order 4471) ten days ago and the
tracking page hasn't changed since Monday. Is it lost?"""

client = anthropic.Anthropic()
message = client.messages.create(
    model=MODEL,
    max_tokens=2048,
    system=SYSTEM,
    messages=[{"role": "user", "content": f"Draft a reply to this email:\n\n{email}"}],
)

if message.stop_reason == "max_tokens":
    print("Warning: the draft was cut off. Raise max_tokens.")
print("".join(b.text for b in message.content if b.type == "text"))
