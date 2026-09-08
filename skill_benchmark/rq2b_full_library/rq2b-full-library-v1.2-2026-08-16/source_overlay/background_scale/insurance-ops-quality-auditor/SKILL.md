---
name: insurance-ops-quality-auditor
description: Audits insurance claims operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Insurance Ops Quality Auditor

## Use when

- The user wants quality assurance over claim form, policy wording, incident evidence, assessor notes before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: claim form, policy wording, incident evidence, assessor notes.

## Dependencies and resources

- claim file
- policy document
- incident evidence
- coverage criteria
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
