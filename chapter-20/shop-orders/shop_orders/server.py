from typing import Annotated, Any

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import BaseModel, Field

from .shop_data import find_order


class Order(BaseModel):
    """One order, as the shop's order system records it."""

    order_number: str
    item: str
    status: str
    last_event: str = Field(description="The latest tracking event")
    days_since_last_event: int


def lookup_order(
    order_number: Annotated[str, Field(
        pattern=r"^[0-9]{4}$", description="The four-digit order number")],
) -> Order:
    """Returns the shop's record of one order: the item, its delivery status,
    the latest tracking event, and how many days ago it happened. Use it
    whenever an email gives an order number, before saying anything about
    that order. It doesn't return payment or refund information, and it
    can't change an order."""
    try:
        record = find_order(order_number)
    except KeyError:
        raise ToolError(f"No order {order_number} in the shop's order system. "
                        "Check the number with the customer.") from None
    return Order(order_number=order_number, **record)


def create_server(**options: Any) -> MCPServer:
    """The server with its one tool. options: sign-in settings for HTTP."""
    server = MCPServer(
        "shop-orders",
        version="1.0.0",
        instructions="Read-only access to the shop's order records.",
        **options,
    )
    server.add_tool(
        lookup_order,
        title="Look up an order",
        annotations=ToolAnnotations(read_only_hint=True, open_world_hint=False),
    )
    return server


def main() -> None:
    create_server().run()  # stdio: the host starts this program


if __name__ == "__main__":
    main()
