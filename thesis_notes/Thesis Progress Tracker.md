# Thesis Progress Tracker

Date: 2026-06-06

This is the high-level tracker for the thesis so the project does not drift. Detailed benchmark criteria live in `skill_benchmark/notes/benchmark_methodology_rubric.md`. The experimental roadmap lives in `thesis_notes/Thesis Experiment Roadmap.md`. The source of truth for experiment method choices, representation/retriever/reranker combinations, and run commands is `thesis_notes/Experiment Methodology Tracker.md`.

Note: some lower sections retain historical 1006/2089/2349 results for comparison. The active result summary is `thesis_notes/Current Results Summary.md`.

## Core Thesis Framing

The thesis is about skill retrieval as a candidate-subsetting component before the main agent loads full skill artifacts.

Current research position:

> This thesis investigates what information agent skill representations must preserve, and how different retrieval strategies exploit that information, so that agents can distinguish semantically similar but procedurally different skills at scale.

Current research questions:

**RQ1:** What information must agent skill representations preserve to distinguish semantically similar but procedurally distinct skills at scale?

**RQ2:** How do retrieval strategies that use flat text, dense embeddings, structured procedural fields, or hybrid reranking differ in accuracy, efficiency, and failure modes when applied to scalable skill libraries?

Earlier assignment wording, now developed:

**Previous RQ1:** How can agent skills be represented and retrieved so that agents can accurately select among semantically similar but procedurally distinct skills as skill libraries scale?

**Previous RQ2:** To what extent do structure-aware skill representations improve retrieval accuracy, context efficiency, and downstream task performance compared with flat description-based skill retrieval?

The previous questions are not wrong, but the current version is sharper. The old RQ2 framed the thesis as testing whether structure-aware representation improves performance. The current framing makes the novelty clearer: the thesis asks which information should be preserved in skill representations, then evaluates which retrieval strategies can use that information effectively.

The thesis is not mainly about which commercial provider wins. Provider models are used to test whether the representation findings survive stronger retrievers and rerankers.

## Current Validity Critique

The latest detailed methodology critique is recorded in `thesis_notes/Methodology Deep Critique and Improvement Plan - 2026-06-05.md`. The earlier critique response remains useful background in `thesis_notes/Critique Response and Validity Improvement Plan.md`.

The current benchmark risk register is `thesis_notes/Benchmark Risk Register and Mitigation Plan - 2026-06-06.md`. Use it when deciding whether to add prompts, import more public skills, create public-style controlled skills, or introduce new method variants.

Main validity risks to actively address:

- the controlled benchmark and schema reranker may be co-adapted;
- representation-layer effects and retriever/reranker effects can be conflated if Qwen, SkillRouter, and local rerankers are compared while using different skill representations;
- gold labels may be unstable when public/background alternatives are plausible;
- 201 evaluated controlled prompts is enough for a controlled honours study but not for broad universal claims;
- generated background skills provide scale pressure but not full real-world messiness;
- MiniLM semantic-confusability checks are construction evidence, not final semantic authority;
- the public-skill field audit grounds the taxonomy but is not a full gold annotation study;
- downstream task success has not yet been demonstrated;
- the current M6-v1-local matcher is lexical field-aware routing, not robust semantic field understanding;
- the strongest SkillRouter + M6-v1 result uses a top-100 candidate budget, so it must not be compared as a direct reranker-only win over SkillRouter top-20 reranking;
- the crossed representation-by-architecture matrix is incomplete: current active results do not yet include reruns on the expanded 201-prompt / 2433-skill controlled benchmark;
- final results still need confidence intervals or paired statistical tests.
- prompt information level, platform/provider cues, and boundary negations need to be stratified rather than treated as simple leakage/no-leakage.

Current response:

