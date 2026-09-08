---
name: legal-ops-risk-reviewer
description: Reviews legal and policy operations material for operational, compliance, security, quality, or delivery risk.
---

# Legal Ops Risk Reviewer

## Use when

- The user wants risk findings from policy text, legal memo, contract clause, compliance question rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: policy text, legal memo, contract clause, compliance question.

## Dependencies and resources

- legal text
- jurisdiction note
- policy version
- review purpose
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
