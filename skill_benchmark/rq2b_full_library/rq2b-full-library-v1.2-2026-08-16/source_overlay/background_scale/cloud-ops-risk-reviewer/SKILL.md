---
name: cloud-ops-risk-reviewer
description: Reviews cloud infrastructure operations material for operational, compliance, security, quality, or delivery risk.
---

# Cloud Ops Risk Reviewer

## Use when

- The user wants risk findings from cloud config, resource inventory, deployment note, cost report rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: cloud config, resource inventory, deployment note, cost report.

## Dependencies and resources

- cloud account
- resource inventory
- deployment config
- cost data
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
