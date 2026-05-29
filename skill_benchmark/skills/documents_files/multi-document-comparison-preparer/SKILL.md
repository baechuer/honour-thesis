---
name: multi-document-comparison-preparer
description: Prepares two or more documents for comparison by aligning their sections, fields, clauses, themes, or key details into a comparison-ready structure.
---

# Multi-Document Comparison Preparer

Aligns multiple documents into a comparison-ready view.

## Use when

- The user wants to compare two or more documents.
- The source documents have overlapping content, fields, sections, clauses, or themes.
- The goal is to prepare a structured basis for comparison rather than fully analyse every difference in prose.

## Not for

- Single-document summary, extraction, rewrite, or conversion.
- Producing a final argumentative synthesis instead of comparison-ready alignment.
- Changing the documents' content.

## Preconditions

- The user provides one or more documents, document excerpts, forms, PDFs, policies, invoices, or practical files.
- The desired artifact is clear: summary, structured extraction, rewrite, normalization, conversion, or comparison.

## Workflow

1. Identify the documents and the most useful comparison dimensions.
2. Pull out comparable sections, fields, or ideas from each document.
3. Align them into a structure that makes similarities and differences easier to inspect.
4. Preserve important scope differences, missing pieces, and asymmetries between documents.
5. Return a comparison-ready representation.

## Writing rules

- Optimise for comparability rather than narrative flow.
- Make comparison dimensions explicit when possible.
- Preserve meaningful mismatches instead of forcing artificial symmetry.
- Return only the prepared comparison unless the user asks for further analysis.

## Default shape

Use this shape unless the user asks for something else:

- Comparison dimensions or alignment headings
- Document A
- Document B
- Matching points
- Differences or gaps

For worked examples, see `examples.md`.
