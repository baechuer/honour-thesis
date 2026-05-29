---
name: data-analysis-overview
description: Produces a broad analytical readout of a spreadsheet, highlighting the overall picture, strongest patterns, and main watch areas without committing too early to one narrow interpretation.
---

# Data Analysis Overview

Summarises a spreadsheet or tabular dataset into a broad analytical readout.

## Use when

- The user wants a high-level understanding of a spreadsheet or dataset.
- The task is to identify the main patterns, notable values, and broad takeaways.
- The output should help someone understand what stands out without narrowing too quickly to one analytical frame.

## Not for

- Validating whether the data can be trusted before use.
- Explaining the cause of a specific spike, drop, or regression.
- Producing a manager-ready report, forecast, or ranking recommendation.

## Preconditions

- The user provides a spreadsheet, CSV, table, or tabular summary.
- The user has an analysis goal such as overview, validation, anomaly detection, diagnosis, reporting, ranking, or forecasting.

## Workflow

1. Identify what the rows, columns, and main measures represent.
2. Pull out the most important patterns, changes, or contrasts.
3. Distinguish broad trends from smaller local noise.
4. Note any uncertainty caused by missing context, unclear definitions, or short time windows.
5. Return a compact overview with the main takeaways.

## Writing rules

- Prefer broad analytical structure over metric-by-metric narration.
- Keep the output concise and easy to scan.
- Preserve uncertainty where the data does not justify strong claims.
- Return only the overview unless the user asks for a different format.

## Deterministic helper

For sheet-wide rollups and biggest-mover checks, run `scripts/channel_rollup_summary.py`.

## Output pattern

Use this shape unless the user asks for something else:

- Overall picture
- Notable patterns
- Main concern or opportunity
- Key takeaway

For worked examples, see `examples.md`.
