---
name: ecommerce-ops-risk-reviewer
description: Reviews ecommerce operations material for operational, compliance, security, quality, or delivery risk.
---

# Ecommerce Ops Risk Reviewer

## Use when

- The user wants risk findings from order export, product listing, refund note, marketplace report rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: order export, product listing, refund note, marketplace report.

## Dependencies and resources

- order data
- product catalog
- marketplace rules
- customer message
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
