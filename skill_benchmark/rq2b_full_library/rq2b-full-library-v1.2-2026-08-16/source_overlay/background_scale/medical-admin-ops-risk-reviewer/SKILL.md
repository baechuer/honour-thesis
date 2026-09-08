---
name: medical-admin-ops-risk-reviewer
description: Reviews medical administration operations material for operational, compliance, security, quality, or delivery risk.
---

# Medical Admin Ops Risk Reviewer

## Use when

- The user wants risk findings from appointment note, referral text, intake form, clinic instruction rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: appointment note, referral text, intake form, clinic instruction.

## Dependencies and resources

- patient-provided note
- appointment details
- clinic policy
- form fields
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
