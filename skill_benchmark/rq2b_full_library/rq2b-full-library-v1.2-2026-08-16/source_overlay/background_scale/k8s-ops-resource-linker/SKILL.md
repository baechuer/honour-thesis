---
name: k8s-ops-resource-linker
description: Links Kubernetes platform operations work to relevant resources, references, files, systems, or supporting evidence.
---

# K8s Ops Resource Linker

## Use when

- The user wants resource mapping for Kubernetes platform operations rather than completing the task itself.

## Input and preconditions

- Candidate resources, references, or system links are available or named.
- Relevant material: manifest, pod log, deployment event, cluster configuration.

## Dependencies and resources

- cluster context
- manifest
- pod logs
- namespace
- task-specific constraints

## Procedure

1. Identify resources, references, files, systems, and evidence relevant to the task.
2. Explain the purpose and limits of each selected resource.
3. Associate an owner or usage note where available.
4. Return the resource map.

## Output

Resource map with purpose, relevance, owner, and usage notes.
