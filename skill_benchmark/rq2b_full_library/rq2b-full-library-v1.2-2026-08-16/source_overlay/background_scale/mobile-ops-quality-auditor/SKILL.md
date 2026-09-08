---
name: mobile-ops-quality-auditor
description: Audits mobile application operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Mobile Ops Quality Auditor

## Use when

- The user wants quality assurance over app crash log, release note, store review, mobile test report before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: app crash log, release note, store review, mobile test report.

## Dependencies and resources

- mobile app build
- device context
- crash log
- release channel
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
