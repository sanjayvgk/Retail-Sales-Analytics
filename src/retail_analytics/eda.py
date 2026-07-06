"""Exploratory analysis calculations for retail sales."""
from __future__ import annotations

import pandas as pd


def total_orders(df: pd.DataFrame) -> int:
    """Count unique orders when possible, otherwise count rows."""
    return int(df["Order ID"].nunique()) if "Order ID" in df.columns else int(len(df))


def summarize_metrics(df: pd.DataFrame) -> dict[str, float | int]:
    """Return high-level business KPIs."""
    return {
        "total_revenue": float(df["Sales"].sum()) if "Sales" in df.columns else 0.0,
        "total_profit": float(df["Profit"].sum()) if "Profit" in df.columns else 0.0,
        "total_orders": total_orders(df),
        "average_profit_margin": float(df["Profit Margin"].mean()) if "Profit Margin" in df.columns else 0.0,
    }


def monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly revenue and profit trends."""
    monthly = df.set_index("Order Date").resample("ME").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
    monthly["Month"] = monthly["Order Date"].dt.to_period("M").astype(str)
    return monthly


def grouped_sales(df: pd.DataFrame, group_col: str, top_n: int | None = None, ascending: bool = False) -> pd.DataFrame:
    """Aggregate sales, profit, quantity, and margin by a categorical column."""
    grouped = df.groupby(group_col, dropna=False).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum") if "Quantity" in df.columns else ("Sales", "count")
    ).reset_index()
    grouped["Profit Margin"] = grouped["Profit"] / grouped["Sales"].replace(0, pd.NA)
    grouped = grouped.sort_values("Sales", ascending=ascending)
    return grouped.head(top_n) if top_n else grouped


def discount_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize sales and profit by discount level."""
    data = df.copy()
    data["Discount Band"] = pd.cut(
        data["Discount"], bins=[-0.01, 0, 0.1, 0.2, 0.4, 1.0], labels=["No discount", "0-10%", "10-20%", "20-40%", "40%+"],
    )
    return data.groupby("Discount Band", observed=True).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique")).reset_index()


def shipping_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze orders by shipping mode."""
    aggregations = {"Sales": ("Sales", "sum"), "Profit": ("Profit", "sum"), "Orders": ("Order ID", "nunique")}
    if "Shipping Days" in df.columns:
        aggregations["Average Shipping Days"] = ("Shipping Days", "mean")
    return df.groupby("Ship Mode", dropna=False).agg(**aggregations).reset_index().sort_values("Sales", ascending=False)


def run_complete_eda(df: pd.DataFrame) -> dict[str, pd.DataFrame | dict[str, float | int]]:
    """Run all requested EDA tables and metrics."""
    return {
        "kpis": summarize_metrics(df),
        "monthly_trends": monthly_trends(df),
        "sales_by_category": grouped_sales(df, "Category"),
        "sales_by_subcategory": grouped_sales(df, "Sub-Category"),
        "sales_by_region": grouped_sales(df, "Region"),
        "sales_by_state": grouped_sales(df, "State"),
        "top_10_customers": grouped_sales(df, "Customer Name", top_n=10),
        "top_10_products": grouped_sales(df, "Product Name", top_n=10),
        "bottom_10_products": grouped_sales(df, "Product Name", top_n=10, ascending=True),
        "discount_analysis": discount_analysis(df),
        "profit_margin_analysis": grouped_sales(df, "Category").sort_values("Profit Margin", ascending=False),
        "shipping_analysis": shipping_analysis(df),
    }
