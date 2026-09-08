---
name: meeting-ops-quality-auditor
description: Audits meeting and planning operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Meeting Ops Quality Auditor

## Use when

- The user wants quality assurance over meeting transcript, agenda notes, calendar constraints, action list before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: meeting transcript, agenda notes, calendar constraints, action list.

## Dependencies and resources

- meeting notes
- participant list
- calendar window
- action owners
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
