---
name: sales-ops-quality-auditor
description: Audits sales enablement operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Sales Ops Quality Auditor

## Use when

- The user wants quality assurance over deal note, pitch deck, objection log, account plan before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: deal note, pitch deck, objection log, account plan.

## Dependencies and resources

- account profile
- deal stage
- buyer role
- sales collateral
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
