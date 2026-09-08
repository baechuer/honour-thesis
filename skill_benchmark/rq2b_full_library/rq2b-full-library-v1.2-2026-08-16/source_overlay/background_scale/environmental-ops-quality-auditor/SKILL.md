---
name: environmental-ops-quality-auditor
description: Audits environmental compliance operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Environmental Ops Quality Auditor

## Use when

- The user wants quality assurance over emissions report, permit condition, monitoring data, incident note before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: emissions report, permit condition, monitoring data, incident note.

## Dependencies and resources

- permit
- monitoring data
- emissions factor
- reporting period
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