- frame the thesis as controlled evidence about representation information, not a universal benchmark claim;
- treat representation layer and retriever/reranker architecture as two experimental factors, and report missing matrix cells rather than hiding them;
- prioritize fair horizontal comparisons: R1, R2, and full skill artifacts tested under the same retrievers/rerankers, prompt strata, scale, and candidate budgets;
- freeze the field taxonomy and method set before further tuning;
- run targeted independent/second-pass adjudication on non-core winners and strongest-method failures;
- perform a manual cluster design audit before adding more controlled or public-gold prompts;
- verify the field taxonomy against additional public skills as a background stress test, without turning them into evaluated gold tasks unless they are manually atomized and annotated;
- add public-style controlled skills to test whether the representation layer can extract useful fields from messier skill artifacts, not only from neat schema-authored skills;
- run Step 9 downstream validation before final claims about agent reliability.

Current crossed-design priority:

| Priority | Missing / hardening item | Why it matters |
|---|---|---|
| 1 | Report the completed local selector baselines and field-aware rerankers by original controlled vs public-style controlled strata. | Establishes whether the expansion changed benchmark pressure before spending provider/API budget. |
| 2 | Audit the 19 weak Step 2 requirement-alignment prompts from the 201-prompt rerun. | Prevents label instability from being mistaken for retrieval failure. |
| 3 | Run Qwen and SkillRouter on the expanded controlled 201 / 2433 benchmark, with R1/R2/full representations and matched candidate budgets where feasible. | Separates representation effects from model effects on the new active benchmark. |
| 4 | Run SkillRouter embedding and SkillRouter rerank on R1 and R2 for public-gold 82 / 2433 if public-gold is used in final tables. | Tests whether Qwen R2 + rerank is a representation advantage or a model/stratum artifact. |
| 5 | Report public-gold by source-family and cluster type. | Prevents the public-gold stratum from acting like one undifferentiated bucket. |
| 6 | Add M6-v2 semantic field matching after the matrix is filled. | Tests whether field-aware retrieval fails because of fields or because the current matcher is too lexical. |
| 7 | Add paired tests and confidence intervals for final selected comparisons. | Needed for final thesis-level empirical claims. |
| 8 | Run downstream validation only after offline retrieval results stabilize. | Avoids spending main-agent cost before candidate selection is understood. |

## Supervisor Feedback Incorporated

Assignment 3 feedback asked for more concrete empirical details from reviewed papers, clearer benchmark construction, and a more specific experimental setup including gold labels, model settings, prompts, and statistical comparison.

Current response plan:

- `thesis_notes/Supervisor Feedback Response Plan - A3 to Current Thesis.md`

Methodology impact:

- the literature review needs a concrete empirical-detail table for key papers;
- the benchmark chapter needs a reproducible construction pipeline;
- the methodology chapter needs a final method-configuration table;
- benchmark examples need prompt-level gold rationales, alternative rejection rationales, and field-axis justifications; the evidence map is `thesis_notes/Gold Label Evidence Map.md`;
- final result tables need strict versus acceptable labels, candidate budgets, model settings, and statistical uncertainty.

## Representation Classes To Compare

- Flat metadata: skill name, description, family/tags.
- Full skill artifact: whole `SKILL.md` or fuller skill text.
- Structured procedural representation: use case, inputs, outputs, preconditions, workflow, constraints, success criteria.
- Dependency/resource-aware representation: tools, files, public imports, external services, optional resources.
- Graph/tree representation: explicit relations among skills, families, dependencies, resources, and procedural fields.

## Method Families

- M0: progressive disclosure baseline, where the main agent sees visible skill cards and decides which full skill documents to load.
- M1: lexical flat retrieval, such as BM25 or TF-IDF over metadata.
- M2: embedding retrieval over description or full skill text.
- M3: structured/schema-based retrieval.
- M4: tree routing, not implemented yet.
- M5: graph retrieval, not implemented yet.
- M6-v0: local two-stage retrieval plus deterministic schema reranking; keep as a diagnostic method, not the final structure-aware claim.
- M6-v1: proposed field-aware procedural reranker that parses request requirements and compares them against extracted skill fields.
- M7: API embedding retrieval, implemented and executed with Qwen.
- M8: API embedding retrieval plus neural reranking, implemented and executed with Qwen.
- M8b: API embedding retrieval plus local schema reranking, implemented and executed; strong historical/diagnostic hybrid.

