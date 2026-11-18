import anthropic

client = anthropic.Anthropic()
history = []  # the whole conversation; the API keeps none of it

while True:
    text = input("You: ").strip()
    if not text:
        break
    history.append({"role": "user", "content": text})
    message = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=1024,
        messages=history,
    )
    history.append({"role": "assistant", "content": message.content})
    print("Claude:", "".join(b.text for b in message.content if b.type == "text"))
    print(f"  (this turn sent {message.usage.input_tokens} input tokens)")
