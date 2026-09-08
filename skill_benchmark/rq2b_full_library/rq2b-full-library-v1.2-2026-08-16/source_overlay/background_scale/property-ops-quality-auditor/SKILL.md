---
name: property-ops-quality-auditor
description: Audits property management operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Property Ops Quality Auditor

## Use when

- The user wants quality assurance over lease, maintenance ticket, inspection report, tenant message before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: lease, maintenance ticket, inspection report, tenant message.

## Dependencies and resources

- property record
- lease terms
- maintenance history
- tenant context
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
