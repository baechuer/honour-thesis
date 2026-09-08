---
name: thesis-ops-evidence-grounder
description: Grounds thesis research operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Thesis Ops Evidence Grounder

## Use when

- The user wants claims checked against thesis notes, supervisor feedback, proposal draft, experiment log rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: thesis notes, supervisor feedback, proposal draft, experiment log.

## Dependencies and resources

- research question
- supervisor note
- method plan
- literature notes
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
