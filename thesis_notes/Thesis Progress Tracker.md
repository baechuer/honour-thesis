# Thesis Progress Tracker

Date: 2026-05-28

This is the high-level tracker for the thesis so the project does not drift. Detailed benchmark criteria live in `skill_benchmark/notes/benchmark_methodology_rubric.md`. The experimental roadmap lives in `thesis_notes/Thesis Experiment Roadmap.md`.

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

The latest independent critique is recorded in `thesis_notes/Critique Response and Validity Improvement Plan.md`.

Main validity risks to actively address:

- the controlled benchmark and schema reranker may be co-adapted;
- gold labels may be unstable when public/background alternatives are plausible;
- 85 evaluated prompts is enough for a controlled honours study but not for broad universal claims;
- generated background skills provide scale pressure but not full real-world messiness;
- MiniLM semantic-confusability checks are construction evidence, not final semantic authority;
- the public-skill field audit grounds the taxonomy but is not a full gold annotation study;
- downstream task success has not yet been demonstrated.

Current response:

- frame the thesis as controlled evidence about representation information, not a universal benchmark claim;
- freeze the field taxonomy and method set before further tuning;
- run targeted independent/second-pass adjudication on non-core winners and strongest-method failures;
- verify the field taxonomy against additional public skills as a background stress test, without turning them into evaluated gold tasks unless they are manually atomized and annotated;
- run Step 9 downstream validation before final claims about agent reliability.

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
- M6: local two-stage retrieval plus deterministic schema reranking.
- M7: API embedding retrieval, implemented and executed with Qwen.
- M8: API embedding retrieval plus neural reranking, implemented and executed with Qwen.
- M8b: API embedding retrieval plus local schema reranking, implemented and executed; strongest current method.

## Completed Work

- Thesis framing clarified: retriever/reranker is separate from the main agent.
- Benchmark library expanded to 2349 skills:
  - 85 controlled/evaluated core skills.
  - 1800 generated background-scale skills.
  - 460 public imported background skills.
  - 4 support/email skills.
- Prompt set expanded to 85 evaluated prompts.
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
- Step 6 public/real-world skill field audit executed on 200 imported public skills with both heuristic extraction and DeepSeek model verification; pattern-level disagreement adjudication completed.
- Public imported background layer expanded to 460 skills and revalidated as a heuristic/taxonomy/background stress-test layer.
- Step 7 local selector/reranker evaluation passed as useful benchmark pressure.
- Step 7 Qwen full-skill provider conditions rerun on the active 2089-skill benchmark.
- Step 7 field ablation executed on the 2089-skill benchmark; use conditions, output artifacts, and workflow/procedure are the strongest helpful fields, while naive not-for/dependency concatenation can add noise.
- Step 8 M0 progressive-disclosure core baseline completed historically.
- Step 9 downstream validation plan prepared, but not executed.
- Optional Qwen/OpenAI provider runner added.
- Qwen core smoke test executed successfully with `text-embedding-v4` plus `qwen3-rerank` on 5 prompts.
- Qwen full-library provider runs completed for R1 flat cards, full `SKILL.md`, and R2 structured cards, with and without `qwen3-rerank`.
- Qwen + local schema reranker ablation completed on both the historical 1006-skill condition and the active 2089-skill full-skill provider condition.
- Low-information prompt stress test added and run separately to check whether schema reranking depends too strongly on explicit procedural cues.
- Failure mode analysis completed for the current strongest method.

## Current Key Results

Active local full-library results on 2089 skills:

- M1 BM25 flat: 70.6% strict top-1.
- M1 TF-IDF flat: 58.8% strict top-1.
- M2a MiniLM description embedding: 49.4% strict top-1.
- M2b MiniLM full-skill embedding: 64.7% strict top-1.
- M3 TF-IDF schema: 78.8% strict top-1.
- M6 BM25 -> schema rerank: 78.8% strict top-1.
- M6 TF-IDF -> schema rerank: 75.3% strict top-1.
- M6 MiniLM full-skill -> schema rerank: 82.3% strict top-1.

