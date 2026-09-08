---
name: support-ops-quality-auditor
description: Audits customer support operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Support Ops Quality Auditor

## Use when

- The user wants quality assurance over support tickets, chat transcripts, issue labels, customer history before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: support tickets, chat transcripts, issue labels, customer history.

## Dependencies and resources

- ticket queue
- customer context
- product area
- severity policy
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
