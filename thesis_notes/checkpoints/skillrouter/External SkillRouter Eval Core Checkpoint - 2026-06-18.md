# External SkillRouter Eval Core Checkpoint - 2026-06-18

Purpose: add an external validation track using the public `pipizhao/SkillRouter-Eval-Core` benchmark. This track is not a replacement for the controlled thesis benchmark. It tests whether the information-layer framing transfers to a large public skill-routing benchmark.

Extraction note: this checkpoint uses heuristic I3 (`I3H`), not model-parsed I3 (`I3M`). No DeepSeek, Qwen, or other LLM API was used to produce the first external I3 parse. Model-parsed I3M is planned under `thesis_notes/current/I3 Model Extraction Protocol.md`.

## Dataset Status

- Raw dataset folder: `skill_benchmark/external/skillrouter_eval_core/raw`
- Derived folder: `skill_benchmark/external/skillrouter_eval_core/derived`
- Output folder: `skill_benchmark/external/skillrouter_eval_core/outputs`
- Source: Hugging Face dataset `pipizhao/SkillRouter-Eval-Core`
- Raw files downloaded: 23
- All tasks: 87
- Default scored tasks: 75, excluding `generic_only` tasks according to SkillRouter's public protocol
- Easy skills: 78,361
- Hard skills: 79,141
- Hard-only distractors: 780
- Hard contains all Easy skills: yes

Hard-only computation:

```text
hard_only = hard_skill_ids - easy_skill_ids
```

This confirms the Hard tier is exactly the Easy tier plus 780 generated hard distractors.

## Derived Information Layers

The external set is mapped into the thesis information layers:

| Information layer | External implementation | Meaning |
|---|---|---|
| I1 | `easy_I1.jsonl`, `hard_I1.jsonl` | name, source, short description |
| I2 | `easy_I2.jsonl`, `hard_I2.jsonl` | name, source, description, full body |
| I3H | `easy_I3.jsonl`, `hard_I3.jsonl` | heuristic extracted use conditions, boundaries, preconditions, workflow, outputs, dependencies/resources |

I3H parsing is chunked and resumable:

- Chunk folder: `skill_benchmark/external/skillrouter_eval_core/derived/i3_chunks`
- Chunk count: 16
- Chunk size: up to 5,000 skills
- Parser: conservative heuristic extraction reused from the local benchmark representation exporter

I3 field coverage:

| Tier | Rows | Approx tokens | use_when | not_for | preconditions | workflow | output | dependencies | resources |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Easy | 78,361 | 63,119,911 | 61,887 | 7,687 | 26,231 | 43,676 | 9,381 | 0 | 0 |
| Hard | 79,141 | 63,232,478 | 62,385 | 7,688 | 26,358 | 43,842 | 9,409 | 0 | 0 |

Important caveat: the current I3H external parser recovers many use/workflow/precondition fields, but it does not yet recover dependency/resource fields from this dataset. It is also broad: I3H is much smaller than I2 but still large, so model-parsed I3M may be needed before making strong portability claims.

## First External Evaluation

Report:

- `skill_benchmark/external/skillrouter_eval_core/outputs/skillrouter_eval_core_fts_information_layers.md`
- `skill_benchmark/external/skillrouter_eval_core/outputs/skillrouter_eval_core_fts_information_layers.json`

Method:

- Retriever: SQLite FTS5 BM25
- Reason: disk-backed indexing makes full I2 body retrieval feasible on the laptop without loading a giant TF-IDF matrix into memory
- Ranking limit: top-50
- Metrics: Hit@1, MRR@10, nDCG@10, Recall@10/20/50, FullCoverage@10/20, Hard-only top1 rate

Summary:

| Tier | Information layer | Hit@1 | MRR@10 | Recall@20 | FullCoverage@20 | Tokens |
|---|---|---:|---:|---:|---:|---:|
| Easy | I1 | 36.0% | 0.448 | 48.3% | 32.0% | 5,488,975 |
| Easy | I2 | 48.0% | 0.558 | 57.4% | 42.7% | 152,669,986 |
| Easy | I3H | 38.7% | 0.453 | 46.0% | 29.3% | 63,119,911 |
| Hard | I1 | 28.0% | 0.373 | 46.1% | 30.7% | 5,536,118 |
| Hard | I2 | 44.0% | 0.525 | 55.7% | 41.3% | 153,155,878 |
| Hard | I3H | 36.0% | 0.439 | 45.1% | 28.0% | 63,232,478 |

Initial interpretation:

- I2 full body is strongest under disk-backed lexical BM25 on both Easy and Hard. This matches SkillRouter's claim that full skill bodies contain routing-critical signal.
- I3H improves over I1 on Hard Hit@1, which suggests extracted procedural fields can help under distractor pressure.
- I3H loses to I1 on Recall@20 and FullCoverage@20, and loses to I2 overall. This means the current heuristic I3H extraction is not yet a portable replacement for full body retrieval on this benchmark.
- I3H has lower token cost than I2, but it is still far larger than I1. Its usefulness must therefore be argued as a compact/interpretable partial recovery of body signal, not as an obvious cheap win in this first pass.
- Hard-only top1 drops from 10.7% on I1 to 2.7% on I3, suggesting I3 may reduce some generated-distractor top-rank failures even when recall does not improve.

## Commands

Download:

```bash
python3 - <<'PY'
from pathlib import Path
from huggingface_hub import snapshot_download
root = Path('skill_benchmark/external/skillrouter_eval_core/raw')
root.mkdir(parents=True, exist_ok=True)
snapshot_download(
    repo_id='pipizhao/SkillRouter-Eval-Core',
    repo_type='dataset',
    local_dir=str(root),
    allow_patterns=[
        'manifest.json',
        'tasks.jsonl',
        'relevance.json',
        'easy/*.jsonl.gz',
        'hard/*.jsonl.gz',
    ],
)
PY
```

Prepare layers:

```bash
python3 skill_benchmark/scripts/prepare_skillrouter_eval_core.py --chunk-size 5000 --workers 8
```

Run disk-backed lexical external validation:

```bash
/usr/bin/python3 skill_benchmark/scripts/run_skillrouter_eval_core_fts_ablation.py \
  --tiers easy,hard \
  --representations I1,I2,I3 \
  --ranking-limit 50
```

Use `/usr/bin/python3` for the FTS runner because the local Anaconda Python currently has a broken SQLite binding.

## Next Steps

1. Inspect representative I3 extraction rows from SkillRouter gold skills and hard-only distractors.
2. Add model-parsed I3M using the frozen protocol if the current heuristic parser is too broad.
3. Run dense retrieval only after deciding whether external I3 extraction quality is adequate, because embedding 79K full bodies through an API may be expensive.
4. Consider absorbing selected high-quality hard-only distractor clusters into a separate `skillrouter_derived_hard` stress split only after manual adjudication.
5. Report this as portability evidence, not as the main causal benchmark.
