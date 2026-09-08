---
name: community-ops-evidence-grounder
description: Grounds community management operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Community Ops Evidence Grounder

## Use when

- The user wants claims checked against forum post, moderation queue, announcement draft, user feedback thread rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: forum post, moderation queue, announcement draft, user feedback thread.

## Dependencies and resources

- community guidelines
- thread context
- user history
- announcement goal
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
