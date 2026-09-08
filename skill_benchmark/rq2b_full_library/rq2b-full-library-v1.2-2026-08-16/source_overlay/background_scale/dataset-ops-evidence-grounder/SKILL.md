---
name: dataset-ops-evidence-grounder
description: Grounds dataset and analytics preparation claims in specific evidence snippets, source locations, and confidence notes.
---

# Dataset Ops Evidence Grounder

## Use when

- The user wants claims checked against CSV files, data dictionary, metric definitions, quality notes rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: CSV files, data dictionary, metric definitions, quality notes.

## Dependencies and resources

- dataset file
- schema
- metric definitions
- sampling notes
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
