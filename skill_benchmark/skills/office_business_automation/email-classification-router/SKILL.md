---
name: email-classification-router
description: "Classifies emails into categories, priority, routing destination, required action, and escalation risk."
---

# Email Classification Router

Routes incoming emails for workflow handling.

## Use when

- The user provides email content or an inbox export.
- They need categories, priorities, routing, or escalation flags.

## Not for

- Writing a polished email reply.
- Extracting meeting notes.
- Building an Airtable base.

## Preconditions

- Email text and category scheme are available or can be proposed.
- The goal is classification/routing rather than drafting.

## Workflow

1. Read sender, subject, body, and attachments clues.
2. Classify category and urgency.
3. Choose routing/action.
4. Flag escalation or missing info.

## Writing rules

- Do not answer emails when asked only to classify.
- Keep categories consistent.

## Default shape

- Email
- Category
- Priority
- Route/action
