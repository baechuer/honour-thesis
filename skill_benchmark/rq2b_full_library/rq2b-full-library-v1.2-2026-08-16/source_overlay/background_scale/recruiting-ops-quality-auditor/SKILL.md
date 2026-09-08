---
name: recruiting-ops-quality-auditor
description: Audits recruiting pipeline operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Recruiting Ops Quality Auditor

## Use when

- The user wants quality assurance over resume, interview notes, job criteria, candidate comparison table before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: resume, interview notes, job criteria, candidate comparison table.

## Dependencies and resources

- resume file
- job criteria
- interview notes
- candidate stage
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
