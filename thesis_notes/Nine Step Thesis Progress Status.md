# Nine-Step Thesis Progress Status

Date: 2026-05-28

This note maps the current thesis progress onto the nine-step benchmark/experiment loop from `skill_benchmark/notes/benchmark_methodology_rubric.md`.

The active local validation benchmark is:

- 2349 total skills.
- 85 evaluated prompts.
- 85 controlled/evaluated core skills.
- 1800 generated background-scale skills.
- 460 public imported background skills.
- 4 support/email skills.

## Summary Table

| Step | Name | Updated 2349 Benchmark? | Status | Current Result |
|---|---|---|---|---|
| 1 | Skill and prompt integrity | Yes | DONE / PASS | 85 prompts and 2349 skills resolve. |
| 2 | Representation coverage and procedural requirement alignment | Yes | DONE / PASS | Field audit 85/85; pair audit 251/251; prompt alignment 85/85. |
| 3 | Semantic confusability | Yes, with backend caveat | DONE / PASS with caveat | Previous MiniLM checkpoint: 75/85. Current 2349 TF-IDF fallback check: 27/85, not directly comparable. |
| 4 | Gold-label stability and prompt leakage | Mostly yes | DONE / PASS, with ongoing adjudication | Leakage: 0 critical, 0 high-risk. Non-core winners manually reviewed. |
| 5 | Scale regime | Yes | DONE / PASS | 2349-skill public-expanded condition built; R1 about 120k tokens. |
| 6 | Public/real-world skill field audit | Yes, expanded heuristic + earlier model audit | MOSTLY DONE | 460/460 public skills audited heuristically; earlier 200-skill DeepSeek verifier and targeted disagreement adjudication exist. |
| 7 | Offline selectors, rerankers, field ablations, scale sensitivity | Yes | DONE / PASS with caveats | Lexical/schema selectors and field ablations rerun on 2349; Qwen/MiniLM provider-style runs remain 2089/historical unless rerun. |
| 8 | M0 progressive-disclosure main-agent baseline | No, historical/core only | PARTLY DONE | M0 exists for older 67-prompt/67-skill core; not rerun on 85-prompt or 2089-scale. |
| 9 | Candidate-subsetting plus downstream main-agent validation | No | NOT DONE | Plan and readiness report exist; downstream execution not run. |

## Step 1: Skill And Prompt Integrity

Purpose:

Check that the benchmark is mechanically valid before making retrieval claims.

Done:

- Ran `skill_benchmark/scripts/validate_benchmark_integrity.py`.
- Confirmed all prompt references resolve.
- Confirmed no duplicate prompt IDs.
- Confirmed skill frontmatter is valid enough for export/evaluation.

Current result:

- PASS.
- 85 prompts.
- 2349 skills.

Current report:

- `skill_benchmark/outputs/benchmark_integrity_report.md`

Remaining:

- Nothing blocking.

## Step 2: Representation Coverage And Procedural Requirement Alignment

Purpose:

Check that the benchmark tests procedural distinctions, not just rephrased descriptions.

Done:

- Ran field-level procedural distinctness.
- Ran stricter prompt-specific requirement alignment.
- Fixed older weak prompts.
- Fixed the alignment analyzer so negated phrases are not counted as positive evidence.

Current result:

- Field audit: PASS, 85/85 prompts.
- Pair audit: PASS, 251/251 gold/alternative pairs differ on at least two primary axes.
- Prompt-specific alignment: PASS, 85/85 prompts.

Current reports:

- `skill_benchmark/outputs/procedural_distinctness_report.md`
- `skill_benchmark/outputs/procedural_requirement_alignment_report.md`

Remaining:

- No immediate benchmark fix required.
- Later thesis writing should explain that Step 2 has two layers:
  - schema/field difference
  - prompt-specific procedural justification

## Step 3: Semantic Confusability

Purpose:

Check that alternatives are plausible semantic neighbours, not random distractors.

Done:

- Ran semantic confusability with local MiniLM embedding backend.
- Checked gold/alternative similarity and prompt/alternative similarity.

Current result:

- PASS with caveat.
- 75/85 prompts pass.
- 10 prompts are weaker semantic-confusion cases.

Current report:

- `skill_benchmark/outputs/semantic_confusability_report.md`

Caveat:

- Some weak Step 3 cases are not necessarily bad. They are high-precision tasks where the gold skill is naturally clearer than the alternatives.
- Do not over-fix this unless final selector results become too easy or these cases dominate failure analysis.
- MiniLM semantic-confusability checks are construction evidence, not a final modern semantic authority. Final writing should describe semantic confusability as controlled near-neighbour design plus local embedding validation.

