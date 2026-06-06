---
name: psc-pdf-scan-ocr-recovery
description: "PDF document workflow involving extraction, OCR recovery, evidence answering, redaction, document packets, page anchors, and external sharing. Recover text from scanned PDF images while preserving page order, low-confidence spans, and manual-review regions."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_pdf_document_work
---

# Pdf Scan Ocr Recovery

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Public-style PDF work where extraction, OCR, question answering, and redaction sound close.

## When to use

Use this when the PDF is image-based, photographed, faxed, or has no selectable text.

## Requirements

- Scanned PDF or page images
- Need to mark uncertain characters or regions
- Page-by-page recovery

## Instructions

- Detect image-only pages.
- Run OCR or describe OCR recovery steps.
- Mark low-confidence tokens, signatures, handwriting, and unreadable regions.

## Deliverables

- Recovered page text
- Uncertainty markers
- Manual-review list

## When not to use

Not for native table extraction, form filling, or redaction planning when text is already available.

## External dependencies to preserve

- OCR engine
- image preprocessing when needed

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
