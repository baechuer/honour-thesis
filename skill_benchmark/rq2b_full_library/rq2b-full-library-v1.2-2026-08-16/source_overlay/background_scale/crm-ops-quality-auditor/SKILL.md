---
name: crm-ops-quality-auditor
description: Audits CRM and sales operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Crm Ops Quality Auditor

## Use when

- The user wants quality assurance over CRM records, account notes, opportunity fields, email history before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: CRM records, account notes, opportunity fields, email history.

## Dependencies and resources

- CRM export
- account stage
- contact fields
- activity history
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
