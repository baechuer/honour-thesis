---
name: personal-ops-evidence-grounder
description: Grounds personal productivity operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Personal Ops Evidence Grounder

## Use when

- The user wants claims checked against task list, personal note, habit log, calendar item rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: task list, personal note, habit log, calendar item.

## Dependencies and resources

- task list
- calendar
- priority context
- personal constraints
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
