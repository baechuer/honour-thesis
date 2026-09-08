---
name: knowledge-ops-quality-auditor
description: Audits knowledge management operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Knowledge Ops Quality Auditor

## Use when

- The user wants quality assurance over notes, wiki pages, knowledge base articles, taxonomy before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: notes, wiki pages, knowledge base articles, taxonomy.

## Dependencies and resources

- note corpus
- taxonomy
- source links
- owner context
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