## Active 2026-06-06 Snapshot

- Active library: 2433 skills.
- Active main prompts: 201 controlled/evaluated prompts, including 10 implicit-field stress prompts and 64 public-style controlled prompts.
- Public imported skills: 460, all with original `SKILL.md` files downloaded.
- Public field audit: 460/460 public skills audited heuristically and with DeepSeek model-assisted verification.
- Public-gold stratum: 82 cleaned public-gold prompts; this creates 283 total evaluated prompts across controlled + public-gold strata if combined.
- Current method cleanup: local schema rerank is `M6-v0`; `M6-v1-local` field-aware procedural reranking is implemented as a lexical prototype.
- Current main concern: show that extracted selection information helps when it is actually used as structured evidence, while separating field usefulness from extraction quality, candidate budget, length bias, and lexical overlap.
- Step 4b manual cluster audit: first pass complete in `skill_benchmark/outputs/cluster_design_audit.md`; future expansion should follow its expand/revise/freeze decisions.
- Public-style controlled expansion: 32 prose-style skills and 64 prompts added to test whether representation fields can be extracted from less neatly schema-authored artifacts.
- First active local selector rerun on 201/2433 is complete: flat metadata ranges from 55.2% to 61.7% top-1, local schema/rerank reaches 65.7%, and M6-v1 local field-aware reranking reaches 72.6% top-1 with high candidate recall.

## Status Corrections Since Earlier Notes

Some older notes still mention 85 prompts, 137 prompts, 2089 skills, 2349 skills, or 2401 skills. Treat those as historical unless explicitly labelled. The active controlled benchmark is 201 prompts over 2433 skills.

Items previously marked done but now requiring redo or hardening:

- Step 7 field ablations: done as useful evidence, but final claims need length-control or field-dropout checks.
- M6-v1: implemented, but only as `M6-v1-local`; it still needs request-parser audit and possibly an M6-v2 semantic field matcher.
- SkillRouter comparison: done, but top-20 and top-100 budgets must be reported separately.
- Public-gold validation: cleaned into a separate 82-prompt external-validity stratum; residual gold-label hard cases were prompt-tightened; provider/SkillRouter runs still need rerun on this cleaned stratum.
- Step 6 public field audit: done as heuristic/model-assisted evidence, but final paper-level claims need manual/sample calibration and evidence-span examples.
- Literature review: scaffold exists, but needs concrete empirical details from key papers.
- M0 progressive disclosure: historical only; not current on 201/2433.
- Downstream validation: planned only.

## Completed Work

- Thesis framing clarified: retriever/reranker is separate from the main agent.
- Benchmark library expanded to 2433 skills:
  - 169 controlled/evaluated skills, including 10 implicit-field stress skills and 32 public-style controlled skills.
  - 1800 generated background-scale skills.
  - 460 public imported background skills.
  - 4 support/email skills.
- Prompt set expanded to 201 controlled/evaluated prompts.
- Controlled-core v2 clusters added:
  - office artifact workflows.
  - deployment/browser QA.
  - API/backend design.