Remaining:

- Optional: revise only if a weak Step 3 case becomes a serious method-comparison problem.

## Step 4: Gold-Label Stability And Prompt Leakage

Purpose:

Check that prompts do not leak the answer and that gold labels remain defensible under scale.

Done:

- Ran prompt leakage check.
- Manually reviewed non-core semantic/procedural winners after the 2089 expansion; targeted second-pass review remains recommended after the 2349 public expansion.
- Added acceptable alternatives where a non-core skill is genuinely near-equivalent.

Current result:

- Prompt leakage: PASS.
- Critical exact-name leaks: 0.
- High-risk leaks: 0.
- Manual adjudication completed for the current flagged non-core winners.

Current reports:

- `skill_benchmark/outputs/prompt_leakage_report.md`
- `skill_benchmark/outputs/non_core_human_adjudication.md`
- `skill_benchmark/annotations/acceptable_alternatives.json`

Caveat:

- Manual adjudication is currently single-reviewer.
- For thesis rigor, describe it as manual review and optionally do a small second-pass recheck later.
- The independent critique identified this as one of the largest validity risks: if a non-core winner is genuinely better than gold, the benchmark is testing annotation instability rather than retrieval failure.

Remaining:

- Recommended before final result tables: do a targeted second-pass review of acceptable alternatives, non-core winners, and strongest-method failures.

## Step 5: Build Or Refresh Scale Regimes

Purpose:

Make sure the benchmark actually tests scalable skill libraries rather than a small controlled toy set.

Done:

- Expanded background-scale skills to 1800.
- Imported 460 public skills.
- Added 18 controlled-core v2 skills/prompts.
- Exported R1-R4 representations.

Current result:

- PASS.
- Active local scale condition is 2349 skills.
- R1 flat metadata is about 120k visible tokens.
- Full `SKILL.md` exposure is about 1.07M visible tokens.

Current reports:

- `thesis_notes/Scale Expansion 2089 Validation.md`
- `thesis_notes/Context Scale Audit.md`
- `skill_benchmark/outputs/representation_coverage.md`

Remaining:

- Do not expand further for now.
- Public-skill field audit is still useful, but that is now methodology/literature support rather than benchmark expansion.

## Step 6: Public/Real-World Skill Field Audit

Purpose:

Check whether our proposed representation fields are grounded in real skill artifacts, rather than only in our controlled generated skills.

What this should answer:

- Are fields like inputs, outputs, workflow, constraints, dependencies, and resources actually present in public `SKILL.md` files?
- If not explicit, are they extractable from the skill body?
- Do heuristic and model-assisted semantic extraction agree on which fields are present?
- Which fields are empirical observations, and which are proposed normalization fields for better retrieval?

Done:

- We have imported 460 public skills and downloaded 460/460 original `SKILL.md` files, so the raw material exists.
- We have literature support from the public-skill quality paper and related skill retrieval papers.
- A resumable public-skill field audit script now exists: `skill_benchmark/scripts/audit_public_skill_fields.py`.
- A manual-review packet script now exists: `skill_benchmark/scripts/build_public_skill_manual_review_packet.py`.
- A model-assisted semantic verification script now exists: `skill_benchmark/scripts/model_verify_public_skill_fields.py`.
- A heuristic/model agreement report script now exists: `skill_benchmark/scripts/compare_public_skill_field_audits.py`.
- A subagent/manual calibration protocol now exists: `thesis_notes/Public Skill Subagent Review Protocol.md`.
- Subagent pilot review batches completed for 10 public skills.
- Subagent pilot summary exists at `skill_benchmark/outputs/subagent_reviews/public_skill_subagent_pilot_summary.md`.
- DeepSeek model-assisted verification checkpoint completed for the earlier 200 imported public-skill subset.
- Agreement report exists at `skill_benchmark/outputs/public_skill_field_agreement_report.md`.
- Checkpoint note exists at `thesis_notes/Public Skill Model Verification Checkpoint - 20 Skills.md`.
- Full checkpoint note exists at `thesis_notes/Public Skill Model Verification Checkpoint - 200 Skills.md`.
- Targeted disagreement review packet exists at `skill_benchmark/outputs/public_skill_field_disagreement_review_packet.md`.
- Pattern-level adjudication note exists at `thesis_notes/Public Skill Disagreement Adjudication - Step 6.md`.
- Current expanded heuristic checkpoint: 460/460 imported public skills audited. Output files:
  - `skill_benchmark/outputs/public_skill_field_audit.jsonl`
  - `skill_benchmark/outputs/public_skill_field_audit_summary.json`
  - `skill_benchmark/outputs/public_skill_field_audit.md`
  - `skill_benchmark/outputs/public_skill_field_manual_review_packet.md`

