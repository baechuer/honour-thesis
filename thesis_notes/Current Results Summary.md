# Current Results Summary

Date: 2026-06-06

This file consolidates the benchmark and retrieval results completed so far.

Methodology hardening update, 2026-06-05:

- Treat `M6-v1-local` as a lexical field-aware prototype, not a finished semantic field matcher.
- Compare rerankers at equal candidate budgets. The fair SkillRouter comparison is top-20 versus top-20; the M6-v1 top-100 result is a larger-budget condition.
- Report strict-gold and gold-or-acceptable metrics separately.
- Do not use `non-main top-1` as a headline metric for public-gold, because public-gold targets are themselves public/background skills.
- Add confidence intervals or paired tests before final headline claims.
- See `thesis_notes/Methodology Deep Critique and Improvement Plan - 2026-06-05.md`.

Supervisor feedback update, 2026-06-05:

- Assignment 3 feedback requested more concrete empirical details from reviewed papers, clearer benchmark construction, and a more specific experimental setup covering gold labels, model settings, prompts, and statistical comparison.
- This is now tracked in `thesis_notes/Supervisor Feedback Response Plan - A3 to Current Thesis.md`.
- Current status against that feedback:
  - empirical literature details: partial, needs a thesis-ready table;
  - benchmark construction: partial, needs a clear pipeline in the benchmark chapter;
  - gold labels: partial, controlled golds exist and public-gold cleanup plus provider reruns are done, but final statistical reporting remains;
  - model settings: partial, provider notes exist but final method table needs standardized settings;
  - prompts: partial, files exist but thesis needs clearer prompt strata and examples;
  - statistical comparison: not done.

## Active Scale Update

The active validation condition is now the 2433-skill public-expanded library with a new public-style controlled stratum. The 2401/137 provider results remain important historical comparisons, but the active controlled benchmark is now 201 prompts over 2433 skills.

Current library:

- 2433 total skills.
- 169 controlled/evaluated skills.
- 82 cleaned public-gold prompts as a separate external-validity stratum.
- 283 total evaluated prompts across controlled + public-gold strata if combined.
- 1800 generated background-scale skills.
- 460 public imported background skills.
- 4 support/email skills.
- 201 controlled/evaluated prompts, including 10 implicit-field stress prompts and 64 public-style controlled prompts.

Current validation:

| Step | Status | Result |
|---|---|---|
| Step 1 integrity | Done | PASS: 201 prompts and 2433 skills resolve. |
| Step 2 procedural alignment | Done with audit targets | PASS field audit: 201/201 prompts and 641/641 pairs; PASS prompt-specific alignment: 182/201 prompts under MiniLM. |
| Step 3 semantic confusability | Done | MiniLM: PASS, 180/201 prompts at 89.6%; public-style controlled passes 64/64. |
| Step 4 prompt leakage | Done | PASS: 0 critical exact-name leaks; 0 high-risk leaks. |
| Step 5 scale regime | Done | PASS: 2433-skill public-expanded library constructed. |
| Step 6 public-skill field audit | Mostly done | 460/460 imported public skills audited heuristically and with DeepSeek model-assisted verification; 80-case disagreement packet generated for manual taxonomy review. |
| Step 6b public-skill gold validation | Cleaned separate stratum | 82 public-gold prompts; integrity PASS, procedural distinctness 82/82, requirement alignment PASS at 79/82, semantic confusability PASS at 78/82, leakage PASS. |
| Step 7 local selectors | Current local rerun done | PASS: lexical/schema and M6-v1 local rerun on 2433/201; provider runs still need rerun on 2433/201. |
| Step 7 Qwen provider selectors | Historical for 2401/137 and current public-gold | Qwen full-skill embedding and reranking have not yet been rerun on the 2433/201 controlled benchmark. |
| Step 7 field ablation | Done | Local BM25/TF-IDF ablations show use conditions, outputs, and workflow/procedure drive most retrieval gains; naive not-for/dependency concatenation can hurt. |
| Step 7 M6-v1 field-aware reranker | First prototype done | `M6-v1-local` parses request-side fields and reranks fixed candidate sets by field-to-field matching. Controlled results support task/output/workflow as strong fields; public-gold remains weak and needs semantic field matching. |
| Step 7 non-core competition | Needs adjudication | 33/85 semantic non-core-over-gold cases; 16/85 procedural non-core-over-gold cases. |

Current 2433/201 local lexical/schema selector results:

| Method | Full Top-1 | Full Top-5 | MRR | Full Non-Core Top-1 |
|---|---:|---:|---:|---:|
| M1 BM25 flat | 61.7% | 88.1% | 0.727 | 9.0% |
| M1 TF-IDF flat | 55.2% | 86.1% | 0.689 | 15.4% |
| M3 TF-IDF schema | 65.2% | 94.0% | 0.778 | 8.0% |
| M6 BM25 -> schema rerank | 65.7% | 93.5% | 0.781 | 3.0% |
| M6 TF-IDF -> schema rerank | 65.7% | 91.5% | 0.773 | 3.5% |

Current interpretation:

