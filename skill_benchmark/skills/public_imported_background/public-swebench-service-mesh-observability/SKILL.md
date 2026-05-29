---
name: public-swebench-service-mesh-observability
description: "Public-source background skill based on `service-mesh-observability`. Implement comprehensive observability for service meshes including distributed tracing, metrics, and visualization. Use when setting up mesh monitoring, debugging latency issues, or implementing SLOs for service communication. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "service-mesh-observability"
  public_origin: "GeniusHTX/SWE-Skills-Bench"
  source_url: "https://github.com/GeniusHTX/SWE-Skills-Bench/tree/main/skills/service-mesh-observability"
  raw_url: "https://raw.githubusercontent.com/GeniusHTX/SWE-Skills-Bench/main/skills/service-mesh-observability/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "public workflow for service mesh observability; depends on the source artifact and task context named by the user"
---

# Public Imported Background: service-mesh-observability

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: GeniusHTX/SWE-Skills-Bench
- Source page: https://github.com/GeniusHTX/SWE-Skills-Bench/tree/main/skills/service-mesh-observability
- Raw artifact: https://raw.githubusercontent.com/GeniusHTX/SWE-Skills-Bench/main/skills/service-mesh-observability/SKILL.md
- License note: See source repository for license and skill-specific terms.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

public workflow for service mesh observability; depends on the source artifact and task context named by the user

## External Dependencies To Preserve

- user-provided task context
- source material named in the request

## Resource And Structure Signals

- service mesh observability
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
