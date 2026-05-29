---
name: metrics-overview
description: Summarises a metrics snapshot, dashboard, or service health view into the current operational state, notable signals, and practical focus areas.
---

# Metrics Overview

Summarises a metrics snapshot into a concise operational readout.

## Use when

- The user wants a quick read on the current state of a service, system, or dashboard.
- The input is a set of metrics, charts, a dashboard summary, or a health snapshot.
- The main output should help someone understand what looks normal, what looks off, and where attention should go first.

## Not for

- Determining whether a specific SLO or SLA target is breached.
- Explaining the root cause of a known degradation.
- Forecasting future capacity risk or writing incident update text.

## Preconditions

- The user provides service metrics, dashboard values, incident notes, or operational observations.
- The user indicates whether they need current-state summary, anomaly detection, SLO judgment, forecast, root cause, or incident communication.

## Workflow

1. Identify the main health dimensions in the snapshot, such as traffic, latency, errors, saturation, or queueing.
2. Pull out the most important signals rather than describing every metric.
3. Distinguish stable conditions from emerging concerns.
4. Note important uncertainty when thresholds, baselines, or time windows are missing.
5. Return a compact operational overview.

## Writing rules

- Prefer an overall readout over metric-by-metric narration.
- Keep the output practical and easy to scan.
- Preserve important caveats about missing baseline or threshold context.
- Return only the overview unless the user asks for a different format.

## Output pattern

Use this shape unless the user asks for something else:

- Overall state
- Notable signals
- Main concern or watch area
- Immediate priority or open question

For worked examples, see `examples.md`.
