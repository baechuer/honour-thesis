---
name: security-ops-quality-auditor
description: Audits application security operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Security Ops Quality Auditor

## Use when

- The user wants quality assurance over repository files, threat notes, scan findings, architecture description before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: repository files, threat notes, scan findings, architecture description.

## Dependencies and resources

- codebase
- architecture context
- security findings
- asset list
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
