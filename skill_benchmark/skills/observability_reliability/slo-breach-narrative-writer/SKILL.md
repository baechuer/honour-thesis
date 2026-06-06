---
name: slo-breach-narrative-writer
description: "Writes SLO breach summaries with timeline, user impact, error budget effect, mitigation, and follow-up actions."
---

# Slo Breach Narrative Writer

Turns incident/SLO data into stakeholder-readable narrative.

## Use when

- The user has incident notes or SLO breach data.
- They need a timeline, impact, mitigation, and follow-ups.

## Not for

- Writing alert rules.
- Building dashboards.
- Deep trace debugging.

## Preconditions

- Timeline, metrics, or incident notes are available.
- Audience and reporting level are known.

## Workflow

1. Extract timeline and impact.
2. Connect metrics to SLO breach.
3. Summarize mitigation and current status.
4. List follow-up actions.

## Writing rules

- Do not overclaim root cause if not established.
- Keep user impact explicit.

## Default shape

- Summary
- Timeline
- Impact
- Mitigation/follow-up