- The expanded benchmark now creates real scale and confusability pressure: flat metadata top-1 falls to 55-62%, and structure-aware local methods are not near-perfect.
- Description-only and flat retrieval remain fragile under scale; dense/MiniLM evidence is retained from the 2089 checkpoint.
- Schema-aware and hybrid methods degrade less on the controlled benchmark and produce fewer non-core top-1 false positives.
- The current local schema reranker should be treated as `M6-v0`: a diagnostic weighted-overlap method over extracted fields, not the final proposed structure-aware method.
- The next final method should be `M6-v1`: dense candidate generation followed by a field-aware procedural reranker that parses request requirements and compares them to extracted skill fields.
- Tree routing (`M4`) and graph retrieval (`M5`) remain planned structure-aware architectures. They should be added only if they answer a specific question: tree routing tests scale/branch exclusion, while graph retrieval tests whether explicit relations among inputs, outputs, tools, workflows, resources, and families help beyond serialized structured cards.
- The main next validation step is targeted second-pass adjudication of non-core winners and strongest-method failures, especially in `documents_files`, `skill_lifecycle`, `deployment_browser_qa`, and `api_backend_design`.
- The 2433/201 local rerun preserves the main result: task/use, output, and workflow fields help, while naive use of all fields can add noise.

Method cleanup note:

- `thesis_notes/Final Method Set and Information-Use Plan.md`

Manual public-gold adjudication note:

- `thesis_notes/Public Gold Manual Adjudication - 2026-06-01.md`

Current 2089-scale MiniLM/local selector results, retained for comparison:

| Method | Core Top-1 | Full Top-1 | Full Top-5 | Full Non-Core Top-1 |
|---|---:|---:|---:|---:|
| M2a MiniLM description | 67.1% | 49.4% | 77.6% | 31.8% |
| M2b MiniLM full skill | 71.8% | 64.7% | 83.5% | 15.3% |
| M6 MiniLM full -> schema rerank | 90.6% | 82.3% | 89.4% | 5.9% |

Historical 2401/137 Qwen provider results, not yet rerun on 2433/201:

| Method | Candidate Budget | Top-1 | Top-5 | MRR | Public Top-1 | Non-Core Top-1 |
|---|---:|---:|---:|---:|---:|---:|
| Qwen full-skill embedding only | none | 52.5% | 73.7% | 0.617 | n/a | 26.3% |
| Qwen full-skill + Qwen generic rerank | 20 | 62.0% | 75.2% | 0.684 | n/a | 24.8% |
| Qwen full-skill + local schema rerank | 100 | 77.4% | 91.2% | 0.840 | n/a | 8.0% |

Current 2433/201 M6-v1-local field-aware reranker results:

| First stage | Best field set | Top-1 | Top-5 | MRR | Candidate R@100 | Conditional top-1 | Non-Main Top-1 |
|---|---|---:|---:|---:|---:|---:|---:|
| TF-IDF flat | core | 72.6% | 94.0% | 0.824 | 96.0% | 75.6% | 3.5% |
| TF-IDF flat | core + boundary | 72.6% | 94.5% | 0.822 | 96.0% | 75.6% | 3.5% |
| BM25 flat | core + boundary | 72.1% | 95.0% | 0.825 | 97.0% | 74.4% | 3.5% |

Field-set pattern on 2433/201:

- TF-IDF first stage improves from 65.2% with task-only fields to 71.6-72.6% when output/workflow/core fields are added.
- BM25 first stage improves from 63.7% with task-only fields to 72.1% with core + boundary fields.
- All-fields scoring is weaker than the best selective field set, which supports the claim that the representation layer needs field-aware use, not just longer skill text.

Interpretation:

- `M6-v1-local` is a better diagnostic than `M6-v0` because it reports candidate recall and compares request fields to skill fields.
- Qwen generic reranking is a useful neural baseline, but on the controlled benchmark it improves less than the procedural field-aware rerankers.
- The strongest controlled field set is not "all available structure"; it is task/use condition + output + workflow, with input sometimes helping and boundary/dependency/hierarchy needing conditional handling.
- The current M6-v1 matcher is still mostly lexical. It should be treated as the first deterministic field-aware prototype, not the final field-aware architecture.

Current SkillRouter update:

- SkillRouter full-skill embedding is now the strongest first-stage skill-specific retrieval baseline on the controlled benchmark.
- SkillRouter + SkillRouter rerank top-20 reaches 83.2% top-1, 97.8% top-5, and 0.898 MRR.
- SkillRouter + M6-v1-local task/output/workflow top-20 reaches 83.2% top-1, 95.6% top-5, and 0.895 MRR.
- SkillRouter + M6-v1-local task/output/workflow top-100 reaches 86.9% top-1, 98.5% top-5, and 0.927 MRR.
- Interpret this carefully: top-20 is the budget-fair reranker comparison; top-100 is evidence about the value of a larger high-recall candidate pool plus field-aware ordering.

Current implicit-field interpretation:

- The 10 implicit-field cases are now included in the 137-prompt main benchmark.
- Raw implicit skills remain prose-only.
- The representation exporter now performs conservative prose-to-field extraction before building R2/R3.
- This better matches the thesis claim: structure-aware retrieval should include an extraction/normalization layer, not assume all skill authors provide clean headings.

