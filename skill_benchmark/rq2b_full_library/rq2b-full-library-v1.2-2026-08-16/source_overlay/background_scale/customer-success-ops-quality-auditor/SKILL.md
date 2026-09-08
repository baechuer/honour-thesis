---
name: customer-success-ops-quality-auditor
description: Audits customer success operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Customer Success Ops Quality Auditor

## Use when

- The user wants quality assurance over account health note, renewal plan, usage report, success plan before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: account health note, renewal plan, usage report, success plan.

## Dependencies and resources

- account profile
- usage data
- renewal date
- success criteria
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
