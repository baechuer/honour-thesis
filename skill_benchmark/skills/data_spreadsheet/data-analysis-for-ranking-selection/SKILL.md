---
name: data-analysis-for-ranking-selection
description: Compares spreadsheet rows, options, or candidates to produce a justified recommendation, including the strongest choice, tradeoffs, and what could change the decision.
---

# Data Analysis For Ranking Selection

Compares options in a dataset to support ranking and selection.

## Use when

- The user wants to rank rows, candidates, products, vendors, or other options.
- The task is decision-oriented rather than purely descriptive.
- The output should justify prioritisation or selection clearly.

## Not for

- Producing only a broad overview of the table.
- Writing a report without choosing among options.
- Forecasting future values without a selection decision.

## Preconditions

- The user provides a spreadsheet, CSV, table, or tabular summary.
- The user has an analysis goal such as overview, validation, anomaly detection, diagnosis, reporting, ranking, or forecasting.

## Workflow

1. Identify the options being compared and the criteria that matter.
2. Check whether the criteria are explicit, implicit, or need to be inferred from the data.
3. Compare the options using the most relevant dimensions.
4. Surface tradeoffs, strengths, and weaknesses behind the ranking.
5. Return a justified ranking or recommendation.

## Writing rules

- Make the comparison logic explicit.
- Preserve important tradeoffs instead of forcing a false single-winner narrative.
- Avoid pretending that weak or incomplete data supports certainty.
- Return only the ranking or recommendation unless the user asks for explanation.

## Deterministic helper

For simple weighted scoring and ordering, run `scripts/score_candidates.py`.

## Output pattern

Use this shape unless the user asks for something else:

- Ranking or recommended option
- Main reasons
- Tradeoffs or caveats
- What would change the decision

For worked examples, see `examples.md`.