Current Qwen interpretation:

- Qwen flat-card retrieval is highly fragile under public-expanded scale.
- R2 structured cards substantially improve over R1, which supports the claim that representation content matters even with a strong embedding model.
- Qwen's generic reranker improves top-1 but still leaves many non-core/public false positives.
- Qwen full-skill retrieval plus local procedural schema reranking is currently the strongest 2401-scale provider result.
- The strongest method still has 13 strict top-1 failures; several are first-stage candidate-recall failures, so final reporting should separate candidate recall from reranking accuracy.

## Public-Gold Cleaned Stratum

Current status:

- 82 cleaned public-gold prompts now exist as a separate external-validity stratum.
- They should not be blindly merged with the controlled 137-prompt benchmark, because public-gold tests public-wrapper messiness and externally authored skill artifacts.
- Acceptable alternatives are recorded in `skill_benchmark/annotations/public_gold_acceptable_alternatives.json`.
- Total evaluated prompt pool is now 219: 137 controlled plus 82 public-gold.

Validation:

| Gate | Result |
|---|---|
| Step 1 integrity | PASS: 82 prompts, 0 missing references. |
| Step 2 procedural distinctness | PASS: 82/82 prompts; 315/315 pairs with at least one primary differentiator; 288/315 with two or more. |
| Step 2 requirement alignment | PASS with residual hard cases: 79/82 prompts and 79/82 gold top-1 among listed candidates. |
| Step 3 semantic confusability | PASS: 78/82 prompts; 220/315 plausible semantic-neighbour pairs. |
| Step 4 leakage | PASS: 0 critical exact-name leaks; 0 high-risk leaks. |

Interpretation:

- Public-gold is valuable as an external-validity stratum, but controlled clusters remain the cleaner basis for causal field-use claims.
- Remaining weak requirement-alignment cases are Figma library generation, Hugging Face local-model selection, and Shopify-specific automation.
- Remaining weak semantic-confusability cases are setup-pre-commit, git guardrails, document coauthoring, and Zendesk automation; these are retained as high-specificity public hard cases rather than overfit with weak distractors.
- Public-gold results should be reported in strict and gold-or-acceptable forms.
- The `core` scale is not meaningful for public-gold selector evaluation because public target skills are not present in the controlled-core candidate pool; use `current_full`.

Public-gold local selector results after cleanup on `current_full`:

| Method | Top-1 | Top-5 | MRR | Interpretation |
|---|---:|---:|---:|---|
| M1 BM25 flat | 51.2% strict / 67.1% accept | 86.6% strict / 92.7% accept | 0.659 strict / 0.784 accept | Lexical control remains competitive; useful warning about wording cues. |
| M1 TF-IDF flat | 50.0% / 63.4% | 86.6% / 91.5% | 0.649 / 0.751 | Similar flat-card baseline. |
| M2a MiniLM description | 48.8% / 59.8% | 81.7% / 87.8% | 0.626 / 0.718 | Dense description retrieval is comparable to lexical flat cards. |
| M2b MiniLM full skill | 35.4% / 47.6% | 64.6% / 72.0% | 0.494 / 0.604 | Full public artifacts are noisy for small local embeddings. |
| M3 TF-IDF schema | 40.2% / 51.2% | 79.3% / 89.0% | 0.567 / 0.668 | Naive extracted schema is not enough on public-authored skills. |
| M6-v0 local schema rerank | 32.9-36.6% / 51.2-57.3% | 74.4-85.4% / 85.4-92.7% | 0.503-0.558 / 0.653-0.716 | Diagnostic reranker; current scoring is too crude for public-gold. |

Cleaned 82-case public-gold provider results:

| Method | Top-1 | Accept Top-1 | Top-5 | Accept Top-5 | MRR | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| Qwen R1 embedding | 62.2% | 72.0% | 84.2% | 89.0% | 0.720 | Flat public cards are strong on public-authored skills. |
| Qwen R1 + Qwen rerank top-20 | 74.4% | 85.4% | 96.3% | 97.6% | 0.837 | Strong generic reranking recovers many strict public labels. |
| Qwen R2 embedding | 59.8% | 73.2% | 82.9% | 87.8% | 0.714 | Structured cards do not beat R1 by embedding alone on public-gold. |
| Qwen R2 + Qwen rerank top-20 | 76.8% | 90.2% | 100.0% | 100.0% | 0.861 | Best current public-gold provider result. |
| Qwen full-skill embedding | 31.7% | 50.0% | 58.5% | 69.5% | 0.448 | Full public artifacts are noisy for direct embedding. |
| Qwen full-skill + Qwen rerank top-20 | 68.3% | 79.3% | 80.5% | 87.8% | 0.739 | Reranking helps but full-skill first stage is weaker here. |
| SkillRouter full embedding | 68.3% | 79.3% | 95.1% | 97.6% | 0.790 | Strong first-stage domain-specific retrieval. |
| SkillRouter + SkillRouter rerank top-20 | 64.6% | 73.2% | 92.7% | 95.1% | 0.778 | SkillRouter rerank does not improve public-gold top-1 in this run. |

Cleaned 82-case public-gold M6-v1-local results:

