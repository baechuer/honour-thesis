---
name: data-analysis-for-root-cause-diagnosis
description: Uses spreadsheet evidence to form a likely-cause explanation for a change or regression, including the leading driver, a weaker alternative, and the evidence that separates them.
---

# Data Analysis For Root Cause Diagnosis

Builds a likely-cause explanation from tabular evidence.

## Use when

- The user wants to understand what is driving a change, regression, degradation, or performance issue in the data.
- The task asks for driver attribution: which segment, channel, metric, period, or variable best explains the change.
- The task is explanatory rather than merely descriptive.
- The output should connect observed patterns into a plausible cause story.

## Not for

- Only detecting whether something looks unusual.
- Only validating data quality before interpretation.
- Producing broad overview, forecast, or stakeholder report text.

## Preconditions

- The user provides a spreadsheet, CSV, table, or tabular summary.
- The user has an analysis goal such as overview, validation, anomaly detection, diagnosis, reporting, ranking, or forecasting.

## Workflow

1. Identify the main outcome, regression, or change that needs explanation.
2. Look for segments, categories, periods, or variables that move with the problem.
3. Distinguish supporting signals from weak correlations or noise.
4. Form the most plausible explanation or ranked explanations.
5. Return a compact diagnostic readout with evidence and uncertainty.

## Writing rules

- Prefer plausible explanations grounded in the observed data.
- Distinguish evidence from speculation.
- Preserve uncertainty when multiple explanations remain viable.
- Return only the diagnosis unless the user asks for more.

## Deterministic helper

For contribution scans and margin-driver checks, run `scripts/margin_driver_scan.py`.

## Output pattern

Use this shape unless the user asks for something else:

- Main issue
- Likely driver or drivers
- Supporting evidence
- Uncertainty or alternative explanation
- Next check

For worked examples, see `examples.md`.
