---
name: docx-redline-editor
description: "Prepares tracked changes, comments, or revision instructions for a Word document while preserving document structure and author-facing edit rationale."
---

# DOCX Redline Editor

Edits a DOCX-style document as a review artifact with revisions, not as a plain prose rewrite.

## Use when

- The user asks for tracked changes, comments, or redline-style edits.
- The document structure, headings, comments, or reviewer rationale should be preserved.
- The output is an edit plan, change log, or revised Word-compatible document.

## Not for

- Summarising the document.
- Converting the document to Markdown.
- Auditing spreadsheet formulas or slide layout.

## Preconditions

- A DOCX-style document, extracted Word content, or revision target is available.
- The user provides editing goals, reviewer stance, or change policy.
- The document has sections that need traceable edits.

## Workflow

1. Identify the document structure and review objective.
2. Separate direct edits from comments or author queries.
3. Preserve headings, numbering, cross-references, and document flow.
4. Explain edits that materially change meaning.
5. Return changes in a traceable format suitable for Word review.

## Writing rules

- Do not flatten structured documents into generic notes.
- Keep author-facing comments concise and actionable.
- Distinguish wording edits from substantive changes.

## Default shape

- Section
- Proposed edit or comment
- Reason
- Risk or author decision needed