| First stage | Field set | Top-1 | Accept Top-1 | Top-5 | Accept Top-5 | MRR | Candidate R@100 |
|---|---|---:|---:|---:|---:|---:|---:|
| Qwen full-skill | task only | 54.9% | 65.8% | 79.3% | n/a | 0.663 | 95.1% |
| Qwen full-skill | task + output + workflow | 47.6% | 67.1% | 80.5% | n/a | 0.609 | 95.1% |
| Qwen full-skill | core | 48.8% | 67.1% | 79.3% | n/a | 0.619 | 95.1% |
| Qwen full-skill | core + boundary | 48.8% | 67.1% | 82.9% | n/a | 0.617 | 95.1% |
| Qwen full-skill | all fields | 43.9% | 63.4% | 81.7% | n/a | 0.604 | 95.1% |
| SkillRouter full-skill | task only | 68.3% | 78.1% | 90.2% | 95.1% | 0.788 | 98.8% |
| SkillRouter full-skill | core | 63.4% | 79.3% | 92.7% | 97.6% | 0.762 | 98.8% |

Public-gold interpretation:

- These results do not prove that extracted fields improve public-skill retrieval.
- They show that a lexical field-aware reranker is insufficient when public skills are broad, implicit, duplicated, wrapper-like, or heavily source/lexical cued.
- Qwen R2 + Qwen rerank is currently the best public-gold method, which means strong semantic reranking is a serious baseline.
- Candidate recall is high for Qwen full-skill and SkillRouter first stages, so many public-gold failures are reranker/field-matching/extraction failures rather than pure first-stage retrieval failures.
- This strengthens the thesis if framed carefully: field information may matter, but the final method must use it through robust semantic field matching rather than simple lexical overlap.

## Public-Skill Field Audit

Current status:

- Scope: 460 imported public `SKILL.md` files.
- Originals used: 460/460.
- Mean words per skill: 1194.02.
- Median words per skill: 1141.
- Manual review packet: 15 sampled skills for the expanded public set.

Field prevalence:

| Field | Explicit | Explicit or Extractable | Provisional Read |
|---|---:|---:|---|
| routing trigger | 100.0% | 100.0% | observed |
| input/precondition | 25.2% | 81.5% | often extractable |
| output artifact | 45.2% | 85.2% | observed/extractable |
| workflow/procedure | 71.7% | 84.4% | observed/extractable |
| constraints/boundaries | 41.3% | 77.6% | partially observed/extractable |
| dependencies/tools | 72.8% | 85.0% | observed |
| resources/references | 66.7% | 82.0% | observed/extractable |
| examples/tests | 63.5% | 93.9% | observed/extractable |
| safety/side effects | 11.3% | 37.0% | proposed or weakly observed |
| portability/environment | 62.2% | 80.7% | observed/extractable |
| hierarchy/links | 25.2% | 31.1% | partially observed |

Interpretation:

- Public skills do contain many of the procedural signals used by the structured representation, especially triggers, workflows, outputs, dependencies, and examples.
- Some signals are often implicit rather than cleanly fielded, which supports the idea of a representation layer that extracts or normalizes them.
- Safety/side-effect information is weak in the sampled public corpus. Treat this as a proposed field or a quality gap, not a mature public-skill convention.
- The current audit is heuristic. The 20-skill manual review packet must be checked before using these numbers as final thesis evidence.
- A model-assisted semantic verification layer has been added and implemented. The DeepSeek checkpoint now covers the full 460-public-skill subset and is recorded in `thesis_notes/Public Skill Model Verification Checkpoint - 460 Skills.md`.
- A 10-skill subagent/manual calibration pilot is complete. It confirms the main pattern but warns that resources, examples/tests, output artifacts, workflow, and dependencies can be overcounted if keyword matching is too loose.
- A targeted disagreement adjudication note is recorded in `thesis_notes/Public Skill Disagreement Adjudication - Step 6.md`. Its main conclusion is that public skills contain recoverable procedural signals, but the representation layer must normalize them rather than assuming clean author-provided schema fields.
- A draft final taxonomy is recorded in `thesis_notes/Final Representation Field Taxonomy - Draft.md`. It separates primary retrieval fields from secondary feasibility, boundary, and downstream fields.
- The public-expanded validation checkpoint is recorded in `thesis_notes/Public Expansion 2349 Validation Checkpoint.md`.

Model-assisted field prevalence on 460 public skills:

| Field | Model-present rate | Interpretation |
|---|---:|---|
| `workflow_procedure` | 90.4% | strongly observed |
| `dependencies_tools` | 89.6% | strongly observed |
| `examples_tests` | 87.6% | strongly observed |
| `routing_trigger` | 85.7% | observed, but broad descriptions need care |
| `output_artifact` | 80.2% | observed/extractable |
| `resources_references` | 77.2% | observed/extractable |
| `constraints_boundaries` | 75.2% | observed but definition-sensitive |
| `portability_environment` | 74.1% | observed/extractable |
| `input_precondition` | 68.3% | often implicit/extractable |
| `hierarchy_links` | 51.7% | partially observed |
| `safety_side_effects` | 29.8% | weakly observed/proposed |

