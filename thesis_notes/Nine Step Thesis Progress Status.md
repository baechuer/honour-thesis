# Nine-Step Thesis Progress Status

Date: 2026-06-06

This note maps the current thesis progress onto the nine-step benchmark/experiment loop from `skill_benchmark/notes/benchmark_methodology_rubric.md`.

The active local validation benchmark is:

- 2433 total skills.
- 201 controlled/evaluated prompts.
- 82 cleaned public-gold prompts as a separate external-validity stratum.
- 283 total evaluated prompts across controlled + public-gold strata if combined for reporting.
- 169 controlled/evaluated core skills, including 32 public-style controlled skills.
- 1800 generated background-scale skills.
- 460 public imported background skills.
- 4 support/email skills.
- 10 implicit-field stress prompts integrated into the main benchmark.

## Summary Table

| Step | Name | Updated Active Benchmark? | Status | Current Result |
|---|---|---|---|---|
| 1 | Skill and prompt integrity | Yes | DONE / PASS | 201 controlled prompts and 2433 skills resolve. |
| 2 | Representation coverage and procedural requirement alignment | Yes | DONE / PASS, with audit targets | Field/pair audit 201/201 prompts and 641/641 pairs; prompt-specific MiniLM alignment passes 182/201 prompts, with 618/641 pairs passing and gold top-1 among listed candidates for 183/201. |
| 3 | Semantic confusability | Yes | DONE / PASS | MiniLM checkpoint: 180/201 prompts, 89.6%, above 85% pass threshold; public-style controlled stratum passes 64/64. |
| 4 | Gold-label stability and prompt leakage | Mostly yes | DONE / PASS, with ongoing adjudication | Leakage: 0 critical, 0 high-risk. Non-core winners manually reviewed. |
| 4b | Manual cluster design audit before expansion | Yes, first pass used | DONE / FIRST PASS | `skill_benchmark/outputs/cluster_design_audit.md` audits 22 controlled clusters and 34 public-gold source families; 2026-06-06 public-style expansion followed it. |
| 5 | Scale regime | Yes | DONE / PASS | 2433-skill public-expanded condition built; R1 token count needs refresh after public-style expansion. |
| 6 | Public/real-world skill field audit | Yes, expanded heuristic + model audit | MOSTLY DONE | 460/460 public skills audited heuristically and with DeepSeek model verification; 80-case disagreement packet generated for manual taxonomy review. |
| 6b | Public-skill gold validation | Separate public-gold stratum | DONE / PASS WITH CAVEATS | 82 cleaned public-gold cases; integrity PASS, procedural distinctness 82/82, requirement alignment PASS at 79/82, semantic confusability PASS at 78/82, leakage PASS. |
| 7 | Offline selectors, rerankers, field ablations, scale sensitivity | Yes | DONE / HARDENING NEEDED | M6-v1-local is implemented as a lexical field-aware prototype; SkillRouter hosted baselines are done; final claims still need budget-fair reporting, uncertainty tests, parser audit, and length-control ablations. |
| 8 | M0 progressive-disclosure main-agent baseline | No, historical/core only | PARTLY DONE | M0 exists for older 67-prompt/67-skill core; not rerun on the active 201-prompt / 2433-skill condition. |
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
- 201 controlled prompts.
- 2433 skills.

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

- Field audit: PASS, 201/201 prompts.
- Pair audit: PASS, 641/641 gold/alternative pairs differ on at least two primary axes.
- Prompt-specific alignment: PASS with caveat, 182/201 prompts under MiniLM.
- Gold top-1 among listed candidates: 183/201 prompts.

Current reports:

- `skill_benchmark/outputs/procedural_distinctness_report.md`
- `skill_benchmark/outputs/procedural_requirement_alignment_report.md`

Remaining:

- No immediate benchmark fix required.
- Treat the 19 weak alignment prompts as audit targets before final result tables, especially implicit-field stress and the few public-style browser/security/routing cases.
- Later thesis writing should explain that Step 2 has two layers:
  - schema/field difference
  - prompt-specific procedural justification
- Supervisor-feedback action: include gold-label construction and prompt-specific rationales in the methodology chapter, not only in scripts.

## Step 3: Semantic Confusability

Purpose:

Check that alternatives are plausible semantic neighbours, not random distractors.

Done:

- Ran semantic confusability with local MiniLM embedding backend.
- Checked gold/alternative similarity and prompt/alternative similarity.

Current result:

- PASS.
- 180/201 prompts, or 89.6%, have at least two plausible alternatives under MiniLM.
- The new public-style controlled stratum passes 64/64 prompts.
- Remaining weak Step 3 cases are mostly older clusters, not the new expansion.

Current report:

- `skill_benchmark/outputs/semantic_confusability_report.md`

Caveat:

- Some weak Step 3 cases are not necessarily bad. They are high-precision tasks where the gold skill is naturally clearer than the alternatives.
- Do not over-fix this unless final selector results become too easy or these cases dominate failure analysis.
- MiniLM semantic-confusability checks are construction evidence, not a final modern semantic authority. Final writing should describe semantic confusability as controlled near-neighbour design plus local embedding validation.

Remaining:

- Optional: revise only if a weak Step 3 case becomes a serious method-comparison problem.
- Do not use TF-IDF fallback as final semantic authority.

## Step 4: Gold-Label Stability And Prompt Leakage

Purpose:

Check that prompts do not leak the answer and that gold labels remain defensible under scale.

Done:

- Ran prompt leakage check.
- Manually reviewed earlier non-core semantic/procedural winners; targeted second-pass review remains recommended after the 201/2433 public-style expansion.
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
- Public-gold strict labels have been cleaned into an 82-prompt stratum with acceptable alternatives. The residual hard cases were prompt-tightened and should be reported as public-label caveats rather than silently optimized away.

Remaining:

- Recommended before final result tables: do a targeted second-pass review of acceptable alternatives, non-core winners, strongest-method failures, and the three public-gold requirement-alignment residuals.

## Step 4b: Manual Cluster Design Audit Before Expansion

Purpose:

Check whether each cluster is a defensible semantic-confusion unit before adding more prompts or using it as thesis evidence.

Required audit fields:

- cluster ID or source family
- user-intent family
- gold skill type
- skills in the cluster
- typical prompt pattern
- main source of semantic confusion
- procedural differentiating axes
- gold rationale
- alternative rejection rationale
- realism evidence
- ambiguity risk
- scale risk
- expansion decision

Status:

- FIRST PASS COMPLETE.
- Audit artifact: `skill_benchmark/outputs/cluster_design_audit.md`.
- This remains a required gate before any further controlled or public-gold expansion; new clusters should be added to the audit before prompt generation.

Pass condition:

- 100% of clusters selected for expansion have a filled audit row.
- At least 80% of expanded clusters are low ambiguity risk.
- Medium ambiguity clusters have acceptable alternatives or prompt rewrite plans.
- High ambiguity clusters are excluded from strict headline scoring until revised.
- Each expanded cluster identifies at least two plausible distractors and the procedural fields that make the gold skill better.

Why it matters:

- More prompts only help if the cluster is already valid.
- The audit prevents us from creating a larger benchmark that merely repeats easy distinctions or encodes our claims too directly.
- The audit also gives thesis-ready evidence for why the gold labels are defensible.

Current audit conclusions:

- Highest-priority expansion clusters: implicit-field stress, PDF/document operations, browser/deployment QA, Hugging Face workflows, skill representation analysis, API/tooling, GitHub/CI, and public-authored workflow clusters.
- Freeze or revise before expansion: reply messaging, planning meetings, news monitoring, office business automation, and skill lifecycle.
- Main caveat: platform-name cues and negative boundary phrases are useful but should not dominate final claims about procedural representation.

## Step 5: Build Or Refresh Scale Regimes

Purpose:

Make sure the benchmark actually tests scalable skill libraries rather than a small controlled toy set.

Done:

- Expanded background-scale skills to 1800.
- Imported 460 public skills.
- Added 18 controlled-core v2 skills/prompts.
- Added 10 implicit-field stress prompts and additional controlled clusters in the earlier checkpoint, bringing that checkpoint to 137 prompts.
- Added 32 public-style controlled skills and 64 prompts, bringing the active controlled prompt count to 201.
- Exported R1-R4 representations.

Current result:

- PASS.
- Active local scale condition is 2433 skills and 201 controlled/evaluated prompts.
- R1 flat metadata token count needs refresh after the public-style controlled expansion.
- Historical 2401-skill R1 flat metadata was about 123k visible tokens; full `SKILL.md` exposure was about 1.07M visible tokens.

