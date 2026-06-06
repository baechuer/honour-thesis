# Thesis Experiment Roadmap

Date: 2026-06-03

This file is the operational roadmap for the thesis experiments. It exists to prevent drift.

For the current experiment matrix, including method IDs, representation choices, retriever choices, reranker choices, candidate budgets, and canonical run commands, use `thesis_notes/Experiment Methodology Tracker.md`. This roadmap explains priority and sequencing; the tracker defines what each method means.

The thesis is not a provider leaderboard and not a search for every possible retrieval architecture. The thesis asks:

**RQ1:** What information must agent skill representations preserve to distinguish semantically similar but procedurally distinct skills at scale?

**RQ2:** How do retrieval strategies that use flat text, dense embeddings, structured procedural fields, or hybrid reranking differ in accuracy, efficiency, and failure modes when applied to scalable skill libraries?

All experiments should connect back to these two questions.

## Current Position

We are past benchmark construction, initial selector comparison, public-skill import, the 2401-skill scale expansion, public field auditing, the main Qwen provider refresh, the SkillRouter full-skill hosted run, and the 137-prompt controlled-core expansion. The implicit-field cases are now integrated into the main benchmark, and R2/R3 include a conservative prose-to-field extraction step. The next work should fill the crossed representation-by-architecture matrix, consolidate evidence, review weak cases, and compare heuristic extraction with LLM-assisted extraction rather than keep adding providers.

Important scale clarification:

> The active 2401-skill benchmark now tests both semantic/procedural scale and a near-context-limit condition for compact metadata/progressive-disclosure systems. R1 flat metadata is about 123k selector-visible tokens, while full skill artifacts exceed 1M selector-visible tokens. See `thesis_notes/Controlled Cluster Expansion Checkpoint - 2026-05-30.md`.

Current strongest finding:

> Dense retrieval is useful for broad candidate generation, but final skill selection benefits from extracted procedural information. On the active 2401-skill / 137-prompt benchmark, Qwen full-skill retrieval reaches 52.5% top-1 and Qwen full-skill retrieval plus local schema reranking reaches 77.4% top-1 and 91.2% top-5. This strengthens the claim that procedural reranking matters, but the integrated implicit-field cases show that a practical structure-aware method must extract fields from prose rather than rely only on clean headings.

Important method clarification:

> The current local schema reranker is not the final thesis method. It is `M6-v0`, a transparent diagnostic that uses weighted lexical overlap over extracted fields. The first `M6-v1-local` prototype now exists: it parses user requests into fields and compares them field-to-field against extracted skill fields. Controlled results improve slightly over `M6-v0`, but public-gold still shows that a stronger semantic or LLM-assisted field matcher is needed for messy public skills.

Current information clarification:

> The thesis should use "selection information" rather than only "procedural information". The fixed groups are task/use condition, input/precondition, output/artifact, workflow/procedure, dependency/resource/platform, boundary/not-for, and hierarchy/task role. The current results suggest task/use condition, output, and workflow are the strongest positive fields; dependency, boundary, and hierarchy are conditional signals.

Current main risk:

> The project may drift into testing more providers or architectures without improving the thesis answer about representation information. The next expansion should improve benchmark coverage and failure-mode analysis, not become a provider leaderboard.

Current crossed-design risk:

> Representation-layer effects and retriever/reranker effects are not fully separated yet. Qwen has been run across R1/R2/full representations on public-gold, but SkillRouter has only been run on full skill artifacts. The active controlled 137/2401 result set also lacks current Qwen R1/R2 reruns. Final claims must therefore avoid saying that one model or one representation "wins" until each architecture has been tested against the relevant representation layers.

Current methodology hardening update, 2026-06-05:

> A detailed methods critique found that the main risk is conflation: field usefulness, field extraction quality, lexical cue overlap, candidate budget, and authored-skill cleanliness are not always separated. Future headline comparisons must be budget-fair, strict-gold and acceptable-alternative metrics must be separated, M6-v1-local must be named as a lexical field-aware prototype, public-gold false positives need stratum-aware labels, and final results need uncertainty estimates or paired tests.

