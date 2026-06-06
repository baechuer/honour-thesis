---
name: calendar-scheduling-optimizer
description: "Optimizes calendars by proposing meeting times, time blocks, constraints, buffers, and conflict-resolution options."
---

# Calendar Scheduling Optimizer

Solves scheduling constraints rather than summarising meetings.

## Use when

- The user gives availability, constraints, attendees, or calendar conflicts.
- The output should propose times or time blocks.

## Not for

- Extracting action items from meeting notes.
- Automating Airtable.
- Classifying emails.

## Preconditions

- Availability and constraints are available.
- The goal is scheduling rather than note processing.

## Workflow

1. Collect constraints and priorities.
2. Find feasible slots.
3. Add buffers and conflict notes.
4. Return recommended schedule.

## Writing rules

- Do not ignore time zones or hard constraints.
- State tradeoffs between options.

## Default shape

- Recommended slot
- Constraints satisfied
- Tradeoffs
- Alternatives
