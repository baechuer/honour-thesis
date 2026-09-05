# Final Method Set and Information-Use Plan

Date: 2026-06-03

Purpose: make the method comparison align with the thesis claim: extracted selection information should improve skill selection under semantic similarity and scale.

Update, 2026-06-18: this note is retained as a methodology history and implementation plan. The current canonical framing is `thesis_notes/current/Information Layer Framework.md`. Use "information layer" in thesis prose; use "representation" only for implementation artifacts such as `R1`, `R2`, `R3`, and `RFULL`.

## Core Principle

The thesis is not a leaderboard of BM25, MiniLM, Qwen, or any single provider.

The thesis compares information layers and decision stages:

1. What information about a skill is visible to the selector?
2. How is the first candidate subset generated?
3. Does a reranker use procedural fields to choose among semantically plausible candidates?
4. What accuracy, top-k recall, cost, and failure-mode changes result?

## Information Layers

Use the `I*` labels in thesis prose. The old `R*` labels remain implementation artifacts.

| Information layer | Existing artifact | What It Exposes | Thesis Role |
|---|---|---|---|
| `I1` | `R1` flat skill card | Name, description, family/tags | Current lightweight/progressive-disclosure style metadata. |
| `I2` | `RFULL` complete skill artifact | Full `SKILL.md` text | Strong full-text baseline and SkillRouter-style comparison. |
| `I3` | `R2/R3` extracted fields | Task/use condition, inputs/preconditions, outputs, workflow, dependencies/resources, boundaries | Tests whether retrieval improves when selection-critical information is preserved or extracted. |
| `I4` | planned `R4` relation graph | Similarity, alternative, dependency, composition, belong-to, workflow/prerequisite relations | Tests whether explicit relations help beyond serialized text fields. |
| `I5` | planned tree/DAG | Domain, category, subcategory, task-family, atomic skill grouping | Tests scalable hierarchical narrowing and early branch failure. |

The important comparison is not just `embedding vs BM25`. The important comparison is which information is available (`I1/I2/I3/I4/I5`) under comparable retrieval and reranking settings.

## Selection Information Taxonomy

The thesis should not use "procedural information" vaguely. The current frozen taxonomy is broader and more precise:

| Group | What It Means | Role |
|---|---|---|
| `task` / use condition | What problem the skill is meant for | Primary positive retrieval signal. |
| `input` / precondition | Required source material, file type, task state, or prior context | Primary but often implicit. |
| `output` / artifact | Expected answer, report, rows, patch, chart, plan, or other deliverable | Primary disambiguation signal. |
| `workflow` / procedure | Required operation sequence, evidence handling, validation, anchoring, or reasoning style | Primary disambiguation signal. |
| `dependency` / resource / platform | Required tools, APIs, external files, platforms, or reference resources | Conditional feasibility signal; noisy as plain positive text. |
| `boundary` / not-for | Explicit exclusions, negative scope, or mismatch conditions | Conditional guardrail signal. |
| `hierarchy` / task role | Atomic skill versus broad parent, wrapper, router, installer, or overview skill | Conditional structure signal. |

So the core question is not simply "do inputs and outputs help?" It is: which selection-information groups must survive compression from full skill artifact to selection representation, and how should a retriever or reranker use them?

## Representation Versus Architecture

Keep these two levels separate:

- **Representation:** what information is encoded about a skill.
- **Architecture:** how the selector uses that information to produce candidates or a final rank.

This matters because "structure-aware" can mean several different things:

| Layer | Example | What It Tests |
|---|---|---|
| Structured card | `R2` extracted procedural fields | Whether preserving use conditions, inputs, outputs, workflow, and boundaries helps retrieval. |
| Resource/dependency card | `R3` dependency/resource fields | Whether tools, platforms, files, and external requirements help feasibility or introduce noise. |
| Tree routing | `M4` family/category routing | Whether hierarchical narrowing is efficient or whether early branch choices exclude the gold skill. |
| Graph retrieval | `M5` relational retrieval over `R4` edges | Whether explicit relations among inputs, outputs, tools, workflows, resources, and families help beyond serialized text. |
| Procedural reranking | `M6-v1` field-aware reranking | Whether request requirements can be matched field-to-field against skill representations. |

So graph-based retrieval has not been removed. It is currently a planned relation-aware architecture for `I4`, while `R2/R3/R4` are implementation artifacts it may operate over.

Graph/tree clarification:

- A graph should be used when the additional information is relational: dependency, composition, similarity, alternatives, prerequisite/workflow order, resource links, or belong-to relations.
- A tree/DAG should be used when the additional information is hierarchical grouping: domain, category, task family, and atomic skill.
- An embedding method can use relation or hierarchy information only if that information is serialized into text or learned as features. It does not naturally traverse edges.
- Therefore, graph/tree results must be interpreted as information-layer plus architecture results, not pure model comparisons.

Detailed M4/M5 methodology:

