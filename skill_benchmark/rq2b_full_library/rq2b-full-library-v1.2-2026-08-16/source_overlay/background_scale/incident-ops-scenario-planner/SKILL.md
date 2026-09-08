---
name: incident-ops-scenario-planner
description: Plans alternative scenarios for incident and reliability operations decisions under changing assumptions, constraints, or risks.
---

# Incident Ops Scenario Planner

## Use when

- The user wants scenario planning for incident and reliability operations rather than a single recommendation.

## Input and preconditions

- Key assumptions, decision options, or uncertainty drivers are available.
- Relevant material: incident timeline, logs, alerts, postmortem notes.

## Dependencies and resources

- timeline
- service logs
- alert history
- owner map
- task-specific constraints

## Procedure

1. State the decision, assumptions, and uncertainty drivers.
2. Develop bounded alternative scenarios from the available constraints.
3. Identify outcomes, risks, and triggers for each scenario.
4. Return the scenario table and decision triggers.

## Output

Scenario table with assumptions, expected outcomes, risks, and decision triggers.
