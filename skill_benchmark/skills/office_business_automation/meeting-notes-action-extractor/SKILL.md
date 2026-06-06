---
name: meeting-notes-action-extractor
description: "Extracts decisions, action items, owners, due dates, open questions, and follow-up risks from meeting notes or transcripts."
---

# Meeting Notes Action Extractor

Turns meeting content into accountable follow-up items.

## Use when

- The user provides meeting notes or a transcript.
- They need actions, decisions, owners, due dates, and open questions.

## Not for

- Scheduling the meeting.
- Classifying emails.
- Creating a Notion database from scratch.

## Preconditions

- Meeting notes or transcript text exists.
- Action ownership or follow-up extraction is the target.

## Workflow

1. Identify decisions and commitments.
2. Extract action items with owners and due dates.
3. List open questions.
4. Return follow-up risks.

## Writing rules

- Do not invent owners or due dates.
- Mark missing ownership explicitly.

## Default shape

- Decision
- Action/owner/due date
- Open question
- Risk
