"""Composable data-quality checks that return structured results."""
from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, List
import pandas as pd


@dataclass
class CheckResult:
    check: str
    passed: bool
    details: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def required_columns(df: pd.DataFrame, columns: Iterable[str]) -> CheckResult:
    missing = sorted(set(columns) - set(df.columns))
    return CheckResult("required_columns", not missing, {"missing": missing})


def null_rate(df: pd.DataFrame, column: str, max_rate: float = 0.0) -> CheckResult:
    rate = float(df[column].isna().mean())
    return CheckResult("null_rate", rate <= max_rate, {"column": column, "rate": rate, "threshold": max_rate})


def unique_key(df: pd.DataFrame, columns: List[str]) -> CheckResult:
    duplicates = int(df.duplicated(subset=columns).sum())
    return CheckResult("unique_key", duplicates == 0, {"columns": columns, "duplicates": duplicates})


def numeric_range(df: pd.DataFrame, column: str, minimum=None, maximum=None) -> CheckResult:
    values = pd.to_numeric(df[column], errors="coerce")
    invalid = values.isna()
    if minimum is not None:
        invalid |= values < minimum
    if maximum is not None:
        invalid |= values > maximum
    count = int(invalid.sum())
    return CheckResult("numeric_range", count == 0, {"column": column, "invalid_rows": count})
