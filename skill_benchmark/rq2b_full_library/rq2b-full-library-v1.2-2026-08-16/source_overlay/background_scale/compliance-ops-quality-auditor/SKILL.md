---
name: compliance-ops-quality-auditor
description: Audits compliance operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Compliance Ops Quality Auditor

## Use when

- The user wants quality assurance over control checklist, audit finding, policy exception, evidence packet before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: control checklist, audit finding, policy exception, evidence packet.

## Dependencies and resources

- control framework
- evidence files
- audit scope
- owner map
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
