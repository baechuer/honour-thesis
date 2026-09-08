---
name: logistics-ops-quality-auditor
description: Audits logistics and shipment operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Logistics Ops Quality Auditor

## Use when

- The user wants quality assurance over shipment manifest, tracking update, carrier note, customs form before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: shipment manifest, tracking update, carrier note, customs form.

## Dependencies and resources

- shipment manifest
- carrier data
- delivery window
- customs details
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
