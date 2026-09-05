# External SkillRouter I3C V2 FTS Rerun - 2026-06-21

Status: complete.

This checkpoint records the first full-tier retrieval evaluation using the cleaned SkillRouter-Eval-Core I3C V2 structured-field artifact. It is an external verification track for the information-layer claim, not a replacement for the frozen-v0.4 controlled benchmark.

## Inputs

- Source extraction: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/I3C_V2_full_all_cleaned.jsonl`
- FTS-ready Easy output: `skill_benchmark/external/skillrouter_eval_core/derived/representations/easy_I3C.jsonl`
- FTS-ready Hard output: `skill_benchmark/external/skillrouter_eval_core/derived/representations/hard_I3C.jsonl`
- Builder script: `skill_benchmark/scripts/build_i3c_v2_fts_representations.py`
- Summary: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_fts_representation_summary.json`

Generated rows:

| Tier | Rows | Missing I3C rows | Approx tokens |
|---|---:|---:|---:|
| Easy | 78,361 | 0 | 15,677,596 |
| Hard | 79,141 | 0 | 15,833,065 |

Validation:

- JSONL parsing passed for both generated files.
- Missing `skill_id` rows: 0.
- Representation mismatch rows: 0.
- Surrogate-containing text rows after cleanup: 0.

## Run

Command:

```bash
python3 skill_benchmark/scripts/run_skillrouter_eval_core_fts_ablation.py \
  --representations I1,I2,I3,I3C \
  --output-prefix skillrouter_eval_core_fts_information_layers_i3c_v2 \
  --force-index
```

Outputs:

- `skill_benchmark/external/skillrouter_eval_core/outputs/skillrouter_eval_core_fts_information_layers_i3c_v2.md`
- `skill_benchmark/external/skillrouter_eval_core/outputs/skillrouter_eval_core_fts_information_layers_i3c_v2.json`

## Results

| Tier | Layer | Hit@1 | MRR@10 | Recall@20 | FullCoverage@20 | Approx tokens |
|---|---|---:|---:|---:|---:|---:|
| Easy | I1 metadata | 36.0% | 0.448 | 48.3% | 32.0% | 5,488,975 |
| Easy | I2 full body | 48.0% | 0.558 | 57.4% | 42.7% | 152,669,986 |
| Easy | I3H heuristic extracted fields | 38.7% | 0.453 | 46.0% | 29.3% | 63,119,911 |
| Easy | I3C V2 structured fields | 53.3% | 0.586 | 60.5% | 44.0% | 15,677,596 |
| Hard | I1 metadata | 28.0% | 0.373 | 46.1% | 30.7% | 5,536,118 |
| Hard | I2 full body | 44.0% | 0.525 | 55.7% | 41.3% | 153,155,878 |
| Hard | I3H heuristic extracted fields | 36.0% | 0.439 | 45.1% | 28.0% | 63,232,478 |
| Hard | I3C V2 structured fields | 45.3% | 0.527 | 59.2% | 40.0% | 15,833,065 |

## Interpretation

- I3C V2 is the strongest Easy-tier condition across Hit@1, MRR@10, Recall@20, and FullCoverage@20.
- On Hard, I3C V2 narrowly beats I2 on Hit@1, MRR@10, and Recall@20; I2 remains slightly higher on FullCoverage@20.
- I3C V2 is much smaller than I2 full body: about 15.8M approximate tokens versus about 153M on the Hard tier.
- This supports the thesis claim that structured selection information can be useful when recovered cleanly, especially compared with heuristic I3H.
- This does not complete local frozen-v0.4 I3C reruns. The local `I3M_model_parsed.jsonl` artifact is DeepSeek/API-derived and should remain labelled as I3M/paid-model feasibility.
