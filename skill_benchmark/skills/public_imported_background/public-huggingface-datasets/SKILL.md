---
name: public-huggingface-datasets
description: "Public-source background skill based on `huggingface-datasets`. Use this skill for Hugging Face Dataset Viewer API workflows that fetch subset/split metadata, paginate rows, search text, apply filters, download parquet URLs, and read size or statistics. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "huggingface-datasets"
  public_origin: "huggingface/skills"
  source_url: "https://github.com/huggingface/skills/tree/main/skills/huggingface-datasets"
  raw_url: "https://raw.githubusercontent.com/huggingface/skills/main/skills/huggingface-datasets/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "dataset discovery and extraction workflow; depends on Hugging Face Dataset Viewer API, dataset subset/split metadata, pagination, filtering, and download URLs"
---

# Public Imported Background: huggingface-datasets

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: huggingface/skills
- Source page: https://github.com/huggingface/skills/tree/main/skills/huggingface-datasets
- Raw artifact: https://raw.githubusercontent.com/huggingface/skills/main/skills/huggingface-datasets/SKILL.md
- License note: See source repository for license.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

dataset discovery and extraction workflow; depends on Hugging Face Dataset Viewer API, dataset subset/split metadata, pagination, filtering, and download URLs

## External Dependencies To Preserve

- Hugging Face Dataset Viewer API
- dataset repository
- subset/split names
- pagination
- parquet or JSONL URLs

## Resource And Structure Signals

- dataset rows
- subsets
- splits
- filters
- download links
- API calls

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
