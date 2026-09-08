---
name: api-ops-quality-auditor
description: Audits API integration operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Api Ops Quality Auditor

## Use when

- The user wants quality assurance over API spec, endpoint docs, integration error, webhook payload before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: API spec, endpoint docs, integration error, webhook payload.

## Dependencies and resources

- API documentation
- auth method
- payload example
- rate limits
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
