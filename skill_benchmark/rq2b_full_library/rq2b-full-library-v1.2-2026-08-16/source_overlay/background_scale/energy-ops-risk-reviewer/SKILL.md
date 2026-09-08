---
name: energy-ops-risk-reviewer
description: Reviews energy operations material for operational, compliance, security, quality, or delivery risk.
---

# Energy Ops Risk Reviewer

## Use when

- The user wants risk findings from usage report, meter reading, sustainability plan, tariff note rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: usage report, meter reading, sustainability plan, tariff note.

## Dependencies and resources

- meter data
- tariff schedule
- facility profile
- sustainability target
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
