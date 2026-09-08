---
name: analytics-ops-quality-auditor
description: Audits analytics and experimentation operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Analytics Ops Quality Auditor

## Use when

- The user wants quality assurance over experiment result, metric table, cohort data, analytics request before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: experiment result, metric table, cohort data, analytics request.

## Dependencies and resources

- metric definitions
- experiment design
- cohort data
- analysis window
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
