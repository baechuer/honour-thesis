---
name: pdf-redaction-reviewer
description: "Reviews PDF content for sensitive information and prepares a redaction plan with evidence and risk categories."
---

# Pdf Redaction Reviewer

Finds what should be hidden before sharing a PDF externally.

## Use when

- The user wants to share a PDF but avoid exposing sensitive data.
- The output should list redaction targets and reasons.

## Not for

- Extracting all document fields.
- Filling a PDF form.
- Compressing the PDF file.

## Preconditions

- A PDF or text extraction is available.
- The sharing context or sensitivity categories are known.

## Workflow

1. Identify sensitive names, IDs, addresses, financial data, or confidential clauses.
2. Classify redaction risk.
3. Anchor each target to page or section evidence.
4. Return a redaction checklist.

## Writing rules

- Do not replace redaction review with generic privacy advice.
- Keep redaction targets specific.

## Default shape

- Page or section
- Sensitive item
- Risk category
- Redaction recommendation
