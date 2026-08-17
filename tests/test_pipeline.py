import sys
from pathlib import Path
import unittest

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from retail_analytics.data_cleaning import clean_data
from retail_analytics.eda import run_complete_eda


class RetailAnalyticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = ROOT / "data" / "raw" / "superstore.csv"
        cls.raw = pd.read_csv(cls.path)
        cls.cleaned = clean_data(cls.raw)

    def test_duplicate_rows_are_removed(self):
        self.assertLess(len(self.cleaned), len(self.raw))
        self.assertEqual(self.cleaned.duplicated().sum(), 0)

    def test_required_columns_exist(self):
        required = {"Order ID", "Customer ID", "Product ID", "Order Date", "Sales", "Quantity", "Discount", "Profit"}
        self.assertTrue(required.issubset(self.cleaned.columns))

    def test_numeric_ranges(self):
        self.assertTrue((self.cleaned["Sales"] >= 0).all())
        self.assertTrue((self.cleaned["Quantity"] >= 0).all())
        self.assertTrue(self.cleaned["Discount"].between(0, 1).all())
        self.assertTrue((self.cleaned["Shipping Days"] >= 0).all())

    def test_kpis_are_positive(self):
        kpis = run_complete_eda(self.cleaned)["kpis"]
        self.assertGreater(kpis["total_revenue"], 0)
        self.assertNotEqual(kpis["total_profit"], 0)
        self.assertGreater(kpis["total_orders"], 0)

    def test_expected_superstore_row_count_after_deduplication(self):
        self.assertEqual(len(self.cleaned), 9994)


if __name__ == "__main__":
    unittest.main()
