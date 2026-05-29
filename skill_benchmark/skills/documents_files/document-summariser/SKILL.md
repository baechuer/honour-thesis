---
name: document-summariser
description: Summarises a practical document such as a memo, policy, form, contract excerpt, or administrative file into its main purpose, important details, and key conditions in a compact recap.
---

# Document Summariser

Summarises a document into a clear and compact recap.

## Use when

- The user wants to understand a practical document quickly.
- The source is something like a memo, policy update, form, contract excerpt, administrative note, or operational file.
- The main goal is to explain the document's purpose, important details, and meaningful conditions without heavily restructuring it.

## Not for

- Extracting targeted fields, values, clauses, dates, or entities.
- Rewriting or polishing the document text.
- Converting file format or preserving layout.
- Comparing multiple documents side by side.

## Preconditions

- The user provides one or more documents, document excerpts, forms, PDFs, policies, invoices, or practical files.
- The desired artifact is clear: summary, structured extraction, rewrite, normalization, conversion, or comparison.

## Workflow

1. Identify the document's purpose and what kind of practical file it is.
2. Pull out the most important points, obligations, decisions, or supporting details.
3. Remove repetition, boilerplate, and low-value detail.
4. Preserve important qualifiers, deadlines, conditions, and uncertainty.
5. Return a compact summary that is easy to read and useful for acting on the document.

## Writing rules

- Stay close to what the document actually says.
- Prefer a readable recap over heavy restructuring.
- Preserve important nuance, especially when the document contains conditions, limits, deadlines, or unresolved points.
- Return only the summary unless the user asks for a different format.

## Default shape

Use this shape unless the user asks for something else:

- Main purpose or topic
- Key points
- Important detail, condition, deadline, or qualifier
- Main takeaway
