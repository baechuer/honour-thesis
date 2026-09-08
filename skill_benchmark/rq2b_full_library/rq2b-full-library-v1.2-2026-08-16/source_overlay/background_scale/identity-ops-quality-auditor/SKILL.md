---
name: identity-ops-quality-auditor
description: Audits identity and access operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Identity Ops Quality Auditor

## Use when

- The user wants quality assurance over access request, role matrix, audit log, permission review before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: access request, role matrix, audit log, permission review.

## Dependencies and resources

- identity provider
- role matrix
- access logs
- approval policy
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
