# Experiment Methodology Tracker

Last updated: 2026-06-06

This file is the source of truth for experiment methods. Every reported result should identify the prompt stratum, skill library scale, representation, first-stage retriever, reranker, candidate budget, and scoring rule. Do not compare two rows as a pure model comparison unless all other columns match.

For a thesis-facing horizontal comparison of representation layers against retrieval architectures, see `thesis_notes/Representation Layer Horizontal Comparison.md`.

## Current Research Frame

The thesis studies candidate subsetting for large agent skill libraries. The main question is not simply "which retriever wins"; it is which skill information should be preserved, extracted, encoded, and used so a selector can distinguish semantically similar but procedurally different skills under scale.

Current working comparison:

- Flat/progressive skill exposure: what current systems approximate when the main agent sees names, descriptions, and metadata.
- Dense semantic retrieval: scalable first-stage retrieval over either compact cards or full skill artifacts.
- Structure-aware representation: skill information is normalized into fields such as task, inputs, outputs, workflow, constraints, dependencies, resources, and boundaries.
- Hybrid retrieval/reranking: dense or lexical candidate generation followed by a more expensive precision layer.

## Prompt Strata

| Stratum | Prompt count | Purpose | Prompt source |
|---|---:|---|---|
| Controlled | 201 | Designed semantic-confusability clusters with gold labels and near-neighbour alternatives, including 64 public-style controlled prompts. | `skill_benchmark/prompts/*.json` |
| Public-gold | 82 | Externally authored/public skill targets, used to test whether the representation claim generalizes beyond generated controlled skills. | `skill_benchmark/prompts_public_gold/public_gold_validation_confusability.json` |
| Combined | 283 | Reporting view combining controlled and public-gold strata. Use only after reporting strata separately. | Controlled + public-gold |
| Low-information stress | Separate | Tests how methods behave when prompt evidence is vague or under-specified. | `skill_benchmark/prompts_low_information/*.json` |

Default skill-library scale: `current_full`, currently the expanded 2433-skill library. Avoid using `core` for public-gold because public target skills are not present in the controlled-core candidate pool.

Public-gold clustering caveat:

- Public-gold retrieval is not cluster-restricted. The selector ranks against the full `current_full` library.
- The current public-gold prompt file uses one broad `family = public_gold_validation`, so `by_family` result summaries are not informative.
- Public-gold cases do include `source_family` values such as `huggingface`, `office-document`, `github-ci`, `web-quality`, `figma`, and `agent-workflow`. These should be treated as analysis clusters, not retrieval filters.
- Before final reporting, public-gold result analysis should group failures by `source_family` and by manually defined cluster type: public-public confusion, public-controlled confusion, broad-wrapper confusion, duplicate/acceptable alternative, and background false positive.

## Representation Components

| ID | Name | Selector-visible information | Artifact |
|---|---|---|---|
| R0 | Progressive disclosure card | Main agent sees skill names/descriptions/metadata and then loads full docs after selecting. | M0 traces, not a JSONL representation |
| R1 | Flat metadata card | Skill name, family/category, short description. | `skill_benchmark/representations/R1_flat_metadata.jsonl` |
| R2 | Structured procedural card | R1 plus use conditions, avoid conditions, preconditions, workflow, outputs, writing rules, and normalized procedural summaries. | `skill_benchmark/representations/R2_structured_procedural.jsonl` |
| R3 | Dependency/resource-aware card | R2 plus dependency profile, external dependencies, resources, public-source metadata, and bundled resource signals. | `skill_benchmark/representations/R3_dependency_resource_aware.jsonl` |
| R4 | Graph edge view | Edges derived from family, inputs, outputs, workflow, dependencies, resources, boundaries, and public-source relations. | `skill_benchmark/representations/R4_graph_edges.jsonl` |
| RFULL | Full skill artifact | Entire `SKILL.md` text, usually with name/description included by the runner. | `skill_benchmark/skills/**/SKILL.md` |

