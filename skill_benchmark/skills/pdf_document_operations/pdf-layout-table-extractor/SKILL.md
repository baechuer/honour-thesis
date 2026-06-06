---
name: pdf-layout-table-extractor
description: "Extracts tables and repeated fields from PDFs while preserving page, row, column, and layout evidence."
---

# Pdf Layout Table Extractor

Turns layout-sensitive PDF content into structured data with traceable table coordinates.

## Use when

- The user needs tabular values or repeated fields from a PDF.
- Row, column, page, or layout position matters to correctness.

## Not for

- Answering a prose question from the PDF.
- Running OCR as the central task.
- Compressing or watermarking the PDF.

## Preconditions

- A PDF with tables, forms, invoices, or repeated fields is available.
- The requested fields or table boundaries are known.

## Workflow

1. Inspect page layout and table boundaries.
2. Extract rows, columns, labels, and values.
3. Preserve page anchors and uncertain cells.
4. Return structured data with verification notes.

## Writing rules

- Do not flatten row relationships into prose.
- Mark merged cells or ambiguous labels.

## Default shape

- Table or field set
- Page/row/column anchors
- Uncertain cells
- Validation notes
