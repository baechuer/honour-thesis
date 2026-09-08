---
name: k8s-ops-risk-reviewer
description: Reviews Kubernetes platform operations material for operational, compliance, security, quality, or delivery risk.
---

# K8s Ops Risk Reviewer

## Use when

- The user wants risk findings from manifest, pod log, deployment event, cluster configuration rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: manifest, pod log, deployment event, cluster configuration.

## Dependencies and resources

- cluster context
- manifest
- pod logs
- namespace
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
