import unittest

from report import best_seller, compute_revenue, read_setting

ORDERS = [
    {"name": "A", "price": 10, "quantity": 2},
    {"name": "B", "price": 5, "quantity": 5},
]


class ReportTest(unittest.TestCase):
    def test_revenue(self):
        self.assertEqual(compute_revenue(ORDERS), 45)

    def test_best_seller(self):
        self.assertEqual(best_seller(ORDERS), "B")

    def test_setting(self):
        self.assertTrue(read_setting("api_url").startswith("https://"))


if __name__ == "__main__":
    unittest.main()
