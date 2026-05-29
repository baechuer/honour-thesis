---
name: document-rewriter
description: Rewrites an existing document or passage to improve clarity, tone, structure, or readability while preserving its intended meaning and substantive content.
---

# Document Rewriter

Rewrites a document while keeping its substance intact.

## Use when

- The user wants a document rewritten rather than merely summarised.
- The task is to improve wording, flow, tone, polish, or readability for a human reader.
- The output should be a rewritten prose version, not notes, fields, format conversion, or a shortened recap.
- The output should preserve the original meaning, commitments, and substantive content.

## Not for

- Producing only a summary.
- Extracting structured fields.
- Converting file formats.
- Normalizing OCR noise without substantive rewriting.

## Preconditions

- The user provides one or more documents, document excerpts, forms, PDFs, policies, invoices, or practical files.
- The desired artifact is clear: summary, structured extraction, rewrite, normalization, conversion, or comparison.

## Workflow

1. Identify the document's purpose and intended audience if visible from the text.
2. Separate core content from awkward phrasing, repetition, or weak structure.
3. Rewrite the text so it is clearer and more coherent without changing the underlying substance.
4. Preserve important qualifiers, obligations, conditions, or factual details.
5. Return a cleaner rewritten version.

## Writing rules

- Preserve substance unless the user explicitly asks for stronger editing.
- Do not quietly remove important details, caveats, or commitments.
- Improve flow and readability without drifting into summary.
- Return only the rewritten document unless the user asks for commentary.

## Default shape

Use this shape unless the user asks for something else:

- Revised version of the document
- Keep the same core intent
- Keep important specifics intact

For worked examples, see `examples.md`.
