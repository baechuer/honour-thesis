---
name: procurement-ops-quality-auditor
description: Audits procurement operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Procurement Ops Quality Auditor

## Use when

- The user wants quality assurance over purchase request, vendor quote, RFP response, approval note before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: purchase request, vendor quote, RFP response, approval note.

## Dependencies and resources

- purchase request
- vendor quote
- budget code
- approval policy
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
