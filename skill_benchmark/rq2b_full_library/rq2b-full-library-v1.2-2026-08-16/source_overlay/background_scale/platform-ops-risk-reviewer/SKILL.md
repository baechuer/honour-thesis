---
name: platform-ops-risk-reviewer
description: Reviews platform engineering operations material for operational, compliance, security, quality, or delivery risk.
---

# Platform Ops Risk Reviewer

## Use when

- The user wants risk findings from developer platform request, service catalog, template repo, platform metric rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: developer platform request, service catalog, template repo, platform metric.

## Dependencies and resources

- platform service
- template repository
- developer workflow
- service owner
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
