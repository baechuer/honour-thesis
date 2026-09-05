---
name: psc-pdf-native-extraction-pack
description: "PDF document workflow involving extraction, OCR recovery, evidence answering, redaction, document packets, page anchors, and external sharing. Extract native PDF text, tables, metadata, and anchors from born-digital PDFs for downstream structured use."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-pdf-document-work
metadata:
  source_style: public_style_controlled
  cluster_id: psc_pdf_document_work
---

# Pdf Native Extraction Pack

## Purpose

Extract native PDF text, tables, metadata, and anchors from born-digital PDFs for downstream structured use. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Public-style PDF work where extraction, OCR, question answering, and redaction sound close.

The important distinction is not just the file type or tool name. Route here when the user is asking for structured text/table/metadata extraction and the request depends on born-digital pdf or extracted page text, and requested fields, tables, or metadata. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Common requests

Use this when the PDF already has selectable text or embedded table structure and the user wants reusable extracted content. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Born-digital PDF or extracted page text | Structured text/table/metadata extraction |
| Requested fields, tables, or metadata | Page and table anchors |
| Need for page/table anchors | Extraction caveats |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Instructions

A normal run is usually:

1. Check whether text is selectable before assuming OCR.
2. Extract text blocks, table cells, metadata, and page anchors.
3. Return JSON or tables with uncertainty notes.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Born-digital PDF or extracted page text", "Requested fields, tables, or metadata"]
  returns: ["Structured text/table/metadata extraction", "Page and table anchors"]
  tools: ["pdfplumber or equivalent native PDF parser"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Response shape

The handoff is usually a compact artifact rather than a long essay. Include structured text/table/metadata extraction, page and table anchors, and extraction caveats when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Structured text/table/metadata extraction
- Page and table anchors
- Extraction caveats

## Common mistakes

Not the right tool for scanned-image OCR, redaction review, or answering one prose question from the PDF. Nearby skills in this cluster include `psc-pdf-scan-ocr-recovery`, `psc-pdf-evidence-qa`, `psc-pdf-redaction-pass`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Environment notes

This workflow can be carried out with pdfplumber or equivalent native pdf parser. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Born-digital PDF or extracted page text. Requested fields, tables, or metadata. Need for page/table anchors.

## Example prompts

- The vendor packet PDF has selectable text and tables. Pull out the document metadata, section text, and invoice rows into structured JSON with page anchors.
- Use a pdfplumber-style native extraction workflow on the vendor packet. I need embedded text, table cells, metadata, and page anchors, not OCR or a prose answer.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants structured text/table/metadata extraction or a neighbouring artifact, then ask one clarifying question if needed.

## Validation

- The response clearly produces structured text/table/metadata extraction.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
