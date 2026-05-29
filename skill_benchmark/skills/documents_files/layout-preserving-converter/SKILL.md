---
name: layout-preserving-converter
description: Converts a document into another format while trying to preserve headings, section order, labels, tables, and other important layout cues that matter for interpretation.
---

# Layout Preserving Converter

Converts a document while preserving important layout and structure cues.

## Use when

- The user wants the document in another format but still needs its structure to remain recognizable.
- Headings, labels, table-like content, section order, or visual grouping matter to interpretation.
- The output should preserve more document shape than a generic conversion would.

## Not for

- Simple conversion where layout does not matter.
- Narrative summary or field extraction.
- Rewriting content for tone or clarity.
- Comparing multiple documents.

## Preconditions

- The user provides one or more documents, document excerpts, forms, PDFs, policies, invoices, or practical files.
- The desired artifact is clear: summary, structured extraction, rewrite, normalization, conversion, or comparison.

## Workflow

1. Identify the structural features that matter most in the source document.
2. Separate layout-significant elements from purely decorative formatting.
3. Convert the document while preserving headings, grouped sections, labels, and table-like relationships where possible.
4. Keep ordering and structure stable so the target output still reflects the source organization.
5. Return a converted version that keeps the document's shape legible.

## Writing rules

- Preserve structure before polishing prose.
- Keep headings, labels, and section order stable when possible.
- Retain table-like relationships and aligned fields when they matter.
- Return only the converted output unless the user asks for explanation.

## Default shape

Use this shape unless the user asks for something else:

- Converted document in target format
- Preserved headings and section boundaries
- Preserved labels, rows, or grouped fields where possible
- Stable ordering and structure

## Deterministic helper

For predictable markdown or plain-text structure preservation, use `scripts/convert_layout_stub.py`.

For worked examples, see `examples.md`.
