---
name: search-ops-quality-auditor
description: Audits search and retrieval operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Search Ops Quality Auditor

## Use when

- The user wants quality assurance over search query log, retrieval results, index schema, relevance judgment before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: search query log, retrieval results, index schema, relevance judgment.

## Dependencies and resources

- query logs
- index schema
- relevance labels
- retrieval config
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
