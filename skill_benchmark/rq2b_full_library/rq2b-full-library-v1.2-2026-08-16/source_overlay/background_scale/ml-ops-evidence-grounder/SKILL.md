---
name: ml-ops-evidence-grounder
description: Grounds machine learning operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Ml Ops Evidence Grounder

## Use when

- The user wants claims checked against model card, training log, evaluation table, dataset note rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: model card, training log, evaluation table, dataset note.

## Dependencies and resources

- model artifact
- dataset split
- training config
- evaluation metric
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
