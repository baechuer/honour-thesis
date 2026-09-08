---
name: academic-admin-ops-quality-auditor
description: Audits academic administration operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Academic Admin Ops Quality Auditor

## Use when

- The user wants quality assurance over course policy, enrollment note, assessment record, student request before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: course policy, enrollment note, assessment record, student request.

## Dependencies and resources

- institution policy
- student record
- assessment criteria
- deadline
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
