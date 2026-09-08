---
name: k8s-ops-artifact-packager
description: Packages Kubernetes platform operations outputs into a reusable artifact with sections, file naming, dependencies, and delivery notes.
---

# K8s Ops Artifact Packager

## Use when

- The user wants a finished deliverable package rather than raw analysis.

## Input and preconditions

- The required output audience, format, and included materials are known.
- Relevant material: manifest, pod log, deployment event, cluster configuration.

## Dependencies and resources

- cluster context
- manifest
- pod logs
- namespace
- task-specific constraints

## Procedure

1. Identify the audience, required format, and materials that belong in the delivery.
2. Organise files and sections into a usable delivery order.
3. Check naming, dependencies, and missing deliverables.
4. Return the package outline and delivery checklist.

## Output

Packaged artifact outline with included files, section order, and delivery checklist.
