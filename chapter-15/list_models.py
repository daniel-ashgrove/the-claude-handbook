import anthropic

client = anthropic.Anthropic()

for model in client.models.list():
    print(f"{model.id:24} {model.display_name:22} {model.lifecycle}")
