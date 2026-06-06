---
name: psc-pdf-redaction-pass
description: "PDF document workflow involving extraction, OCR recovery, evidence answering, redaction, document packets, page anchors, and external sharing. Review PDFs for sensitive data that must be redacted before external sharing."
metadata:
  source_style: public_style_controlled
  cluster_id: psc_pdf_document_work
---

# Pdf Redaction Pass

This is a public-style controlled skill used for retrieval evaluation. It is written as a practical capability note rather than a neat benchmark schema.

Cluster intent: Public-style PDF work where extraction, OCR, question answering, and redaction sound close.

## When to use

Use this before sending a contract, form, invoice, or legal packet outside the organization.

## Requirements

- Sharing context
- Sensitive categories to look for
- PDF or extracted text with page positions

## Instructions

- Scan for names, IDs, addresses, pricing, signatures, confidential clauses, and account details.
- Classify risk by sensitivity and sharing context.
- Return a redaction checklist with anchors.

## Deliverables

- Redaction target list
- Risk category
- Page/section anchors
- Review notes

## When not to use

Not for general privacy policy review, native table extraction, or question answering.

## External dependencies to preserve

- PDF text/layout inspection
- sensitivity taxonomy

## Example use

A good request names the artifact or situation, gives enough operational context to choose this capability, and asks for the deliverable above.
