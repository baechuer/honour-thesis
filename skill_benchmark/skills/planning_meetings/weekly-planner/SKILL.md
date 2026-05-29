---
name: weekly-planner
description: Organises tasks, obligations, and priorities into a practical weekly plan. Use when the user needs work scheduled or structured across the week rather than simply extracted from notes.
---

# Weekly Planner

Builds a practical weekly plan from tasks, priorities, and constraints.

## Use when

- The user wants to organise work across the coming week.
- The input includes tasks, deadlines, priorities, meetings, or constraints.
- The main output should be a week-level structure rather than a raw task list.

## Not for

- Extracting tasks from rough notes only.
- Preparing an agenda for a specific meeting.
- Summarising a completed meeting.
- Extracting follow-up actions from one meeting.

## Preconditions

- The user provides notes, obligations, tasks, meeting context, or planning constraints.
- The user indicates whether the target is before a meeting, after a meeting, task extraction, or week-level planning.

## Workflow

1. Identify the fixed constraints such as deadlines, meetings, or required milestones.
2. Separate urgent tasks from flexible tasks.
3. Group and sequence work in a way that is realistic across the week.
4. Highlight important priorities, bottlenecks, or overload risks.
5. Produce a weekly plan that is actionable and easy to follow.

## Output pattern

- Week-level plan.
- Sequenced tasks and time windows.
- Constraints, priorities, and risk buffers.

## Writing rules

- Prefer realistic weekly structure over over-optimised scheduling.
- Make priorities explicit.
- Preserve known constraints and deadlines accurately.
- Return the weekly plan only unless the user asks for commentary or alternatives.
