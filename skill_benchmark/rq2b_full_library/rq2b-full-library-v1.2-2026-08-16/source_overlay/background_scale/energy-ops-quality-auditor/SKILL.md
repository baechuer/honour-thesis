---
name: energy-ops-quality-auditor
description: Audits energy operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Energy Ops Quality Auditor

## Use when

- The user wants quality assurance over usage report, meter reading, sustainability plan, tariff note before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: usage report, meter reading, sustainability plan, tariff note.

## Dependencies and resources

- meter data
- tariff schedule
- facility profile
- sustainability target
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
