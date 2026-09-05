---
name: psc-pdf-redaction-pass
description: "PDF document workflow involving extraction, OCR recovery, evidence answering, redaction, document packets, page anchors, and external sharing. Review PDFs for sensitive data that must be redacted before external sharing."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-pdf-document-work
metadata:
  source_style: public_style_controlled
  cluster_id: psc_pdf_document_work
---

# Pdf Redaction Pass

## Purpose

Review PDFs for sensitive data that must be redacted before external sharing. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Public-style PDF work where extraction, OCR, question answering, and redaction sound close.

The important distinction is not just the file type or tool name. Route here when the user is asking for redaction target list and the request depends on sharing context, and sensitive categories to look for. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Common requests

Use this before sending a contract, form, invoice, or legal packet outside the organization. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| Sharing context | Redaction target list |
| Sensitive categories to look for | Risk category |
| PDF or extracted text with page positions | Page/section anchors |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Instructions

A normal run is usually:

1. Scan for names, IDs, addresses, pricing, signatures, confidential clauses, and account details.
2. Classify risk by sensitivity and sharing context.
3. Return a redaction checklist with anchors.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["Sharing context", "Sensitive categories to look for"]
  returns: ["Redaction target list", "Risk category"]
  tools: ["PDF text/layout inspection", "sensitivity taxonomy"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Response shape

The handoff is usually a compact artifact rather than a long essay. Include redaction target list, risk category, page/section anchors, and review notes when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Redaction target list
- Risk category
- Page/section anchors
- Review notes

## Common mistakes

Not for general privacy policy review, native table extraction, or question answering. Nearby skills in this cluster include `psc-pdf-native-extraction-pack`, `psc-pdf-scan-ocr-recovery`, `psc-pdf-evidence-qa`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Environment notes

This workflow can be carried out with pdf text/layout inspection, and sensitivity taxonomy. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: Sharing context. Sensitive categories to look for. PDF or extracted text with page positions.

## Example prompts

- Before I send this contract PDF to a vendor, identify the page-level items that should be hidden, including names, addresses, pricing, IDs, and confidential clauses.
- Prepare a PDF redaction checklist for external sharing. I need sensitive targets with page anchors, not a summary or field extraction table.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants redaction target list or a neighbouring artifact, then ask one clarifying question if needed.

## Validation

- The response clearly produces redaction target list.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