- R1-R4 representations exported.
- Step 1 integrity validation passed.
- Step 2 procedural distinctness and stricter prompt-specific alignment passed after prompt refinements and negation-aware scoring.
- Step 3 semantic confusability passed.
- Step 4 prompt leakage passed.
- Step 5 scale regime passed.
- Step 6 public/real-world skill field audit executed on all 460 imported public skills with heuristic extraction and DeepSeek model-assisted verification; disagreement packet regenerated for taxonomy review.
- Public imported background layer expanded to 460 skills and revalidated as a heuristic/model taxonomy and background stress-test layer.
- Public-style controlled expansion added 8 clusters, 32 skills, and 64 prompts; validation passes integrity, procedural distinctness, semantic confusability, and prompt leakage gates.
- Step 7 local selector/reranker evaluation passed as useful benchmark pressure.
- Step 7 local selectors and M6-v1 local field-aware reranking rerun on the active 201-prompt / 2433-skill benchmark.
- Step 7 Qwen full-skill provider conditions rerun on the pre-public-style 2401-skill / 137-prompt benchmark.
- Step 7 field ablation executed on the active benchmark; use conditions, output artifacts, and workflow/procedure are the strongest helpful fields, while naive not-for/dependency concatenation can add noise.
- Step 8 M0 progressive-disclosure core baseline completed historically.
- Step 9 downstream validation plan prepared, but not executed.
- Optional Qwen/OpenAI provider runner added.
- Qwen core smoke test executed successfully with `text-embedding-v4` plus `qwen3-rerank` on 5 prompts.
- Qwen full-library provider runs completed for R1 flat cards, full `SKILL.md`, and R2 structured cards, with and without `qwen3-rerank`.
- Qwen + local schema reranker ablation completed on historical conditions and the pre-public-style 2401-skill full-skill provider condition.
- Low-information prompt stress test added and run separately to check whether schema reranking depends too strongly on explicit procedural cues.
- Failure mode analysis completed for the current strongest method.
- SkillRouter hosted embedding and reranking baselines completed on the 2401-skill benchmark.
- SkillRouter first-stage plus M6-v1-local reranking completed on the 2401-skill benchmark.
- Thesis LaTeX methodology/results/discussion updated to use budget-fair interpretation and strict/acceptable metric separation.

## Current Key Results

Active 2401-skill / 137-prompt controlled results:

- M1 BM25 flat: 67.9% strict top-1, 88.3% top-5, 0.771 MRR.
- M1 TF-IDF flat: 60.6% strict top-1, 83.9% top-5, 0.713 MRR.
- M3 TF-IDF schema: 71.5% strict top-1, 94.9% top-5, 0.823 MRR.
- Qwen full-skill embedding: 52.5% strict top-1, 73.7% top-5, 0.617 MRR.
- Qwen full-skill + Qwen rerank top-20: 62.0% strict top-1, 75.2% top-5, 0.684 MRR.
- Qwen full-skill + M6-v1-local task/output/workflow top-100: 78.8% strict top-1, 92.0% top-5, 0.851 MRR.
- SkillRouter full-skill embedding: 73.0% strict top-1, 94.2% top-5, 0.827 MRR.
- SkillRouter full-skill + SkillRouter rerank top-20: 83.2% strict top-1, 97.8% top-5, 0.898 MRR.
- SkillRouter first stage + M6-v1-local task/output/workflow top-20: 83.2% strict top-1, 95.6% top-5, 0.895 MRR.
- SkillRouter first stage + M6-v1-local task/output/workflow top-100: 86.9% strict top-1, 98.5% top-5, 0.927 MRR.

Interpretation:

- SkillRouter is now the strongest first-stage skill-specific retriever.
- The fair reranker comparison is SkillRouter top-20 rerank versus M6-v1-local top-20 rerank; both reach 83.2% top-1, with SkillRouter slightly better on top-5/MRR.
- M6-v1-local top-100 is the strongest controlled result, but it is a larger-candidate-budget condition, not a direct reranker-only win.
- Qwen and SkillRouter results support the same broad claim: dense retrieval is useful for candidate generation, but final ordering benefits from selection information when the method can use it.

Public-gold active result summary:

