---
name: library-ops-evidence-grounder
description: Grounds library and archive operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Library Ops Evidence Grounder

## Use when

- The user wants claims checked against catalog record, archive note, metadata sheet, digitization plan rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: catalog record, archive note, metadata sheet, digitization plan.

## Dependencies and resources

- catalog schema
- collection metadata
- rights note
- preservation policy
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
