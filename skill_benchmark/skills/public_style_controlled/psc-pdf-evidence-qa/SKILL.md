---
name: psc-pdf-evidence-qa
description: "PDF document workflow involving extraction, OCR recovery, evidence answering, redaction, document packets, page anchors, and external sharing. Answer focused questions from PDF evidence with page-grounded support and uncertainty notes."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_pdf_document_work
---

# Pdf Evidence Qa

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Public-style PDF work where extraction, OCR, question answering, and redaction sound close.

## When to use

Use this when the PDF is a source of truth and the user asks a question whose answer must be supported by document evidence.

## Requirements

- A focused question
- Readable PDF content
- Need for page or section evidence

## Instructions

- Identify the question first.
- Find relevant pages or sections.
- Answer directly and attach evidence anchors.
- Flag unsupported claims.

## Deliverables

- Short answer
- Evidence with page anchors
- Unsupported or uncertain points

## When not to use

Do not convert the full PDF, extract every table, or perform OCR unless that is needed to answer the question.

## External dependencies to preserve

- PDF reader or extracted page text

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
