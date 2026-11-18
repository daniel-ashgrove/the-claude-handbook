import unittest
from datetime import date
from decimal import Decimal

from shop_tools.delivery import STANDARD_CHARGE, delivery_charge, estimated_arrival


class DeliveryChargeTests(unittest.TestCase):
    def test_small_basket_pays_standard_charge(self):
        self.assertEqual(delivery_charge(Decimal("30.00")), STANDARD_CHARGE)

    def test_large_basket_ships_free(self):
        self.assertEqual(delivery_charge(Decimal("80.00")), Decimal("0.00"))

    def test_negative_basket_is_rejected(self):
        with self.assertRaises(ValueError):
            delivery_charge(Decimal("-1.00"))


class EstimatedArrivalTests(unittest.TestCase):
    def test_monday_order_arrives_thursday(self):
        self.assertEqual(estimated_arrival(date(2026, 11, 16)), date(2026, 11, 19))

    def test_friday_order_skips_the_weekend(self):
        self.assertEqual(estimated_arrival(date(2026, 11, 20)), date(2026, 11, 25))


if __name__ == "__main__":
    unittest.main()
