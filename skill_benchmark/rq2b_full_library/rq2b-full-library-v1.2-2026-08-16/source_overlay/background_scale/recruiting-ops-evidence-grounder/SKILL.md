---
name: recruiting-ops-evidence-grounder
description: Grounds recruiting pipeline operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Recruiting Ops Evidence Grounder

## Use when

- The user wants claims checked against resume, interview notes, job criteria, candidate comparison table rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: resume, interview notes, job criteria, candidate comparison table.

## Dependencies and resources

- resume file
- job criteria
- interview notes
- candidate stage
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
