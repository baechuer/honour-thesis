---
name: k8s-ops-evidence-grounder
description: Grounds Kubernetes platform operations claims in specific evidence snippets, source locations, and confidence notes.
---

# K8s Ops Evidence Grounder

## Use when

- The user wants claims checked against manifest, pod log, deployment event, cluster configuration rather than rewritten or summarized.

## Input and preconditions

- Source material is available and claims can be linked to evidence spans.
- Relevant material: manifest, pod log, deployment event, cluster configuration.

## Dependencies and resources

- cluster context
- manifest
- pod logs
- namespace
- task-specific constraints

## Procedure

1. List the claims that require evidence.
2. Match each claim to the most relevant source passage or record.
3. Classify support as direct, partial, unsupported, or uncertain.
4. Return the claim-evidence map with limitations.

## Output

Claim-evidence map with supported, unsupported, and uncertain claims.
