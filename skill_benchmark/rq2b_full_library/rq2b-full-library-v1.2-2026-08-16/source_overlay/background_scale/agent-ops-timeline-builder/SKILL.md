---
name: agent-ops-timeline-builder
description: Builds a timeline for agent and skill operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Agent Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from agent traces, tool specs, skill cards, evaluation notes.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: agent traces, tool specs, skill cards, evaluation notes.

## Dependencies and resources

- agent trace
- skill library
- tool definitions
- evaluation criteria
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
