#!/usr/bin/env python
"""Run the complete retail sales Python analytics pipeline."""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from retail_analytics.config import PROCESSED_DATA_DIR, ensure_directories
from retail_analytics.data_cleaning import clean_data, describe_columns, inspect_dataset, read_csv, setup_logging
from retail_analytics.eda import run_complete_eda
from retail_analytics.visualizations import create_all_charts

LOGGER = logging.getLogger(__name__)


def save_eda_outputs(results: dict) -> None:
    """Save EDA tables and KPI metrics into data/processed."""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    for name, value in results.items():
        if hasattr(value, "to_csv"):
            value.to_csv(PROCESSED_DATA_DIR / f"{name}.csv", index=False)
        else:
            (PROCESSED_DATA_DIR / f"{name}.json").write_text(json.dumps(value, indent=2), encoding="utf-8")


def main() -> None:
    """Execute data discovery, cleaning, EDA, and chart generation."""
    parser = argparse.ArgumentParser(description="Run retail sales analytics pipeline")
    parser.add_argument("--input", help="Optional path to the raw retail sales CSV")
    args = parser.parse_args()

    setup_logging()
    ensure_directories()

    raw_df = read_csv(args.input)
    raw_summary = inspect_dataset(raw_df)
    LOGGER.info("Dataset contains %s rows and %s columns", raw_summary["rows"], raw_summary["columns"])

    column_dictionary = describe_columns(raw_df)
    column_dictionary.to_csv(PROCESSED_DATA_DIR / "column_dictionary.csv", index=False)

    cleaned_df = clean_data(raw_df)
    cleaned_path = PROCESSED_DATA_DIR / "cleaned_retail_sales.csv"
    cleaned_df.to_csv(cleaned_path, index=False)
    LOGGER.info("Saved cleaned data to %s", cleaned_path)

    results = run_complete_eda(cleaned_df)
    save_eda_outputs(results)
    charts = create_all_charts(results)

    LOGGER.info("Created %s charts in images/", len(charts))
    LOGGER.info("Pipeline complete")


if __name__ == "__main__":
    main()
