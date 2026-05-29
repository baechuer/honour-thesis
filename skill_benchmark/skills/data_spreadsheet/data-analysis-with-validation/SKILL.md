---
name: data-analysis-with-validation
description: Checks whether spreadsheet-based conclusions are safe to trust by surfacing missing data, inconsistent fields, fragile assumptions, and the most important verifications needed before action.
---

# Data Analysis With Validation

Checks whether spreadsheet-based conclusions are trustworthy.

## Use when

- The user wants the analysis checked for weak assumptions or data quality issues.
- The task involves validating totals, joins, missing values, comparisons, filters, or interpretation assumptions.
- The output should identify what might make the analysis unreliable.

## Not for

- Providing only a broad descriptive overview.
- Explaining the likely cause of a confirmed change.
- Writing a polished report or ranking options.

## Preconditions

- The user provides a spreadsheet, CSV, table, or tabular summary.
- The user has an analysis goal such as overview, validation, anomaly detection, diagnosis, reporting, ranking, or forecasting.

## Workflow

1. Identify what conclusion, comparison, or interpretation is being relied on.
2. Check for obvious data quality issues, missing values, inconsistent definitions, or fragile assumptions.
3. Distinguish strong support from questionable support.
4. Surface what needs to be verified before the conclusion should be trusted.
5. Return a compact validation-focused assessment.

## Writing rules

- Be conservative about what the data supports.
- Prefer specific validation concerns over vague caution.
- Distinguish true data problems from ordinary uncertainty.
- Return only the validation assessment unless the user asks for more.

## Deterministic helper

For simple tabular consistency checks, run `scripts/validate_tabular_assumptions.py`.

## Output pattern

Use this shape unless the user asks for something else:

- Validation status
- Main issue or check result
- Why it matters
- What to verify next

For worked examples, see `examples.md`.