Detailed note:

- `thesis_notes/Methodology Deep Critique and Improvement Plan - 2026-06-05.md`

Current validity risk:

> The controlled benchmark exposes clean procedural fields because we authored those skills. Before final claims, we must check whether similar information exists or is extractable from real public skills. If some fields are usually absent, frame them as representation-layer normalization targets rather than assuming skill authors already provide them.

Current public-gold risk:

> Public imported skills currently support field-taxonomy validity and scale pressure. A cleaned 82-case public-gold stratum now exists as a separate external-validity benchmark. It should be reported separately from controlled-authored results because it tests messy public skill artifacts, not only controlled field usefulness. Qwen and SkillRouter full-skill public-gold reruns are complete on the cleaned 82-case stratum, but public-gold still needs per-source-family failure analysis and SkillRouter R1/R2 representation runs.

## Frozen Unless Broken

These should not be changed unless a validation failure is discovered:

- Main evaluated controlled prompt set: 137 prompts, including 10 implicit-field stress prompts. The original 67 and later 85-prompt sets are retained only as historical subsets.
- Core distinction: skill artifact vs selection representation vs retrieval policy.
- Current RQs.
- Main benchmark purpose: semantic confusability plus procedural distinctness.

The 2401-skill public-expanded scale with 137 main prompts is the current active condition. The 1006-, 2089-, 2349-, and 127-prompt 2401-skill conditions remain historical comparisons for older local/provider results.

Allowed small changes:

- Add acceptable alternatives where manual adjudication shows a near-equivalent skill is genuinely acceptable.
- Fix a prompt or skill only if gold-label stability fails.
- Add a note explaining a limitation instead of endlessly rebuilding the benchmark.
- Add more public/generated scale only if manual adjudication shows the current 2401-skill condition is not enough. Current priority is adjudication, failure-mode analysis, and implicit-field representation extraction rather than more background-only expansion.

## Phase 1: Benchmark Validation

Status: Complete, with watch items.

Purpose:

Confirm that the benchmark is testing the intended problem rather than random noise, prompt leakage, or invalid gold labels.

Required evidence:

- Step 1 integrity passes.
- Step 2 procedural alignment passes.
- Step 3 semantic confusability passes.
- Step 4 prompt leakage passes.
- Step 5 scale regime passes.
- Non-core competitors have been checked enough to show they are mostly distractors, not better gold labels.

Definition of done:

- Benchmark validation reports exist.
- Any ambiguous gold labels are either fixed or recorded as acceptable alternatives.
- The thesis can defend why the benchmark targets semantic confusion under scale.

Do not reopen unless:

- A background skill is clearly more procedurally correct than the gold skill.
- A prompt directly leaks the gold skill name.
- All final methods become near-perfect, making the benchmark too easy.

## Phase 2: Final Method Set

Status: Mostly complete, but requires methodology hardening and missing crossed-matrix runs. Method taxonomy was cleaned on 2026-06-01, `M6-v1-local` was implemented on 2026-06-03, and SkillRouter/SkillRouter+M6-v1 hosted full-skill results were added on 2026-06-05. Final claims still need budget-fair reporting, uncertainty estimates, request-parser/field-ablation validity checks, and R1/R2 representation runs for SkillRouter.

Purpose:

Choose a small final set of methods that represent different information conditions. This is the experimental backbone of the thesis.

Required final methods:

| Role | Method | Why keep it |
|---|---|---|
| Normal-agent baseline | M0 progressive disclosure, core only | Represents current practical main-agent selection behavior. |
| Flat lexical control | M1 BM25 or TF-IDF over flat metadata | Tests compressed metadata and lexical cueing; control only, not thesis architecture. |
| Dense card retrieval | M2 Qwen/MiniLM over R1 flat cards | Tests modern semantic retrieval over the same information as flat metadata. |
| Dense full-artifact retrieval | M2 Qwen/MiniLM over full `SKILL.md` | Tests whether full artifact embeddings already encode procedural suitability. |
| Structured-card retrieval | M3 retrieval over R2 procedural cards | Tests whether extracted procedural fields help before reranking. |
| Generic neural reranker | Dense retrieval plus Qwen rerank | Tests whether a strong generic reranker solves the problem without explicit field scoring. |
| Diagnostic schema reranker | M6-v0 current local schema rerank | Retained for transparency and historical comparison, but too crude for the final structure-aware claim. |
| Proposed procedural reranker | M6-v1 dense shortlist plus field-aware procedural rerank | Directly tests the thesis claim that extracted procedural information improves selection when used as fields. |
| Strong skill-specific baseline | SkillRouter embedding plus SkillRouter rerank | Tests against a prior-work-aligned skill retrieval and reranking system. |
| Optional tree router | M4 route by family/category hierarchy | Tests whether hierarchical routing gives scale efficiency or causes early branch-exclusion failures. |
| Optional graph retriever | M5 retrieval/reranking over R4 relation edges | Tests whether explicit input/output/tool/workflow/resource relations help beyond serialized structured cards. |

Optional methods:

- M4 tree routing.
- M5 graph retrieval.
- Additional providers.

Decision rule:

Optional methods are only worth adding if they test a new representation claim. They are not worth adding just because they might improve top-1.

Architecture rule:

- Use `R2/R3` field ablations to answer which information is useful.
- Use `M6-v1` to test whether request-side field matching can exploit that information.
- Use `M5` graph retrieval if we need to test whether explicit relation edges improve over serialized procedural cards.
- Use `M4` tree routing mainly for scalability and branch-exclusion analysis.
- Do not use tree/graph methods as decorations; each must report the additional failure mode it reveals.

Detailed M4/M5 edge methodology:

- `thesis_notes/M4 M5 Structure-Aware Architecture Plan.md`

Definition of done:

- Final method table is frozen.
- Each method has a one-sentence thesis role.
- Each method reports top-1, top-5, MRR, non-core top-1, candidate budget, and cost/latency if available.
- Headline reranker comparisons use the same candidate budget.
- Strict-gold and gold-or-acceptable results are reported separately.
- Final controlled comparisons include uncertainty estimates or paired tests.
- The method table records model settings, candidate budget, prompt stratum, and scoring rule.

Current 2349 Qwen note:

- Qwen R1 embedding: 35.3% top-1, 50.6% non-main top-1.
- Qwen R2 embedding: 50.6% top-1, 36.5% non-main top-1.
- Qwen full-skill embedding: 50.6% top-1, 30.6% non-main top-1.
- Qwen full-skill plus Qwen rerank top-20: 61.2% top-1.
- Qwen full-skill plus local schema rerank top-100: 84.7% top-1.

Current 2401 Qwen note:

- Qwen full-skill embedding: 52.5% top-1, 73.7% top-5.
- Qwen full-skill plus local schema rerank top-100: 77.4% top-1, 91.2% top-5.
- Qwen full-skill plus `M6-v1-local` task/output/workflow rerank top-100: 78.8% top-1, 92.0% top-5, 0.851 MRR, with 93.4% candidate R@100.
- Qwen full-skill plus `M6-v1-local` all-fields rerank drops to 73.0% top-1, which confirms that all structure should not be treated as positive text.
- Integrated implicit-field cases make the task harder, but the structure-aware method still improves top-1 and reduces non-main false positives after conservative field extraction.

Current 2401 SkillRouter note:

- SkillRouter full-skill embedding: 73.0% top-1, 94.2% top-5, 0.827 MRR.
- SkillRouter full-skill plus SkillRouter rerank top-20: 83.2% top-1, 97.8% top-5, 0.898 MRR.
- SkillRouter first stage plus M6-v1-local task/output/workflow top-20: 83.2% top-1, 95.6% top-5, 0.895 MRR.
- SkillRouter first stage plus M6-v1-local task/output/workflow top-100: 86.9% top-1, 98.5% top-5, 0.927 MRR.
- Interpretation rule: top-20 is the budget-fair reranker comparison; top-100 is a larger-candidate-budget condition.

Method design note:

