---
name: data-analysis-for-reporting
description: Turns spreadsheet findings into a short stakeholder-ready update with headline results, supporting evidence, and practical implications that can be shared upward or across a team.
---

# Data Analysis For Reporting

Turns spreadsheet findings into a clear report-style summary.

## Use when

- The user wants spreadsheet findings turned into a readable stakeholder, manager, or upward-facing report artifact.
- The output should include a headline, executive takeaways, supporting numbers, and a caveat when useful.
- The task is to communicate the main results, supporting observations, and implications clearly.
- The output should be more polished and stakeholder-facing than a raw analytical overview.

## Not for

- Exploring the spreadsheet only for internal understanding.
- Ranking options or making a selection decision.
- Forecasting future outcomes or diagnosing a single root cause as the main output.

## Preconditions

- The user provides a spreadsheet, CSV, table, or tabular summary.
- The user has an analysis goal such as overview, validation, anomaly detection, diagnosis, reporting, ranking, or forecasting.

## Workflow

1. Identify the main reporting question or business topic in the data.
2. Pull out the most important findings and supporting observations.
3. Organise them into a concise report-style structure.
4. Highlight implications, risks, or opportunities where the data supports them.
5. Return a readable reporting artifact.

## Writing rules

- Prefer clear communication over exhaustive detail.
- Keep the report grounded in the observed data.
- Preserve uncertainty where the data cannot justify a strong conclusion.
- Return only the report unless the user asks for another format.

## Output pattern

Use this shape unless the user asks for something else:

- Topic or summary line
- Main findings
- Supporting observations
- Practical implication or recommendation

For worked examples, see `examples.md`.
