---
name: support-ops-evidence-grounder
description: Grounds customer support operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Support Ops Evidence Grounder

## Use when

- The user wants claims checked against support tickets, chat transcripts, issue labels, customer history rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: support tickets, chat transcripts, issue labels, customer history.

## Dependencies and resources

- ticket queue
- customer context
- product area
- severity policy
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
