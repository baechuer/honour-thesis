---
name: public-office-chat-with-pdf
description: "Public-source background skill based on `Chat with PDF`. Answer questions about PDF content, summarize, and extract information Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "Chat with PDF"
  public_origin: "claude-office-skills/skills"
  source_url: "https://github.com/claude-office-skills/skills/tree/main/chat-with-pdf"
  raw_url: "https://raw.githubusercontent.com/claude-office-skills/skills/main/chat-with-pdf/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "PDF-focused workflow; depends on file type, page content, layout evidence, and possible OCR or conversion tooling"
---

# Public Imported Background: Chat with PDF

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: claude-office-skills/skills
- Source page: https://github.com/claude-office-skills/skills/tree/main/chat-with-pdf
- Raw artifact: https://raw.githubusercontent.com/claude-office-skills/skills/main/chat-with-pdf/SKILL.md
- License note: See source repository for license and skill-specific terms.

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

- chat with pdf
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
