---
name: document-field-extractor
description: Extracts explicit fields, facts, clauses, entities, dates, figures, and other targeted information from a document into a structured output.
---

# Document Field Extractor

Pulls structured information out of a document.

## Use when

- The user wants specific information pulled out rather than a narrative recap.
- The document contains fields, names, dates, identifiers, clauses, totals, obligations, or other extractable items.
- The result should be easy to scan and reuse.

## Not for

- Producing a narrative summary.
- Rewriting the document for tone or clarity.
- Converting the document format.
- Preparing multi-document comparison as the main goal.

## Preconditions

- The user provides one or more documents, document excerpts, forms, PDFs, policies, invoices, or practical files.
- The desired artifact is clear: summary, structured extraction, rewrite, normalization, conversion, or comparison.

## Workflow

1. Identify the fields or categories that matter for the user's request.
2. Read the document for explicit information tied to those categories.
3. Separate extracted information from surrounding narrative or formatting noise.
4. Preserve ambiguity when a field is incomplete or unclear.
5. Return the extracted result in a compact structured format.

## Writing rules

- Prefer explicit extraction over paraphrased description.
- Do not invent missing values.
- Keep the output easy to scan and easy to reuse.
- Return only the extracted information unless the user asks for explanation.

## Default shape

Use this shape unless the user asks for something else:

- Field or category
- Extracted value
- Important qualifier or condition if needed

For worked examples, see `examples.md`.