Important distinction:

- R2/R3 are not only authoring requirements. They are also representation-layer extraction targets. Public skills may imply these fields without explicitly naming them.
- RFULL is not automatically "more structured"; it may contain more information but also more noise.

## Method Matrix

| Method ID | Status | Representation | First-stage retriever | Reranker | Candidate budget | Main purpose |
|---|---|---|---|---|---:|---|
| M0 | Historical/core only | R0 | Main-agent progressive disclosure | Main agent decides | n/a | Small-library baseline and context/cost stress test. |
| M1-BM25 | Implemented | R1 | BM25 lexical | none | all | Lightweight flat-metadata baseline. |
| M1-TFIDF | Implemented | R1 | TF-IDF lexical | none | all | Lightweight flat-metadata baseline. |
| M2-MiniLM-full | Historical/local | RFULL | MiniLM embedding | none | all | Cheap local reference, not final modern baseline. |
| M2-Qwen-R1 | Implemented public; needs current controlled rerun | R1 | Qwen `text-embedding-v4` | none | all | Modern dense retrieval over flat cards. |
| M2-Qwen-R2 | Implemented public; needs current controlled rerun | R2 | Qwen `text-embedding-v4` | none | all | Modern dense retrieval over structured procedural cards. |
| M2-Qwen-full | Implemented controlled/public | RFULL | Qwen `text-embedding-v4` | none | all | Modern dense retrieval over full skill docs. |
| M2-SkillRouter-full | Implemented controlled/public hosted | RFULL | `pipizhao/SkillRouter-Embedding-0.6B` | none | all | Skill-specific dense retrieval baseline. |
| M2-SkillRouter-R1 | Implemented in script, not yet run | R1 | SkillRouter embedding | none | all | Needed to separate SkillRouter model effect from representation effect. |
| M2-SkillRouter-R2 | Implemented in script, not yet run | R2 | SkillRouter embedding | none | all | Needed for fair comparison to Qwen R2. |
| M3-schema-lexical | Implemented | R2/R3 | TF-IDF/BM25 over schema text | none or schema score | all/top-k | Tests serialized structured procedural information. |
| M4-tree | Planned | Family/category tree | Tree route | optional within-branch rerank | branch/top-k | Tests hierarchical routing and branch-exclusion failures. |
| M5-graph | Planned | R4 graph edges | Graph filter/expansion | graph-aware rerank | top-k | Tests explicit relations rather than serialized text only. |
| M6-v0-schema | Implemented diagnostic | R1/R2/R3 | BM25, TF-IDF, MiniLM, or Qwen shortlist | deterministic schema weighted overlap | 20/50/100 | Transparent diagnostic reranker over extracted fields. |
| M6-v1-local | Implemented prototype | R1/R2/R3 | BM25, TF-IDF, Qwen full, or SkillRouter full | deterministic field-aware matcher | 20/50/100 | Separates first-stage candidate recall from field-aware reranking. |
| M6-v2-semantic-field | Planned | R1/R2/R3 | fixed shortlist | semantic/LLM field matcher | 20/50/100 | Replace lexical field matching with semantic field matching. |
| M8-Qwen-rerank-R1 | Implemented public; needs current controlled rerun | R1 | Qwen embedding | Qwen `qwen3-rerank` | 20 | Strong generic neural rerank over flat cards. |
| M8-Qwen-rerank-R2 | Implemented public; needs current controlled rerun | R2 | Qwen embedding | Qwen `qwen3-rerank` | 20 | Strong generic neural rerank over structured cards. |
| M8-Qwen-rerank-full | Implemented controlled/public | RFULL | Qwen embedding | Qwen `qwen3-rerank` | 20 | Strong generic neural rerank over full skill docs. |
| M8-SkillRouter-rerank-full | Implemented controlled/public hosted | RFULL | SkillRouter embedding | SkillRouter reranker | 20 | Skill-specific retrieve-rerank baseline. |
| M8-SkillRouter-rerank-R1 | Implemented in script, not yet run | R1 | SkillRouter embedding | SkillRouter reranker | 20 | Needed for fair R1 model comparison. |
| M8-SkillRouter-rerank-R2 | Implemented in script, not yet run | R2 | SkillRouter embedding | SkillRouter reranker | 20 | Needed for fair R2 model comparison. |

