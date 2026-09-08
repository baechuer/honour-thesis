---
name: facilities-ops-quality-auditor
description: Audits facilities operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Facilities Ops Quality Auditor

## Use when

- The user wants quality assurance over maintenance request, space plan, safety report, vendor schedule before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: maintenance request, space plan, safety report, vendor schedule.

## Dependencies and resources

- facility map
- maintenance log
- safety policy
- vendor contact
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
