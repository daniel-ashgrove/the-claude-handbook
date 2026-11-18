import os

import anthropic

client = anthropic.Anthropic()

message = client.beta.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=4096,
    betas=["mcp-client-2026-09-15"],
    mcp_servers=[{
        "type": "url",
        "url": "https://mcp.example.com/mcp",  # your helpdesk's MCP server
        "name": "helpdesk",
        "authorization_token": os.environ["HELPDESK_MCP_TOKEN"],
    }],
    tools=[{
        "type": "mcp_toolset",
        "mcp_server_name": "helpdesk",
        "default_config": {"enabled": False},  # no tool unless listed below
        "configs": {"get_ticket": {"enabled": True}},
    }],
    messages=[{"role": "user", "content": "Summarize support ticket 812."}],
)
for block in message.content:
    print(block.type)
