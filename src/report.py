"""Quality report runner."""
from typing import Iterable
import pandas as pd
from quality_checks import CheckResult, required_columns


def run_schema_check(df: pd.DataFrame, required: Iterable[str]) -> dict:
    result: CheckResult = required_columns(df, required)
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "status": "PASS" if result.passed else "FAIL",
        "checks": [result.to_dict()],
    }
