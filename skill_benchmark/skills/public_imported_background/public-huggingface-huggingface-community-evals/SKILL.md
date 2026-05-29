---
name: public-huggingface-huggingface-community-evals
description: "Public-source background skill based on `huggingface-community-evals`. Run evaluations for Hugging Face Hub models using inspect-ai and lighteval on local hardware. Use for backend selection, local GPU evals, and choosing between vLLM / Transformers / accelerate. Not for HF Jobs orchestration, model-card PRs, .eval_results publication, or community-evals automation. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "huggingface-community-evals"
  public_origin: "huggingface/skills"
  source_url: "https://github.com/huggingface/skills/tree/main/skills/huggingface-community-evals"
  raw_url: "https://raw.githubusercontent.com/huggingface/skills/main/skills/huggingface-community-evals/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for huggingface community evals; depends on the source artifact and task context named by the user"
---

# Public Imported Background: huggingface-community-evals

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: huggingface/skills
- Source page: https://github.com/huggingface/skills/tree/main/skills/huggingface-community-evals
- Raw artifact: https://raw.githubusercontent.com/huggingface/skills/main/skills/huggingface-community-evals/SKILL.md
- License note: See source repository for license and skill-specific terms.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for huggingface community evals; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request

## Resource And Structure Signals

- huggingface community evals
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
