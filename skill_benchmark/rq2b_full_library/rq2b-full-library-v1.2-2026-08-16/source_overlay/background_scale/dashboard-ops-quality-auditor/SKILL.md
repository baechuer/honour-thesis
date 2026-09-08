---
name: dashboard-ops-quality-auditor
description: Audits dashboard and metric reporting artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Dashboard Ops Quality Auditor

## Use when

- The user wants quality assurance over dashboard screenshots, metric tables, alert notes, KPI definitions before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: dashboard screenshots, metric tables, alert notes, KPI definitions.

## Dependencies and resources

- dashboard export
- metric glossary
- time window
- owner notes
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
