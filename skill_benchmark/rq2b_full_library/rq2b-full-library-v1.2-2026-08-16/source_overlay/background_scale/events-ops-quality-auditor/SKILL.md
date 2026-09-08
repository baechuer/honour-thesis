---
name: events-ops-quality-auditor
description: Audits event planning operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Events Ops Quality Auditor

## Use when

- The user wants quality assurance over event brief, attendee list, venue note, run sheet before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: event brief, attendee list, venue note, run sheet.

## Dependencies and resources

- event brief
- attendee list
- venue constraints
- run sheet
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
