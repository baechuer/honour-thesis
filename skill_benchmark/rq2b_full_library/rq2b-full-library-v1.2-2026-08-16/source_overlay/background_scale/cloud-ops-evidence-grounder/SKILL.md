---
name: cloud-ops-evidence-grounder
description: Grounds cloud infrastructure operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Cloud Ops Evidence Grounder

## Use when

- The user wants claims checked against cloud config, resource inventory, deployment note, cost report rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: cloud config, resource inventory, deployment note, cost report.

## Dependencies and resources

- cloud account
- resource inventory
- deployment config
- cost data
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