- 82 public-gold prompts are now cleaned and generated as a separate stratum.
- Validation gates pass with caveats: procedural distinctness 82/82, requirement alignment PASS at 79/82, semantic confusability PASS at 78/82, leakage 0 critical/high-risk.
- Current local public-gold results on `current_full`: best strict top-1 is 51.2% for M1 BM25 flat; best accept top-1 is 67.1% for M1 BM25 flat; best strict top-5 is 86.6% for M1 BM25/TF-IDF flat.
- Schema/rerank local methods underperform flat public-wrapper retrieval on this stratum, which is an external-validity limitation and a useful failure-mode source.
- Qwen and SkillRouter public-gold results currently refer to the older 32-prompt stratum and should be rerun before being used as final public-gold evidence.

Historical results:

The 1006-, 2089-, and 2349-skill sections below are retained as historical development evidence and scale-comparison context. Do not use them as the active headline condition unless explicitly labelled.

Historical local full-library results on 1006 skills:

- M1 BM25 flat: 64.2% strict top-1.
- M1 TF-IDF flat: 58.2% strict top-1.
- M2a MiniLM description embedding: 47.8% strict top-1.
- M2b MiniLM full-skill embedding: 61.2% strict top-1.
- M3 TF-IDF schema: 71.6% strict top-1.
- M6 BM25 -> schema rerank: 71.6% strict top-1.
- M6 TF-IDF -> schema rerank: 70.2% strict top-1.
- M6 MiniLM full-skill -> schema rerank: 80.6% strict top-1.

M0 progressive disclosure on 67 controlled core skills:

- Strict top-1: 61.2%.
- Strict any-hit: 64.2%.
- No explicit skill loaded: 31.3%.
- Mean full docs loaded: 0.78.

Qwen provider smoke test:

- Scale: core, 67 skills.
- Prompts: first 5 benchmark prompts.
- Method: `text-embedding-v4` over full `SKILL.md` plus `qwen3-rerank` over top-20 candidates.
- Result: 100.0% top-1, 100.0% top-5, MRR 1.000.
- Output report: `skill_benchmark/outputs/provider_selector_qwen_core_smoke.md`.

Historical Qwen provider full-library results on 1006 skills:

- R1 flat card embedding only: 35.8% top-1, 56.7% top-5.
- R1 flat card embedding + rerank: 64.2% top-1, 67.2% top-5.
- Full `SKILL.md` embedding only: 46.3% top-1, 71.6% top-5.
- Full `SKILL.md` embedding + rerank: 61.2% top-1, 65.7% top-5.
- R2 structured-card embedding only: 47.8% top-1, 65.7% top-5.
- R2 structured-card embedding + rerank: 65.7% top-1, 71.6% top-5.
- Output comparison: `skill_benchmark/outputs/provider_selector_qwen_comparison.md`.

Qwen + local schema reranker:

- Full `SKILL.md` embedding + local schema rerank, top-20: 68.7% top-1.
- Full `SKILL.md` embedding + local schema rerank, top-50: 80.6% top-1.
- Full `SKILL.md` embedding + local schema rerank, top-100: 85.1% top-1.
- Interpretation: Qwen embeddings are useful as a broad candidate generator, but procedural schema reranking is better aligned with the final selection task than Qwen's generic reranker.
- Output report: `thesis_notes/Qwen Local Schema Reranker Ablation.md`.

Interpretation:

- Qwen reranking improves top-1 over Qwen embedding-only for every tested representation.
- Generic Qwen reranking is weaker than procedural schema reranking on this benchmark.
- The current strongest result is Qwen full-skill retrieval plus local schema reranking over a top-100 candidate pool.
- This supports the thesis framing that strong semantic retrieval and procedural schema reranking are complementary.

Low-information stress test:

- 12 separate prompts with deliberately weaker procedural wording.
- Best strict top-1 is 41.7% for MiniLM full-skill embedding.
- Qwen full + local schema top-100 gets 25.0% top-1 and 66.7% top-5.
- Interpretation: the schema reranker is not cheating by inferring hidden intent; it needs procedural evidence in the request.
- Report: `thesis_notes/Low Information Stress Test.md`.

Failure mode analysis:

