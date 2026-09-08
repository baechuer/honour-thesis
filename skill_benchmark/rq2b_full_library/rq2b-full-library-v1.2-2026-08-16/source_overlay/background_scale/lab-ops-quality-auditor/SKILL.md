---
name: lab-ops-quality-auditor
description: Audits laboratory and experiment operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Lab Ops Quality Auditor

## Use when

- The user wants quality assurance over experiment protocol, measurement table, lab notes, result log before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: experiment protocol, measurement table, lab notes, result log.

## Dependencies and resources

- protocol
- measurement data
- instrument notes
- safety constraints
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
