---
name: sre-ops-quality-auditor
description: Audits site reliability engineering operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Sre Ops Quality Auditor

## Use when

- The user wants quality assurance over SLO report, runbook, alert history, reliability review before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: SLO report, runbook, alert history, reliability review.

## Dependencies and resources

- service map
- SLO definitions
- alert data
- runbook
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
