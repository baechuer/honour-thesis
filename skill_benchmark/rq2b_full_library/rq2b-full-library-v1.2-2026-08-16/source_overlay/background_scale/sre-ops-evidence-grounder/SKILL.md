---
name: sre-ops-evidence-grounder
description: Grounds site reliability engineering operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Sre Ops Evidence Grounder

## Use when

- The user wants claims checked against SLO report, runbook, alert history, reliability review rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: SLO report, runbook, alert history, reliability review.

## Dependencies and resources

- service map
- SLO definitions
- alert data
- runbook
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
