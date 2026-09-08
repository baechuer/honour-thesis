---
name: warehouse-ops-quality-auditor
description: Audits warehouse inventory operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Warehouse Ops Quality Auditor

## Use when

- The user wants quality assurance over stock count, pick list, receiving note, inventory adjustment before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: stock count, pick list, receiving note, inventory adjustment.

## Dependencies and resources

- inventory export
- SKU catalog
- location map
- receiving record
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