Current reports:

- `thesis_notes/Scale Expansion 2089 Validation.md`
- `thesis_notes/Context Scale Audit.md`
- `skill_benchmark/outputs/representation_coverage.md`

Remaining:

- Do not blindly expand further until the 201-prompt local selector results are rerun and weak alignment cases are audited.
- Public-skill field audit is still useful, but that is now methodology/literature support rather than benchmark expansion.
- The supervisor-feedback response requires the construction process to be written clearly: skill unit, clusters, gold labels, alternatives, field axes, and validation gates.

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
- DeepSeek model-assisted verification checkpoint completed for all 460 imported public skills.
- Agreement report exists at `skill_benchmark/outputs/public_skill_field_agreement_report.md`.
- Checkpoint note exists at `thesis_notes/Public Skill Model Verification Checkpoint - 20 Skills.md`.
- Full checkpoint note exists at `thesis_notes/Public Skill Model Verification Checkpoint - 460 Skills.md`.
- Targeted disagreement review packet exists at `skill_benchmark/outputs/public_skill_field_disagreement_review_packet.md`.
- Pattern-level adjudication note exists at `thesis_notes/Public Skill Disagreement Adjudication - Step 6.md`.
- Current expanded checkpoint: 460/460 imported public skills audited heuristically and with model assistance. Output files:
  - `skill_benchmark/outputs/public_skill_field_audit.jsonl`
  - `skill_benchmark/outputs/public_skill_field_audit_summary.json`
  - `skill_benchmark/outputs/public_skill_field_audit.md`
  - `skill_benchmark/outputs/public_skill_field_model_audit.jsonl`
  - `skill_benchmark/outputs/public_skill_field_agreement_report.md`
  - `skill_benchmark/outputs/public_skill_field_disagreement_review_packet.md`
  - `skill_benchmark/outputs/public_skill_field_manual_review_packet.md`

Remaining:

- Freeze the field taxonomy into observed / extractable / proposed categories before final reporting.
- Avoid rerunning the 460-skill checkpoint unless the schema, prompt, model, or field definitions change.
- Use the completed subagent pilot review to calibrate heuristic/model disagreement cases.
- If a stricter appendix is required, manually label the 80 selected rows in the disagreement packet.
- If field definitions change materially, refine the detector and rerun the full 460-skill checkpoint.
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

## Step 6b: Public-Skill Gold Validation

Purpose:

Turn selected imported public skills into evaluated gold-label retrieval cases. This is a stricter step than the public field audit. The field audit says our proposed information types appear or are extractable in public skill artifacts. Public-gold validation asks whether a public skill can be the correct answer to a realistic retrieval prompt while competing against semantically similar alternatives.

Status:

- CLEANED STRATUM BUILT.
- Public-gold has been expanded from 32 to 82 prompts.
- The combined evaluated prompt pool is now 219 prompts: 137 controlled prompts plus 82 public-gold prompts.
- Acceptable alternatives are now generated into `skill_benchmark/annotations/public_gold_acceptable_alternatives.json`.
- Public-gold should still be reported as a separate external-validity stratum, not merged blindly into the controlled benchmark.
- Public skills remain valid as background scale, distractors, and field-taxonomy evidence.

Planned construction:

- Cleaned subset contains 82 public-gold prompts.
- Covers public-source clusters including Office/PDF automation, browser QA, web quality, GitHub/CI, deployment, API/tooling, Hugging Face, Notion/Figma/Obsidian, finance/business automation, commerce, and support workflows.
- Uses imported public skills as gold labels in a separate prompt stratum.
- Broad/hierarchical cases still need manual adjudication before final use.
- For each prompt, record:
  - public `gold_skill`
  - natural user request with no skill-name or source leakage
  - 2-4 semantically plausible alternatives
  - gold rationale and rejection rationale for each alternative
  - field axes responsible for the distinction
  - acceptable alternatives, if any

Validation rubric:

- Step 1: PASS, 82/82 prompt references resolve, 0 missing references.
- Step 2 procedural distinctness: PASS, 82/82 prompts; 315/315 pairs have at least one primary procedural differentiator; 288/315 pairs have two or more primary differentiators.
- Step 2 prompt-specific alignment: PASS with residual hard cases, 79/82 prompts; gold top-1 among listed candidates for 79/82.
- Step 3 semantic confusability: PASS, 78/82 prompts have at least two plausible listed alternatives under MiniLM; remaining weak prompts are retained as high-specificity public hard cases.
- Step 4 leakage: PASS, 0 critical and 0 high-risk prompt leaks.
- Retrieval result: DONE for local selectors on the cleaned 82-prompt stratum.

