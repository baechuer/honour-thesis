---
name: k8s-ops-intake-classifier
description: Classifies Kubernetes platform operations requests by input type, expected artifact, routing owner, urgency, and missing context.
---

# K8s Ops Intake Classifier

## Use when

- The user needs classification or routing for Kubernetes platform operations material before deeper work begins.

## Input and preconditions

- There is enough task context to decide category, owner, urgency, and next action.
- Relevant material: manifest, pod log, deployment event, cluster configuration.

## Dependencies and resources

- cluster context
- manifest
- pod logs
- namespace
- task-specific constraints

## Procedure

1. Separate the request into its material type, stated objective, urgency, and owner cues.
2. Apply the available category and routing criteria.
3. Record missing context that prevents a confident route.
4. Return the classification and the immediate next action.

## Output

Classification labels, routing decision, missing-context list, and next-step recommendation.
