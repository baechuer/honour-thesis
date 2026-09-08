---
name: search-ops-monitoring-plan-builder
description: Builds a monitoring plan for search and retrieval operations with signals, thresholds, review cadence, and escalation owners.
---

# Search Ops Monitoring Plan Builder

## Use when

- The user wants ongoing monitoring or follow-up design for search and retrieval operations.

## Input and preconditions

- Relevant signals, owners, and decision thresholds can be defined.
- Relevant material: search query log, retrieval results, index schema, relevance judgment.

## Dependencies and resources

- query logs
- index schema
- relevance labels
- retrieval config
- task-specific constraints

## Procedure

1. Define the signals that indicate healthy, degraded, or unsafe operation.
2. Set measurable thresholds, review cadence, and escalation ownership.
3. Connect each alert to a practical response action.
4. Return the monitoring plan and escalation rules.

## Output

Monitoring plan with signals, thresholds, cadence, owners, and escalation rules.
