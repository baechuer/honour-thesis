---
name: research-ops-quality-auditor
description: Audits research and source review artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Research Ops Quality Auditor

## Use when

- The user wants quality assurance over papers, reports, source notes, citation metadata before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: papers, reports, source notes, citation metadata.

## Dependencies and resources

- source text
- citation metadata
- method section
- evidence snippets
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
