---
name: dataset-ops-quality-auditor
description: Audits dataset and analytics preparation artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Dataset Ops Quality Auditor

## Use when

- The user wants quality assurance over CSV files, data dictionary, metric definitions, quality notes before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: CSV files, data dictionary, metric definitions, quality notes.

## Dependencies and resources

- dataset file
- schema
- metric definitions
- sampling notes
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
