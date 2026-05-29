---
name: document-normaliser
description: Cleans and regularises a document into a more consistent, readable structure while preserving its original content, sections, and meaning.
---

# Document Normaliser

Cleans and regularises a document into a stable structure.

## Use when

- The user has a messy, uneven, or inconsistently formatted document.
- The goal is to make the document more readable and regular without substantially rewriting its content.
- The output should preserve the document's structure and content while improving consistency.

## Not for

- Changing the meaning, tone, or substantive content.
- Extracting only specific fields.
- Summarizing the document.
- Converting format while preserving layout as the main goal.

## Preconditions

- The user provides one or more documents, document excerpts, forms, PDFs, policies, invoices, or practical files.
- The desired artifact is clear: summary, structured extraction, rewrite, normalization, conversion, or comparison.

## Workflow

1. Identify the document's existing structure, sections, headings, lists, and formatting patterns.
2. Remove obvious formatting noise and inconsistencies.
3. Rebuild the document into a cleaner, more regular structure.
4. Preserve section order, content boundaries, and important wording.
5. Return a cleaned version that is easier to work with.

## Writing rules

- Preserve content before improving style.
- Prefer structural cleanup over substantive rewriting.
- Keep section boundaries, labels, and ordering stable where possible.
- Return only the normalised document unless the user asks for explanation.

## Default shape

Use this shape unless the user asks for something else:

- Cleaned version of the source
- Stable headings or sections
- Consistent list and spacing style
- Preserved content order

For worked examples, see `examples.md`.
