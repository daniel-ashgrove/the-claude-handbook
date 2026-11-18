import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

message = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "In one sentence, what is an API?"},
    ],
)

for block in message.content:
    if block.type == "text":
        print(block.text)

print("Stop reason:", message.stop_reason)
print("Tokens in/out:", message.usage.input_tokens, message.usage.output_tokens)
