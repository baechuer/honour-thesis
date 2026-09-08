---
name: finance-ops-evidence-grounder
description: Grounds finance and accounting operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Finance Ops Evidence Grounder

## Use when

- The user wants claims checked against financial report, budget sheet, invoice set, forecast model rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: financial report, budget sheet, invoice set, forecast model.

## Dependencies and resources

- financial data
- accounting period
- chart of accounts
- assumption notes
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
