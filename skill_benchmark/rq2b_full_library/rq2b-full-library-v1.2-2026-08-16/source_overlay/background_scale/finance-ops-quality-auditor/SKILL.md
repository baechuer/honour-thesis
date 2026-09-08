---
name: finance-ops-quality-auditor
description: Audits finance and accounting operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Finance Ops Quality Auditor

## Use when

- The user wants quality assurance over financial report, budget sheet, invoice set, forecast model before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: financial report, budget sheet, invoice set, forecast model.

## Dependencies and resources

- financial data
- accounting period
- chart of accounts
- assumption notes
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
