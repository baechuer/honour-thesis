---
name: public-huggingface-huggingface-zerogpu
description: "Public-source background skill based on `huggingface-zerogpu`. AI demos and GPU compute with Gradio Spaces and Hugging Face Spaces ZeroGPU. Use when writing or reviewing code that uses `@spaces.GPU`, configuring `python_version` or `requirements.txt` for a ZeroGPU Space, or handling ZeroGPU-specific code constraints \u2014 pickle-based process isolation, `gr.State` semantics across the worker boundary, no `torch.compile` (use AoTI instead), CUDA wheel-only builds (no `nvcc` at build or runtime), large vs xlarge sizing, and dynamic duration callables. Make sure to use this skill whenever the user mentions ZeroGPU, `@spaces.GPU`, or the `spaces` Python package, or hits ZeroGPU-specific code errors like `PicklingError` across the worker boundary, `illegal duration`, or `flash-attn` wheel-build failures \u2014 even when the user does not explicitly ask for ZeroGPU coding guidance. Trigger on `import spaces` or `@spaces.GPU` in code. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "huggingface-zerogpu"
  public_origin: "huggingface/skills"
  source_url: "https://github.com/huggingface/skills/tree/main/skills/huggingface-zerogpu"
  raw_url: "https://raw.githubusercontent.com/huggingface/skills/main/skills/huggingface-zerogpu/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for huggingface zerogpu; depends on the source artifact and task context named by the user"
---

# Public Imported Background: huggingface-zerogpu

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: huggingface/skills
- Source page: https://github.com/huggingface/skills/tree/main/skills/huggingface-zerogpu
- Raw artifact: https://raw.githubusercontent.com/huggingface/skills/main/skills/huggingface-zerogpu/SKILL.md
- License note: See source repository for license and skill-specific terms.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for huggingface zerogpu; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request

## Resource And Structure Signals

- huggingface zerogpu
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
