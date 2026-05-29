---
name: document-converter
description: Converts a document into another representation or output format, such as plain text, markdown, memo form, or structured notes, when layout fidelity is not the main priority.
---

# Document Converter

Converts a document into another representation.

## Use when

- The user wants the document turned into another format or representation.
- The target output may be plain text, markdown, notes, memo form, bullets, or another simplified structure.
- The main goal is usable conversion rather than preserving detailed layout.

## Not for

- Preserving layout fidelity as the central success criterion.
- Rewriting or improving the content.
- Extracting targeted fields.
- Summarizing the document.

## Preconditions

- The user provides one or more documents, document excerpts, forms, PDFs, policies, invoices, or practical files.
- The desired artifact is clear: summary, structured extraction, rewrite, normalization, conversion, or comparison.

## Workflow

1. Identify the source form and the target representation implied by the request.
2. Separate substantive content from source-specific formatting noise.
3. Convert the content into the new structure while preserving meaning.
4. Keep important labels, sections, or references when they matter to understanding.
5. Return the converted output in the requested or most natural target form.

## Writing rules

- Prioritise a usable target format over source formatting fidelity.
- Preserve meaning and important content while simplifying representation.
- Do not overpreserve layout details unless the user clearly needs them.
- Return only the converted output unless the user asks for commentary.

## Default shape

Use this shape unless the user asks for something else:

- Converted document in target form
- Clear sectioning when useful
- Important content preserved
- Source formatting simplified

For worked examples, see `examples.md`.
