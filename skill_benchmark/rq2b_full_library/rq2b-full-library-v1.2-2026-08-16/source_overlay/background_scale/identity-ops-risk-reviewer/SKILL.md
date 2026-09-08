---
name: identity-ops-risk-reviewer
description: Reviews identity and access operations material for operational, compliance, security, quality, or delivery risk.
---

# Identity Ops Risk Reviewer

## Use when

- The user wants risk findings from access request, role matrix, audit log, permission review rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: access request, role matrix, audit log, permission review.

## Dependencies and resources

- identity provider
- role matrix
- access logs
- approval policy
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