- `thesis_notes/methodology/M4 M5 Structure-Aware Architecture Plan.md`

## Final Method Families

| Role | Method | Uses Extracted Information? | Keep? | Purpose |
|---|---|---:|---|---|
| Normal-agent baseline | `M0` progressive disclosure | No, except flat visible cards | Yes, historical/context baseline | Shows what happens when the main agent sees many compact skill descriptions and decides what to load. |
| Lexical control | BM25/TF-IDF over `R1` | No | Yes, control only | Checks whether exact wording already solves the prompt. If strong, it diagnoses lexical cueing, not a final architecture. |
| Dense card retrieval | Qwen/MiniLM over `R1` | No | Yes | Tests modern semantic retrieval over the same flat metadata. |
| Dense full-artifact retrieval | Qwen/MiniLM over `Full` | Indirectly | Yes | Tests whether full skill text alone is enough, similar to SkillRouter-style evidence. |
| Structured card retrieval | Qwen/TF-IDF over `R2` | Yes, as representation | Yes | Tests whether extracted procedural fields help before reranking. |
| Generic neural reranker | Dense retrieval + Qwen rerank | Only if full text contains it | Yes, strong baseline | Tests whether a modern generic reranker solves the problem without explicit field scoring. |
| Procedural field reranker v0 | Dense/lexical shortlist + current local schema rerank | Yes, weakly | Keep as diagnostic | Current deterministic reranker uses weighted lexical overlap with `use_when`, outputs, preconditions, workflow, and dependencies. Transparent but too crude for final claims. |
| Procedural field reranker v1 | Dense shortlist + field-aware procedural rerank | Yes, explicitly | Build next as `M6-v1` | Proposed main structure-aware method: extract request fields, compare field-to-field, penalize boundary/hierarchy mismatches, and use dependencies conditionally. |
| Tree routing | `M4` route through family/category hierarchy | Yes, if tree nodes expose procedural summaries | Optional diagnostic | Tests efficient scale routing and early branch-exclusion failure. |
| Graph retrieval/reranking | `M5` query matched against `R4` relation edges | Yes, explicitly relational | Optional after `M6-v1` | Tests whether relation structure helps beyond serialized cards. |
| LLM field-aware reranker | Dense shortlist + LLM rerank over extracted field JSON | Yes, explicitly | Optional final method | Stronger but more expensive version of v1. Useful if deterministic v1 underperforms due implicit language. |

Recommended priority:

1. Use field ablations over `R2/R3` to answer **which information helps**.
2. Use `M6-v1` to test whether that information helps when used field-to-field.
3. Add `M5` graph retrieval only if we need to test whether explicit relations improve over serialized structured cards.
4. Add `M4` tree routing mainly as a scalability/failure-mode comparison, not as the central information-discovery method.

## Current Local Schema Rerank: What It Actually Does

The existing `schema_pair_score` is a v0 diagnostic, not the final proposed method.

It scores query-token overlap against these skill fields:

- skill name: weight `0.08`
- flat description: `0.20`
- `use_when`: `0.30`
- output shape: `0.22`
- preconditions: `0.10`
- workflow: `0.06`
- dependency/resource signals: `0.04`
- `not_for` boundary penalty: `-0.12`

This is useful because it is transparent and cheap. But it has limitations:

- It does not extract structured requirements from the user request first.
- It uses lexical overlap rather than semantic field matching.
- It underweights workflow/procedure relative to the thesis claim.
- It can favor skills with many resource/dependency words.
- It does not reliably detect broad parent/router skills.
- It treats public-skill extraction noise as if it were clean schema.

Conclusion: keep local schema rerank as `M6-v0`, but do not present it as the final structure-aware method.

## Proposed Procedural Reranker v1

This is the method that better matches the thesis claim.

Pipeline:

1. First-stage retrieval returns a candidate set, probably top-50 or top-100.
2. A request parser extracts request-side fields:
   - intended action
   - input/precondition
   - desired output artifact
   - workflow/procedure requirements
   - required tools/platforms
   - explicit exclusions or boundaries
   - success criteria
3. The reranker compares request fields to extracted skill fields from `R2/R3`.
4. The final score combines:
   - first-stage retrieval score
   - positive procedural field match
   - output artifact match
   - input/precondition match
   - workflow/procedure match
   - dependency/tool match only when the request makes the dependency relevant
   - boundary and `not_for` penalty
   - broad/hierarchical skill penalty

Suggested scoring shape:

```text
score =
  0.30 * normalized_first_stage_score
+ 0.20 * use_when_match
+ 0.20 * output_match
+ 0.15 * workflow_match
+ 0.10 * input_precondition_match
+ 0.05 * success_criterion_match
+ conditional_dependency_bonus
- boundary_mismatch_penalty
- hierarchy_router_penalty
```

This method directly tests whether the extracted information helps selection. It is stronger than simply embedding `R2` text because it uses the fields as fields.

