---
name: meeting-summary-writer
description: Summarises a completed meeting into the main discussion points, decisions, and current status. Use when the user needs a concise record of what happened rather than a plan or action-only list.
---

# Meeting Summary Writer

Summarises a completed meeting into a compact and readable recap.

## Use when

- The meeting has already happened.
- The user wants a concise recap of the discussion.
- The output should explain what was discussed, decided, or left unresolved.

## Not for

- Preparing an agenda for a future meeting.
- Extracting only follow-up actions and owners.
- Converting rough notes into a weekly plan.
- Extracting generic tasks outside meeting context.

## Preconditions

- The user provides notes, obligations, tasks, meeting context, or planning constraints.
- The user indicates whether the target is before a meeting, after a meeting, task extraction, or week-level planning.

## Workflow

1. Identify the main purpose of the meeting.
2. Track the important discussion points, decisions, and unresolved issues.
3. Remove repetition and side discussion.
4. Summarise the meeting so the current state is easy to understand.
5. Highlight open questions when relevant.

## Output pattern

- Concise meeting recap.
- Discussion points, decisions, unresolved issues.
- Current status or takeaway.

## Writing rules

- Focus on the most important outcomes and discussion points.
- Preserve important decisions and unresolved issues.
- Keep the summary compact and easy to scan.
- Return only the summary unless the user asks for a different format.
