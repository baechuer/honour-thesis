---
name: public-huggingface-huggingface-local-models
description: "Public-source background skill based on `huggingface-local-models`. Use to select models to run locally with llama.cpp and GGUF on CPU, Mac Metal, CUDA, or ROCm. Covers finding GGUFs, quant selection, running servers, exact GGUF file lookup, conversion, and OpenAI-compatible local serving. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "huggingface-local-models"
  public_origin: "huggingface/skills"
  source_url: "https://github.com/huggingface/skills/tree/main/skills/huggingface-local-models"
  raw_url: "https://raw.githubusercontent.com/huggingface/skills/main/skills/huggingface-local-models/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for huggingface local models; depends on the source artifact and task context named by the user"
---

# Public Imported Background: huggingface-local-models

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: huggingface/skills
- Source page: https://github.com/huggingface/skills/tree/main/skills/huggingface-local-models
- Raw artifact: https://raw.githubusercontent.com/huggingface/skills/main/skills/huggingface-local-models/SKILL.md
- License note: See source repository for license and skill-specific terms.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for huggingface local models; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request

## Resource And Structure Signals

- huggingface local models
- public SKILL.md metadata

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
