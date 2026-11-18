import asyncio

from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client

# An existing server: the reference filesystem server, limited to one folder.
SERVER = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem@2.0.1", "policies"],
)


async def main() -> None:
    async with Client(stdio_client(SERVER)) as server:
        info = server.server_info
        print(f"Server: {info.name} {info.version}" if info else "Server: unnamed")
        print(f"Protocol version: {server.protocol_version}")
        listing = await server.list_tools()
        for tool in listing.tools:
            hints = tool.annotations  # hints from the server, not guarantees
            reads_only = bool(hints and hints.read_only_hint)
            label = "reads only" if reads_only else "can change things"
            print(f"  {tool.name:26} {label}")


asyncio.run(main())
