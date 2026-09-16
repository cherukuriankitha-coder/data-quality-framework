"""Reusable data-quality checks for analytics datasets."""
from dataclasses import dataclass
import pandas as pd

@dataclass
class QualityReport:
    rows: int
    duplicate_rows: int
    missing_values: int
    passed: bool

def validate(df: pd.DataFrame, required_columns=None) -> QualityReport:
    required_columns = required_columns or []
    missing_columns = [c for c in required_columns if c not in df.columns]
    duplicates = int(df.duplicated().sum())
    missing = int(df.isna().sum().sum())
    return QualityReport(
        rows=len(df),
        duplicate_rows=duplicates,
        missing_values=missing,
        passed=not missing_columns and duplicates == 0,
    )

def reconcile(source: pd.DataFrame, target: pd.DataFrame, key: str) -> dict:
    source_keys = set(source[key].dropna())
    target_keys = set(target[key].dropna())
    return {
        "missing_in_target": sorted(source_keys - target_keys),
        "unexpected_in_target": sorted(target_keys - source_keys),
    }
