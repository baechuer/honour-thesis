# Thesis Experiment Roadmap

Date: 2026-05-28

This file is the operational roadmap for the thesis experiments. It exists to prevent drift.

The thesis is not a provider leaderboard and not a search for every possible retrieval architecture. The thesis asks:

**RQ1:** What information must agent skill representations preserve to distinguish semantically similar but procedurally distinct skills at scale?

**RQ2:** How do retrieval strategies that use flat text, dense embeddings, structured procedural fields, or hybrid reranking differ in accuracy, efficiency, and failure modes when applied to scalable skill libraries?

All experiments should connect back to these two questions.

## Current Position

We are past benchmark construction, initial selector comparison, and the first 2000-scale expansion. The next work should consolidate evidence, audit real public skill artifacts, and test field ablations rather than keep expanding method families.

Important scale clarification:

> The active 2089-skill benchmark now tests both semantic/procedural scale and a near-context-limit condition for compact metadata/progressive-disclosure systems. R1 flat metadata is about 105k selector-visible tokens, while full skill artifacts exceed 1M selector-visible tokens. See `thesis_notes/Scale Expansion 2089 Validation.md`.

Current strongest finding:

> Dense retrieval is useful for broad candidate generation, but final skill selection benefits from explicit procedural information. On the active 2089-skill benchmark, M6 MiniLM full-skill retrieval plus local schema reranking reaches 82.3% full-library top-1, while Qwen full-skill retrieval plus local schema reranking reaches 84.7% top-1. Qwen's generic reranker reaches only 63.5%, which strengthens the claim that procedural reranking matters.

Current main risk:

> The project may drift into testing more providers or architectures without improving the thesis answer about representation information.

Current validity risk:

> The controlled benchmark exposes clean procedural fields because we authored those skills. Before final claims, we must check whether similar information exists or is extractable from real public skills. If some fields are usually absent, frame them as representation-layer normalization targets rather than assuming skill authors already provide them.

## Frozen Unless Broken

These should not be changed unless a validation failure is discovered:

- Main evaluated prompt set: 85 prompts, with the original 67 retained as the v1 historical subset.
- Core distinction: skill artifact vs selection representation vs retrieval policy.
- Current RQs.
- Main benchmark purpose: semantic confusability plus procedural distinctness.

Main 2089-skill scale is the current active condition. The 1006-skill condition remains historical comparison for older local and provider results.

Allowed small changes:

- Add acceptable alternatives where manual adjudication shows a near-equivalent skill is genuinely acceptable.
- Fix a prompt or skill only if gold-label stability fails.
- Add a note explaining a limitation instead of endlessly rebuilding the benchmark.
- Add more public/generated scale only if manual adjudication shows the current 2089-skill condition is not enough. Current priority is adjudication, not further expansion.

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

Status: Mostly complete, but needs final selection.

Purpose:

Choose a small final set of methods that represent different information conditions. This is the experimental backbone of the thesis.

Required final methods:

| Role | Method | Why keep it |
|---|---|---|
| Normal-agent baseline | M0 progressive disclosure, core only | Represents current practical main-agent selection behavior. |
| Flat lexical baseline | M1 BM25 or TF-IDF over flat metadata | Tests compressed metadata without neural semantics. |
| Dense retrieval baseline | M2 full-skill embedding, local or Qwen | Tests whether exposing the full artifact to embeddings helps. |
| Structured baseline | M3 schema retrieval | Tests procedural fields directly. |
| Generic neural rerank baseline | Qwen embedding plus Qwen rerank | Tests whether a stronger generic retriever/reranker solves the problem. |
| Hybrid representation method | Qwen full-skill embedding plus local schema rerank | Tests semantic candidate generation plus procedural final selection. |

Optional methods:

- M4 tree routing.
- M5 graph retrieval.
- SkillRouter.
- Additional providers.

Decision rule:

Optional methods are only worth adding if they test a new representation claim. They are not worth adding just because they might improve top-1.

Definition of done:

- Final method table is frozen.
- Each method has a one-sentence thesis role.
- Each method reports top-1, top-5, MRR, non-core top-1, candidate budget, and cost/latency if available.

## Phase 2b: Real-World Skill Audit and 2000-Scale Condition

Status: Partly implemented. The 2089-scale condition and public imports are done; the public-skill field audit is not done.

Purpose:

Use public skills to check whether our proposed representation fields correspond to information found in real skill artifacts, then create a larger scale-sensitivity condition.

Required evidence:

- Public imported skills are stored separately from generated background and controlled core skills.
- Source URL and import status are recorded.
- A field audit reports which public skills contain descriptions, inputs, outputs, workflow steps, dependencies, resources, examples, limitations, and negative boundaries.
- The audit classifies each field as `observed`, `extractable`, or `proposed normalization`.
- Controlled core expansion is kept modest. Current expansion is 67 to 85 evaluated cases, with old 67-case results remaining comparable.
- The 2089-skill condition uses 85 prompts and gold labels.
- Non-core public winners are manually inspected for whether they are better, acceptable, or only plausible distractors.

Definition of done:

- The thesis can say the representation fields are not only invented from our generated benchmark, but are motivated by literature and checked against public skill artifacts.
- The thesis can separately report results on the original 67-case core and the expanded 85-case core.
- 1006 vs 2089 results are compared as scale sensitivity where historical results are available.
- Gold-label stability remains defensible after public imports.

See `thesis_notes/Real World Skill Expansion Plan.md`.

## Phase 2c: Representation Field Ablation

Status: Executed on 2026-05-29.

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

Status: Next required phase.

Purpose:

Decide whether the strongest hybrid method is practical, especially at top-100 candidate budget.

Required comparisons:

- Qwen full embedding plus local schema rerank at top-20, top-50, top-100.
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

1. Run the public-skill field audit over imported public skills.
2. Run representation field ablations.
3. Freeze the final method set for thesis comparison.
4. Decide whether to run full 2089-skill M0 as a context/cost stress test or only report the context-scale audit.
5. Run or consolidate candidate-budget cost/latency for top-20, top-50, and top-100.
6. Decide whether top-50 or top-100 is the final hybrid candidate budget.
7. Complete failure-mode comparison across the final method set.
8. Run Step 9 downstream validation on the 12-prompt sample.
9. Update thesis LaTeX chapters with the final results.
