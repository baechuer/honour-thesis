---
name: seo-ops-evidence-grounder
description: Grounds search engine optimization operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Seo Ops Evidence Grounder

## Use when

- The user wants claims checked against keyword list, page audit, ranking report, content brief rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: keyword list, page audit, ranking report, content brief.

## Dependencies and resources

- target page
- keyword data
- search intent
- ranking baseline
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
