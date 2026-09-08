---
name: product-ops-evidence-grounder
description: Grounds product management operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Product Ops Evidence Grounder

## Use when

- The user wants claims checked against feature brief, roadmap item, user feedback, acceptance criteria rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: feature brief, roadmap item, user feedback, acceptance criteria.

## Dependencies and resources

- feature brief
- user feedback
- roadmap context
- acceptance criteria
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
