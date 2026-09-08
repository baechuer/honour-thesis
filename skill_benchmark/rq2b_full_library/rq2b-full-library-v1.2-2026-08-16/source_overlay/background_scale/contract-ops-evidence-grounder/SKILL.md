---
name: contract-ops-evidence-grounder
description: Grounds contract operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Contract Ops Evidence Grounder

## Use when

- The user wants claims checked against contract text, amendment notes, renewal terms, obligation logs rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: contract text, amendment notes, renewal terms, obligation logs.

## Dependencies and resources

- contract document
- party names
- clause references
- effective dates
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
