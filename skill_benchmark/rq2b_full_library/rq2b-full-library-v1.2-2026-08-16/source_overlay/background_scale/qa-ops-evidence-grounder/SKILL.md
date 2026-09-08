---
name: qa-ops-evidence-grounder
description: Grounds quality assurance operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Qa Ops Evidence Grounder

## Use when

- The user wants claims checked against test plan, defect report, acceptance criteria, release evidence rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: test plan, defect report, acceptance criteria, release evidence.

## Dependencies and resources

- test plan
- defect log
- acceptance criteria
- release scope
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