## Fair Comparison Rules

1. Model-only comparison: representation, prompt stratum, skill library scale, candidate budget, and reranker type must match.
2. Representation-only comparison: model, prompt stratum, skill library scale, candidate budget, and reranker type must match.
3. Reranker-only comparison: first-stage retriever, representation, prompt stratum, candidate set size, and candidate text must match.
4. Controlled and public-gold must be reported separately before any combined score.
5. Top-20 rerankers should be compared against top-20 rerankers. Top-100 results are larger-budget trade-off conditions, not direct wins over top-20 systems.
6. Report candidate recall before reranking whenever using M6/M8. A failure can be caused by the first-stage retriever or by the reranker.
7. Acceptable alternatives and strict gold labels are separate scoring rules. Report both when available.

## Canonical Commands

Run from repository root:

```bash
cd "/Users/jackyzhang/Work/Honour Thesis"
```

Environment:

```bash
# Required for Qwen/DashScope-backed provider runs.
# The scripts read this automatically with --dotenv .env.
DASHSCOPE_API_KEY=...

# Required only for hosted/local Hugging Face model access or jobs.
HF_TOKEN=...
```

Re-export representation components after changing skills:

```bash
python3 skill_benchmark/scripts/export_skill_representations.py
python3 skill_benchmark/scripts/analyze_representation_coverage.py
```

Validate controlled benchmark construction:

```bash
python3 skill_benchmark/scripts/validate_benchmark_integrity.py \
  --output-md skill_benchmark/outputs/benchmark_integrity_report.md \
  --output-json skill_benchmark/outputs/benchmark_integrity_report.json

python3 skill_benchmark/scripts/analyze_procedural_distinctness.py \
  --output-md skill_benchmark/outputs/procedural_distinctness_report.md \
  --output-json skill_benchmark/outputs/procedural_distinctness_report.json

python3 skill_benchmark/scripts/analyze_semantic_confusability.py \
  --output-md skill_benchmark/outputs/semantic_confusability_report_minilm_2401.md \
  --output-json skill_benchmark/outputs/semantic_confusability_report_minilm_2401.json

python3 skill_benchmark/scripts/analyze_prompt_leakage.py \
  --output-md skill_benchmark/outputs/prompt_leakage_report.md \
  --output-json skill_benchmark/outputs/prompt_leakage_report.json
```

Run local offline selector baselines on controlled prompts:

```bash
python3 skill_benchmark/scripts/run_offline_selectors.py \
  --prompts "skill_benchmark/prompts/*.json" \
  --scales current_full \
  --methods m1_bm25_flat,m1_tfidf_flat,m3_tfidf_schema,m6_bm25_schema_rerank,m6_tfidf_schema_rerank \
  --rerank-candidates 100 \
  --output-md skill_benchmark/outputs/offline_selector_evaluation_2433_201_local.md \
  --output-json skill_benchmark/outputs/offline_selector_evaluation_2433_201_local.json
```

Run Qwen embedding-only controlled RFULL:

```bash
python3 skill_benchmark/scripts/run_provider_selectors.py \
  --dotenv .env \
  --prompts "skill_benchmark/prompts/*.json" \
  --scale current_full \
  --embedding-provider qwen \
  --embedding-model text-embedding-v4 \
  --embedding-representation full \
  --reranker-provider none \
  --output-md skill_benchmark/outputs/provider_selector_qwen_2401_137_full_embedding.md \
  --output-json skill_benchmark/outputs/provider_selector_qwen_2401_137_full_embedding.json
```