Manual adjudication report:

- `thesis_notes/Public Gold Manual Adjudication - 2026-06-01.md`
- `skill_benchmark/outputs/public_gold_step1_integrity.md`
- `skill_benchmark/outputs/public_gold_step2_procedural_distinctness.md`
- `skill_benchmark/outputs/public_gold_step2_requirement_alignment.md`
- `skill_benchmark/outputs/public_gold_step3_semantic_confusability.md`
- `skill_benchmark/outputs/public_gold_step4_prompt_leakage.md`
- `skill_benchmark/outputs/public_gold_offline_selector_evaluation.md`

Manual interpretation:

- Public-gold is now usable as a separate external-validity stratum.
- The remaining weak requirement-alignment cases are useful hard cases rather than immediate rewrite targets: Figma library generation, Hugging Face local-model selection, and Shopify-specific automation.
- Several public skills are genuine near-equivalents; these are recorded as acceptable alternatives instead of treated as wrong labels.
- The public-gold stratum should test external validity and public-skill messiness, while the controlled clusters remain the cleaner source for causal claims about field usefulness.

Current local public-gold selector result:

- M1 BM25 flat: 51.2% strict top-1, 67.1% accept top-1, 86.6% top-5, 92.7% accept top-5.
- M1 TF-IDF flat: 50.0% strict top-1, 63.4% accept top-1, 86.6% top-5, 91.5% accept top-5.
- M2a MiniLM description: 48.8% strict top-1, 59.8% accept top-1, 81.7% top-5, 87.8% accept top-5.
- M2b MiniLM full skill: 35.4% strict top-1, 47.6% accept top-1, 64.6% top-5, 72.0% accept top-5.
- M3 TF-IDF schema: 40.2% strict top-1, 51.2% accept top-1, 79.3% top-5, 89.0% accept top-5.
- M6 BM25 -> schema rerank: 35.4% strict top-1, 57.3% accept top-1, 85.4% top-5, 92.7% accept top-5.
- M6 TF-IDF -> schema rerank: 36.6% strict top-1, 52.4% accept top-1, 81.7% top-5, 89.0% accept top-5.
- M6 MiniLM full -> schema rerank: 32.9% strict top-1, 51.2% accept top-1, 74.4% top-5, 85.4% accept top-5.
- The `core` scale is not meaningful for public-gold because public target skills are absent from the controlled-core candidate pool; use `current_full`.

Cleaned 82-case Qwen/SkillRouter public-gold selector result:

- Qwen R1 flat-card embedding: 62.2% strict top-1, 84.2% top-5.
- Qwen R1 + Qwen rerank top-20: 74.4% strict top-1, 96.3% top-5.
- Qwen R2 structured-card embedding: 59.8% strict top-1, 82.9% top-5.
- Qwen R2 + Qwen rerank top-20: 76.8% strict top-1, 90.2% accept top-1, 100.0% top-5.
- Qwen full-skill embedding: 31.7% strict top-1, 58.5% top-5.
- Qwen full-skill + Qwen rerank top-20: 68.3% strict top-1, 80.5% top-5.
- SkillRouter full-skill embedding: 68.3% strict top-1, 95.1% top-5.
- SkillRouter full-skill + SkillRouter rerank top-20: 64.6% strict top-1, 92.7% top-5.
- Best current public-gold method: Qwen R2 + Qwen rerank top-20.

Interpretation:

- Public-gold behaves differently from controlled-authored clusters.
- Naive extracted-schema methods currently underperform flat/description retrieval on public-authored skills, suggesting extraction noise, wrapper breadth, and field-matching weakness are real external-validity issues.
- BM25 is retained as a lexical control baseline, not as the thesis architecture. If BM25 is competitive, that is diagnostic evidence about lexical cues and wrapper text, not a reason to center the thesis on BM25.
- Qwen provider results show the same caution from a modern angle: long full-skill embedding is noisy for public artifacts, but neural reranking can recover better top-1 behavior.
- SkillRouter results show that domain-specific skill embeddings are strong first-stage retrievers, but the released SkillRouter reranker did not improve public-gold top-1 in this run.
- This is useful evidence, but it requires failure-mode review before thesis claims.

