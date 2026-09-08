---
name: travel-ops-monitoring-plan-builder
description: Builds a monitoring plan for travel planning operations with signals, thresholds, review cadence, and escalation owners.
---

# Travel Ops Monitoring Plan Builder

## Use when

- The user wants ongoing monitoring or follow-up design for travel planning operations.

## Input and preconditions

- Relevant signals, owners, and decision thresholds can be defined.
- Relevant material: itinerary, booking email, visa note, travel constraint list.

## Dependencies and resources

- destination
- dates
- booking details
- traveler constraints
- task-specific constraints

## Procedure

1. Define the signals that indicate healthy, degraded, or unsafe operation.
2. Set measurable thresholds, review cadence, and escalation ownership.
3. Connect each alert to a practical response action.
4. Return the monitoring plan and escalation rules.

## Output

Monitoring plan with signals, thresholds, cadence, owners, and escalation rules.
