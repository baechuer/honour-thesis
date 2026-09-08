---
name: supply-chain-ops-evidence-grounder
description: Grounds supply chain operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Supply Chain Ops Evidence Grounder

## Use when

- The user wants claims checked against supplier update, demand forecast, inventory plan, risk note rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: supplier update, demand forecast, inventory plan, risk note.

## Dependencies and resources

- supplier list
- forecast data
- inventory position
- risk register
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