Remaining:

- Freeze the field taxonomy into observed / extractable / proposed categories before final reporting.
- Avoid rerunning the 200-skill checkpoint unless the schema, prompt, model, or field definitions change.
- Use the completed subagent pilot review to calibrate heuristic/model disagreement cases.
- If a stricter appendix is required, manually label all 50 rows in the disagreement packet.
- If field definitions change materially, refine the detector and rerun the full 200-skill checkpoint.
- Otherwise, do not rerun the full public audit.
- Count explicit and implicit presence of:
  - routing trigger / description
  - input or precondition
  - output artifact
  - workflow or procedure
  - constraints / not-for boundaries
  - tools, APIs, platform dependencies
  - scripts, resources, references
  - examples or tests
- Classify each field as observed, extractable, or proposed.

Caveat:

- If public skills lack some fields, that does not kill the thesis. It changes the claim: the representation layer should extract/infer/normalize these retrieval-critical fields, rather than assuming authors always provide them.
- The heuristic audit alone is not enough for final claims. The final Step 6 result should combine deterministic extraction, model-assisted semantic extraction, and manual calibration.
- The public audit is grounding evidence, not a full gold-standard corpus annotation study. Avoid overclaiming field prevalence.

## Step 7: Offline Selectors, Rerankers, Field Ablations, And Scale Sensitivity

Purpose:

Compare representation/retrieval methods using the benchmark before involving expensive main-agent downstream tasks.

Done on updated 2349 benchmark:

- M1 BM25 flat.
- M1 TF-IDF flat.
- M3 TF-IDF schema retrieval.
- M6 BM25 plus schema rerank.
- M6 TF-IDF plus schema rerank.
- Non-core semantic competition.
- Non-core procedural competition.
- Field ablations.

Done on updated 2089 benchmark but not rerun after the 2349 public expansion:

- M2a MiniLM description embedding.
- M2b MiniLM full-skill embedding.
- M6 MiniLM full-skill plus schema rerank.

Current 2349 local lexical/schema results:

| Method | Core Top-1 | Full Top-1 | Full Top-5 | Full Non-Core Top-1 |
|---|---:|---:|---:|---:|
| M1 BM25 flat | 76.5% | 68.2% | 87.1% | 15.3% |
| M1 TF-IDF flat | 75.3% | 58.8% | 78.8% | 28.2% |
| M3 TF-IDF schema | 84.7% | 76.5% | 94.1% | 10.6% |
| M6 BM25 -> schema rerank | 80.0% | 78.8% | 91.8% | 5.9% |
| M6 TF-IDF -> schema rerank | 84.7% | 74.1% | 87.1% | 14.1% |

Current reports:

- `skill_benchmark/outputs/offline_selector_evaluation.md`
- `skill_benchmark/outputs/offline_selector_evaluation_2349_lexical.md`
- `skill_benchmark/outputs/non_core_semantic_competition_embedding_report.md`
- `skill_benchmark/outputs/all_non_core_procedural_competition_embedding_report.md`
- `skill_benchmark/outputs/field_ablation_results.md`
- `thesis_notes/Field Ablation Results - 2089 Scale.md`
- `thesis_notes/Public Expansion 2349 Validation Checkpoint.md`

Done on updated 2089 benchmark for provider baselines:

- Qwen `text-embedding-v4` full-skill embedding-only retrieval.
- Qwen `text-embedding-v4` full-skill embedding plus Qwen `qwen3-rerank` over top-20.
- Qwen `text-embedding-v4` full-skill embedding plus local schema reranking over top-50.
- Qwen `text-embedding-v4` full-skill embedding plus local schema reranking over top-100.

Current 2089 provider results:

| Method | Candidate Budget | Top-1 | Accept Top-1 | Top-5 | Accept Top-5 | MRR | Non-Core Top-1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen full-skill embedding only | none | 50.6% | 51.8% | 69.4% | 71.8% | 0.591 | 30.6% |
| Qwen full-skill + Qwen rerank | 20 | 63.5% | 68.2% | 69.4% | 72.9% | 0.668 | 32.9% |
| Qwen full-skill + local schema rerank | 50 | 80.0% | 81.2% | 84.7% | 85.9% | 0.822 | 12.9% |
| Qwen full-skill + local schema rerank | 100 | 84.7% | 84.7% | 89.4% | 89.4% | 0.872 | 9.4% |

Done but still historical 1006-scale only:

