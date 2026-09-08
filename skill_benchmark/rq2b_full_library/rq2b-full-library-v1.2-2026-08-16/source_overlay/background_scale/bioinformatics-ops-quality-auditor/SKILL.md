---
name: bioinformatics-ops-quality-auditor
description: Audits bioinformatics operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Bioinformatics Ops Quality Auditor

## Use when

- The user wants quality assurance over sequence file, variant table, pipeline log, sample metadata before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: sequence file, variant table, pipeline log, sample metadata.

## Dependencies and resources

- sequence data
- sample metadata
- pipeline config
- reference genome
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
