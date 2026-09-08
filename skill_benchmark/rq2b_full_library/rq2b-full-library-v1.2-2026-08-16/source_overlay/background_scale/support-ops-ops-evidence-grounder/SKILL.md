---
name: support-ops-ops-evidence-grounder
description: Grounds support process operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Support Ops Ops Evidence Grounder

## Use when

- The user wants claims checked against support macro, escalation rule, queue report, knowledge base article rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: support macro, escalation rule, queue report, knowledge base article.

## Dependencies and resources

- support policy
- queue data
- macro library
- escalation owner
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
