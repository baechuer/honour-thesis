---
name: web-ops-risk-reviewer
description: Reviews web automation and QA material for operational, compliance, security, quality, or delivery risk.
---

# Web Ops Risk Reviewer

## Use when

- The user wants risk findings from web page, browser state, test flow, screenshot evidence rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: web page, browser state, test flow, screenshot evidence.

## Dependencies and resources

- web target
- browser runtime
- test data
- screenshot evidence
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
