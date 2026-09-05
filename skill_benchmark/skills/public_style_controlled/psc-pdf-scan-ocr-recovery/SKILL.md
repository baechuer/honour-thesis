---
name: psc-pdf-scan-ocr-recovery
description: "PDF document workflow involving extraction, OCR recovery, evidence answering, redaction, document packets, page anchors, and external sharing. Recover text from scanned PDF images while preserving page order, low-confidence spans, and manual-review regions."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-pdf-document-work
metadata:
  source_style: public_style_controlled
  cluster_id: psc_pdf_document_work
---

# Pdf Scan Ocr Recovery

## Guide

Recover text from scanned PDF images while preserving page order, low-confidence spans, and manual-review regions. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Public-style PDF work where extraction, OCR, question answering, and redaction sound close.

The important distinction is not just the file type or tool name. Route here when the user is asking for recovered page text and the request depends on scanned pdf or page images, and need to mark uncertain characters or regions. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Routing notes

Use this when the PDF is image-based, photographed, faxed, or has no selectable text. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Scanned PDF or page images | Recovered page text |
| Need to mark uncertain characters or regions | Uncertainty markers |
| Page-by-page recovery | Manual-review list |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Workflow

A normal run is usually:

1. Detect image-only pages.
2. Run OCR or describe OCR recovery steps.
3. Mark low-confidence tokens, signatures, handwriting, and unreadable regions.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Scanned PDF or page images", "Need to mark uncertain characters or regions"]
  returns: ["Recovered page text", "Uncertainty markers"]
  tools: ["OCR engine", "image preprocessing when needed"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Deliverables

The handoff is usually a compact artifact rather than a long essay. Include recovered page text, uncertainty markers, and manual-review list when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Recovered page text
- Uncertainty markers
- Manual-review list

## Anti-patterns

Not for native table extraction, form filling, or redaction planning when text is already available. Nearby skills in this cluster include `psc-pdf-native-extraction-pack`, `psc-pdf-evidence-qa`, `psc-pdf-redaction-pass`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Dependencies

This workflow can be carried out with ocr engine, and image preprocessing when needed. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Scanned PDF or page images. Need to mark uncertain characters or regions. Page-by-page recovery.

## Usage examples

- This signed PDF packet looks like photographed scans. Recover the readable text page by page and flag uncertain handwriting or blurred regions.
- Run an OCR recovery workflow for the scanned receipt PDF. Preserve page order and confidence notes instead of treating it as a born-digital table extraction.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants recovered page text or a neighbouring artifact, then ask one clarifying question if needed.

## Quality bar

- The response clearly produces recovered page text.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
