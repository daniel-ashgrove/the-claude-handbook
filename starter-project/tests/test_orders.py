import unittest
from decimal import Decimal

from shop_tools.orders import basket_total, order_total

TEAPOT = (Decimal("24.00"), 1)
MUGS = (Decimal("8.50"), 2)


class OrderTotalTests(unittest.TestCase):
    def test_basket_adds_every_line(self):
        self.assertEqual(basket_total([TEAPOT, MUGS]), Decimal("41.00"))

    def test_small_order_adds_delivery(self):
        self.assertEqual(order_total([TEAPOT, MUGS]), Decimal("45.95"))

    def test_discount_code_takes_ten_percent(self):
        lines = [(Decimal("100.00"), 1)]
        self.assertEqual(order_total(lines, "WELCOME10"), Decimal("90.00"))

    def test_discount_code_ignores_case(self):
        lines = [(Decimal("100.00"), 1)]
        self.assertEqual(order_total(lines, "welcome10"), Decimal("90.00"))

    def test_unknown_code_is_rejected(self):
        with self.assertRaises(ValueError):
            order_total([TEAPOT], "FREESTUFF")


if __name__ == "__main__":
    unittest.main()
