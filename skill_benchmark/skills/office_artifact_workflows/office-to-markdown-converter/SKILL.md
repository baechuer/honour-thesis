---
name: office-to-markdown-converter
description: "Converts Office-style documents, slides, spreadsheets, or mixed files into Markdown while preserving content hierarchy, labels, tables, and source traceability."
---

# Office To Markdown Converter

Turns office artifacts into Markdown for repositories, notes, or downstream text workflows.

## Use when

- The user wants an Office or PDF-derived artifact converted into Markdown.
- The priority is reusable text structure, headings, tables, and traceability.
- The output should be Markdown rather than a visual layout review.

## Not for

- Checking rendered PDF page fidelity.
- Auditing spreadsheet formulas.
- Producing tracked changes in a Word document.

## Preconditions

- A source file or extracted content is available.
- The target format is Markdown or Markdown-compatible notes.
- The user accepts some layout simplification unless they explicitly require pixel-level fidelity.

## Workflow

1. Identify source format, content hierarchy, tables, and embedded artifacts.
2. Convert headings, lists, labels, and tables into clean Markdown.
3. Preserve source traceability for important sections or pages.
4. Flag content that cannot be safely represented in Markdown.
5. Return a clean Markdown artifact or conversion plan.

## Writing rules

- Do not summarize away source content during conversion.
- Keep tables readable in Markdown.
- Mark omitted or unconvertible visual material explicitly.

## Default shape

- Markdown output
- Conversion notes
- Unconverted or uncertain elements
