---
name: travel-ops-risk-reviewer
description: Reviews travel planning operations material for operational, compliance, security, quality, or delivery risk.
---

# Travel Ops Risk Reviewer

## Use when

- The user wants risk findings from itinerary, booking email, visa note, travel constraint list rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: itinerary, booking email, visa note, travel constraint list.

## Dependencies and resources

- destination
- dates
- booking details
- traveler constraints
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
