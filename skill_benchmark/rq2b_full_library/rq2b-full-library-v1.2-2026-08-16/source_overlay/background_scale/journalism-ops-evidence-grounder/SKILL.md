---
name: journalism-ops-evidence-grounder
description: Grounds journalism operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Journalism Ops Evidence Grounder

## Use when

- The user wants claims checked against source notes, interview transcript, news brief, fact-check log rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: source notes, interview transcript, news brief, fact-check log.

## Dependencies and resources

- source material
- editorial policy
- fact-check criteria
- deadline
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
