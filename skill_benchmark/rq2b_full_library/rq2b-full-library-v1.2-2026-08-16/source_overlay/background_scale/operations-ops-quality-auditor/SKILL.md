---
name: operations-ops-quality-auditor
description: Audits general business operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Operations Ops Quality Auditor

## Use when

- The user wants quality assurance over SOP, process note, operations checklist, team request before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: SOP, process note, operations checklist, team request.

## Dependencies and resources

- process document
- owner map
- deadline
- operational constraint
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
