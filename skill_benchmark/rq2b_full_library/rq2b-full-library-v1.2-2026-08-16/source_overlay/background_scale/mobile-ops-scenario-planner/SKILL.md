---
name: mobile-ops-scenario-planner
description: Plans alternative scenarios for mobile application operations decisions under changing assumptions, constraints, or risks.
---

# Mobile Ops Scenario Planner

## Use when

- The user wants scenario planning for mobile application operations rather than a single recommendation.

## Input and preconditions

- Key assumptions, decision options, or uncertainty drivers are available.
- Relevant material: app crash log, release note, store review, mobile test report.

## Dependencies and resources

- mobile app build
- device context
- crash log
- release channel
- task-specific constraints

## Procedure

1. State the decision, assumptions, and uncertainty drivers.
2. Develop bounded alternative scenarios from the available constraints.
3. Identify outcomes, risks, and triggers for each scenario.
4. Return the scenario table and decision triggers.

## Output

Scenario table with assumptions, expected outcomes, risks, and decision triggers.
