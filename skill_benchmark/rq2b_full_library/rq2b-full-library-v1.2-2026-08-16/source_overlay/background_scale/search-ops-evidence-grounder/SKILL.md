---
name: search-ops-evidence-grounder
description: Grounds search and retrieval operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Search Ops Evidence Grounder

## Use when

- The user wants claims checked against search query log, retrieval results, index schema, relevance judgment rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: search query log, retrieval results, index schema, relevance judgment.

## Dependencies and resources

- query logs
- index schema
- relevance labels
- retrieval config
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