- `thesis_notes/Final Method Set and Information-Use Plan.md`
- `thesis_notes/M6-v1 Field-Aware Reranker Checkpoint - 2026-06-03.md`
- `thesis_notes/Methodology Deep Critique and Improvement Plan - 2026-06-05.md`

## Phase 2b: Real-World Skill Audit and Public-Expanded Scale Condition

Status: Mostly complete. The 2349-scale condition, 460 public imports, heuristic public-skill audit, and DeepSeek model-assisted public-skill audit are done. Remaining work is selective manual adjudication of disagreement cases and non-core/public winners.

Purpose:

Use public skills to check whether our proposed representation fields correspond to information found in real skill artifacts, then create a larger scale-sensitivity condition.

Required evidence:

- Public imported skills are stored separately from generated background and controlled core skills.
- Source URL and import status are recorded.
- A field audit reports which public skills contain descriptions, inputs, outputs, workflow steps, dependencies, resources, examples, limitations, and negative boundaries.
- The audit classifies each field as `observed`, `extractable`, or `proposed normalization`.
- Controlled core expansion is kept modest. Current expansion is 67 to 85 evaluated cases, with old 67-case results remaining comparable.
- Historical 2089-skill and 85-prompt results remain useful for development comparison, but the active scale condition is 2401 skills and 137 prompts.
- Non-core public winners are manually inspected for whether they are better, acceptable, or only plausible distractors.

Definition of done:

- The thesis can say the representation fields are not only invented from our generated benchmark, but are motivated by literature and checked against public skill artifacts.
- The thesis can separately report results on the original 67-case core and the expanded 85-case core.
- 1006 vs 2089 results are compared as scale sensitivity where historical results are available.
- Gold-label stability remains defensible after public imports.

See `thesis_notes/Real World Skill Expansion Plan.md`.

## Phase 2d: Public-Skill Gold Validation

Status: Draft built, validation gates pass, and first manual adjudication completed. Cleanup is still needed before final reporting.

Purpose:

Test whether externally authored public skills can become stable gold-label retrieval targets, rather than serving only as background distractors or evidence for the field taxonomy.

Required evidence:

- 30-50 public-gold prompts for the first validation pass. Current draft: 32 prompts.
- At least 6 public-skill clusters or source families represented.
- Each prompt has one imported public `gold_skill`.
- Each prompt has 2-4 semantically plausible alternatives.
- Each prompt records a concrete `gold_rationale`, per-alternative rejection rationale, and field-axis annotation.
- Broad or hierarchical public skills are either atomized into a single stable procedure or rejected as gold candidates.
- Prompt text does not name the skill, source repository, or copied distinctive phrases.
- Acceptable alternatives are explicitly recorded instead of being counted as ordinary failures.

Pass criteria:

- 100% prompt references resolve.
- At least 85% of candidate public-gold prompts survive manual gold-label adjudication.
- At least 80% pass prompt-specific procedural alignment.
- At least 70-80% pass semantic-confusability checks under a modern embedding model, with documented exceptions for high-precision cases.
- 0 critical or high-risk prompt leaks.
- Selector results show useful method spread and interpretable failure modes.
- Public-gold results are reported as their own stratum: controlled-authored, public-gold, and combined.

Current checkpoint:

- `thesis_notes/Public Gold Expansion Checkpoint - 2026-06-05.md`
- Step 1 integrity: PASS, 82/82 references resolve.
- Step 2 procedural distinctness: PASS, 82/82 prompts.
- Step 2 prompt-specific alignment: PASS with caveats, 79/82 prompts.
- Step 3 semantic confusability: PASS, 78/82 prompts.
- Step 4 prompt leakage: PASS, 0 critical and 0 high-risk.
- Local selector result: public-gold cases show useful pressure. M1 BM25 flat is strongest locally at 51.2% strict top-1 and 67.1% accept top-1; M1 TF-IDF flat reaches 50.0% strict top-1. Naive schema/rerank methods underperform flat/description retrieval on this stratum.
- Provider result: Qwen and SkillRouter have now been rerun on the cleaned 82-prompt stratum. Best current public-gold method is Qwen R2 + Qwen rerank top-20 at 76.8% strict top-1, 90.2% accept top-1, and 100.0% top-5.
- Manual/acceptable-alternative cleanup is encoded in `skill_benchmark/annotations/public_gold_acceptable_alternatives.json`.
- Method interpretation: current schema rerank underperformance on public-gold is evidence that naive field overlap is not enough. The final structure-aware method should parse request-side requirements and compare fields explicitly.

