---
name: personal-ops-quality-auditor
description: Audits personal productivity operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Personal Ops Quality Auditor

## Use when

- The user wants quality assurance over task list, personal note, habit log, calendar item before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: task list, personal note, habit log, calendar item.

## Dependencies and resources

- task list
- calendar
- priority context
- personal constraints
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
