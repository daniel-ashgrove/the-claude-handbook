import anthropic

client = anthropic.Anthropic(max_retries=3)  # the default is 2

try:
    message = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": "In one sentence, what is an API?"}],
    )
except anthropic.AuthenticationError:
    print("401: the key is wrong, expired or disabled.")
except anthropic.BadRequestError as e:
    print("400: something in the request needs fixing:", e.message)
except anthropic.RateLimitError as e:
    print("429 even after retries. Request ID:", e.request_id)
except anthropic.APIStatusError as e:
    print(f"{e.status_code} {e.type}. Request ID: {e.request_id}")
except anthropic.APIConnectionError:
    print("No response from the API: check the network and try again.")
else:
    print("OK. Request ID:", message._request_id)
