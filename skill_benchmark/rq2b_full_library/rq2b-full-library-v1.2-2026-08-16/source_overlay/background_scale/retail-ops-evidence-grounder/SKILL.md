---
name: retail-ops-evidence-grounder
description: Grounds retail operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Retail Ops Evidence Grounder

## Use when

- The user wants claims checked against sales report, product catalog, store note, promotion plan rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: sales report, product catalog, store note, promotion plan.

## Dependencies and resources

- sales data
- store profile
- product catalog
- promotion calendar
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
