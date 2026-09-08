---
name: api-ops-risk-reviewer
description: Reviews API integration operations material for operational, compliance, security, quality, or delivery risk.
---

# Api Ops Risk Reviewer

## Use when

- The user wants risk findings from API spec, endpoint docs, integration error, webhook payload rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: API spec, endpoint docs, integration error, webhook payload.

## Dependencies and resources

- API documentation
- auth method
- payload example
- rate limits
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
