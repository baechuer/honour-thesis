# Controlled Cluster Expansion Checkpoint

Date: 2026-05-30

Purpose: expand the benchmark beyond the previous 85 controlled prompts, add harder implicit-field stress cases, and rerun the benchmark validation loop.

## Expansion Summary

The main evaluated benchmark now contains:

- 137 controlled prompts, up from 85.
- 137 main evaluated skills, up from 85.
- 2401 total skills in the full library.
- 1800 generated background-scale skills.
- 460 imported public skills.
- 4 support/email skills.
- 10 implicit-field stress prompts now included in the main prompt glob and also mirrored under `skill_benchmark/stress_prompts/`.

New controlled clusters added:

| Cluster | Prompts | Purpose |
|---|---:|---|
| `pdf_document_operations` | 6 | Tests PDF question answering, layout table extraction, OCR cleanup, form completion, redaction review, and PDF-to-DOCX conversion. |
| `huggingface_ml_workflows` | 6 | Tests dataset inspection, local model selection, sentence-transformer fine-tuning, Gradio UI building, ZeroGPU deployment, and model evaluation. |
| `github_ci_maintenance` | 6 | Tests CI failure diagnosis, PR review comment resolution, fresh code review, issue triage, changelog generation, and git guardrail setup. |
| `api_mcp_tooling` | 6 | Tests REST interface design, MCP server building, webhook planning, auth integration, API docs, and API security review. |
| `observability_reliability` | 6 | Tests Prometheus alerts, Grafana dashboards, distributed traces, SLO breach narratives, resilience review, and service mesh debugging. |
| `office_business_automation` | 6 | Tests spreadsheet modelling, Airtable automation, Notion research databases, calendar scheduling, meeting action extraction, and email routing. |
| `skill_representation_analysis` | 6 | Tests skill field auditing, skill authoring, router policy design, hierarchy flattening, skill installation, and benchmark evaluation. |

New implicit-field stress set:

- 10 prompts.
- Skills intentionally avoid clean `Use when`, `Workflow`, `Preconditions`, and `Default shape` headings.
- Procedural information is encoded in prose, similar to many public skills.
- This set is now included in the main prompt glob. The representation exporter performs a conservative prose-to-field extraction pass before building R2/R3, so the test reflects the representation layer's responsibility to recover structure from messy skill artifacts.

## Validation Results

Main benchmark validation:

| Step | Result | Notes |
|---|---:|---|
| Step 1 integrity | PASS | 137 prompts and 2401 skills resolve. |
| Step 2 procedural distinctness | PASS | 137/137 prompts; 449/449 gold/alternative pairs differ on at least two primary axes. |
| Step 2 prompt-specific alignment | PASS | 122/137 prompts pass under MiniLM embedding alignment; report status is still PASS. |
| Step 3 semantic confusability | WARN | 116/137 prompts pass under MiniLM; this is 84.7%, just below the 85% pass threshold. TF-IDF fallback remains too lexical and should not be used as the final semantic authority. |
| Step 4 prompt leakage | PASS | 0 critical exact-name leaks and 0 high-risk leaks. |
| Step 5 scale | PASS | Full library now has 2401 skills. |

Interpretation:

- The expanded benchmark is mechanically valid and procedurally defensible.
- The new public-grounded alternatives make the benchmark more realistic.
- Step 3 is not yet perfect, but it is close enough to proceed with selector/failure-mode analysis while marking the remaining weak semantic cases for later review.
- The remaining Step 3 weak prompts are mostly highly specialized operational tasks where the gold skill is naturally clearer than near-neighbour alternatives.

## Local Selector Results On 2401 Skills

| Method | Core Top-1 | Full Top-1 | Full Top-5 | Full MRR | Non-main Top-1 |
|---|---:|---:|---:|---:|---:|
| M1 BM25 flat | 71.5% | 67.9% | 88.3% | 0.771 | 10.9% |
| M1 TF-IDF flat | 72.3% | 60.6% | 83.9% | 0.713 | 19.0% |
| M3 TF-IDF schema | 78.8% | 71.5% | 94.9% | 0.823 | 7.3% |
| M6 BM25 -> schema rerank | 75.2% | 72.3% | 93.4% | 0.817 | 3.6% |
| M6 TF-IDF -> schema rerank | 75.9% | 73.0% | 89.8% | 0.808 | 8.0% |

Qwen provider refresh on 2401:

| Method | Prompts | Top-1 | Top-5 | MRR | Non-main Top-1 |
|---|---:|---:|---:|---:|---:|
| Qwen full-skill embedding | 137 | 52.5% | 73.7% | 0.617 | 26.3% |
| Qwen full-skill + local schema rerank top-100 | 137 | 77.4% | 91.2% | 0.840 | 8.0% |

These results preserve the main thesis pattern: dense retrieval helps candidate generation, but procedural/schema-aware reranking substantially improves final selection and reduces non-main false positives.

## Field Ablation Result

The expanded field ablation still supports the representation-field claim.

On full scale:

- TF-IDF description-only: 62.2% top-1.
- TF-IDF through workflow/procedure fields: 81.1% top-1.
- BM25 description-only: 67.7% top-1.
- BM25 through workflow/procedure fields: 88.2% top-1.
- Adding naive constraints/dependencies/resources after workflow reduces or does not improve top-1, confirming that those fields need field-aware handling rather than simple concatenation.

## Implicit-Field Integration Result

The implicit cases are now part of the main benchmark. The raw skills remain prose-only, but the representation exporter performs conservative field extraction from body text before building R2/R3.

Before this extraction step, the schema reranker collapsed on the separate 10-prompt stress set. After integration and extraction, the full 137-prompt benchmark still shows the thesis pattern: schema-aware methods remain above flat baselines and reduce non-main false positives, but the task is harder than the clean 127-prompt condition.

Interpretation:

- Current schema methods work best when fields are explicitly represented.
- When procedural information is embedded in prose, the representation layer needs an extraction/normalization step before retrieval.
- The current implementation uses a conservative heuristic extractor; a stronger LLM-assisted extractor is a natural next method variant.

## What This Means For The Thesis

The benchmark now supports two levels of claim:

1. Clean controlled cases: procedural fields improve scalable skill selection under semantic confusion.
2. Integrated implicit cases: a practical representation layer cannot simply rely on author-provided headings; it must extract or normalize procedural information from natural skill artifacts.

Recommended next step:

- Freeze the 127-prompt main benchmark unless a specific gold-label issue appears.
- Do targeted manual review of the 20 weak Step 3 prompts and the strongest-method failures.
- Start designing the next representation layer for implicit/prose-encoded skills: either heuristic field extraction, LLM-assisted field extraction, or graph/schema construction from full skill text.
