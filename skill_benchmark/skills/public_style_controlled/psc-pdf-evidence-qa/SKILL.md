---
name: psc-pdf-evidence-qa
description: "PDF document workflow involving extraction, OCR recovery, evidence answering, redaction, document packets, page anchors, and external sharing. Answer focused questions from PDF evidence with page-grounded support and uncertainty notes."
category: public-style-controlled
tags:
  - public-style
  - controlled-confusability
  - psc-pdf-document-work
metadata:
  source_style: public_style_controlled
  cluster_id: psc_pdf_document_work
---

# Pdf Evidence Qa

## Guide

Answer focused questions from PDF evidence with page-grounded support and uncertainty notes. This guide is written for a public-skill style library where the same artifact can be handled by several neighbouring workflows. Public-style PDF work where extraction, OCR, question answering, and redaction sound close.

The important distinction is not just the file type or tool name. Route here when the user is asking for short answer and the request depends on a focused question, and readable pdf content. If the task shifts toward a different final artifact, keep the domain context but choose the neighbouring skill instead.

## Routing notes

Use this when the PDF is a source of truth and the user asks a question whose answer must be supported by document evidence. In practice the request may mention only part of the context, so check for the combination of source material, requested judgement, and the kind of handoff the user expects.

| Useful clue | Why it matters |
|---|---|
| A focused question | Short answer |
| Readable PDF content | Evidence with page anchors |
| Need for page or section evidence | Unsupported or uncertain points |

When the request is underspecified, ask for the smallest missing item. For example, if the user gives the artifact but not the acceptance criterion, state what you will assume before doing irreversible work.

## Workflow

A normal run is usually:

1. Identify the question first.
2. Find relevant pages or sections.
3. Answer directly and attach evidence anchors.
4. Flag unsupported claims.

Do not treat the list above as a rigid template. Public skills often arrive with partial notes, linked files, or copied examples. Preserve the user's ordering when it matters, but keep the final answer focused on the decision the skill is responsible for.

```yaml
handoff:
  needs: ["A focused question", "Readable PDF content"]
  returns: ["Short answer", "Evidence with page anchors"]
  tools: ["PDF reader or extracted page text"]
  uncertainty: keep page, file, row, log, or source anchors when available
```

## Deliverables

The handoff is usually a compact artifact rather than a long essay. Include short answer, evidence with page anchors, and unsupported or uncertain points when those pieces are supported by the source material. If a requested field cannot be found, mark it as missing instead of inventing it.

Typical return blocks:

- Short answer
- Evidence with page anchors
- Unsupported or uncertain points

## Anti-patterns

Do not convert the full PDF, extract every table, or perform OCR unless that is needed to answer the question. Nearby skills in this cluster include `psc-pdf-native-extraction-pack`, `psc-pdf-scan-ocr-recovery`, `psc-pdf-redaction-pass`. They may share nouns with this skill, so route by the requested artifact and the work sequence, not by the domain word alone.

A common routing mistake is to select by a shared noun in the prompt and miss the user's requested output. Prefer the skill whose procedure would actually produce the requested handoff.

## Dependencies

This workflow can be carried out with pdf reader or extracted page text. Equivalent tools are fine, but they must preserve the same inspection or verification standard. Keep anchors such as filenames, pages, rows, source snippets, log lines, screenshots, or model/dataset identifiers when they are available.

Useful source clues, in rough order: A focused question. Readable PDF content. Need for page or section evidence.

## Usage examples

- From the policy PDF, tell me whether delayed-travel meals are reimbursable and point to the page evidence that supports the answer.
- Answer a narrow question from the PDF with cited page evidence. I only need the supported answer and uncertainty notes, not a converted document or extracted table.

Less ideal but still valid request: "Can you look at this and tell me what should happen next?" In that case, first decide whether the user wants short answer or a neighbouring artifact, then ask one clarifying question if needed.

## Quality bar

- The response clearly produces short answer.
- The answer explains uncertainty instead of silently guessing.
- The chosen process matches the user's artifact and requested outcome.
- Secondary outputs are included only when they support the requested result.

Before finishing, compare the answer against the nearby-skill boundary above. If the output would be more naturally produced by another skill, say so and switch rather than stretching this workflow.
