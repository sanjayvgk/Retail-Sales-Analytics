"""Project configuration and dataset discovery helpers."""
from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
IMAGES_DIR = PROJECT_ROOT / "images"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

RETAIL_KEYWORDS = ("retail", "sales", "superstore", "orders", "store")


def ensure_directories() -> None:
    """Create output directories used by the analytics pipeline."""
    for path in (RAW_DATA_DIR, PROCESSED_DATA_DIR, IMAGES_DIR, NOTEBOOKS_DIR):
        path.mkdir(parents=True, exist_ok=True)


def find_dataset(explicit_path: str | Path | None = None) -> Path:
    """Return the most likely retail sales CSV dataset path.

    The function first honors an explicit path. If none is supplied, it scans
    ``data/raw`` and then the full repository for CSV files. Files with retail
    sales keywords in their names are preferred, with larger files ranked first.
    """
    if explicit_path:
        path = Path(explicit_path).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"Dataset not found: {path}")
        if path.suffix.lower() != ".csv":
            raise ValueError(f"Expected a CSV file, got: {path}")
        return path

    search_roots = [RAW_DATA_DIR, PROJECT_ROOT]
    candidates: list[Path] = []
    for root in search_roots:
        if root.exists():
            candidates.extend(p for p in root.rglob("*.csv") if "data/processed" not in p.as_posix())

    unique_candidates = sorted(set(candidates))
    if not unique_candidates:
        raise FileNotFoundError(
            "No CSV dataset found. Place the downloaded retail sales CSV in data/raw/ "
            "or pass --input path/to/file.csv."
        )

    def score(path: Path) -> tuple[int, int]:
        name = path.name.lower()
        keyword_score = sum(keyword in name for keyword in RETAIL_KEYWORDS)
        return (keyword_score, path.stat().st_size)

    return max(unique_candidates, key=score)
