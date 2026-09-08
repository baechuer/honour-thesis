---
name: iot-ops-quality-auditor
description: Audits IoT operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Iot Ops Quality Auditor

## Use when

- The user wants quality assurance over device telemetry, firmware note, sensor log, provisioning record before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: device telemetry, firmware note, sensor log, provisioning record.

## Dependencies and resources

- device registry
- telemetry data
- firmware version
- network context
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
