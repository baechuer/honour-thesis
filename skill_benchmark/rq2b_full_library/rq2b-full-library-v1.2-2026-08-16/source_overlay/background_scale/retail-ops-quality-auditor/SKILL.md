---
name: retail-ops-quality-auditor
description: Audits retail operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Retail Ops Quality Auditor

## Use when

- The user wants quality assurance over sales report, product catalog, store note, promotion plan before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: sales report, product catalog, store note, promotion plan.

## Dependencies and resources

- sales data
- store profile
- product catalog
- promotion calendar
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
