---
name: iot-ops-handoff-brief-writer
description: Writes a handoff brief for IoT operations work with context, decisions, constraints, owners, and next actions.
---

# Iot Ops Handoff Brief Writer

## Use when

- The user wants another person or agent to continue IoT operations work without losing context.

## Input and preconditions

- Current state, unresolved questions, and expected next owner can be identified.
- Relevant material: device telemetry, firmware note, sensor log, provisioning record.

## Dependencies and resources

- device registry
- telemetry data
- firmware version
- network context
- task-specific constraints

## Procedure

1. Collect the current state, completed work, decisions, constraints, and open issues.
2. Identify the next owner and the work needed for a safe continuation.
3. Structure the brief so unresolved assumptions are visible.
4. Return the handoff brief with acceptance criteria.

## Output

Handoff brief with context, completed work, open issues, owner, and acceptance criteria.
