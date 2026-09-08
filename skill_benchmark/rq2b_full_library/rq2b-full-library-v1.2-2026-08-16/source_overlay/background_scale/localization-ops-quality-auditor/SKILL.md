---
name: localization-ops-quality-auditor
description: Audits localization and translation operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Localization Ops Quality Auditor

## Use when

- The user wants quality assurance over source copy, translation memory, locale guide, glossary before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: source copy, translation memory, locale guide, glossary.

## Dependencies and resources

- source text
- target locale
- glossary
- style guide
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
