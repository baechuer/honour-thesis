---
name: web-ops-evidence-grounder
description: Grounds web automation and QA claims in specific evidence snippets, source locations, and confidence notes.
---

# Web Ops Evidence Grounder

## Use when

- The user wants claims checked against web page, browser state, test flow, screenshot evidence rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: web page, browser state, test flow, screenshot evidence.

## Dependencies and resources

- web target
- browser runtime
- test data
- screenshot evidence
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
