---
name: ecommerce-ops-intake-classifier
description: Classifies ecommerce operations requests by input type, expected artifact, routing owner, urgency, and missing context.
---

# Ecommerce Ops Intake Classifier

## Use when

- The user needs classification or routing for ecommerce operations material before deeper work begins.

## Input and preconditions

- There is enough task context to decide category, owner, urgency, and next action.
- Relevant material: order export, product listing, refund note, marketplace report.

## Dependencies and resources

- order data
- product catalog
- marketplace rules
- customer message
- task-specific constraints

## Procedure

1. Separate the request into its material type, stated objective, urgency, and owner cues.
2. Apply the available category and routing criteria.
3. Record missing context that prevents a confident route.
4. Return the classification and the immediate next action.

## Output

Classification labels, routing decision, missing-context list, and next-step recommendation.
