---
name: dataset-ops-scenario-planner
description: Plans alternative scenarios for dataset and analytics preparation decisions under changing assumptions, constraints, or risks.
---

# Dataset Ops Scenario Planner

## Use when

- The user wants scenario planning for dataset and analytics preparation rather than a single recommendation.

## Input and preconditions

- Key assumptions, decision options, or uncertainty drivers are available.
- Relevant material: CSV files, data dictionary, metric definitions, quality notes.

## Dependencies and resources

- dataset file
- schema
- metric definitions
- sampling notes
- task-specific constraints

## Procedure

1. State the decision, assumptions, and uncertainty drivers.
2. Develop bounded alternative scenarios from the available constraints.
3. Identify outcomes, risks, and triggers for each scenario.
4. Return the scenario table and decision triggers.

## Output

Scenario table with assumptions, expected outcomes, risks, and decision triggers.
