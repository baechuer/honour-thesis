---
name: vendor-ops-quality-auditor
description: Audits vendor and procurement review artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Vendor Ops Quality Auditor

## Use when

- The user wants quality assurance over vendor proposal, security questionnaire, pricing sheet, contract summary before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: vendor proposal, security questionnaire, pricing sheet, contract summary.

## Dependencies and resources

- vendor profile
- pricing document
- security answers
- procurement criteria
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
