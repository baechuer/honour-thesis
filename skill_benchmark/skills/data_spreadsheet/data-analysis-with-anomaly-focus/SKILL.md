---
name: data-analysis-with-anomaly-focus
description: Produces an anomaly watchlist from spreadsheet data, surfacing unusual values, concentrated deviations, and signs that a pattern may be a real issue rather than ordinary noise.
---

# Data Analysis With Anomaly Focus

Finds unusual values and patterns in tabular data.

## Use when

- The user wants to know what looks unusual or out of pattern in the dataset.
- The task is about spikes, dips, outliers, unexpected changes, or irregular segments.
- The output should focus on what deserves attention before moving into deeper explanation.

## Not for

- Checking general data trustworthiness without a salient abnormal pattern.
- Explaining root cause after the anomaly is already established.
- Forecasting future outcomes or writing stakeholder report text.

## Preconditions

- The user provides a spreadsheet, CSV, table, or tabular summary.
- The user has an analysis goal such as overview, validation, anomaly detection, diagnosis, reporting, ranking, or forecasting.

## Workflow

1. Identify the baseline pattern or comparison frame implied by the data.
2. Look for spikes, drops, outliers, breakpoints, or concentrated deviations.
3. Distinguish meaningful anomalies from expected variation where possible.
4. Note where the anomalies appear to be concentrated.
5. Return a compact anomaly-focused readout.

## Writing rules

- Focus on what looks unusual before trying to explain why.
- Distinguish broad movement from isolated anomalies.
- Preserve uncertainty when the baseline is weak or the sample is small.
- Return only the anomaly-focused analysis unless the user asks for more.

## Deterministic helper

For table-aware anomaly scans across segments and weeks, run `scripts/tabular_anomaly_scan.py`.
For simple single-series checks, run `scripts/basic_anomaly_checks.py`.

## Output pattern

Use this shape unless the user asks for something else:

- Observed anomaly
- Evidence
- Scope or affected segment
- Why it matters
- Confidence or uncertainty

For worked examples, see `examples.md`.