## Benchmark Status

The following section records the earlier 1006-skill v1 state.

Library:

- 1006 total skills.
- 67 controlled core skills.
- 920 generated background-scale skills.
- 15 public imported background skills.
- 4 support/email skills.
- 67 evaluated prompts.

Validation:

| Step | Status | Result |
|---|---|---|
| Step 1 integrity | Done | PASS: 67 prompts and 1006 skills resolve. |
| Step 2 procedural alignment | Done | PASS: 67/67 prompts pass field audit; 65/67 pass stricter prompt-specific alignment. |
| Step 3 semantic confusability | Done | PASS: 61/67 prompts pass local MiniLM semantic-confusability check. |
| Step 4 prompt leakage | Done | PASS: 0 critical exact-name leaks; 0 high-risk leaks. |
| Step 5 scale regime | Done | PASS: 1006-skill library constructed. |
| Step 7 local selectors | Done | PASS: useful spread from 47.8% to 80.6% top-1. |
| Step 7 Qwen provider selectors | Done | PASS: Qwen embedding and reranking tested on R1, full skill, and R2. |
| Low-information stress test | Done separately | Performance drops sharply; confirms schema reranking depends on explicit procedural evidence. |
| Failure mode analysis | Done for current strongest method | 10 failures: 4 first-stage exclusions, 6 reranking/boundary/annotation failures. |
| Step 8 M0 progressive disclosure | Done on core | PASS as baseline trace; not yet full-library stress test. |
| Step 9 downstream task validation | Not done | Plan exists; artifact generation/evaluation still pending. |

## Local Selector Results

Core scale means 67 controlled skills. Full scale means 1006 skills.

| Method | Representation | Core Top-1 | Core Top-5 | Full Top-1 | Full Top-5 | Full MRR | Full Non-Core Top-1 |
|---|---|---:|---:|---:|---:|---:|---:|
| M1 BM25 flat | R1 flat metadata | 67.2% | 94.0% | 64.2% | 86.6% | 0.733 | 16.4% |
| M1 TF-IDF flat | R1 flat metadata | 68.7% | 92.5% | 58.2% | 85.1% | 0.697 | 16.4% |
| M2a MiniLM description | R1 description embedding | 61.2% | 91.0% | 47.8% | 74.6% | 0.603 | 25.4% |
| M2b MiniLM full skill | Full `SKILL.md` embedding | 64.2% | 92.5% | 61.2% | 82.1% | 0.717 | 9.0% |
| M3 TF-IDF schema | R2 structured procedural | 74.6% | 100.0% | 71.6% | 95.5% | 0.808 | 9.0% |
| M6 BM25 -> schema rerank | Flat shortlist + schema rerank | 77.6% | 95.5% | 71.6% | 92.5% | 0.815 | 7.5% |
| M6 TF-IDF -> schema rerank | Flat shortlist + schema rerank | 80.6% | 97.0% | 70.2% | 85.1% | 0.778 | 10.4% |
| M6 MiniLM full -> schema rerank | Full-skill shortlist + schema rerank | 89.6% | 100.0% | 80.6% | 91.0% | 0.856 | 7.5% |

Best local method:

- M6 MiniLM full-skill retrieval plus deterministic schema reranking.
- Full-library top-1: 80.6%.
- Full-library top-5: 91.0%.

## Historical Qwen Provider Results

The following Qwen full-library runs use the historical 1006-skill scale. The active 2089-scale Qwen full-skill results are listed near the top of this file.

| Method | Representation | Top-1 | Accept Top-1 | Top-5 | Accept Top-5 | MRR | Non-Core Top-1 |
|---|---|---:|---:|---:|---:|---:|---:|
| Qwen embedding only | R1 flat card | 35.8% | 35.8% | 56.7% | 59.7% | 0.449 | 43.3% |
| Qwen embedding + rerank | R1 flat card | 64.2% | 67.2% | 67.2% | 70.2% | 0.649 | 31.3% |
| Qwen embedding only | Full `SKILL.md` | 46.3% | 47.8% | 71.6% | 74.6% | 0.574 | 29.8% |
| Qwen embedding + rerank | Full `SKILL.md` | 61.2% | 65.7% | 65.7% | 70.2% | 0.644 | 37.3% |
| Qwen embedding only | R2 structured card | 47.8% | 47.8% | 65.7% | 67.2% | 0.563 | 31.3% |
| Qwen embedding + rerank | R2 structured card | 65.7% | 67.2% | 71.6% | 73.1% | 0.688 | 26.9% |

## Qwen + Local Schema Reranker

This ablation uses Qwen `text-embedding-v4` for first-stage retrieval, then uses our deterministic schema reranker instead of Qwen `qwen3-rerank`.

| Method | Candidate Budget | Top-1 | Top-5 | MRR | Non-Core Top-1 |
|---|---:|---:|---:|---:|---:|
| Qwen R1 + local schema | 20 | 58.2% | 67.2% | 0.622 | 25.4% |
| Qwen full + local schema | 20 | 68.7% | 74.6% | 0.715 | 22.4% |
| Qwen full + local schema | 50 | 80.6% | 88.1% | 0.834 | 11.9% |
| Qwen full + local schema | 100 | 85.1% | 91.0% | 0.878 | 9.0% |
| Qwen R2 + local schema | 20 | 64.2% | 73.1% | 0.687 | 22.4% |
| Qwen R2 + local schema | 50 | 70.2% | 79.1% | 0.746 | 14.9% |
| Qwen R2 + local schema | 100 | 79.1% | 89.5% | 0.838 | 10.4% |

