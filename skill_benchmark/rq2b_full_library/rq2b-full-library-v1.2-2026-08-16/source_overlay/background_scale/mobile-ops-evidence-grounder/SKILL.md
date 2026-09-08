---
name: mobile-ops-evidence-grounder
description: Grounds mobile application operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Mobile Ops Evidence Grounder

## Use when

- The user wants claims checked against app crash log, release note, store review, mobile test report rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: app crash log, release note, store review, mobile test report.

## Dependencies and resources

- mobile app build
- device context
- crash log
- release channel
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
