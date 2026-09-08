---
name: incident-ops-monitoring-plan-builder
description: Builds a monitoring plan for incident and reliability operations with signals, thresholds, review cadence, and escalation owners.
---

# Incident Ops Monitoring Plan Builder

## Use when

- The user wants ongoing monitoring or follow-up design for incident and reliability operations.

## Input and preconditions

- Relevant signals, owners, and decision thresholds can be defined.
- Relevant material: incident timeline, logs, alerts, postmortem notes.

## Dependencies and resources

- timeline
- service logs
- alert history
- owner map
- task-specific constraints

## Procedure

1. Define the signals that indicate healthy, degraded, or unsafe operation.
2. Set measurable thresholds, review cadence, and escalation ownership.
3. Connect each alert to a practical response action.
4. Return the monitoring plan and escalation rules.

## Output

Monitoring plan with signals, thresholds, cadence, owners, and escalation rules.
