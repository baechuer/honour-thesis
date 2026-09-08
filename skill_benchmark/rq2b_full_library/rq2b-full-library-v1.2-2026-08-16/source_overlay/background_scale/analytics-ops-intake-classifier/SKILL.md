---
name: analytics-ops-intake-classifier
description: Classifies analytics and experimentation operations requests by input type, expected artifact, routing owner, urgency, and missing context.
---

# Analytics Ops Intake Classifier

## Use when

- The user needs classification or routing for analytics and experimentation operations material before deeper work begins.

## Input and preconditions

- There is enough task context to decide category, owner, urgency, and next action.
- Relevant material: experiment result, metric table, cohort data, analytics request.

## Dependencies and resources

- metric definitions
- experiment design
- cohort data
- analysis window
- task-specific constraints

## Procedure

1. Separate the request into its material type, stated objective, urgency, and owner cues.
2. Apply the available category and routing criteria.
3. Record missing context that prevents a confident route.
4. Return the classification and the immediate next action.

## Output

Classification labels, routing decision, missing-context list, and next-step recommendation.
