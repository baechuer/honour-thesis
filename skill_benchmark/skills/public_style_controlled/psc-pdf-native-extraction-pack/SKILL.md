---
name: psc-pdf-native-extraction-pack
description: "PDF document workflow involving extraction, OCR recovery, evidence answering, redaction, document packets, page anchors, and external sharing. Extract native PDF text, tables, metadata, and anchors from born-digital PDFs for downstream structured use."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_pdf_document_work
---

# Pdf Native Extraction Pack

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Public-style PDF work where extraction, OCR, question answering, and redaction sound close.

## When to use

Use this when the PDF already has selectable text or embedded table structure and the user wants reusable extracted content.

## Requirements

- Born-digital PDF or extracted page text
- Requested fields, tables, or metadata
- Need for page/table anchors

## Instructions

- Check whether text is selectable before assuming OCR.
- Extract text blocks, table cells, metadata, and page anchors.
- Return JSON or tables with uncertainty notes.

## Deliverables

- Structured text/table/metadata extraction
- Page and table anchors
- Extraction caveats

## When not to use

Not the right tool for scanned-image OCR, redaction review, or answering one prose question from the PDF.

## External dependencies to preserve

- pdfplumber or equivalent native PDF parser

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
