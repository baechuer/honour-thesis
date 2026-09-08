---
name: database-ops-quality-auditor
description: Audits database operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Database Ops Quality Auditor

## Use when

- The user wants quality assurance over schema, migration file, query plan, data quality note before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: schema, migration file, query plan, data quality note.

## Dependencies and resources

- database schema
- migration file
- query plan
- data sample
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
