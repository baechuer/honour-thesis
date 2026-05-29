---
name: public-openai-pdf
description: "Public-source background skill based on `pdf`. Use when tasks involve reading, creating, or reviewing PDF files where rendering and layout matter; prefer visual checks by rendering pages (Poppler) and use Python tools such as `reportlab`, `pdfplumber`, and `pypdf` for generation and extraction. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "pdf"
  public_origin: "openai/skills"
  source_url: "https://github.com/openai/skills/tree/main/skills/.curated/pdf"
  raw_url: "https://raw.githubusercontent.com/openai/skills/main/skills/.curated/pdf/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "PDF-focused workflow; depends on file type, page content, layout evidence, and possible OCR or conversion tooling"
---

# Public Imported Background: pdf

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: openai/skills
- Source page: https://github.com/openai/skills/tree/main/skills/.curated/pdf
- Raw artifact: https://raw.githubusercontent.com/openai/skills/main/skills/.curated/pdf/SKILL.md
- License note: See source skill directory for license.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

PDF-focused workflow; depends on file type, page content, layout evidence, and possible OCR or conversion tooling

## External Dependencies To Preserve

- user-provided task context
- source material named in the request
- PDF file
- page rendering or text extraction
- layout evidence

## Resource And Structure Signals

- pdf
- public SKILL.md metadata
- PDF
- pages
- layout
- extraction

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