Fail criteria:

- The public skill is too broad, hierarchical, or conditional to be an atomic target.
- The prompt tests a behavior that is not clearly present in the public skill.
- Multiple alternatives are equally correct and no acceptable-alternative label is recorded.
- The result mostly tests source/name matching rather than procedural fit.
- Structure-aware methods win only because our extractor hallucinated fields without evidence spans.

Recommended sequence:

1. Select candidate public skills from the imported corpus.
2. Screen for atomicity and reject broad/hierarchical candidates.
3. Extract fields with the current representation layer, then verify difficult cases with model-assisted evidence spans.
4. Draft public-gold prompts and alternatives.
5. Manually adjudicate gold stability.
6. Run the existing Steps 1-4 validation scripts on the public-gold subset.
7. Run final method selectors on public-gold-only and combined strata.
8. Analyse failures as candidate-recall, extraction, reranking, ambiguity, hierarchy, or acceptable-alternative failures.

Detailed plan: `thesis_notes/Public Skill Gold Validation Plan.md`.

## Phase 2c: Representation Field Ablation

Status: Executed, but final causal field claims need hardening.

Purpose:

Test the thesis claim about which information matters. This is different from showing that one architecture performs well. It asks which fields contribute to distinguishing semantically similar skills.

Required ablations:

- Description only.
- Description + use conditions.
- + input/precondition fields.
- + output artifact fields.
- + workflow/procedure fields.
- + constraints/not-for boundaries.
- + dependencies/resources.

Definition of done:

- A table reports top-1, top-5, MRR, non-core top-1, and visible tokens for each field set.
- The analysis identifies which fields give measurable gains and which add little or mostly help specific clusters.
- The thesis can answer RQ1 with evidence rather than only intuition.
- Length-control or field-dropout checks are added before final causal claims about individual fields.

Current report:

- `skill_benchmark/outputs/field_ablation_results.md`
- `thesis_notes/Field Ablation Results - 2089 Scale.md`

Main result:

- Description-only retrieval is substantially weaker at 2089 scale.
- Use conditions provide the largest early gain.
- Output artifacts and workflow/procedure provide the strongest additional gains.
- Preconditions help modestly.
- Naively adding `not_for` and dependency/resource text can hurt top-1, which means these fields should be handled through field-aware scoring/reranking rather than plain concatenation.

Pass condition:

- At least one non-description field improves retrieval or reduces non-core false positives.
- If a field does not help, it is reported honestly as context-dependent or mainly useful for downstream execution rather than retrieval.

## Phase 3: Candidate Budget, Cost, and Latency

Status: Still required, but now follows the methodology-hardening checks.

Purpose:

Decide whether the strongest hybrid method is practical, especially at top-100 candidate budget.

Required comparisons:

- Qwen full embedding plus M6-v1-local or schema rerank at top-20, top-50, top-100.
- SkillRouter first stage plus SkillRouter rerank and M6-v1-local at matching budgets where feasible.
- Record top-1, top-5, MRR.
- Record local rerank time.
- Record whether embeddings are cached or require API calls.
- Estimate exposed candidate text length or token cost.
- Include a context-scale statement distinguishing compact metadata scale from full-artifact/structured-representation scale.

Definition of done:

- A table shows accuracy-efficiency trade-off for top-20, top-50, and top-100.
- A written decision states whether top-100 is acceptable, or whether top-50 is a better thesis recommendation.
- The thesis can say whether the best accuracy gain is worth the extra candidate budget.

Pass condition:

- One candidate budget is selected for downstream validation.
- The selection is justified by both accuracy and efficiency.

## Phase 4: Failure Mode Analysis

Status: Partially complete.

Purpose:

Turn result tables into thesis insight about what information retrieval methods preserve or lose.

