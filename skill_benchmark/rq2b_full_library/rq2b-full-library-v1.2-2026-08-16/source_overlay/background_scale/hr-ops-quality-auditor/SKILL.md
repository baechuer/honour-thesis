---
name: hr-ops-quality-auditor
description: Audits human resources operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Hr Ops Quality Auditor

## Use when

- The user wants quality assurance over candidate notes, performance feedback, role description, HR policy before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: candidate notes, performance feedback, role description, HR policy.

## Dependencies and resources

- role profile
- employee context
- policy document
- feedback records
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
