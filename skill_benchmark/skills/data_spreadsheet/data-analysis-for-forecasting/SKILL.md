---
name: data-analysis-for-forecasting
description: Uses recent spreadsheet patterns to produce a cautious near-term forecast, emphasizing likely direction, confidence, and the conditions that could break the expectation.
---

# Data Analysis For Forecasting

Uses observed data patterns for cautious near-term forecasting.

## Use when

- The user wants to know what the data suggests may happen next if the current pattern continues.
- The output should forecast direction or continuation, not rank options or explain the past cause.
- The task is forward-looking rather than purely descriptive.
- The output should focus on direction, likely continuation, and uncertainty rather than exact prediction claims.

## Not for

- Summarizing the current state only.
- Explaining why a past change happened.
- Ranking candidates or writing a stakeholder report.

## Preconditions

- The user provides a spreadsheet, CSV, table, or tabular summary.
- The user has an analysis goal such as overview, validation, anomaly detection, diagnosis, reporting, ranking, or forecasting.

## Workflow

1. Identify the relevant trend, sequence, or comparison window in the data.
2. Check whether the recent pattern looks stable, accelerating, slowing, or noisy.
3. Estimate the most plausible near-term continuation or directional outcome.
4. Note what makes the forecast weak, conditional, or fragile.
5. Return a compact forward-looking assessment.

## Writing rules

- Be cautious and explicit about uncertainty.
- Prefer directional judgments over overconfident point predictions unless the user asks for exact estimates.
- Distinguish recent movement from stable long-run pattern.
- Return only the forecasting assessment unless the user asks for more.

## Deterministic helper

For simple recent-window and directional checks, run `scripts/simple_trend_checks.py`.

## Output pattern

Use this shape unless the user asks for something else:

- Forecast direction or likely near-term outcome
- Supporting pattern
- Main uncertainty or risk
- What to watch next

For worked examples, see `examples.md`.
