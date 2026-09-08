---
name: iot-ops-risk-reviewer
description: Reviews IoT operations material for operational, compliance, security, quality, or delivery risk.
---

# Iot Ops Risk Reviewer

## Use when

- The user wants risk findings from device telemetry, firmware note, sensor log, provisioning record rather than extraction or formatting.

## Input and preconditions

- The task includes enough context to identify impact, likelihood, and mitigation.
- Relevant material: device telemetry, firmware note, sensor log, provisioning record.

## Dependencies and resources

- device registry
- telemetry data
- firmware version
- network context
- task-specific constraints

## Procedure

1. Identify concrete risks in the supplied material.
2. Estimate impact and likelihood using the available evidence.
3. Connect each material risk to a mitigation or an owner question.
4. Return a prioritised risk register.

## Output

Risk register with severity, evidence, mitigation, and owner questions.
