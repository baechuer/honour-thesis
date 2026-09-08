---
name: training-ops-timeline-builder
description: Builds a timeline for training and enablement operations events, deadlines, dependencies, decisions, and follow-up checkpoints.
---

# Training Ops Timeline Builder

## Use when

- The user wants sequence reconstruction or schedule structure from training brief, learner feedback, curriculum outline, assessment result.

## Input and preconditions

- The source contains dates, order cues, event descriptions, or dependency markers.
- Relevant material: training brief, learner feedback, curriculum outline, assessment result.

## Dependencies and resources

- learning objective
- audience profile
- training materials
- assessment rubric
- task-specific constraints

## Procedure

1. Extract dated events, ordering cues, dependencies, and unresolved timing gaps.
2. Place events in chronological order without inventing missing dates.
3. Flag conflicts, dependencies, and uncertain sequence points.
4. Return the dated timeline and gap list.

## Output

Timeline with dates, event descriptions, dependencies, and unresolved gaps.
