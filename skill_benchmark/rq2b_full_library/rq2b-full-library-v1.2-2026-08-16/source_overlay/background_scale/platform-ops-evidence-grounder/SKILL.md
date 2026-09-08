---
name: platform-ops-evidence-grounder
description: Grounds platform engineering operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Platform Ops Evidence Grounder

## Use when

- The user wants claims checked against developer platform request, service catalog, template repo, platform metric rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: developer platform request, service catalog, template repo, platform metric.

## Dependencies and resources

- platform service
- template repository
- developer workflow
- service owner
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
