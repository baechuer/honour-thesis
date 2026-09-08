---
name: library-ops-quality-auditor
description: Audits library and archive operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Library Ops Quality Auditor

## Use when

- The user wants quality assurance over catalog record, archive note, metadata sheet, digitization plan before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: catalog record, archive note, metadata sheet, digitization plan.

## Dependencies and resources

- catalog schema
- collection metadata
- rights note
- preservation policy
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
