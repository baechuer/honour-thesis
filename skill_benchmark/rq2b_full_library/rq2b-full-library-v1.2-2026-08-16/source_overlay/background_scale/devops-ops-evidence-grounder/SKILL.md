---
name: devops-ops-evidence-grounder
description: Grounds DevOps pipeline operations claims in specific evidence snippets, source locations, and confidence notes.
---

# Devops Ops Evidence Grounder

## Use when

- The user wants claims checked against pipeline log, build script, deploy config, release checklist rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: pipeline log, build script, deploy config, release checklist.

## Dependencies and resources

- CI logs
- build config
- environment variables
- release target
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
