---
name: email-ops-quality-auditor
description: Audits email and messaging operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Email Ops Quality Auditor

## Use when

- The user wants quality assurance over draft email, message thread, recipient context, tone constraints before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: draft email, message thread, recipient context, tone constraints.

## Dependencies and resources

- message thread
- recipient relationship
- tone target
- requested action
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
