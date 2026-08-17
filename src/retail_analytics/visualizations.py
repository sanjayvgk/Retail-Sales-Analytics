"""Visualization functions for the retail sales analytics pipeline."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from .config import IMAGES_DIR, ensure_directories

sns.set_theme(style="whitegrid")


def _save(fig: plt.Figure, filename: str) -> Path:
    ensure_directories()
    path = IMAGES_DIR / filename
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return path


def bar_chart(data: pd.DataFrame, x: str, y: str, title: str, filename: str, horizontal: bool = False) -> Path:
    """Create and save a labeled bar chart."""
    fig, ax = plt.subplots(figsize=(11, 6))
    if horizontal:
        sns.barplot(data=data, y=x, x=y, ax=ax, color="#4C78A8")
        ax.set_xlabel(y)
        ax.set_ylabel(x)
    else:
        sns.barplot(data=data, x=x, y=y, ax=ax, color="#4C78A8")
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.tick_params(axis="x", rotation=35)
    ax.set_title(title, fontsize=14, weight="bold")
    return _save(fig, filename)


def line_chart(data: pd.DataFrame, x: str, y: str, title: str, filename: str) -> Path:
    """Create and save a time-series line chart."""
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=data, x=x, y=y, marker="o", ax=ax, color="#F58518")
    ax.set_title(title, fontsize=14, weight="bold")
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.tick_params(axis="x", rotation=45)
    return _save(fig, filename)


def create_all_charts(eda_results: dict) -> list[Path]:
    """Generate every requested professional chart and return their paths."""
    monthly = eda_results["monthly_trends"]
    charts = [
        line_chart(monthly, "Month", "Sales", "Monthly Revenue Trend", "monthly_revenue_trend.png"),
        line_chart(monthly, "Month", "Profit", "Monthly Profit Trend", "monthly_profit_trend.png"),
        bar_chart(eda_results["sales_by_category"], "Category", "Sales", "Sales by Category", "sales_by_category.png"),
        bar_chart(eda_results["sales_by_subcategory"].head(15), "Sub-Category", "Sales", "Sales by Subcategory", "sales_by_subcategory.png"),
        bar_chart(eda_results["sales_by_region"], "Region", "Sales", "Sales by Region", "sales_by_region.png"),
        bar_chart(eda_results["sales_by_state"].head(15), "State", "Sales", "Top States by Sales", "sales_by_state.png"),
        bar_chart(eda_results["top_10_customers"], "Customer Name", "Sales", "Top 10 Customers", "top_10_customers.png", horizontal=True),
        bar_chart(eda_results["top_10_products"], "Product Name", "Sales", "Top 10 Products", "top_10_products.png", horizontal=True),
        bar_chart(eda_results["bottom_10_products"], "Product Name", "Sales", "Bottom 10 Products", "bottom_10_products.png", horizontal=True),
        bar_chart(eda_results["discount_analysis"], "Discount Band", "Profit", "Profit by Discount Band", "discount_analysis.png"),
        bar_chart(eda_results["profit_margin_analysis"], "Category", "Profit Margin", "Profit Margin by Category", "profit_margin_analysis.png"),
        bar_chart(eda_results["shipping_analysis"], "Ship Mode", "Sales", "Sales by Shipping Mode", "shipping_analysis.png"),
    ]
    return charts
