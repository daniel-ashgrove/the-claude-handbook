import os

import anthropic

client = anthropic.Anthropic()

message = client.beta.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=4096,
    betas=["mcp-client-2026-09-15"],
    mcp_servers=[{
        "type": "url",
        "url": "https://orders.example.com/mcp",  # the deployed order server
        "name": "shop-orders",
        "authorization_token": os.environ["SHOP_MCP_TOKEN"],  # issued for it
    }],
    tools=[{
        "type": "mcp_toolset",
        "mcp_server_name": "shop-orders",
        "default_config": {"enabled": False},  # no tool unless listed below
        "configs": {"lookup_order": {"enabled": True}},
    }],
    messages=[{"role": "user", "content": "Where is order 4471, and since when?"}],
)
for block in message.content:
    print(block.type)
