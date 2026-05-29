---
name: public-pdf
description: "Public-source background skill based on `pdf`. Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "pdf"
  public_origin: "anthropics/skills"
  source_url: "https://github.com/anthropics/skills/tree/main/skills/pdf"
  raw_url: "https://raw.githubusercontent.com/anthropics/skills/main/skills/pdf/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "PDF artifact workflow; depends on page rendering, text extraction, layout evidence, and document-specific utilities"
---

# Public Imported Background: pdf

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: anthropics/skills
- Source page: https://github.com/anthropics/skills/tree/main/skills/pdf
- Raw artifact: https://raw.githubusercontent.com/anthropics/skills/main/skills/pdf/SKILL.md
- License note: Many skills in anthropics/skills are Apache-2.0; see source directory for exact license.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

PDF artifact workflow; depends on page rendering, text extraction, layout evidence, and document-specific utilities

## External Dependencies To Preserve

- PDF file
- page rendering
- text extraction
- layout inspection
- possible Python/PDF tools

## Resource And Structure Signals

- pages
- layout
- forms
- text extraction
- rendered evidence

## Use when

- The retrieval setting needs realistic public-skill noise around this capability.
- The selector should consider tool requirements, file types, resource links, or external systems as part of skill suitability.
- The task is closer to this public skill's dependency profile than to a controlled core skill.

## Not for

- Replacing a controlled gold-label core skill in the main confusable evaluation.
- Hiding a second routing problem inside the selected skill.
- Treating public-source imports as cleanly annotated gold labels.

## Benchmark Role

This skill is intended for large-library and dependency-aware retrieval settings. It helps test whether skill representations preserve information such as required tools, file formats, repository context, external services, and optional resources.