Public-expanded local lexical results on 2349 skills:

- M1 BM25 flat: 68.2% strict top-1, 87.1% top-5, 15.3% non-core top-1.
- M1 TF-IDF flat: 58.8% strict top-1, 78.8% top-5, 28.2% non-core top-1.
- M3 TF-IDF schema: 76.5% strict top-1, 94.1% top-5, 10.6% non-core top-1.
- M6 BM25 -> schema rerank: 78.8% strict top-1, 91.8% top-5, 5.9% non-core top-1.
- M6 TF-IDF -> schema rerank: 74.1% strict top-1, 87.1% top-5, 14.1% non-core top-1.

Note: MiniLM-backed methods were not rerun on the 2349-skill condition because `sentence_transformers` is unavailable in the current shell. Qwen provider methods remain 2089-scale unless explicitly rerun.

Active validation read:

- Step 1 integrity: PASS for 85 prompts and 2349 skills after public expansion.
- Step 2 field audit: PASS for 85/85 prompts and 251/251 pairs.
- Step 2 prompt-specific alignment: PASS, 85/85 prompts pass.
- Step 3 semantic confusability: previous MiniLM checkpoint PASS, 75/85. The 2349 rerun used TF-IDF fallback and got 27/85, so it is a non-comparable sanity check rather than a replacement result.
- Step 4 prompt leakage: PASS, 0 critical and 0 high-risk leaks.
- Non-core competition: on the 2349 TF-IDF fallback check, 26/85 prompts have non-core top-1, 30/85 have best non-core above gold, and 14/85 have a procedural non-core above gold. Acceptable alternatives are recorded separately from strict gold labels.

Active Qwen provider results on 2089 skills:

- Qwen full-skill embedding only: 50.6% strict top-1, 69.4% top-5.
- Qwen full-skill + Qwen rerank top-20: 63.5% strict top-1, 69.4% top-5.
- Qwen full-skill + local schema rerank top-50: 80.0% strict top-1, 84.7% top-5.
- Qwen full-skill + local schema rerank top-100: 84.7% strict top-1, 89.4% top-5.

Interpretation: Qwen is useful as a modern semantic candidate generator, but the strongest current 2089-scale result comes from adding local procedural schema reranking.

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

Current phase: Phase 3, candidate budget, cost, and latency.

Immediate next steps:

1. Review and confirm the draft final representation-field taxonomy.
2. Run targeted second-pass adjudication on non-core winners and strongest-method failures.
3. Decide whether to rerun MiniLM/Qwen semantic checks on the 2349 condition or keep the 2349 run as local lexical validation.
4. Freeze the final method set for thesis comparison.
5. Consolidate or run candidate-budget cost/latency for top-20, top-50, and top-100.
6. Decide whether top-50 or top-100 is the final hybrid candidate budget.
7. Complete failure-mode comparison across the final method set.
8. Run Step 9 downstream validation on the 12-prompt sample.
9. Update thesis LaTeX chapters with final method, result, and failure-analysis tables.

## What Not To Do Yet

- Do not expand beyond 2089 skills as a new controlled benchmark unless final methods make the benchmark too easy or adjudication shows the scale layer is too artificial.
- It is acceptable to expand public skills as background/taxonomy validation if they are clearly separated from controlled gold skills.
- Do not host SkillRouter before trying Qwen and a local SkillRouter smoke test.
- Do not treat provider choice as the thesis contribution.
- Do not add more providers or model variants unless they test a new representation claim.
- Do not tune prompts, gold labels, or schema weights after the final method set is frozen unless the change is logged as a validity correction.
- Do not run Step 9 downstream validation until the field taxonomy, final method set, and candidate budget are chosen.

## Canonical Reference Files

- Benchmark rubric: `skill_benchmark/notes/benchmark_methodology_rubric.md`
- Experiment roadmap: `thesis_notes/Thesis Experiment Roadmap.md`
- Draft final field taxonomy: `thesis_notes/Final Representation Field Taxonomy - Draft.md`
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
