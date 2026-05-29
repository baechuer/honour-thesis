---
name: incident-summary-writer
description: Turns incident notes, metrics, and operational observations into a concise incident summary covering impact, symptoms, timeline, status, and next actions.
---

# Incident Summary Writer

Builds a concise operational incident summary.

## Use when

- The user wants a readable summary of an incident, degradation, or outage.
- The input includes incident notes, metrics observations, timeline fragments, or response details.
- The output should help someone quickly understand what happened and where things stand.

## Not for

- Root-cause investigation as the main task.
- SLO calculation as the main task.
- Anomaly detection without communication needs.
- Capacity forecasting.

## Preconditions

- The user provides service metrics, dashboard values, incident notes, or operational observations.
- The user indicates whether they need current-state summary, anomaly detection, SLO judgment, forecast, root cause, or incident communication.

## Workflow

1. Identify the core incident or degradation being described.
2. Pull out the most important symptoms, impact, and timeline points.
3. Note current status, mitigation, and unresolved issues.
4. Keep the summary compact and operationally useful.
5. Return a clean incident summary rather than a deep diagnosis.

## Writing rules

- Focus on what happened, impact, and current state.
- Keep timeline detail only if it helps explain the incident progression.
- Preserve uncertainty when the cause or scope is still unclear.
- Return only the summary unless the user asks for another format.

## Output pattern

Use this shape unless the user asks for something else:

- Incident overview
- Customer or system impact
- Key timeline points
- Current status
- Next actions or open issues

For worked examples, see `examples.md`.