Current reports:

- `thesis_notes/Public Skill Gold Validation Checkpoint - 2026-05-30.md`
- `skill_benchmark/prompts_public_gold/public_gold_validation_confusability.json`
- `skill_benchmark/outputs/public_gold_validation_draft.md`
- `skill_benchmark/outputs/public_gold_step1_integrity.md`
- `skill_benchmark/outputs/public_gold_step2_procedural_distinctness.md`
- `skill_benchmark/outputs/public_gold_step2_requirement_alignment.md`
- `skill_benchmark/outputs/public_gold_step3_semantic_confusability.md`
- `skill_benchmark/outputs/public_gold_step4_prompt_leakage.md`
- `skill_benchmark/outputs/public_gold_offline_selector_evaluation.md`

Failure labels to record:

- public skill too broad or hierarchical
- prompt tests behavior not clearly present in the public skill
- extraction failed to recover implicit fields
- first-stage retriever excluded gold
- reranker chose a semantically plausible but procedurally wrong alternative
- alternative is genuinely acceptable or better than gold
- prompt or skill title leaked the answer

Reporting rule:

Report public-gold prompts separately from controlled-authored prompts. The final thesis should distinguish:

- controlled-authored benchmark results
- public-gold externally authored results
- combined full-scale results

This prevents the thesis from overclaiming that public skills are already cleanly structured while still testing whether the proposed representation layer generalizes beyond our generated clusters.

## Step 7: Offline Selectors, Rerankers, Field Ablations, And Scale Sensitivity

Purpose:

Compare representation/retrieval methods using the benchmark before involving expensive main-agent downstream tasks.

Current 2026-06-06 correction:

Step 7 is not complete as a final crossed experiment. It is complete as an initial selector/reranker comparison, but the final thesis design must treat representation layer and retriever/reranker architecture as two crossed factors. The current evidence is strongest for full-skill artifact retrieval and reranking. The missing cells are:

- SkillRouter embedding and SkillRouter reranking on R1 flat metadata for controlled 201 / 2433 and public-gold 82 / 2433.
- SkillRouter embedding and SkillRouter reranking on R2 structured procedural cards for controlled 201 / 2433 and public-gold 82 / 2433.
- Qwen R1, R2, and full-skill reruns on the active controlled 201 / 2433 condition.
- Per-source-family public-gold failure analysis, because public-gold currently has one broad `public_gold_validation` family but many `source_family` clusters.

Until these are run or explicitly scoped out, do not claim that Qwen, SkillRouter, R1, R2, or full-skill representation is globally superior. The safe claim is that current results show interactions between representation layer and retrieval architecture.

Done on the active 2433/201 benchmark:

- M1 BM25 flat.
- M1 TF-IDF flat.
- M3 TF-IDF schema retrieval.
- M6 BM25 plus schema rerank.
- M6 TF-IDF plus schema rerank.
- M6-v1-local field-aware reranking with BM25 and TF-IDF first stages.

Done on the pre-public-style 2401/137 benchmark:

- Non-core semantic competition.
- Non-core procedural competition.
- Field ablations.
- Qwen full-skill embedding and reranking variants.
- M6-v1-local field-aware reranking with Qwen and SkillRouter first stages.
- SkillRouter full-skill embedding and SkillRouter reranking hosted on Hugging Face Jobs.

Historical 2089 benchmark methods, not rerun after later scale expansions:

- M2a MiniLM description embedding.
- M2b MiniLM full-skill embedding.
- M6 MiniLM full-skill plus schema rerank.

Current 2433/201 local lexical/schema results:

| Method | Full Top-1 | Full Top-5 | MRR | Full Non-Core Top-1 |
|---|---:|---:|---:|---:|
| M1 BM25 flat | 61.7% | 88.1% | 0.727 | 9.0% |
| M1 TF-IDF flat | 55.2% | 86.1% | 0.689 | 15.4% |
| M3 TF-IDF schema | 65.2% | 94.0% | 0.778 | 8.0% |
| M6 BM25 -> schema rerank | 65.7% | 93.5% | 0.781 | 3.0% |
| M6 TF-IDF -> schema rerank | 65.7% | 91.5% | 0.773 | 3.5% |
| M6-v1 TF-IDF field-aware | 72.6% | 94.0-94.5% | 0.822-0.824 | 3.5% |
| M6-v1 BM25 field-aware | 72.1% | 95.0% | 0.825 | 3.5% |

