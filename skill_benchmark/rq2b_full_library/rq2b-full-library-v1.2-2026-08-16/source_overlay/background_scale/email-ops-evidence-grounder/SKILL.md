---
name: email-ops-evidence-grounder
description: Grounds email and messaging operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Email Ops Evidence Grounder

## Use when

- The user wants claims checked against draft email, message thread, recipient context, tone constraints rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: draft email, message thread, recipient context, tone constraints.

## Dependencies and resources

- message thread
- recipient relationship
- tone target
- requested action
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
