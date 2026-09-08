---
name: analytics-ops-evidence-grounder
description: Grounds analytics and experimentation operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Analytics Ops Evidence Grounder

## Use when

- The user wants claims checked against experiment result, metric table, cohort data, analytics request rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: experiment result, metric table, cohort data, analytics request.

## Dependencies and resources

- metric definitions
- experiment design
- cohort data
- analysis window
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