Run Qwen full embedding plus Qwen reranker controlled:

```bash
python3 skill_benchmark/scripts/run_provider_selectors.py \
  --dotenv .env \
  --prompts "skill_benchmark/prompts/*.json" \
  --scale current_full \
  --embedding-provider qwen \
  --embedding-model text-embedding-v4 \
  --embedding-representation full \
  --reranker-provider qwen \
  --reranker-model qwen3-rerank \
  --rerank-candidates 20 \
  --output-md skill_benchmark/outputs/provider_selector_qwen_2401_137_full_qwen_rerank_top20.md \
  --output-json skill_benchmark/outputs/provider_selector_qwen_2401_137_full_qwen_rerank_top20.json
```

Run Qwen R1/R2 public-gold variants:

```bash
for rep in r1 r2 full; do
  python3 skill_benchmark/scripts/run_provider_selectors.py \
    --dotenv .env \
    --prompts "skill_benchmark/prompts_public_gold/*.json" \
    --scale current_full \
    --embedding-provider qwen \
    --embedding-model text-embedding-v4 \
    --embedding-representation "$rep" \
    --acceptable-alternatives skill_benchmark/annotations/public_gold_acceptable_alternatives.json \
    --reranker-provider none \
    --output-md "skill_benchmark/outputs/provider_selector_qwen_public_gold_82_${rep}_embedding.md" \
    --output-json "skill_benchmark/outputs/provider_selector_qwen_public_gold_82_${rep}_embedding.json"

  python3 skill_benchmark/scripts/run_provider_selectors.py \
    --dotenv .env \
    --prompts "skill_benchmark/prompts_public_gold/*.json" \
    --scale current_full \
    --embedding-provider qwen \
    --embedding-model text-embedding-v4 \
    --embedding-representation "$rep" \
    --acceptable-alternatives skill_benchmark/annotations/public_gold_acceptable_alternatives.json \
    --reranker-provider qwen \
    --reranker-model qwen3-rerank \
    --rerank-candidates 20 \
    --output-md "skill_benchmark/outputs/provider_selector_qwen_public_gold_82_${rep}_qwen_rerank_top20.md" \
    --output-json "skill_benchmark/outputs/provider_selector_qwen_public_gold_82_${rep}_qwen_rerank_top20.json"
done
```

Run Qwen first-stage plus M6-v1 local field-aware reranker:

```bash
python3 skill_benchmark/scripts/run_m6v1_field_aware_reranker.py \
  --dotenv .env \
  --prompts "skill_benchmark/prompts/*.json" \
  --scale current_full \
  --first-stage qwen_full \
  --rerank-candidates 100 \
  --field-sets task,task_output_workflow,core,core_boundary,all \
  --output-md skill_benchmark/outputs/m6v1_qwen_full_field_aware.md \
  --output-json skill_benchmark/outputs/m6v1_qwen_full_field_aware.json
```

Run SkillRouter locally only for smoke tests; full-scale local runs are currently impractical on the 8 GB laptop:

```bash
python3 skill_benchmark/scripts/run_skillrouter_selectors.py \
  --prompts "skill_benchmark/prompts/*.json" \
  --scale current_full \
  --skill-subset-from-prompts \
  --embedding-representation full \
  --rerank-candidates 20 \
  --max-prompts 5 \
  --device cpu \
  --output-md skill_benchmark/outputs/skillrouter_smoke_full.md \
  --output-json skill_benchmark/outputs/skillrouter_smoke_full.json
```

Hosted SkillRouter full-scale runs should use the same script in a Hugging Face Job or another GPU environment. Required fair reruns not yet completed:

```bash
# Controlled and public-gold, both R1 and R2:
python3 skill_benchmark/scripts/run_skillrouter_selectors.py \
  --prompts "skill_benchmark/prompts/*.json" \
  --scale current_full \
  --embedding-representation r2 \
  --rerank-candidates 20 \
  --device cuda \
  --output-md skill_benchmark/outputs/skillrouter_controlled_r2_rerank_top20.md \
  --output-json skill_benchmark/outputs/skillrouter_controlled_r2_rerank_top20.json

python3 skill_benchmark/scripts/run_skillrouter_selectors.py \
  --prompts "skill_benchmark/prompts_public_gold/*.json" \
  --scale current_full \
  --embedding-representation r2 \
  --acceptable-alternatives skill_benchmark/annotations/public_gold_acceptable_alternatives.json \
  --rerank-candidates 20 \
  --device cuda \
  --output-md skill_benchmark/outputs/skillrouter_public_gold_82_r2_rerank_top20.md \
  --output-json skill_benchmark/outputs/skillrouter_public_gold_82_r2_rerank_top20.json
```

## Current Key Results Snapshot

Use this only as a quick orientation. For final writing, regenerate tables from JSON artifacts or hosted-job summaries.

### Controlled, 201 prompts

| Method | Representation | Top-1 | Accept top-1 | Top-5 | MRR | Caveat |
|---|---|---:|---:|---:|---:|---|
| M1 BM25 flat | R1 | 61.7% | n/a | 88.1% | 0.727 | Current 2433/201 local rerun. |
| M1 TF-IDF flat | R1 | 55.2% | n/a | 86.1% | 0.689 | Current 2433/201 local rerun. |
| M3 TF-IDF schema | R2/R3 serialized | 65.2% | n/a | 94.0% | 0.778 | Current 2433/201 local rerun. |
| M6 BM25 schema rerank | R1 first stage, R2/R3 rerank | 65.7% | n/a | 93.5% | 0.781 | Current 2433/201 local diagnostic, top-100. |
| M6 TF-IDF schema rerank | R1 first stage, R2/R3 rerank | 65.7% | n/a | 91.5% | 0.773 | Current 2433/201 local diagnostic, top-100. |
| M6-v1 TF-IDF field-aware | R1 first stage, R2/R3 rerank | 72.6% | n/a | 94.0% | 0.824 | Current 2433/201 local prototype, best `core`/`core_boundary`, top-100. |
| M6-v1 BM25 field-aware | R1 first stage, R2/R3 rerank | 72.1% | n/a | 95.0% | 0.825 | Current 2433/201 local prototype, best `core_boundary`, top-100. |
| Qwen embedding | RFULL | 52.5% | 53.3% | 73.7% | 0.617 | Full-document embedding only. |
| Qwen embedding + Qwen rerank | RFULL | 62.0% | 65.0% | 75.2% | 0.684 | Top-20 neural rerank. |
| Qwen embedding + local schema rerank | RFULL first stage, R1/R2/R3 rerank | 77.4% | 77.4% | 91.2% | 0.840 | Top-100 larger-budget diagnostic. |
| SkillRouter embedding | RFULL | 73.0% | 75.9% | 94.2% | 0.827 | Hosted GPU summary. |
| SkillRouter embedding + SkillRouter rerank | RFULL | 83.2% | 83.2% | 97.8% | 0.898 | Hosted GPU summary, top-20. |
| SkillRouter embedding + M6-v1 local | RFULL first stage, R1/R2/R3 rerank | 86.9% | 86.9% | 98.5% | 0.927 | Hosted GPU summary, top-100. |

### Public-gold, 82 prompts

