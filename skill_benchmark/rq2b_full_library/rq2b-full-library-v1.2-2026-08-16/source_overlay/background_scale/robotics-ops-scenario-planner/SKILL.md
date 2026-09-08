---
name: robotics-ops-scenario-planner
description: Plans alternative scenarios for robotics operations decisions under changing assumptions, constraints, or risks.
---

# Robotics Ops Scenario Planner

## Use when

- The user wants scenario planning for robotics operations rather than a single recommendation.

## Input and preconditions

- Key assumptions, decision options, or uncertainty drivers are available.
- Relevant material: robot log, mission plan, sensor trace, calibration note.

## Dependencies and resources

- robot platform
- sensor data
- mission objective
- calibration file
- task-specific constraints

## Procedure

1. State the decision, assumptions, and uncertainty drivers.
2. Develop bounded alternative scenarios from the available constraints.
3. Identify outcomes, risks, and triggers for each scenario.
4. Return the scenario table and decision triggers.

## Output

Scenario table with assumptions, expected outcomes, risks, and decision triggers.