- Qwen R1 flat-card embedding and reranking variants.
- Qwen R2 structured-card embedding and reranking variants.
- Earlier Qwen candidate-budget ablations over the 1006-skill condition.
- Low-information stress test.
- Failure-mode analysis for Qwen full-skill plus local schema top-100.

Caveat:

- Qwen R1 and R2 representation variants are still historical 1006-scale unless rerun on 2089.
- Qwen full-skill provider variants remain 2089-scale unless rerun on 2349.
- MiniLM is a local construction/evaluation baseline, not the final "strong modern embedding" claim, and was not rerun on 2349 because `sentence_transformers` is unavailable in the current shell.

Field ablation result:

- Description-only full-scale TF-IDF top-1: 60.0%.
- Description + use conditions full-scale TF-IDF top-1: 74.1%.
- + output artifacts full-scale TF-IDF top-1: 82.3%.
- + workflow/procedure full-scale TF-IDF top-1: 84.7%, with stronger top-5/MRR.
- Full-scale BM25 peaks at 89.4% top-1 with description + use + preconditions + outputs + workflow.
- Naive `not_for` concatenation reduces top-1 because negative boundaries are treated as positive lexical evidence.
- Naive dependency/resource concatenation adds token cost and noise; it is better treated as field-aware reranker/downstream feasibility evidence.

Remaining:

- Decide whether rerunning Qwen/MiniLM conditions on 2349 is necessary. It is optional unless the thesis needs provider results for every representation variant on the exact final scale.
- Freeze final method set.
- Run final failure-mode comparison across selected methods.
- Decide final candidate budget, probably top-50 or top-100 for hybrid reranking.
- Avoid further benchmark/schema tuning after the final method set is frozen, unless logged as a validity correction.

## Step 8: M0 Progressive-Disclosure Main-Agent Baseline

Purpose:

Compare retriever-style methods against the normal agent behavior where the main agent sees skill cards and decides whether to load full skill docs.

Done:

- Historical M0 baseline exists for older 67-prompt/67-skill core.

Historical result:

- Strict top-1: 61.2%.
- Strict any-hit: 64.2%.
- No explicit skill loaded: 31.3%.
- Mean full docs loaded: 0.78.

Current reports:

- `skill_benchmark/outputs/m0_progressive_disclosure_core_report.md`

Caveat:

- M0 has not been rerun on the updated 85-prompt core.
- M0 has not been run on the 2089-skill scale condition.
- Full 2089 M0 may be mainly a context/cost stress test, because compact metadata is about 105k visible tokens and full skill docs exceed 1M tokens.

Remaining:

- Recommended minimum: rerun M0 on the updated 85-prompt controlled core.
- Optional: estimate or simulate 2089-scale M0 context cost rather than running expensive full-agent trials.

## Step 9: Candidate-Subsetting Plus Main-Agent Downstream Validation

Purpose:

Check whether better retrieval actually improves downstream task output, not just offline ranking metrics.

Done:

- Step 9 downstream validation plan exists.
- Step 9 candidate readiness report exists.

Not done:

- No actual downstream artifact-generation runs yet.
- No downstream artifact grading yet.

Current reports:

- `skill_benchmark/outputs/step8_downstream_validation_plan.md`
- `skill_benchmark/outputs/step8_candidate_readiness_report.md`

Remaining:

- Select a small sample, probably 12 prompts.
- Compare 2-4 retrieval conditions, not every method.
- Generate downstream outputs with the selected candidate sets.
- Grade outputs for task success, artifact correctness, evidence use, and misuse of wrong skill.

## What Is Actually Current On The Updated Benchmark?

Current on 2349:

- Steps 1, 2, 3, 4 leakage, 5.
- Step 6 public-skill heuristic/model audit and pattern-level disagreement adjudication.
- Step 7 local offline selectors.
- Step 7 non-core semantic/procedural competition.
- Step 7 field ablation.
- Manual adjudication of current flagged non-core winners.

Not current on 2349:

- Qwen R1/R2 provider representation variants.
- Qwen full-skill provider conditions.
- MiniLM local selector conditions.
- M0 progressive-disclosure agent baseline.
- Step 9 downstream validation.

## Recommended Next Order

1. Freeze the benchmark and stop expanding skills.
2. Review and confirm the draft final representation-field taxonomy.
3. Run targeted second-pass adjudication on non-core winners and strongest-method failures.
4. Decide whether Qwen/MiniLM runs must be rerun on 2349 or whether the 2349 lexical/schema validation plus 2089 provider results are enough.
5. Rerun M0 on the updated 85-prompt core if feasible.
6. Choose final method set and candidate budget.
7. Run final failure-mode analysis on the final method set.
8. Run Step 9 downstream validation on a small sample.
9. Move results into thesis chapters.
