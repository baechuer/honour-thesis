---
name: warehouse-ops-monitoring-plan-builder
description: Builds a monitoring plan for warehouse inventory operations with signals, thresholds, review cadence, and escalation owners.
---

# Warehouse Ops Monitoring Plan Builder

## Use when

- The user wants ongoing monitoring or follow-up design for warehouse inventory operations.

## Input and preconditions

- Relevant signals, owners, and decision thresholds can be defined.
- Relevant material: stock count, pick list, receiving note, inventory adjustment.

## Dependencies and resources

- inventory export
- SKU catalog
- location map
- receiving record
- task-specific constraints

## Procedure

1. Define the signals that indicate healthy, degraded, or unsafe operation.
2. Set measurable thresholds, review cadence, and escalation ownership.
3. Connect each alert to a practical response action.
4. Return the monitoring plan and escalation rules.

## Output

Monitoring plan with signals, thresholds, cadence, owners, and escalation rules.
