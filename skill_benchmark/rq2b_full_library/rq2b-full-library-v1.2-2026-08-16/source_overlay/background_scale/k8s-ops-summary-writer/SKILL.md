---
name: k8s-ops-summary-writer
description: Summarizes Kubernetes platform operations material into concise takeaways, decisions, open questions, and evidence limits.
---

# K8s Ops Summary Writer

## Use when

- The user wants a readable summary of manifest, pod log, deployment event, cluster configuration rather than structured extraction.

## Input and preconditions

- The source is long enough that condensation is useful and the audience is known.
- Relevant material: manifest, pod log, deployment event, cluster configuration.

## Dependencies and resources

- cluster context
- manifest
- pod logs
- namespace
- task-specific constraints

## Procedure

1. Read the supplied material for decisions, facts, open questions, and caveats.
2. Group the most consequential points for the named audience.
3. Separate confirmed information from assumptions and gaps.
4. Write a concise summary with action-relevant detail.

## Output

Concise summary with key points, caveats, and action-relevant details.
