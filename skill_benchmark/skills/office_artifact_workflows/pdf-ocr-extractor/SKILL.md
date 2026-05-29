---
name: pdf-ocr-extractor
description: "Extracts text from scanned or image-based PDFs where OCR uncertainty, page anchors, and unreadable regions must be preserved."
---

# PDF OCR Extractor

Handles PDFs where the core problem is text recovery from images or scans.

## Use when

- The source PDF is scanned, image-heavy, or has text that cannot be reliably selected.
- The user wants recovered text with uncertain or low-confidence regions marked.
- The output should preserve page anchors for later verification.

## Not for

- Reviewing layout fidelity of a rendered PDF.
- Summarising a readable document.
- Converting a born-digital office document where OCR is unnecessary.

## Preconditions

- A scanned PDF, image PDF, or page images are available.
- The user accepts OCR uncertainty rather than expecting perfect structured fields.
- Page order or page numbers are available for anchoring.

## Workflow

1. Identify whether the source is scanned or image-based.
2. Run or simulate OCR extraction page by page.
3. Mark unreadable, ambiguous, or low-confidence text spans.
4. Preserve page anchors and important spatial clues.
5. Return recovered text or extracted fields only when evidence is strong.

## Writing rules

- Do not silently correct uncertain OCR output.
- Keep page anchors attached to recovered text.
- Flag areas that require manual inspection.

## Default shape

- Page
- Recovered text or field
- Confidence or uncertainty note
- Manual check needed
