---
name: ecommerce-ops-quality-auditor
description: Audits ecommerce operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Ecommerce Ops Quality Auditor

## Use when

- The user wants quality assurance over order export, product listing, refund note, marketplace report before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: order export, product listing, refund note, marketplace report.

## Dependencies and resources

- order data
- product catalog
- marketplace rules
- customer message
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
