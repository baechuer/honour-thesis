---
name: reply-drafter
description: Drafts a reply message or email from conversation context. Use when the user needs a fresh reply written from the source message and does not already have a usable draft.
---

# Reply Drafter

Writes a sendable reply from the source message and the user's goal.

## Use when

- The user wants to reply to an email, chat message, or thread.
- The user provides source context but not a usable already-written reply, and wants a new response written from scratch.
- The output should be a fresh sendable response, even when the reply contains a simple commitment or timing confirmation.
- The main task is to produce a new response that can be sent with light editing.

## Not for

- Polishing an existing reply draft.
- Editing an already-written reply while preserving the same meaning and commitments.
- Editing an already-written message while keeping its meaning, availability, commitments, flow, phrasing, tone, and readability.
- Summarizing a thread without writing a reply.
- Extracting only tasks or deadlines.
- Recipient-specific cases where a more specialized reply skill is clearly a better fit.

## Preconditions

- The user provides message context and recipient context, but not a reply that should simply be polished.
- The user indicates whether the goal is a fresh draft, refinement, academic reply, group coordination, or follow-up commitment.

## Workflow

1. Identify what the sender is asking, implying, or expecting.
2. Infer the user's likely response goal from the prompt and context.
3. Draft a reply that addresses the important points directly.
4. Preserve key facts, dates, and commitments from the context.
5. Keep the message clear, sendable, and appropriately concise.

## Output pattern

- Fresh sendable reply.
- Appropriate tone for the recipient and context.
- No unsupported commitments.

## Writing rules

- Do not invent facts, promises, or deadlines not supported by the context.
- Prefer a direct, professional tone unless the context clearly suggests otherwise.
- If context is missing, ask for clarification inside the draft rather than hallucinating details.
- Return only the reply unless the user asks for alternatives or explanation.
