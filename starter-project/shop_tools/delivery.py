"""Delivery charges and arrival estimates for the shop's orders."""

from datetime import date, timedelta
from decimal import Decimal

FREE_DELIVERY_FROM = Decimal("50.00")  # baskets of this much or more ship free
STANDARD_CHARGE = Decimal("4.95")
STANDARD_WORKING_DAYS = 3


def delivery_charge(basket_total: Decimal) -> Decimal:
    """Return the delivery charge for a basket, after any discount."""
    if basket_total < 0:
        raise ValueError("basket_total can't be negative")
    if basket_total > FREE_DELIVERY_FROM:
        return Decimal("0.00")
    return STANDARD_CHARGE


def estimated_arrival(ordered_on: date,
                      working_days: int = STANDARD_WORKING_DAYS) -> date:
    """Return the date an order should arrive, counting Monday to Friday only."""
    if working_days < 1:
        raise ValueError("working_days must be at least 1")
    day = ordered_on
    remaining = working_days
    while remaining > 0:
        day += timedelta(days=1)
        if day.weekday() < 5:  # Monday is 0, Friday is 4
            remaining -= 1
    return day
