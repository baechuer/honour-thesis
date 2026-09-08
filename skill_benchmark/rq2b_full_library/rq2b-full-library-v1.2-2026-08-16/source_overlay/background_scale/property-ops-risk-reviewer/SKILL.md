---
name: property-ops-risk-reviewer
description: Reviews property management operations material for operational, compliance, security, quality, or delivery risk.
---

# Property Ops Risk Reviewer

## Use when

- The user wants risk findings from lease, maintenance ticket, inspection report, tenant message rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: lease, maintenance ticket, inspection report, tenant message.

## Dependencies and resources

- property record
- lease terms
- maintenance history
- tenant context
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
