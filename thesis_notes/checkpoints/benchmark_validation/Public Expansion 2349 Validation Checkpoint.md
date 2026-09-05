# Public Expansion 2349 Validation Checkpoint

Date: 2026-05-29

Purpose: expand the public background layer and revalidate whether the original controlled clusters still work under a larger, messier public-skill pool.

## Expansion Summary

The public imported background layer was expanded from 200 to 460 public `SKILL.md` artifacts.

Current library:

- 2349 total skills.
- 85 controlled/evaluated core skills.
- 1800 generated background-scale skills.
- 460 public imported background skills.
- 4 support/email skills.
- 85 evaluated prompts.

Public import status:

- 460/460 public originals downloaded.

Largest public origins:

| Origin | Skills |
|---|---:|
| `claude-office-skills/skills` | 136 |
| `akillness/oh-my-skills` | 127 |
| `GeniusHTX/SWE-Skills-Bench` | 49 |
| `openai/skills` | 41 |
| `mattpocock/skills` | 25 |
| `addyosmani/agent-skills` | 23 |
| `anthropics/skills` | 17 |
| `huggingface/skills` | 15 |
| `addyosmani/web-quality-skills` | 6 |
| other smaller sources | 21 |

## Validation Loop Rerun

Rerun commands:

```bash
python3 skill_benchmark/scripts/import_public_background_skills.py
python3 skill_benchmark/scripts/validate_benchmark_integrity.py
python3 skill_benchmark/scripts/export_skill_representations.py
python3 skill_benchmark/scripts/analyze_representation_coverage.py
python3 skill_benchmark/scripts/analyze_procedural_distinctness.py
python3 skill_benchmark/scripts/analyze_requirement_alignment.py
python3 skill_benchmark/scripts/analyze_prompt_leakage.py
python3 skill_benchmark/scripts/analyze_semantic_confusability.py
python3 skill_benchmark/scripts/audit_public_skill_fields.py
python3 skill_benchmark/scripts/build_public_skill_manual_review_packet.py
python3 skill_benchmark/scripts/analyze_non_core_competition.py --backend tfidf
python3 skill_benchmark/scripts/analyze_all_non_core_procedural_competition.py --backend tfidf
python3 skill_benchmark/scripts/run_offline_selectors.py --methods m1_bm25_flat,m1_tfidf_flat,m3_tfidf_schema,m6_bm25_schema_rerank,m6_tfidf_schema_rerank --output-md skill_benchmark/outputs/offline_selector_evaluation_2349_lexical.md --output-json skill_benchmark/outputs/offline_selector_evaluation_2349_lexical.json
python3 skill_benchmark/scripts/run_field_ablation_selectors.py --include-single
```

## Step Results

| Step | Result |
|---|---|
| Step 1 integrity | PASS: 85 prompts and 2349 skills resolve. |
| Step 2 procedural distinctness | PASS: 85/85 prompts; 251/251 gold/alternative pairs differ on 2+ primary axes. |
| Step 2 prompt-specific alignment | PASS: 85/85 prompts; gold top-1 among listed candidates for 85/85. |
| Step 3 semantic confusability | 27/85 under TF-IDF fallback. Not comparable to previous MiniLM run. |
| Step 4 prompt leakage | PASS: 0 critical exact-name leaks; 0 high-risk leaks. |
| Step 5 scale | PASS: 2349 skills; R1 flat-card visible tokens about 120k. |
| Step 6 public field audit | PASS as heuristic checkpoint: 460/460 public skills audited. |
| Step 7 non-core semantic competition | 26/85 prompts have a non-core top-1 under TF-IDF; best non-core beats gold for 30/85. |
| Step 7 all-non-core procedural competition | 14/85 prompts have at least one non-core above gold; 49 above-gold comparisons. |
| Step 7 lexical selector subset | PASS useful pressure; no MiniLM methods run because `sentence_transformers` is unavailable in this shell. |
| Step 7 field ablation | PASS; original field pattern is preserved. |

