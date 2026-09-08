---
name: contract-ops-quality-auditor
description: Audits contract operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Contract Ops Quality Auditor

## Use when

- The user wants quality assurance over contract text, amendment notes, renewal terms, obligation logs before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: contract text, amendment notes, renewal terms, obligation logs.

## Dependencies and resources

- contract document
- party names
- clause references
- effective dates
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
