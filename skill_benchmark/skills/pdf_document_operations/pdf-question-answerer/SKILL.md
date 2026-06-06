---
name: pdf-question-answerer
description: "Answers specific questions from PDF content while citing page or section evidence."
---

# Pdf Question Answerer

Uses a PDF as an evidence source for question answering, not as a conversion or extraction task.

## Use when

- The user asks a focused question about PDF content.
- The answer must be grounded in page, section, or quoted evidence.

## Not for

- Extracting tables or fields as a reusable dataset.
- Converting the PDF into DOCX or Markdown.
- Filling a PDF form.

## Preconditions

- A readable PDF or extracted page text is available.
- The user asks a question whose answer should come from the PDF.

## Workflow

1. Identify the question and relevant pages.
2. Find supporting evidence in the PDF.
3. Answer directly with citations or page anchors.
4. Flag uncertainty if evidence is missing.

## Writing rules

- Do not invent facts beyond the PDF.
- Keep citations attached to claims.

## Default shape

- Answer
- Evidence with page or section anchors
- Uncertainty or missing evidence
