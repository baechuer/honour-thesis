---
name: slo-breach-checker
description: Evaluates whether the available service metrics indicate an SLO miss, burn-rate issue, or material risk to the defined reliability target.
---

# SLO Breach Checker

Evaluates whether the observed metrics imply a reliability target miss or risk.

## Use when

- The user wants to know whether a service is breaching or endangering an SLO.
- The input includes an SLO target, success/error indicators, availability data, or burn-rate context.
- The output should make a clear judgment about compliance, risk, and uncertainty.

## Not for

- Detecting unusualness without a target or reliability objective.
- Explaining root cause as the main output.
- Forecasting capacity risk or writing incident summary text.

## Preconditions

- The user provides service metrics, dashboard values, incident notes, or operational observations.
- The user indicates whether they need current-state summary, anomaly detection, SLO judgment, forecast, root cause, or incident communication.

## Workflow

1. Identify the reliability target or implied service objective if one is provided.
2. Pull out the relevant error, success, availability, or burn-rate signals.
3. Judge whether the snapshot shows compliance, active breach, or meaningful risk.
4. Note what assumptions are required if the time window or target is incomplete.
5. Return a compact SLO-focused assessment.

## Writing rules

- Make the reliability judgment explicit.
- Separate active breach from approaching breach.
- Preserve uncertainty when the target, window, or denominator is unclear.
- Return only the assessment unless the user asks for another format.

## Output pattern

Use this shape unless the user asks for something else:

- SLO status
- Supporting evidence
- Risk level
- What to verify next

For worked examples, see `examples.md`.
