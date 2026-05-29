---
name: metrics-root-cause-diagnoser
description: Diagnoses likely causes behind an operational regression or incident by comparing causal hypotheses, identifying the current degradation driver, and tying evidence to that explanation.
---

# Metrics Root Cause Diagnoser

Builds a likely-cause explanation from multiple operational signals.

## Use when

- The user wants help understanding what is driving a regression, outage, or performance problem.
- The input includes several related metrics or observations rather than one isolated chart.
- The task asks for causal driver attribution by comparing competing hypotheses against evidence.
- The output should connect signals into a plausible operational explanation of the current driver.

## Not for

- Only detecting an anomaly.
- Only checking SLO compliance.
- Forecasting future capacity risk.
- Writing stakeholder incident text as the main output.

## Preconditions

- The user provides service metrics, dashboard values, incident notes, or operational observations.
- The user indicates whether they need current-state summary, anomaly detection, SLO judgment, forecast, root cause, or incident communication.

## Workflow

1. Identify the main regression or incident symptom.
2. Look for supporting and contradicting signals across latency, errors, traffic, saturation, or dependency indicators.
3. Form the most plausible cause hypothesis or ranked hypotheses.
4. Explain why the leading driver fits better than alternatives.
5. Note what evidence is missing or ambiguous.
6. Return a compact diagnostic explanation with next checks.

## Writing rules

- Prefer plausible causal structure over a list of disconnected observations.
- Distinguish strong evidence from speculation.
- Include what would confirm or falsify the leading hypothesis.
- Return only the diagnosis unless the user asks for more.

## Output pattern

Use this shape unless the user asks for something else:

- Main symptom
- Likely cause or current degradation driver
- Supporting signals
- Contradicting or missing signals
- Next checks

For worked examples, see `examples.md`.
