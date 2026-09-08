---
name: web-ops-quality-auditor
description: Audits web automation and QA artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Web Ops Quality Auditor

## Use when

- The user wants quality assurance over web page, browser state, test flow, screenshot evidence before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: web page, browser state, test flow, screenshot evidence.

## Dependencies and resources

- web target
- browser runtime
- test data
- screenshot evidence
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
