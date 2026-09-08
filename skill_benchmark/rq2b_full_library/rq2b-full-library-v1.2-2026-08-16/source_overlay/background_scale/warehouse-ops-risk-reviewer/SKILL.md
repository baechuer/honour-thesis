---
name: warehouse-ops-risk-reviewer
description: Reviews warehouse inventory operations material for operational, compliance, security, quality, or delivery risk.
---

# Warehouse Ops Risk Reviewer

## Use when

- The user wants risk findings from stock count, pick list, receiving note, inventory adjustment rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: stock count, pick list, receiving note, inventory adjustment.

## Dependencies and resources

- inventory export
- SKU catalog
- location map
- receiving record
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
