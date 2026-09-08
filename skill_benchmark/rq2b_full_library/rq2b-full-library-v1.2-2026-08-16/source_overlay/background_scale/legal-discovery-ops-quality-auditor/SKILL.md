---
name: legal-discovery-ops-quality-auditor
description: Audits legal discovery operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Legal Discovery Ops Quality Auditor

## Use when

- The user wants quality assurance over document production, privilege log, deposition note, evidence request before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: document production, privilege log, deposition note, evidence request.

## Dependencies and resources

- case context
- document set
- privilege criteria
- request scope
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
