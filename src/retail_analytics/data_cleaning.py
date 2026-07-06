"""Data loading, inspection, and cleaning for the retail sales dataset."""
from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from .config import PROCESSED_DATA_DIR, ensure_directories, find_dataset

LOGGER = logging.getLogger(__name__)

COLUMN_DESCRIPTIONS = {
    "Row ID": "A simple row number for each record.",
    "Order ID": "The unique code for a customer order.",
    "Order Date": "The date when the customer placed the order.",
    "Ship Date": "The date when the order was shipped.",
    "Ship Mode": "The shipping speed or service selected for the order.",
    "Customer ID": "The unique code for each customer.",
    "Customer Name": "The name of the customer.",
    "Segment": "The type of customer, such as consumer or corporate.",
    "Country": "The country where the order was delivered.",
    "City": "The delivery city.",
    "State": "The delivery state or province.",
    "Postal Code": "The delivery postal or ZIP code.",
    "Region": "The broader sales region for the order.",
    "Product ID": "The unique code for the product.",
    "Category": "The main product group.",
    "Sub-Category": "The smaller product group inside the category.",
    "Product Name": "The product sold to the customer.",
    "Sales": "The revenue earned from the line item before profit calculations.",
    "Quantity": "The number of units sold.",
    "Discount": "The discount rate applied to the line item.",
    "Profit": "The money left after costs for the line item.",
    "Year": "The year extracted from the order date.",
    "Month": "The month extracted from the order date.",
    "Quarter": "The quarter extracted from the order date.",
    "Profit Margin": "Profit divided by sales; shows how much profit came from each sales dollar.",
    "Shipping Days": "The number of days between order date and ship date.",
}


def setup_logging() -> None:
    """Configure readable console logging for scripts."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


def read_csv(path: str | Path | None = None) -> pd.DataFrame:
    """Locate and read the retail CSV dataset."""
    dataset_path = find_dataset(path)
    LOGGER.info("Reading dataset from %s", dataset_path)
    return pd.read_csv(dataset_path, encoding="utf-8-sig")


def inspect_dataset(df: pd.DataFrame) -> dict[str, object]:
    """Return key inspection facts about the dataset."""
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": df.isna().sum().astype(int).to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
    }


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the retail dataset and add analysis-ready features."""
    cleaned = df.copy()
    cleaned.columns = cleaned.columns.str.strip()
    before = len(cleaned)
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)
    LOGGER.info("Removed %s duplicate rows", before - len(cleaned))

    for column in ("Order Date", "Ship Date"):
        if column in cleaned.columns:
            cleaned[column] = pd.to_datetime(cleaned[column], errors="coerce")

    numeric_columns = ["Sales", "Quantity", "Discount", "Profit", "Postal Code"]
    for column in numeric_columns:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    text_columns = cleaned.select_dtypes(include="object").columns
    for column in text_columns:
        cleaned[column] = cleaned[column].fillna("Unknown").astype(str).str.strip()

    for column in cleaned.select_dtypes(include=np.number).columns:
        if cleaned[column].isna().any():
            cleaned[column] = cleaned[column].fillna(cleaned[column].median())

    if "Order Date" in cleaned.columns:
        cleaned = cleaned.dropna(subset=["Order Date"]).copy()
        cleaned["Year"] = cleaned["Order Date"].dt.year
        cleaned["Month"] = cleaned["Order Date"].dt.month
        cleaned["Quarter"] = cleaned["Order Date"].dt.quarter

    if {"Profit", "Sales"}.issubset(cleaned.columns):
        cleaned["Profit Margin"] = np.where(cleaned["Sales"] != 0, cleaned["Profit"] / cleaned["Sales"], 0.0)

    if {"Order Date", "Ship Date"}.issubset(cleaned.columns):
        cleaned["Shipping Days"] = (cleaned["Ship Date"] - cleaned["Order Date"]).dt.days
        cleaned["Shipping Days"] = cleaned["Shipping Days"].clip(lower=0)

    return cleaned


def save_cleaned_data(df: pd.DataFrame, filename: str = "cleaned_retail_sales.csv") -> Path:
    """Save cleaned data to the processed data folder."""
    ensure_directories()
    output_path = PROCESSED_DATA_DIR / filename
    df.to_csv(output_path, index=False)
    LOGGER.info("Saved cleaned data to %s", output_path)
    return output_path


def describe_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Create a simple-English data dictionary for the available columns."""
    return pd.DataFrame(
        {"column": df.columns, "simple_english_description": [COLUMN_DESCRIPTIONS.get(col, "A dataset field used for retail sales analysis.") for col in df.columns]}
    )
