---
name: k8s-ops-timeline-builder
description: Builds a timeline for Kubernetes platform operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# K8s Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from manifest, pod log, deployment event, cluster configuration.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: manifest, pod log, deployment event, cluster configuration.

## Dependencies and resources

- cluster context
- manifest
- pod logs
- namespace
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
