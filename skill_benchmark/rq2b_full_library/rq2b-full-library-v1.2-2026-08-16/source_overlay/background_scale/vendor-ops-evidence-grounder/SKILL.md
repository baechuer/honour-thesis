---
name: vendor-ops-evidence-grounder
description: Grounds vendor and procurement review claims in specific evidence snippets, source locations, and confidence notes.
---

# Vendor Ops Evidence Grounder

## Use when

- The user wants claims checked against vendor proposal, security questionnaire, pricing sheet, contract summary rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: vendor proposal, security questionnaire, pricing sheet, contract summary.

## Dependencies and resources

- vendor profile
- pricing document
- security answers
- procurement criteria
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
