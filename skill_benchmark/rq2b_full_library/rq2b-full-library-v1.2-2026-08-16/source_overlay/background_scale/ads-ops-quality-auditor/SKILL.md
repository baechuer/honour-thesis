---
name: ads-ops-quality-auditor
description: Audits paid advertising operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Ads Ops Quality Auditor

## Use when

- The user wants quality assurance over ad account report, campaign settings, creative brief, budget note before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: ad account report, campaign settings, creative brief, budget note.

## Dependencies and resources

- ad platform
- budget
- targeting settings
- conversion data
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