Qwen core smoke test:

- Scale: 67 controlled core skills.
- Prompts: first 5 prompts.
- Method: full `SKILL.md` embedding plus Qwen rerank.
- Result: 100.0% top-1 and 100.0% top-5.

Main Qwen interpretation:

- Qwen reranking improves top-1 over embedding-only for every representation.
- The best Qwen condition is R2 structured card plus rerank at 65.7% top-1.
- Qwen does not solve the full benchmark.
- Qwen's generic reranker underperforms the best local structure-aware M6 result.
- Qwen embeddings combined with the local schema reranker now produce the strongest current result: 85.1% top-1 with full-skill Qwen retrieval and top-100 schema reranking.

## M0 Progressive Disclosure Baseline

M0 is the normal-agent baseline where the main agent sees skill cards and chooses which full skill documents to load.

Current run:

- Scale: 67 controlled core skills.
- Strict top-1: 61.2%.
- Strict any-hit: 64.2%.
- No explicit skill loaded: 31.3%.
- Mean full skill docs loaded: 0.78.

Interpretation:

- M0 is useful as a realistic main-agent behavior baseline.
- It is not a clean retriever-only measure because the agent sometimes answers directly without loading a skill.
- Full 1006-skill M0 has not been run and should be treated as a context/cost stress test rather than a necessary immediate result.

## Step 9 Candidate Readiness

Step 9 downstream artifact generation has not been executed. A 12-prompt readiness check exists. The underlying files still use `step8` in their names from the earlier numbering.

| Method | Top-1 Gold/Accept | Top-5 Gold/Accept |
|---|---:|---:|
| M1 BM25 flat | 75.0% | 91.7% |
| M1 TF-IDF flat | 41.7% | 100.0% |
| M2b MiniLM full skill | 50.0% | 83.3% |
| M3 TF-IDF schema | 66.7% | 91.7% |
| M6 BM25 -> schema rerank | 75.0% | 91.7% |
| M6 TF-IDF -> schema rerank | 50.0% | 91.7% |
| M6 MiniLM full -> schema rerank | 83.3% | 91.7% |

Interpretation:

- Downstream validation is only fair when the correct or acceptable skill is in the candidate set.
- Missing top-5 cases should be treated as retrieval failures before judging generated artifacts.

## Low-Information Stress Test

This separate 12-prompt set uses less explicit user requests. It is not mixed into the main benchmark.

Best strict top-1 results:

- M2b MiniLM full skill: 41.7%.
- M6 MiniLM full -> schema rerank: 33.3%.
- Qwen full + qwen3-rerank: 33.3%.
- Qwen full + local schema rerank, top-100: 25.0%.

Interpretation:

- This is an anti-cheating check.
- The schema reranker does not infer hidden intent from vague prompts.
- It works best when the user request contains enough procedural evidence to match structured fields.
- Very underspecified requests may need a clarification or query-understanding stage before retrieval.

Detailed report: `thesis_notes/Low Information Stress Test.md`.

## What The Results Currently Show

1. Flat metadata is weak under scale.
2. Description-only embedding is especially fragile.
3. Full skill text helps compared with short descriptions, but does not fully solve procedural confusion.
4. Structured procedural information is useful.
5. Reranking helps when the correct skill is already in the candidate set.
6. Stronger provider embeddings/rerankers do not remove the need for good representation.
7. The strongest controlled-benchmark result comes from Qwen broad semantic retrieval plus the current local schema reranker, but that reranker is now treated as `M6-v0` diagnostic rather than the final proposed method.
8. Field ablations show the most retrieval-critical information is use conditions, output artifacts, and workflow/procedure; not-for and dependency/resource fields need field-aware handling because naive text concatenation can add noise.

## Current Critique And Validity Risks

The formal critique/action plan is recorded in `thesis_notes/Critique Response and Validity Improvement Plan.md`.

Main risks:

- Benchmark construction and schema scoring may be co-adapted.
- Some non-core winners may be genuinely acceptable or better than the intended gold skill.
- 85 evaluated prompts supports a controlled honours-scale benchmark, but not broad universal claims.
- Generated background skills create scale pressure but not full real-world messiness.
- MiniLM semantic-confusability checks are useful construction evidence, not final semantic authority.
- The public-skill audit grounds the field taxonomy but is not a full human annotation study.
- Downstream task success is not yet demonstrated.

Planned response:

- Freeze the representation-field taxonomy and method set before further tuning.
- Run targeted second-pass adjudication over non-core winners and strongest-method failures.
- Report public-skill findings as observed/extractable/proposed, not as clean ecosystem-wide schema prevalence.
- Keep the cleaned public-gold validation subset separate from controlled gold skills; use it as external-validity evidence and as a failure-mode source for extraction noise.
- Run small Step 9 downstream validation before claiming agent reliability benefits.

