"""Order totals: the basket, any discount code, then delivery."""

from decimal import ROUND_HALF_UP, Decimal

from .delivery import delivery_charge

DISCOUNT_CODES = {
    "WELCOME10": Decimal("0.10"),  # 10 percent off a first order
}
CENT = Decimal("0.01")


def basket_total(lines: list[tuple[Decimal, int]]) -> Decimal:
    """Add up (unit price, quantity) pairs."""
    total = Decimal("0.00")
    for price, quantity in lines:
        if quantity < 1:
            raise ValueError("each line needs a quantity of at least 1")
        total += price * quantity
    return total.quantize(CENT, rounding=ROUND_HALF_UP)


def order_total(lines: list[tuple[Decimal, int]],
                code: str | None = None) -> Decimal:
    """Return what the customer pays: basket, less any discount, plus delivery."""
    basket = basket_total(lines)
    if code:
        rate = DISCOUNT_CODES.get(code.strip().upper())
        if rate is None:
            raise ValueError(f"Unknown discount code: {code}")
        basket = (basket * (1 - rate)).quantize(CENT, rounding=ROUND_HALF_UP)
    return basket + delivery_charge(basket)
