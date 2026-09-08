---
name: robotics-ops-risk-reviewer
description: Reviews robotics operations material for operational, compliance, security, quality, or delivery risk.
---

# Robotics Ops Risk Reviewer

## Use when

- The user wants risk findings from robot log, mission plan, sensor trace, calibration note rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: robot log, mission plan, sensor trace, calibration note.

## Dependencies and resources

- robot platform
- sensor data
- mission objective
- calibration file
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