## Public-Gold Validation

Current status:

- Public-gold candidate prompts: 82 cleaned prompts.
- Gold labels: imported public skills.
- Current location: `skill_benchmark/prompts_public_gold/public_gold_validation_confusability.json`.
- Checkpoint outputs: `skill_benchmark/outputs/public_gold_step*.md` and `skill_benchmark/outputs/public_gold_offline_selector_evaluation.md`.

Validation gates:

| Gate | Result |
|---|---:|
| Step 1 integrity | PASS, 82/82 references resolve |
| Step 2 procedural distinctness | PASS, 82/82 prompts |
| Step 2 prompt-specific alignment | PASS, 79/82 prompts |
| Step 3 semantic confusability | PASS, 78/82 prompts |
| Step 4 prompt leakage | PASS, 0 critical, 0 high-risk |

Public-gold local selector read:

| Method | Strict Top-1 | Accept Top-1 | Strict Top-5 | Accept Top-5 | Strict MRR |
|---|---:|---:|---:|---:|---:|
| M1 BM25 flat | 51.2% | 67.1% | 86.6% | 92.7% | 0.659 |
| M1 TF-IDF flat | 50.0% | 63.4% | 86.6% | 91.5% | 0.649 |
| M2a MiniLM description | 48.8% | 59.8% | 81.7% | 87.8% | 0.626 |
| M2b MiniLM full skill | 35.4% | 47.6% | 64.6% | 72.0% | 0.494 |
| M3 TF-IDF schema | 40.2% | 51.2% | 79.3% | 89.0% | 0.567 |
| M6 BM25 -> schema rerank | 35.4% | 57.3% | 85.4% | 92.7% | 0.558 |
| M6 TF-IDF -> schema rerank | 36.6% | 52.4% | 81.7% | 89.0% | 0.556 |
| M6 MiniLM full -> schema rerank | 32.9% | 51.2% | 74.4% | 85.4% | 0.503 |

Historical 32-case public-gold Qwen provider read:

| Method | Top-1 | Top-5 | MRR |
|---|---:|---:|---:|
| Qwen R1 flat-card embedding | 59.4% | 87.5% | 0.716 |
| Qwen R2 structured-card embedding | 59.4% | 87.5% | 0.732 |
| Qwen full-skill embedding | 28.1% | 65.6% | 0.469 |
| Qwen R1 + local schema rerank top-100 | 40.6% | 90.6% | 0.616 |
| Qwen R2 + local schema rerank top-100 | 46.9% | 90.6% | 0.653 |
| Qwen full-skill + local schema rerank top-100 | 25.0% | 78.1% | 0.482 |
| Qwen full-skill + Qwen rerank top-20 | 68.8% | 84.4% | 0.763 |

Interpretation:

- Public-gold cases now satisfy the Step 6b construction rubric as a cleaned 82-case stratum.
- Unlike the controlled benchmark, naive schema extraction underperforms flat/description retrieval on this public-only stratum.
- This supports a more careful thesis claim: structure-aware retrieval depends on the quality of the extraction/normalization layer when skills are authored by others.
- BM25 is kept as a lexical control, not as the thesis method. Its relatively strong result on public-gold cases helps diagnose how much exact wording and public wrapper text still influence the benchmark.
- Provider reruns are now complete on the cleaned 82-case stratum. The strongest current public-gold condition is Qwen R2 + Qwen rerank top-20; M6-v1-local remains weaker, which points to field-matching and extraction limitations rather than a lack of candidate recall.

## Current Strongest-Method Failure Analysis

Target:

- Qwen full `SKILL.md` embedding.
- Top-100 candidate pool.
- Local schema reranker.

Failure split:

- 10 strict top-1 failures out of 67 prompts.
- 4 first-stage exclusions where Qwen did not place the gold skill in top-100.
- 6 reranking, boundary, or annotation failures where the gold was inside the top-100 but did not rank first.

Main failure types:

- first-stage embedding confuses task object with required procedure;
- schema reranker overweights secondary terms;
- negation and `not_for` handling is too weak;
- meta-skill tasks such as editing/evaluating a skill are confused with using the named skill;
- one domain-specific extractor may need acceptable-alternative adjudication.

Detailed report: `thesis_notes/Failure Mode Analysis - Qwen Full Local Schema Top100.md`.

## Not Done Yet

- Provider/SkillRouter reruns on the cleaned 82-prompt public-gold stratum.
- Public-gold failure-mode analysis on the cleaned 82-prompt stratum.
- Targeted second-pass adjudication over non-core winners and strongest-method failures.
- Refinement of `M6-v1` field-aware procedural reranking, especially public-skill extraction/matching and failure analysis.
- Latency/cost comparison for top-20, top-50, and top-100 candidate budgets.
- Hybrid Qwen candidate text experiments, such as R2 first-stage plus full-skill rerank text.
- SkillRouter local smoke test: runner implemented at `skill_benchmark/scripts/run_skillrouter_selectors.py`. Local attempts on 2026-06-05 reached model loading but did not complete a tiny one-prompt CPU/MPS smoke test within a practical window on the 8 GB laptop. Treat local full-scale SkillRouter as currently impractical unless quantized or run on stronger hardware.
- SkillRouter hosted test: completed via Hugging Face Jobs on 2026-06-05 using `t4-small` after uploading a private 5.6 MB benchmark snapshot to `baechuer1/honour-thesis-skillrouter-benchmark-snapshot`. The reranker is not available as a normal Hugging Face Inference Provider model, so this was run as a custom GPU job rather than an ordinary provider API call.
- M4 tree routing.
- M5 graph retrieval.
- Full 1006-skill M0 cost/context stress test.
- Step 9 downstream artifact generation and grading.
- Final thesis results tables and written discussion.

