---
name: manufacturing-ops-quality-auditor
description: Audits manufacturing operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Manufacturing Ops Quality Auditor

## Use when

- The user wants quality assurance over work order, defect log, production schedule, quality report before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: work order, defect log, production schedule, quality report.

## Dependencies and resources

- work order
- production line
- quality criteria
- operator notes
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
