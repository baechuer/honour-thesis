---
name: community-ops-quality-auditor
description: Audits community management operations artifacts for completeness, consistency, missing evidence, malformed fields, and process gaps.
---

# Community Ops Quality Auditor

## Use when

- The user wants quality assurance over forum post, moderation queue, announcement draft, user feedback thread before the artifact is used downstream.

## Input and preconditions

- Expected quality criteria or artifact shape is available.
- Relevant material: forum post, moderation queue, announcement draft, user feedback thread.

## Dependencies and resources

- community guidelines
- thread context
- user history
- announcement goal
- task-specific constraints

## Procedure

1. Compare the artifact against its expected structure and quality criteria.
2. Identify missing, inconsistent, malformed, or unsupported elements.
3. Distinguish blocking defects from minor improvements.
4. Return findings with a correction checklist.

## Output

Quality findings, missing elements, inconsistent details, and correction checklist.
