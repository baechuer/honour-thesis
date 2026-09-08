---
name: dashboard-ops-evidence-grounder
description: Grounds dashboard and metric reporting claims in specific evidence snippets, source locations, and confidence notes.
---

# Dashboard Ops Evidence Grounder

## Use when

- The user wants claims checked against dashboard screenshots, metric tables, alert notes, KPI definitions rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: dashboard screenshots, metric tables, alert notes, KPI definitions.

## Dependencies and resources

- dashboard export
- metric glossary
- time window
- owner notes
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