Current reports:

- `skill_benchmark/outputs/offline_selector_evaluation.md`
- `skill_benchmark/outputs/offline_selector_evaluation_2349_lexical.md`
- `skill_benchmark/outputs/offline_selector_evaluation_2401_expanded_extraction.md`
- `skill_benchmark/outputs/offline_selector_evaluation_2433_201_local.md`
- `skill_benchmark/outputs/m6v1_tfidf_flat_field_aware_2433_201.md`
- `skill_benchmark/outputs/m6v1_bm25_flat_field_aware_2433_201.md`
- `skill_benchmark/outputs/non_core_semantic_competition_embedding_report.md`
- `skill_benchmark/outputs/all_non_core_procedural_competition_embedding_report.md`
- `skill_benchmark/outputs/field_ablation_results.md`
- `thesis_notes/Field Ablation Results - 2089 Scale.md`
- `thesis_notes/Public Expansion 2349 Validation Checkpoint.md`

Done on updated 2349 benchmark for provider baselines:

- Qwen `text-embedding-v4` R1 flat-card embedding-only retrieval.
- Qwen R1 flat-card embedding plus Qwen `qwen3-rerank` over top-20.
- Qwen R1 flat-card embedding plus local schema reranking over top-100.
- Qwen `text-embedding-v4` R2 structured-card embedding-only retrieval.
- Qwen R2 structured-card embedding plus Qwen `qwen3-rerank` over top-20.
- Qwen R2 structured-card embedding plus local schema reranking over top-100.
- Qwen `text-embedding-v4` full-skill embedding-only retrieval.
- Qwen full-skill embedding plus Qwen `qwen3-rerank` over top-20.
- Qwen full-skill embedding plus local schema reranking over top-50.
- Qwen full-skill embedding plus local schema reranking over top-100.

Current 2349 provider results:

| Method | Candidate Budget | Top-1 | Top-5 | MRR | Public Top-1 | Non-Core Top-1 |
|---|---:|---:|---:|---:|---:|---:|
| Qwen R1 embedding only | none | 35.3% | 48.2% | 0.426 | 14.1% | 50.6% |
| Qwen R1 + Qwen rerank | 20 | 60.0% | 63.5% | 0.615 | 16.5% | 36.5% |
| Qwen R1 + local schema rerank | 100 | 69.4% | 74.1% | 0.719 | 1.2% | 21.2% |
| Qwen R2 embedding only | none | 50.6% | 64.7% | 0.571 | 9.4% | 36.5% |
| Qwen R2 + Qwen rerank | 20 | 65.9% | 70.6% | 0.682 | 9.4% | 27.1% |
| Qwen R2 + local schema rerank | 100 | 80.0% | 84.7% | 0.820 | 4.7% | 14.1% |
| Qwen full-skill embedding only | none | 50.6% | 69.4% | 0.590 | 1.2% | 30.6% |
| Qwen full-skill + Qwen rerank | 20 | 61.2% | 68.2% | 0.648 | 3.5% | 34.1% |
| Qwen full-skill + local schema rerank | 50 | 80.0% | 84.7% | 0.822 | 2.4% | 12.9% |
| Qwen full-skill + local schema rerank | 100 | 84.7% | 89.4% | 0.872 | 1.2% | 9.4% |

Done but still historical 1006-scale only:

- Qwen R1 flat-card embedding and reranking variants.
- Qwen R2 structured-card embedding and reranking variants.
- Earlier Qwen candidate-budget ablations over the 1006-skill condition.
- Low-information stress test.
- Failure-mode analysis for Qwen full-skill plus local schema top-100.

Caveat:

- Qwen R1/R2/full-skill main variants are current on 2349.
- Historical 1006- and 2089-scale Qwen runs remain useful for scale comparison, but should not be mixed with the current 2349 table unless labelled.
- MiniLM is a local construction/evaluation baseline, not the final "strong modern embedding" claim, and was not rerun on 2349 because `sentence_transformers` is unavailable in the current shell.

Field ablation result:

