---
name: docs-ops-quality-auditor
description: Audits document operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Docs Ops Quality Auditor

## Use when

- The user wants quality assurance over PDF, DOCX, Markdown file, policy draft, extracted text before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: PDF, DOCX, Markdown file, policy draft, extracted text.

## Dependencies and resources

- document file
- layout evidence
- source text
- format target
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
