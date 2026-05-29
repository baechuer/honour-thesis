---
name: meeting-agenda-builder
description: Builds a clear meeting agenda from goals, notes, and discussion topics. Use when the user needs a structured plan for an upcoming meeting rather than a summary of one that already happened.
---

# Meeting Agenda Builder

Creates a structured agenda for an upcoming meeting.

## Use when

- The user is preparing for a meeting that has not happened yet.
- The task is to organize discussion topics, priorities, questions, or goals into a usable agenda.
- The main output should help guide the meeting itself.

## Not for

- Summarizing meeting notes after the meeting.
- Extracting follow-up actions from a completed discussion.
- Building a general weekly plan.
- Extracting tasks from rough notes without meeting structure.

## Preconditions

- The user provides notes, obligations, tasks, meeting context, or planning constraints.
- The user indicates whether the target is before a meeting, after a meeting, task extraction, or week-level planning.

## Workflow

1. Identify the meeting purpose and desired outcome.
2. Group the input topics into a sensible discussion order.
3. Turn broad topics into concrete agenda items or questions.
4. Prioritize items if time is limited.
5. Produce an agenda that makes the meeting easy to run.

## Output pattern

- Meeting objective.
- Agenda items in useful order.
- Discussion prompts, decisions needed, and preparation notes.

## Writing rules

- Prefer agenda items that are concrete and discussable.
- Keep the structure easy to scan.
- Include decision points or unresolved questions when relevant.
- Return the agenda only unless the user asks for commentary.
