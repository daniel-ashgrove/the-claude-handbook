import pytest
from mcp import Client
from mcp.types import TextContent

from shop_orders.server import create_server


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    async with Client(create_server(), raise_exceptions=True) as c:  # in memory
        yield c


@pytest.mark.anyio
async def test_only_one_tool_and_it_only_reads(client: Client):
    listing = await client.list_tools()
    assert [tool.name for tool in listing.tools] == ["lookup_order"]
    hints = listing.tools[0].annotations
    assert hints is not None and hints.read_only_hint is True


@pytest.mark.anyio
async def test_known_order(client: Client):
    result = await client.call_tool("lookup_order", {"order_number": "4471"})
    assert not result.is_error
    assert result.structured_content == {
        "order_number": "4471", "item": "ceramic teapot",
        "status": "with the courier",
        "last_event": "Arrived at the local delivery depot",
        "days_since_last_event": 4,
    }


@pytest.mark.anyio
async def test_unknown_order_is_a_tool_error(client: Client):
    result = await client.call_tool("lookup_order", {"order_number": "9999"})
    block = result.content[0]
    assert result.is_error and isinstance(block, TextContent)
    assert "No order 9999" in block.text


@pytest.mark.anyio
async def test_bad_order_number_is_refused(client: Client):
    result = await client.call_tool("lookup_order", {"order_number": "#4471"})
    block = result.content[0]
    assert result.is_error and isinstance(block, TextContent)
    assert "pattern" in block.text
