# M6-v1 Field-Aware Reranker Checkpoint - 2026-06-03

Purpose: implement the first `M6-v1` prototype and test whether fixed information groups improve skill selection under the same first-stage candidate generator.

## Framing Update

Use the term **selection information** rather than only "procedural information".

The taxonomy currently has seven groups:

| Group | Role | Current interpretation |
|---|---|---|
| `task` / use condition | What problem the skill is meant for | Primary positive retrieval signal. |
| `input` / precondition | What source material or prior state the skill expects | Primary but often implicit. |
| `output` / artifact | What the skill should produce | Primary positive disambiguation signal. |
| `workflow` / procedure | What operations or reasoning steps must happen | Primary positive disambiguation signal. |
| `dependency` / resource / platform | Required tools, files, APIs, platforms, or resources | Conditional feasibility signal; noisy as plain positive text. |
| `boundary` / not-for | Explicit exclusions or mismatch conditions | Conditional negative/guardrail signal. |
| `hierarchy` / task role | Whether the skill is atomic, broad, wrapper-like, router-like, or parent-like | Conditional structure signal; useful for broad-skill penalties. |

This is broader than "inputs and outputs". The thesis should ask which of these information groups must survive in the selection representation and how they should be used.

## Implementation

New files:

- `skill_benchmark/scripts/field_aware_matching.py`
- `skill_benchmark/scripts/run_m6v1_field_aware_reranker.py`

The current `M6-v1` prototype:

1. fixes a first-stage candidate generator;
2. parses the user request into request-side fields;
3. compares request fields to skill-side `R2/R3` fields;
4. combines normalized first-stage score with field-aware score;
5. reports candidate recall separately from reranker quality.

Important limitation:

- The current matcher is still transparent and mostly lexical.
- It is stronger than `M6-v0` because it uses request-side fields and field-to-field comparison, but it is not yet a semantic/LLM field matcher.
- Therefore it should be reported as `M6-v1-local`, or as the first deterministic prototype of `M6-v1`, not the final possible version of field-aware reranking.

## Controlled 2401-Skill Results

### Qwen Full-Skill Candidate Generator

Command:

```bash
python3 skill_benchmark/scripts/run_m6v1_field_aware_reranker.py \
  --first-stage qwen_full \
  --scale current_full \
  --rerank-candidates 100 \
  --field-sets task,task_output_workflow,core,core_boundary,all \
  --output-md skill_benchmark/outputs/m6v1_qwen_full_field_aware.md \
  --output-json skill_benchmark/outputs/m6v1_qwen_full_field_aware.json
```

| Field set | Top-1 | Top-5 | MRR | Candidate R@100 | Conditional top-1 | Non-main top-1 |
|---|---:|---:|---:|---:|---:|---:|
| `task` | 75.2% | 88.3% | 0.816 | 93.4% | 80.5% | 8.0% |
| `task_output_workflow` | 78.8% | 92.0% | 0.851 | 93.4% | 84.4% | 6.6% |
| `core` | 77.4% | 92.0% | 0.843 | 93.4% | 82.8% | 6.6% |
| `core_boundary` | 77.4% | 92.7% | 0.841 | 93.4% | 82.8% | 8.0% |
| `all` | 73.0% | 89.0% | 0.809 | 93.4% | 78.1% | 11.7% |

Interpretation:

- `task_output_workflow` is the strongest Qwen-backed `M6-v1-local` field set.
- It slightly improves over the previous Qwen full-skill + `M6-v0` schema reranker result of 77.4% top-1 / 91.2% top-5 / 0.840 MRR.
- Adding all fields hurts, especially non-main top-1. This supports the claim that dependencies, boundaries, and hierarchy must be used conditionally rather than appended as positive text.
- Candidate R@100 is 93.4%, so remaining failures include both first-stage misses and reranker misordering.

### Local Lexical Candidate Generators

Best `tfidf_flat` result:

- `core_boundary`: 79.6% top-1, 94.9% top-5, 0.866 MRR, 95.6% candidate R@100, 5.1% non-main top-1.

Best `bm25_flat` result:

- `task_output_workflow` or `core`: 78.8% top-1, 95.6% top-5, about 0.873 MRR, 97.8% candidate R@100, 2.2% non-main top-1.

Interpretation:

- The field-aware reranker improves over flat local baselines and over the older local `M6-v0` results.
- Again, the stable gain comes from task/use condition, output artifact, and workflow/procedure fields.

## Public-Gold Results

Command:

```bash
python3 skill_benchmark/scripts/run_m6v1_field_aware_reranker.py \
  --prompts skill_benchmark/prompts_public_gold/*.json \
  --acceptable-alternatives skill_benchmark/annotations/public_gold_acceptable_alternatives.json \
  --first-stage qwen_full \
  --scale current_full \
  --rerank-candidates 100 \
  --field-sets task,task_output_workflow,core,core_boundary,all \
  --output-md skill_benchmark/outputs/m6v1_public_gold_qwen_full_field_aware.md \
  --output-json skill_benchmark/outputs/m6v1_public_gold_qwen_full_field_aware.json
```

| Field set | Top-1 | Accept Top-1 | Top-5 | Accept Top-5 | MRR | Candidate R@100 | Conditional top-1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `task` | 53.1% | 59.4% | 78.1% | 78.1% | 0.647 | 96.9% | 54.8% |
| `task_output_workflow` | 46.9% | 56.2% | 84.4% | 87.5% | 0.619 | 96.9% | 48.4% |
| `core` | 50.0% | 59.4% | 81.2% | 84.4% | 0.635 | 96.9% | 51.6% |
| `core_boundary` | 50.0% | 59.4% | 90.6% | 93.8% | 0.640 | 96.9% | 51.6% |
| `all` | 46.9% | 53.1% | 87.5% | 87.5% | 0.621 | 96.9% | 48.4% |

Interpretation:

- Public-gold remains a stress test rather than a clean proof of the method.
- Candidate R@100 is high, so Qwen generally finds the right public skill, but `M6-v1-local` often misorders candidates.
- Generic Qwen reranking remains stronger on public-gold top-1 than this local field-aware prototype.
- This does not invalidate the information-taxonomy claim. It shows the final field-aware method needs better field extraction and/or semantic field matching for messy public skills.

## Thesis Claim Supported So Far

Supported:

- Specific field groups matter.
- Task/use condition, output artifact, and workflow/procedure are the strongest positive disambiguation fields.
- Adding all available structure is not automatically better.
- Candidate recall decomposition is necessary: Qwen has high candidate recall but still needs final selection logic.

Not yet supported:

- A claim that `M6-v1-local` solves public-skill retrieval.
- A claim that field-aware reranking is generally stronger than generic neural reranking.
- A downstream task-success claim.

## Next Steps

1. Clean public-gold labels into strict / acceptable / revise-exclude and rerun public-gold.
2. Add a semantic or LLM-assisted field matcher variant of `M6-v1`.
3. Add candidate-recall/failure-mode tables to thesis results.
4. Decide whether M4/M5 are still needed after `M6-v1` evidence is stronger.

