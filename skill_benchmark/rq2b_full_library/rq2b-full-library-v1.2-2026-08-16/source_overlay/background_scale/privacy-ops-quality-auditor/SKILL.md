---
name: privacy-ops-quality-auditor
description: Audits privacy operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Privacy Ops Quality Auditor

## Use when

- The user wants quality assurance over data inventory, DSR request, privacy notice, processing activity before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: data inventory, DSR request, privacy notice, processing activity.

## Dependencies and resources

- data map
- privacy policy
- jurisdiction note
- request details
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
