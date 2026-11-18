import asyncio
import os
import sys

import httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client
from mcp.types import TextContent

URL = os.environ["SHOP_MCP_URL"]  # the address people will enter in Claude


async def main(order_number: str) -> None:
    headers = {"Authorization": f"Bearer {os.environ['SHOP_MCP_TOKEN']}"}
    async with httpx2.AsyncClient(headers=headers) as http:
        transport = streamable_http_client(URL, http_client=http)
        async with Client(transport) as server:
            listing = await server.list_tools()
            print("Tools:", [tool.name for tool in listing.tools])
            result = await server.call_tool("lookup_order",
                                            {"order_number": order_number})
            text = "\n".join(b.text for b in result.content
                             if isinstance(b, TextContent))
            print("Error:" if result.is_error else "Order:",
                  result.structured_content or text)


asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "4471"))
