---
name: bioinformatics-ops-evidence-grounder
description: Grounds bioinformatics operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Bioinformatics Ops Evidence Grounder

## Use when

- The user wants claims checked against sequence file, variant table, pipeline log, sample metadata rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: sequence file, variant table, pipeline log, sample metadata.

## Dependencies and resources

- sequence data
- sample metadata
- pipeline config
- reference genome
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
