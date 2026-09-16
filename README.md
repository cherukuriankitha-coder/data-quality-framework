# Data Quality Framework

Reusable Python framework for expressing common data-quality rules and returning structured, machine-readable validation results.

## Quality Dimensions
- Schema completeness
- Null-rate thresholds
- Key uniqueness
- Numeric range validation
- Dataset-level reporting

## Tech Stack
Python, Pandas

## Structure
```text
src/quality_checks.py  # composable validation checks
src/report.py          # report runner / summary output
```

## Example
```python
import pandas as pd
from src.quality_checks import required_columns, null_rate, unique_key

df = pd.read_csv("customers.csv")
print(required_columns(df, ["customer_id", "email"]).to_dict())
print(null_rate(df, "email", max_rate=0.01).to_dict())
print(unique_key(df, ["customer_id"]).to_dict())
```

## Design
Each check returns a consistent `CheckResult` containing the check name, pass/fail status, and diagnostic details. This makes the framework suitable for console reporting, JSON output, dashboards, or ETL quality gates.

## Next Steps
Add referential-integrity checks, regex validation, freshness checks, YAML rule configuration, pytest coverage, and CI quality gates.