## Implemented M6-v1 Prototype

Checkpoint:

- `thesis_notes/checkpoints/methods/M6-v1 Field-Aware Reranker Checkpoint - 2026-06-03.md`

Implementation:

- `skill_benchmark/scripts/field_aware_matching.py`
- `skill_benchmark/scripts/run_m6v1_field_aware_reranker.py`

The current implementation should be called `M6-v1-local` or "the deterministic M6-v1 prototype". It is not just the old schema overlap. It extracts request-side fields and compares them field-to-field against skill-side `R2/R3` fields. However, the field matcher is still mostly lexical and transparent, so the thesis should not treat it as the final possible field-aware architecture.

Current controlled result on the active 2401-skill / 137-prompt benchmark:

- Qwen full-skill first stage + `task_output_workflow` field-aware reranking: 78.8% top-1, 92.0% top-5, 0.851 MRR.
- Qwen full-skill + Qwen generic rerank top-20: 62.0% top-1, 75.2% top-5, 0.684 MRR. This is stronger than raw Qwen full-skill embedding but weaker than explicit procedural reranking on controlled confusable cases.
- Candidate R@100 is 93.4%, so remaining errors include first-stage misses and reranker mistakes.
- Adding all fields drops to 73.0% top-1 and increases non-main top-1 to 11.7%, confirming that dependencies, boundaries, and hierarchy are conditional fields rather than simple positive text.

Current public-gold result:

- Public-gold Qwen full-skill + `M6-v1-local` remains weak: best strict top-1 is 53.1%, while candidate R@100 is 96.9%.
- Interpretation: public-gold failures are mostly reranker/extraction/matching failures, not first-stage candidate misses.
- Next improvement should be semantic or LLM-assisted field matching and public-gold cleanup.

## What Results Currently Say

Controlled benchmark:

- Extracted procedural fields help in the controlled benchmark.
- Qwen full-skill retrieval plus local schema rerank improves substantially over Qwen full-skill retrieval alone on the main 2401-skill benchmark.
- Field ablations suggest `use_when`, `output_artifact`, and `workflow_procedure` are the strongest positive fields.
- `M6-v1-local` strengthens this interpretation: task/use condition + output + workflow is currently the strongest controlled Qwen-backed field set, while all-fields scoring hurts.

Public-gold benchmark:

- Public-gold is harder and noisier.
- Qwen full-skill embedding alone performs poorly, suggesting long public artifacts and wrappers can add noise.
- Qwen generic rerank currently performs best on public-gold.
- Current local schema rerank improves top-5 in some R1/R2 provider runs but hurts top-1, which suggests extraction/normalization and field-aware scoring are not mature enough yet.
- `M6-v1-local` also struggles on public-gold top-1 despite high candidate recall. This means public skills need stronger field extraction and semantic field matching before field-aware reranking can be claimed as a public-skill solution.

External skill-router baseline to add next:

- Evaluate `pipizhao/SkillRouter-Embedding-0.6B` and `pipizhao/SkillRouter-Reranker-0.6B` as a domain-specific retrieve-and-rerank baseline.
- Compare it under the same candidate budgets against Qwen full-skill + Qwen rerank and Qwen full-skill + M6-v1-local.
- Interpret this as a strong skill-routing baseline, not as a direct ablation of the proposed field taxonomy. If M6-v1 beats it, explicit field use is promising. If SkillRouter beats M6-v1, the thesis should analyse whether its learned model implicitly captures the same procedural signals.

Thesis interpretation:

> Extracted information is valuable, but only if it is extracted accurately and used with field-aware logic. Naively appending fields or using crude lexical schema overlap is not enough.

## Final Reporting Recommendation

Report methods by class:

1. `M0`: progressive-disclosure baseline.
2. `M1`: lexical flat-card control, BM25/TF-IDF.
3. `M2`: dense flat/full retrieval, Qwen or MiniLM.
4. `M3`: structured-card retrieval over `R2`.
5. `M4`: dense retrieval plus generic neural reranking.
6. `M6-v1`: dense retrieval plus procedural field reranking.

Provider names should be implementation details inside these classes, not the intellectual framing.

## Next Implementation Step

Improve `M6-v1` beyond the deterministic local prototype:

- Keep the fixed information taxonomy.
- Add semantic or LLM-assisted field matching for request fields against skill fields.
- Clean public-gold strict/acceptable/revise labels before reporting public-gold results.
- Add reranker failure categories: first-stage miss, extraction error, semantic field mismatch, broad parent/router skill, and gold ambiguity.
- Evaluate on:
  - controlled 137-prompt benchmark;
  - public-gold strict subset;
  - public-gold gold-or-acceptable subset;
  - implicit-field stress prompts.

Then compare it directly against:

- Qwen R1 embedding;
- Qwen R2 embedding;
- Qwen full-skill embedding;
- Qwen full-skill + Qwen rerank;
- current local schema rerank v0.
