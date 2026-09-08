---
name: logistics-ops-risk-reviewer
description: Reviews logistics and shipment operations material for operational, compliance, security, quality, or delivery risk.
---

# Logistics Ops Risk Reviewer

## Use when

- The user wants risk findings from shipment manifest, tracking update, carrier note, customs form rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: shipment manifest, tracking update, carrier note, customs form.

## Dependencies and resources

- shipment manifest
- carrier data
- delivery window
- customs details
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