## Current Next Step

Rerun cleaned public-gold provider/SkillRouter conditions and refine `M6-v1` before adding more provider variants.

Specifically:

- classify public-skill fields as observed, extractable, or proposed normalization using the completed heuristic/model disagreement adjudication;
- use the completed field-ablation results to freeze the final representation-field set;
- use the cleaned 82-prompt public-gold stratum for any final public-gold claims;
- refine `M6-v1`, especially request-side extraction, public-skill field normalization, and field-to-field matching;
- run targeted second-pass adjudication on non-core winners and strongest-method failures;
- compare top-20, top-50, and top-100 latency/cost;
- decide whether top-100 is acceptable as a retriever/reranker budget;
- decide whether to add acceptable alternatives for domain-specific near-equivalents;
- then move to Step 9 downstream validation.

## SkillRouter Hosted Results

Run date: 2026-06-05. Hardware: Hugging Face Jobs `t4-small`. Models: `pipizhao/SkillRouter-Embedding-0.6B` and `pipizhao/SkillRouter-Reranker-0.6B`. Representation: full skill artifact. Rerank budget: top-20.

| Prompt set | Method | Top-1 | Accept top-1 | Top-5 | Accept top-5 | MRR | Non-main top-1 |
|---|---|---:|---:|---:|---:|---:|---:|
| Controlled, 137 prompts | SkillRouter full embedding | 73.0% | 75.9% | 94.2% | 94.9% | 0.827 | 14.6% |
| Controlled, 137 prompts | SkillRouter full embedding + SkillRouter rerank top-20 | 83.2% | 83.2% | 97.8% | 98.5% | 0.898 | 4.4% |
| Public-gold, 32 prompts | SkillRouter full embedding | 65.6% | 75.0% | 96.9% | 96.9% | 0.770 | 84.4% |
| Public-gold, 32 prompts | SkillRouter full embedding + SkillRouter rerank top-20 | 65.6% | 68.8% | 93.8% | 96.9% | 0.788 | 87.5% |

Interpretation:

- SkillRouter embedding alone is much stronger than generic Qwen full-skill embedding on the controlled set, which means the benchmark remains meaningful under a skill-specific dense retriever.
- SkillRouter reranking is now the strongest controlled result so far: 83.2% top-1 and 97.8% top-5.
- On public-gold cases, SkillRouter embedding is already strong. The reranker improves MRR slightly but does not improve strict top-1, and it lowers top-5 from 96.9% to 93.8%.
- This suggests that learned skill-routing models can capture substantial procedural signal from full artifacts, but they still do not eliminate all semantic/procedural confusion.
- The proposed field-aware methods should now be interpreted against SkillRouter as a strong domain-specific retrieve-and-rerank baseline.

## SkillRouter + M6-v1 Field-Aware Hybrid

Run date: 2026-06-05. Hardware: Hugging Face Jobs `t4-small`. First stage: `pipizhao/SkillRouter-Embedding-0.6B` over full skill artifacts. Reranker: local deterministic M6-v1 field-aware matcher. Summary artifact: `skill_benchmark/outputs/m6v1_skillrouter_hybrid_summary_2026_06_05.md`.

Best results:

| Prompt set | Candidate budget | Best field set | Top-1 | Top-5 | MRR | Non-main top-1 |
|---|---:|---|---:|---:|---:|---:|
| Controlled, 137 prompts | top-20 | `task_output_workflow` | 83.2% | 95.6% | 0.895 | 5.1% |
| Controlled, 137 prompts | top-100 | `task_output_workflow` | 86.9% | 98.5% | 0.927 | 0.7% |
| Public-gold, 32 prompts | top-20 | `task` / `core_boundary` | 62.5% | 93.8-96.9% | 0.765 / 0.762 | 62.5-68.8% |
| Public-gold, 32 prompts | top-100 | `task` | 62.5% | 93.8% | 0.765 | 68.8% |

Interpretation:

- This is now the strongest controlled result currently recorded.
- SkillRouter embedding gives excellent candidate recall, and explicit `task + output + workflow` field-aware reranking improves final top-1 beyond SkillRouter's own neural reranker on the controlled benchmark.
- The same reranker does not improve public-gold top-1. This is an important limitation: the current deterministic field matcher works well on controlled/extracted procedural fields, but it is not robust enough for messy externally authored skills.
- This strengthens the thesis direction: the contribution should not be "fields always win"; it should be "which procedural information helps, under which representation/extraction conditions, and where learned retrieval still needs interpretable procedural matching."
