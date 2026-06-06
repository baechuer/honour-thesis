---
name: pdf-to-docx-converter
description: "Converts a PDF into an editable DOCX-style document while preserving headings, paragraphs, tables, and basic reading order."
---

# Pdf To Docx Converter

Creates an editable Word-style artifact from PDF content.

## Use when

- The user wants a PDF converted into an editable Word document.
- Headings, paragraphs, and tables should remain usable after conversion.

## Not for

- Answering questions from the PDF.
- Filling a form PDF.
- Finding redaction targets.

## Preconditions

- A PDF exists and the desired output is DOCX or Word-compatible structure.
- Some layout simplification is acceptable.

## Workflow

1. Identify headings, paragraphs, tables, and page order.
2. Convert content into DOCX-compatible structure.
3. Preserve tables and labels where possible.
4. Flag elements that may require manual repair.

## Writing rules

- Do not summarize away source content.
- Keep editable structure more important than visual perfection.

## Default shape

- Converted DOCX structure
- Preserved elements
- Repair notes