| Method | Representation | Top-1 | Accept top-1 | Top-5 | MRR | Caveat |
|---|---|---:|---:|---:|---:|---|
| Qwen embedding | R1 | 62.2% | 72.0% | 84.2% | 0.720 | Public-only current R1 run. |
| Qwen embedding + Qwen rerank | R1 | 74.4% | 85.4% | 96.3% | 0.837 | Public-only current R1 run. |
| Qwen embedding | R2 | 59.8% | 73.2% | 82.9% | 0.714 | Public-only current R2 run. |
| Qwen embedding + Qwen rerank | R2 | 76.8% | 90.2% | 100.0% | 0.861 | Best current public-gold result; not directly comparable to SkillRouter full. |
| Qwen embedding | RFULL | 31.7% | 50.0% | 58.5% | 0.448 | Full public artifacts are noisy for direct Qwen embedding. |
| Qwen embedding + Qwen rerank | RFULL | 68.3% | 79.3% | 80.5% | 0.739 | Fairer full-representation comparison to SkillRouter full. |
| SkillRouter embedding | RFULL | 68.3% | 79.3% | 95.1% | 0.790 | Hosted 82-case result recorded in notes, not local JSON artifact. |
| SkillRouter embedding + SkillRouter rerank | RFULL | 64.6% | 73.2% | 92.7% | 0.778 | Reranker did not improve public-gold top-1. |
| SkillRouter embedding + M6-v1 local | RFULL first stage, R1/R2/R3 rerank | 68.3% | 78.1% | 90.2% | 0.788 | Field matcher weak on public-gold. |

### Weighted combined, 219 prompts

Historical weighted view from the 137 controlled + 82 public-gold checkpoint. Recompute before using it with the active 201 controlled + 82 public-gold setting.

| Method | Representation | Top-1 | Accept top-1 | Top-5 | MRR |
|---|---|---:|---:|---:|---:|
| Qwen embedding | RFULL | 44.7% | 52.1% | 68.0% | 0.554 |
| Qwen embedding + Qwen rerank | RFULL | 64.4% | 70.3% | 77.2% | 0.705 |
| Qwen embedding + local schema rerank | RFULL first stage, R1/R2/R3 rerank | 58.0% | 65.8% | 84.0% | 0.695 |
| SkillRouter embedding | RFULL | 71.2% | 77.2% | 94.5% | 0.813 |
| SkillRouter embedding + SkillRouter rerank | RFULL | 76.2% | 79.5% | 95.9% | 0.853 |
| SkillRouter embedding + M6-v1 local | RFULL first stage, R1/R2/R3 rerank | 79.9% | 83.6% | 95.4% | 0.875 |

## Open Experiment Gaps

Priority gaps before final claims:

The highest-priority gap is the crossed representation-by-architecture matrix. Both factors are thesis-critical:

- representation layer answers what information is preserved or normalized;
- retriever/reranker architecture answers how that information is exploited.

Final claims should be phrased as representation-architecture interactions until the missing cells below are filled or explicitly scoped out.

1. Run SkillRouter with R1 and R2 on controlled and public-gold strata.
2. Rerun Qwen R1/R2/RFULL on the current controlled 2433/201 condition, if final representation-only comparisons need them.
3. Build exact combined prompt file or combined report generator; current combined values are weighted aggregates.
4. Add per-cluster and per-source-family failure analysis, especially for public-gold.
5. Expand controlled and public-gold cases in a cluster-balanced way. Target at least 200 total evaluated prompts, with each added public cluster having a public gold skill and 2-4 plausible alternatives drawn from public, controlled, or background skills.
6. Add M6-v2 semantic field matching so field-aware reranking is not only lexical overlap.
7. Decide whether M4 tree and M5 graph are final experiment families or thesis discussion/proposed future work.
8. Add cost/latency/token reporting for top-20, top-50, and top-100 budgets.
9. Run paired significance tests for final selected comparisons.

## Result Reporting Template

Use this template when adding any new result:

```text
Method ID:
Prompt stratum:
Prompt count:
Skill count:
Representation:
First-stage retriever:
Reranker:
Candidate budget:
Model/provider:
Cache state:
Output artifacts:
Strict top-1:
Accept top-1:
Top-5:
Accept top-5:
MRR:
Candidate recall:
Latency/cost:
Known caveats:
```
