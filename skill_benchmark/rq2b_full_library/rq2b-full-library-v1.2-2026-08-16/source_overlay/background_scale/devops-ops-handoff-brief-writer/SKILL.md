---
name: devops-ops-handoff-brief-writer
description: Writes a handoff brief for DevOps pipeline operations work with context, decisions, constraints, owners, and next actions.
---

# Devops Ops Handoff Brief Writer

## Use when

- The user wants another person or agent to continue DevOps pipeline operations work without losing context.

## Input and preconditions

- Current state, unresolved questions, and expected next owner can be identified.
- Relevant material: pipeline log, build script, deploy config, release checklist.

## Dependencies and resources

- CI logs
- build config
- environment variables
- release target
- task-specific constraints

## Procedure

1. Collect the current state, completed work, decisions, constraints, and open issues.
2. Identify the next owner and the work needed for a safe continuation.
3. Structure the brief so unresolved assumptions are visible.
4. Return the handoff brief with acceptance criteria.

## Output

Handoff brief with context, completed work, open issues, owner, and acceptance criteria.
