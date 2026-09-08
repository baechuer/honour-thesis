---
name: platform-ops-quality-auditor
description: Audits platform engineering operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Platform Ops Quality Auditor

## Use when

- The user wants quality assurance over developer platform request, service catalog, template repo, platform metric before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: developer platform request, service catalog, template repo, platform metric.

## Dependencies and resources

- platform service
- template repository
- developer workflow
- service owner
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