## Public Field Audit, 460 Skills

Heuristic public-field prevalence:

| Field | Explicit | Explicit or Extractable |
|---|---:|---:|
| `routing_trigger` | 100.0% | 100.0% |
| `input_precondition` | 25.2% | 81.5% |
| `output_artifact` | 45.2% | 85.2% |
| `workflow_procedure` | 71.7% | 84.4% |
| `constraints_boundaries` | 41.3% | 77.6% |
| `dependencies_tools` | 72.8% | 85.0% |
| `resources_references` | 66.7% | 82.0% |
| `examples_tests` | 63.5% | 93.9% |
| `safety_side_effects` | 11.3% | 37.0% |
| `portability_environment` | 62.2% | 80.7% |
| `hierarchy_links` | 25.2% | 31.1% |

Interpretation:

- The expanded public audit still supports the field taxonomy.
- Core procedural fields remain common or extractable: input/precondition, output artifact, workflow, dependencies/tools, resources, examples/tests, and portability/environment.
- Safety/side effects remains weakly observed.
- Hierarchy/links is less common in this broader imported set than in the earlier 200-skill sample.

## Local Lexical Selector Results, 2349 Skills

These are local lexical/schema runs only. MiniLM-backed methods were not rerun because `sentence_transformers` is unavailable in the current shell.

| Method | Full Top-1 | Full Top-5 | MRR | Non-Core Top-1 |
|---|---:|---:|---:|---:|
| M1 BM25 flat | 68.2% | 87.1% | 0.765 | 15.3% |
| M1 TF-IDF flat | 58.8% | 78.8% | 0.688 | 28.2% |
| M3 TF-IDF schema | 76.5% | 94.1% | 0.845 | 10.6% |
| M6 BM25 -> schema rerank | 78.8% | 91.8% | 0.851 | 5.9% |
| M6 TF-IDF -> schema rerank | 74.1% | 87.1% | 0.799 | 14.1% |

Interpretation:

- The expanded public layer increases or preserves scale pressure.
- Schema-aware methods still outperform flat lexical methods.
- M6 BM25 -> schema rerank is especially stable: only a small drop from core to full scale and lower non-core top-1 than flat methods.

## Field Ablation Stability

The original field-ablation conclusion still holds under 2349 skills.

Full-scale cumulative results:

| Scorer | Best useful field set | Top-1 | Top-5 | MRR | Non-Core Top-1 |
|---|---|---:|---:|---:|---:|
| TF-IDF | description + use + preconditions + output + workflow | 84.7% | 95.3% | 0.891 | 8.2% |
| BM25 | description + use + preconditions + output + workflow | 89.4% | 97.7% | 0.927 | 2.4% |

Adding constraints/not-for and dependencies/resources as plain text still hurts top-1:

- TF-IDF drops from 84.7% at workflow to 77.6% with constraints and 75.3% with dependencies/resources.
- BM25 drops from 89.4% at workflow to 78.8% with constraints/dependencies/resources.

This strengthens the thesis claim that structure-aware representation should preserve the right fields and use boundary/dependency/resource information carefully.

## Caveats

- Step 3 semantic confusability reran with TF-IDF fallback, not MiniLM. The 27/85 result should not replace the previous MiniLM-based semantic-confusability evidence.
- Qwen provider runs were not rerun on 2349 skills. The current Qwen results remain 2089-scale.
- DeepSeek model-assisted public-field verification was not rerun on all 460 public skills. The new 460-skill result is a heuristic audit plus manual-review packet.

## Decision

The expansion is useful and should be kept as the active public-expanded local validation condition.

Do not promote the imported public skills into controlled gold tasks unless they are atomized, assigned prompts, and passed through Steps 1-4.

Next recommended work:

1. Install/use a comparable semantic backend if we need a MiniLM rerun, or use Qwen embeddings for final semantic checks.
2. Do targeted second-pass adjudication on non-core winners under the 2349 condition.
3. Decide whether provider runs should be rerun on 2349 or kept as 2089-scale evidence.
