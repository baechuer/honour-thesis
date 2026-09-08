---
name: k8s-ops-failure-diagnoser
description: Diagnoses why a Kubernetes platform operations workflow, artifact, or previous answer failed to meet expectations.
---

# K8s Ops Failure Diagnoser

## Use when

- The user wants failure analysis for Kubernetes platform operations rather than a fresh artifact.

## Input and preconditions

- There is a failed output, error report, mismatch, or user complaint to analyze.
- Relevant material: manifest, pod log, deployment event, cluster configuration.

## Dependencies and resources

- cluster context
- manifest
- pod logs
- namespace
- task-specific constraints

## Procedure

1. Collect the failed output, expected outcome, and available evidence.
2. Classify the observed mismatch and trace plausible contributing causes.
3. Separate established causes from hypotheses needing verification.
4. Return corrective actions with evidence links.

## Output

Failure classification, evidence, root-cause hypothesis, and corrective action.
