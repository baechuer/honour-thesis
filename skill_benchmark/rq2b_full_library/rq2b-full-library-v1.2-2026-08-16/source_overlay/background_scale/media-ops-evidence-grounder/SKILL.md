---
name: media-ops-evidence-grounder
description: Grounds media production operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Media Ops Evidence Grounder

## Use when

- The user wants claims checked against script, transcript, image brief, video shot list rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: script, transcript, image brief, video shot list.

## Dependencies and resources

- media brief
- asset list
- audience
- format constraints
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
