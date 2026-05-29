---
name: public-markitdown
description: "Public-source background skill based on `markitdown`. Convert files and office documents to Markdown. Supports PDF, DOCX, PPTX, XLSX, images (with OCR), audio (with transcription), HTML, CSV, JSON, XML, ZIP, YouTube URLs, EPubs and more. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "markitdown"
  public_origin: "K-Dense-AI/scientific-agent-skills via public skill directory"
  source_url: "https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/markitdown"
  raw_url: "https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/markitdown/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "document conversion workflow; depends on Microsoft MarkItDown-style conversion tools and input file types"
---

# Public Imported Background: markitdown

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: K-Dense-AI/scientific-agent-skills via public skill directory
- Source page: https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/markitdown
- Raw artifact: https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/markitdown/SKILL.md
- License note: SkillRet metadata reports MIT for this source; see upstream repository for exact terms.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

document conversion workflow; depends on Microsoft MarkItDown-style conversion tools and input file types

## External Dependencies To Preserve

- MarkItDown or equivalent converter
- PDF/DOCX/PPTX/XLSX/image files
- OCR support when needed

## Resource And Structure Signals

- file conversion
- Markdown output
- OCR
- office documents
- scientific documents

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
