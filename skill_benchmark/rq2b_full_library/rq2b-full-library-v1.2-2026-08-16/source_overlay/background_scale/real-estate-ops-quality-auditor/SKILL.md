---
name: real-estate-ops-quality-auditor
description: Audits real estate transaction operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Real Estate Ops Quality Auditor

## Use when

- The user wants quality assurance over listing brief, offer terms, inspection note, settlement timeline before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: listing brief, offer terms, inspection note, settlement timeline.

## Dependencies and resources

- listing details
- buyer criteria
- offer terms
- inspection evidence
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