- Target: Qwen full-skill embedding plus local schema reranking over top-100 candidates.
- 10 strict top-1 failures.
- 4 failures are first-stage exclusions where Qwen does not place gold in top-100.
- 6 failures are reranker, boundary, negation, meta-skill, or annotation issues.
- Report: `thesis_notes/Failure Mode Analysis - Qwen Full Local Schema Top100.md`.

Interpretation:

- The benchmark is currently good enough for method comparison.
- Structure-aware reranking is strongest among local methods so far.
- MiniLM is a construction/local baseline, not the final modern embedding baseline.

## What To Do Next

Follow the roadmap in `thesis_notes/Thesis Experiment Roadmap.md`.

Current phase: methodology hardening before final downstream validation.

Immediate next steps:

1. Rerun provider/SkillRouter public-gold selectors on the cleaned 82-prompt stratum, or clearly label older public-gold provider numbers as historical.
2. Add statistical uncertainty and paired tests for final controlled comparisons.
3. Audit M6-v1-local request-field extraction on a manually labelled sample.
4. Run length-control or field-dropout ablations so field-value claims are not just token-volume claims.
5. Add thesis-ready experimental setup table: model settings, prompts, gold labels, candidate budgets, scoring rules, cache/cost, and metrics.
6. Add literature-review empirical-detail table responding to supervisor feedback.
7. Freeze the final method set and label M6-v1-local as lexical prototype; decide whether M6-v2 semantic field matching is needed.
8. Consolidate candidate-budget cost/latency for top-20, top-50, and top-100.
9. Complete failure-mode comparison across final methods and public-gold failures.
10. Decide whether full 2401-skill M0 is useful as a context/cost stress test.
11. Run downstream validation on the 12-prompt sample after offline metrics are stable.
12. Update thesis LaTeX chapters with final method, result, statistical, and failure-analysis tables.

## What Not To Do Yet

- Do not expand beyond 2401 skills as a new controlled benchmark unless final methods make the benchmark too easy or adjudication shows the scale layer is too artificial.
- It is acceptable to expand public skills as background/taxonomy validation if they are clearly separated from controlled gold skills.
- Do not treat provider choice as the thesis contribution.
- Do not add more providers or model variants unless they test a new representation claim.
- Do not tune prompts, gold labels, or schema weights after the final method set is frozen unless the change is logged as a validity correction.
- Do not run Step 9 downstream validation until the field taxonomy, final method set, and candidate budget are chosen.

## Canonical Reference Files

- Benchmark rubric: `skill_benchmark/notes/benchmark_methodology_rubric.md`
- Experiment roadmap: `thesis_notes/Thesis Experiment Roadmap.md`
- Draft final field taxonomy: `thesis_notes/Final Representation Field Taxonomy - Draft.md`
- Public model verification checkpoint: `thesis_notes/Public Skill Model Verification Checkpoint - 460 Skills.md`
- Critique response plan: `thesis_notes/Critique Response and Validity Improvement Plan.md`
- Public expansion checkpoint: `thesis_notes/Public Expansion 2349 Validation Checkpoint.md`
- Provider API setup: `skill_benchmark/notes/provider_api_baselines.md`
- Literature refresh: `thesis_notes/Reranking and Skill Retrieval Literature Refresh 2026-05-25.md`
- Offline selector results: `skill_benchmark/outputs/offline_selector_evaluation.md`
- M0 baseline report: `skill_benchmark/outputs/m0_progressive_disclosure_core_report.md`
- Step 9 downstream plan: `skill_benchmark/outputs/step8_downstream_validation_plan.md` (file name still says step8 from the earlier numbering)

## Drift Check

Before adding a new experiment, ask:

- Does this test a representation class or only a provider?
- Does it preserve the same prompts, gold labels, and scale condition?
- Does it report accuracy, top-k recall, MRR, context/cost, and failure modes?
- Does it help answer which information a skill representation needs to preserve?

If the answer is no, postpone it.