Required methods to analyze:

- One flat baseline.
- One dense retrieval baseline.
- One generic neural reranker.
- The strongest hybrid method.

Required failure categories:

- First-stage exclusion.
- Semantic similarity collapse.
- Procedural field missing or underweighted.
- Negative boundary failure.
- Object/task confusion.
- Meta-skill confusion.
- Underspecified prompt.
- Acceptable alternative or annotation ambiguity.

Definition of done:

- Each final method has failure counts by category.
- At least 5 representative examples are written as thesis-ready case studies.
- The analysis explicitly connects each failure type to missing or misused representation information.

## Phase 5: Downstream Validation

Status: Planned, not executed.

Purpose:

Show whether retrieval improvements matter for actual task completion, not only ranking metrics.

Minimum viable design:

- Use 12 representative prompts.
- Include easy-success, known-confusion, and failure-prone cases.
- Compare 3 conditions:
  - flat baseline;
  - dense full-skill baseline;
  - strongest hybrid method.
- Add oracle-gold skill condition if feasible.

Pass condition:

- Oracle-gold downstream success should be at least 80%. If not, the task or skill artifact is unstable.
- Retrieval methods should only be judged downstream when the gold or acceptable skill is in the candidate set.
- Failures should be labelled as retrieval failure, skill-use failure, or task ambiguity.

Definition of done:

- Downstream artifacts exist.
- A grading rubric exists.
- Results connect retrieval quality to task success.

## Phase 6: Thesis Writing Integration

Status: Scaffold created.

Purpose:

Make sure experiments feed directly into the thesis rather than becoming disconnected reports.

Required updates:

- Update Chapter 1 with final RQs and contribution wording.
- Update Chapter 2 literature review so the final synthesis matches the current RQs.
- Fill Chapter 4 with benchmark cluster examples and validation table.
- Fill Chapter 5 with final method table and schema reranker formula.
- Fill Chapter 6 with final result tables.
- Fill Chapter 7 with failure mode analysis and design implications.
- Update conclusion only after downstream validation is complete or explicitly scoped out.

Definition of done:

- Every final result table has a matching interpretation paragraph.
- Every major claim has evidence from either literature, benchmark validation, retrieval metrics, efficiency metrics, or failure analysis.
- The thesis answers RQ1 and RQ2 directly.

## Stop Rules

Stop adding new experiments when:

- The experiment only changes provider/model but not representation information.
- The experiment cannot be compared on the same prompts, library size, and metrics.
- The experiment delays Phase 3 cost/latency or Phase 5 downstream validation.
- The expected thesis contribution would still be the same without it.

Run a new experiment only if it answers one of these:

- Does this representation preserve different information?
- Does this retrieval strategy exploit preserved information differently?
- Does this explain a failure mode in the current best method?
- Does this improve the final thesis argument, not just the score table?

## Immediate Next Steps

1. Run public-gold failure-mode analysis on the cleaned 82-prompt stratum, now that Qwen and SkillRouter provider reruns are complete.
2. Audit M6-v1-local request-field extraction on a manually labelled prompt sample.
3. Decide whether to implement M6-v2 semantic field matching, because lexical M6-v1-local underperforms strong semantic rerankers on public-gold.
4. Add statistical uncertainty and paired tests for final controlled comparisons.
5. Run length-control or field-dropout ablations.
6. Add the supervisor-feedback experimental setup table: gold labels, prompt strata, model settings, candidate budget, scoring rule, cache/cost, and metrics.
7. Add the literature-review empirical-detail table.
8. Freeze the field taxonomy as observed, extractable, or proposed normalization using the completed public audit.
9. Freeze the final method set for thesis comparison.
10. Run or consolidate candidate-budget cost/latency for top-20, top-50, and top-100.
11. Complete failure-mode comparison across the final method set, including public-gold failures if the subset passes validation.
12. Decide whether to run full 2401-skill M0 as a context/cost stress test or only report the context-scale audit.
13. Run Step 9 downstream validation on the 12-prompt sample.
14. Update thesis LaTeX chapters with the final results.
