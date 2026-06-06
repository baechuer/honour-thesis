---
name: pdf-ocr-cleaner
description: "Recovers text from scanned or image-based PDFs and marks OCR uncertainty, unreadable regions, and page anchors."
---

# Pdf Ocr Cleaner

Handles scanned PDF text recovery where confidence and manual verification matter.

## Use when

- The PDF is scanned, image-based, or not selectable.
- The user needs recovered text with uncertainty rather than a polished summary.

## Not for

- Extracting clean born-digital tables.
- Filling form fields.
- Reviewing redaction risk.

## Preconditions

- A scanned PDF or page image exists.
- OCR uncertainty should be preserved.

## Workflow

1. Identify scanned pages.
2. Recover text page by page.
3. Mark low-confidence spans.
4. Preserve page anchors and manual-check regions.

## Writing rules

- Do not silently correct uncertain OCR.
- Keep doubtful tokens visible.

## Default shape

- Page
- Recovered text
- Confidence or uncertainty
- Manual check needed