- Description-only full-scale TF-IDF top-1: 60.0%.
- Description + use conditions full-scale TF-IDF top-1: 74.1%.
- + output artifacts full-scale TF-IDF top-1: 82.3%.
- + workflow/procedure full-scale TF-IDF top-1: 84.7%, with stronger top-5/MRR.
- Full-scale BM25 peaks at 89.4% top-1 with description + use + preconditions + outputs + workflow.
- Naive `not_for` concatenation reduces top-1 because negative boundaries are treated as positive lexical evidence.
- Naive dependency/resource concatenation adds token cost and noise; it is better treated as field-aware reranker/downstream feasibility evidence.

Current method interpretation:

- The old local schema reranker is now `M6-v0`: a transparent deterministic diagnostic using weighted lexical overlap over extracted fields.
- `M6-v0` should not be presented as the final structure-aware method because it does not parse request-side fields, uses lexical overlap rather than field-to-field matching, and can be distorted by dependency/resource text.
- The next proposed method is `M6-v1`: dense candidate generation plus field-aware procedural reranking over extracted request fields and extracted skill fields.
- Detailed method cleanup is recorded in `thesis_notes/Final Method Set and Information-Use Plan.md`.

Remaining:

- MiniLM can be rerun only if the local dependency is restored; otherwise use Qwen/SkillRouter as the modern dense retrieval conditions.
- Audit M6-v1-local request-field extraction; current implementation is lexical and cue-based.
- Run length-control, shuffled-field, or field-dropout ablations before strong field-causality claims.
- Add statistical uncertainty and paired tests for final tables.
- Run final failure-mode comparison across selected methods.
- Run public-gold failure-mode analysis on the cleaned 82-prompt stratum, especially where M6-v1-local loses to Qwen/SkillRouter baselines.
- Decide final candidate budget, probably top-20 for budget-fair reranker comparison and top-50/top-100 as larger-budget trade-off conditions.
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

- M0 has not been rerun on the updated 137-prompt controlled benchmark.
- M0 has not been run on the 2401-skill scale condition.
- Full 2401 M0 may be mainly a context/cost stress test, because compact metadata is about 123k visible tokens and full skill docs exceed 1M tokens.

Remaining:

- Recommended minimum: rerun or simulate M0 on a representative controlled subset with context-token instrumentation.
- Optional: estimate or simulate 2401-scale M0 context cost rather than running expensive full-agent trials.

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

Current on 2401:

- Steps 1, 2, 3, 4 leakage, 5.
- Step 6 public-skill heuristic/model audit and pattern-level disagreement adjudication.
- Step 6b public-skill gold validation is built as a separate 82-prompt cleaned stratum and passes automated construction gates with residual public-hard-case caveats.
- Step 7 local offline selectors.
- Step 7 non-core semantic/procedural competition.
- Step 7 field ablation.
- Manual adjudication of current flagged non-core winners.
- Qwen full-skill provider conditions.
- SkillRouter hosted embedding/reranking conditions.
- M6-v1-local field-aware reranking over Qwen and SkillRouter candidate sets.
- Public-gold provider/SkillRouter reruns on the cleaned 82-prompt stratum.

Not current on 2401:

- MiniLM local selector conditions.
- M0 progressive-disclosure agent baseline.
- Step 9 downstream validation.
- Statistical uncertainty / paired tests.
- Length-control or field-dropout ablations.
- Request-parser manual audit.
- Public-gold failure-mode analysis on the cleaned 82-prompt stratum.

## Recommended Next Order

1. Run public-gold failure-mode analysis, especially where M6-v1-local underperforms Qwen/SkillRouter baselines.
2. Audit M6-v1-local request-field extraction on a manually labelled prompt sample.
3. Decide whether to implement M6-v2 semantic field matching, because lexical M6-v1-local is not competitive on public-gold.
4. Add statistical uncertainty and paired tests for final controlled comparisons.
5. Run length-control or field-dropout ablations.
6. Freeze the representation-field taxonomy as observed, extractable, or proposed normalization.
7. Add supervisor-feedback writing artifacts: empirical literature table, benchmark-construction pipeline, method-configuration table.
8. Choose the final method set and candidate budget.
9. Measure top-20/top-50/top-100 latency and cost for the final hybrid method.
10. Decide whether full 2401-skill M0 is useful as a context/cost stress test.
11. Run Step 9 downstream validation on a small sample.
12. Move results into thesis chapters.
