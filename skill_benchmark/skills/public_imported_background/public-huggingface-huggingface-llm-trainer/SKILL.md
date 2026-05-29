---
name: public-huggingface-huggingface-llm-trainer
description: "Public-source background skill based on `huggingface-llm-trainer`. Train or fine-tune language and vision models using TRL (Transformer Reinforcement Learning) or Unsloth with Hugging Face Jobs infrastructure. Covers SFT, DPO, GRPO and reward modeling training methods, plus GGUF conversion for local deployment. Includes guidance on the TRL Jobs package, UV scripts with PEP 723 format, dataset preparation and validation, hardware selection, cost estimation, Trackio monitoring, Hub authentication, model selection/leaderboards and model persistence. Use for tasks involving cloud GPU training, GGUF conversion, or when users mention training on Hugging Face Jobs without local GPU setup. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "huggingface-llm-trainer"
  public_origin: "huggingface/skills"
  source_url: "https://github.com/huggingface/skills/tree/main/skills/huggingface-llm-trainer"
  raw_url: "https://raw.githubusercontent.com/huggingface/skills/main/skills/huggingface-llm-trainer/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for huggingface llm trainer; depends on the source artifact and task context named by the user"
---

# Public Imported Background: huggingface-llm-trainer

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: huggingface/skills
- Source page: https://github.com/huggingface/skills/tree/main/skills/huggingface-llm-trainer
- Raw artifact: https://raw.githubusercontent.com/huggingface/skills/main/skills/huggingface-llm-trainer/SKILL.md
- License note: See source repository for license and skill-specific terms.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for huggingface llm trainer; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request

## Resource And Structure Signals

- huggingface llm trainer
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
