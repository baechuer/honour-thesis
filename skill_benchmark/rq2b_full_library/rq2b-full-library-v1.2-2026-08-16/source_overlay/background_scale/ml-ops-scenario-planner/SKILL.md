---
name: ml-ops-scenario-planner
description: Plans alternative scenarios for machine learning operations decisions under changing assumptions, constraints, or risks.
---

# Ml Ops Scenario Planner

## Use when

- The user wants scenario planning for machine learning operations rather than a single recommendation.

## Input and preconditions

- Key assumptions, decision options, or uncertainty drivers are available.
- Relevant material: model card, training log, evaluation table, dataset note.

## Dependencies and resources

- model artifact
- dataset split
- training config
- evaluation metric
- task-specific constraints

## Procedure

1. State the decision, assumptions, and uncertainty drivers.
2. Develop bounded alternative scenarios from the available constraints.
3. Identify outcomes, risks, and triggers for each scenario.
4. Return the scenario table and decision triggers.

## Output

Scenario table with assumptions, expected outcomes, risks, and decision triggers.
