---
name: meeting-ops-evidence-grounder
description: Grounds meeting and planning operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Meeting Ops Evidence Grounder

## Use when

- The user wants claims checked against meeting transcript, agenda notes, calendar constraints, action list rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: meeting transcript, agenda notes, calendar constraints, action list.

## Dependencies and resources

- meeting notes
- participant list
- calendar window
- action owners
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
