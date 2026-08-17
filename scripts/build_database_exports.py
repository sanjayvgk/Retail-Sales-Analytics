#!/usr/bin/env python
"""Build MySQL dimension/fact CSV exports from the cleaned retail dataset."""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "processed" / "cleaned_retail_sales.csv"
OUT = ROOT / "data" / "processed" / "mysql"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    args = parser.parse_args()

    df = pd.read_csv(args.input, parse_dates=["Order Date", "Ship Date"])
    OUT.mkdir(parents=True, exist_ok=True)

    customers = (
        df[["Customer ID", "Customer Name", "Segment", "Country", "Region", "State", "City", "Postal Code"]]
        .drop_duplicates("Customer ID")
        .rename(columns={
            "Customer ID": "customer_id", "Customer Name": "customer_name", "Segment": "segment",
            "Country": "country", "Region": "region", "State": "state", "City": "city", "Postal Code": "postal_code"
        })
        .sort_values("customer_id")
    )
    products = (
        df[["Product ID", "Product Name", "Category", "Sub-Category"]]
        .drop_duplicates("Product ID")
        .rename(columns={
            "Product ID": "product_id", "Product Name": "product_name", "Category": "category", "Sub-Category": "sub_category"
        })
        .sort_values("product_id")
    )
    sales = df[["Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode", "Customer ID", "Product ID", "Sales", "Quantity", "Discount", "Profit"]].copy()
    sales = sales.rename(columns={
        "Row ID": "row_id", "Order ID": "order_id", "Order Date": "order_date", "Ship Date": "ship_date",
        "Ship Mode": "ship_mode", "Customer ID": "customer_id", "Product ID": "product_id", "Sales": "sales",
        "Quantity": "quantity", "Discount": "discount", "Profit": "profit"
    }).sort_values("row_id")

    customers.to_csv(OUT / "customers.csv", index=False)
    products.to_csv(OUT / "products.csv", index=False)
    sales.to_csv(OUT / "sales.csv", index=False, date_format="%Y-%m-%d")

    # A single denormalized table is convenient for Power BI when MySQL is not available.
    dashboard = df.copy()
    dashboard.to_csv(OUT / "powerbi_sales.csv", index=False, date_format="%Y-%m-%d")

    print(f"Created MySQL exports in {OUT}")
    print(f"customers: {len(customers):,} | products: {len(products):,} | sales rows: {len(sales):,}")


if __name__ == "__main__":
    main()
