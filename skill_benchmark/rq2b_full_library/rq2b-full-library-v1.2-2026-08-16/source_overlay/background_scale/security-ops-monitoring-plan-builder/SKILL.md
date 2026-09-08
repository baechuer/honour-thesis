---
name: security-ops-monitoring-plan-builder
description: Builds a monitoring plan for application security operations with signals, thresholds, review cadence, and escalation owners.
---

# Security Ops Monitoring Plan Builder

## Use when

- The user wants ongoing monitoring or follow-up design for application security operations.

## Input and preconditions

- Relevant signals, owners, and decision thresholds can be defined.
- Relevant material: repository files, threat notes, scan findings, architecture description.

## Dependencies and resources

- codebase
- architecture context
- security findings
- asset list
- task-specific constraints

## Procedure

1. Define the signals that indicate healthy, degraded, or unsafe operation.
2. Set measurable thresholds, review cadence, and escalation ownership.
3. Connect each alert to a practical response action.
4. Return the monitoring plan and escalation rules.

## Output

Monitoring plan with signals, thresholds, cadence, owners, and escalation rules.
