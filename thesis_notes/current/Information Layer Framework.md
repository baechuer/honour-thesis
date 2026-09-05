# Information Layer Framework

Last updated: 2026-08-01

> **2026-08-28 RQ1b execution amendment.** The active natural public-artifact
> extension of RQ1 is a source-grounded field-card availability ablation, not
> a claim that one raw-document field uniquely determines selection. It masks
> a field type across every candidate card, measures paired gold-versus-neighbour
> routing effects with simple first-stage selectors, and records cross-field
> redundancy. The exact scope and limits are frozen in
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Public Field-Type Ablation Protocol - 2026-08-28.md`.
> Its six-family validation pilot passed all applicable local construction and
> preservation gates. No RQ1b selector result exists: no selector, embedding,
> retrieval metric, API call, or external transfer was run in the pilot. The
> hash-audited non-pilot C6 input corpus (193 paired strict routing families;
> 386 prompts; 74 unique candidate compositions) is built. Source cards and
> masks are constructed once per composition, then reviewed per prompt family.

> **2026-08-15 RQ2 status.** RQ1a remains the locked reviewed fact source. RQ2a is complete, user-reviewed, thesis-integrated, and not reopened by the native encoder replication. RQ2b's base-v1 B0G audit completed mechanically but its acceptable-set freeze is `BLOCKED BEFORE RETRIEVAL`: it resolves 7,710 units yet finds 14 strict-gold rows not fully acceptable and eight prompts without a fully acceptable reviewed candidate. This is a benchmark-validity finding, not evidence about an information layer or retriever. A user-directed review of only those 14 cases retains six gold label skills and excludes eight material workflow mismatches; its strict-gold-only v1.1 manifest is locally validated, not an acceptable-set repair. B1R and all scientific execution remain separately unauthorised. Earlier architecture-led experiments remain historical/exploratory.

Status: current canonical thesis framing. This note supersedes the earlier representation-layer-first framing, while preserving the old `R*` and `M*` labels as implementation labels for existing experiments.

Canonical I3 model-extraction protocol: `thesis_notes/current/I3 Model Extraction Protocol.md`.

Detailed RQ1 test-unit design: `thesis_notes/current/RQ1/protocols/RQ1 Field Targeted Test Plan.md`.

## Why This Reframe Exists

Earlier notes often framed the thesis as a comparison between representation architectures such as embeddings, structured cards, graph retrieval, tree routing, and rerankers. That framing was too architecture-led. The current thesis should be information-led:

> The central object of study is the information a skill selector needs in order to distinguish semantically similar but procedurally different skills under scale.

Embeddings, rerankers, graph traversal, tree routing, and progressive disclosure are retrieval or encoding strategies. They are ways of using information, not the information itself.

## Current Research Questions

**RQ1:** Which operational information types help distinguish semantically similar but procedurally distinct agent skills?

**RQ2:** How do skill representation and retrieval-pipeline choices affect the preservation and use of the routing-relevant operational information identified in RQ1 under semantic confusability, and what accuracy, candidate-recall, and retrieval-cost trade-offs result?

These replace the older phrasing that centered "flat metadata vs embedding vs structure-aware methods" as the primary contrast. That older phrasing is now interpreted as an implementation-level comparison under the broader information-layer question.

Current priority: preserve the reviewed RQ1a field suites and implement RQ2a. RQ2a holds the query, candidates, and reviewed propositions fixed while varying their representation and use. RQ2b is only a draft for later end-to-end full-library validation. Graph, tree, DAG, relation-aware, and downstream-execution studies are not part of the current active implementation.

Active RQ1 split:

- **RQ1a:** individual field discriminability under controlled shared context.
- **Supporting RQ1b audit:** field prevalence and recoverability in controlled, public-gold, and external skill corpora.
- **RQ1b-N:** a frozen public-original source, prompt, strict-label, and cue-risk frame. It supplies natural artifacts, not a raw-document causal mask claim.
- **RQ1b-A:** a source-grounded field-card availability ablation. It holds the public candidate set and prompt fixed, withholds one field type across every candidate, and measures conditional routing separation plus residual redundancy. Its six-family local instrument-validation pilot passed; non-pilot C6 corpus construction is now in progress, with no selector result yet. Protocol: `RQ1b Public Field-Type Ablation Protocol - 2026-08-28.md`.
- No RQ1c is currently defined. Combined reviewed facts are used as matched-content RQ2a treatments, not as a new RQ1 result. Graph/tree grouping remains outside the core because it introduces relation or hierarchy information not isolated by RQ1.

Current RQ2 operational sources:

- `thesis_notes/current/RQ2 Current Status and Implementation Tracker - 2026-07-26.md`;
- `thesis_notes/current/RQ2 Comprehensive Methodology Specification - 2026-07-26.md`.

Outdated wording to avoid: "all strategies use the same information" or "graph/tree are just another representation of I3." Some strategies may use the same operational information as I3 after serialization; others organize different routing-relevant signals such as grouping, dependency, provenance, or relation edges. Report those assumptions explicitly for each method.

## Main Claim Boundary

Do not claim that explicit structured fields are the only possible solution.

A defensible claim is:

> If task, input, output, workflow, dependency, boundary, or success/verification information is retrieval-critical, a scalable skill system must make that information available somewhere: through author-provided metadata, deterministic parsing, LLM-assisted extraction, learned encoders/rerankers, or full-artifact retrieval.

This means the thesis can argue that these operational information types are important without claiming that every system must store them as literal JSON fields. Fields are one explicit, inspectable, and relatively cheap normalization strategy. Learned models may encode similar information implicitly, but then the thesis should test whether explicit extraction improves accuracy, robustness, interpretability, or cost. Relation and hierarchy information remain RQ2 strategy directions until their exact carried information is specified.

## Axis 1: Information Layers

Use `I*` names in thesis prose. Existing code may still use `R*` names.

| Information layer | Existing artifact label | Information made selector-visible | Main question tested |
|---|---|---|---|
| `I0` progressive disclosure | `R0` / M0 traces | Names, descriptions, metadata in the main agent context; full docs loaded only after selection. | How current small-library skill loading behaves and why it scales poorly. |
| `I1` flat skill card | `R1` | Name, short description, family/category, tags. | Is compact metadata enough for near-neighbour skill selection? |
| `I2` full skill artifact | `RFULL` | Entire source skill body. For controlled skills this is the authored top-level `SKILL.md`; for imported public-gold targets it should be the upstream public `source/SKILL.original.md`. | Does raw full text contain enough signal, and at what noise/cost? |
| `I3` structured selection fields | `R2` / parts of `R3` | Task/use condition, input/precondition, output/artifact, workflow/procedure, boundary/not-for, dependency/resource, success/verification criteria where available. | Which operational information fields help distinguish confusable skills? This is the near-term RQ1 focus. |
| `I4` skill-relation information | planned `R4` | Candidate relation carriers such as input-to-output direction, workflow order, dependency/resource links, alternatives, composition, provenance, or similarity. Exact thesis-facing edge schema is TBD. | Do explicit relations organize routing-relevant information better than serialized fields for relation-sensitive prompts? |
| `I5` hierarchy/grouping information | planned tree/DAG | Candidate grouping carriers such as domain, task family, capability family, coarse-to-fine branch summaries, and atomic skill grouping. Exact thesis-facing tree/DAG schema is TBD. | Does hierarchical narrowing reduce search cost while preserving branch recall? |

Important: these layers are not a strict ladder where each method must use every layer, and they are not all required to carry the exact same information. For RQ1, the controlled comparison should hold the skills, prompts, and retriever fixed while varying operational fields inside an RQ1 test unit: fixed explicit prompt, near-neighbour skill pair/cluster, shared neutral skill-side context, target field value, exact evidence, and fixed retriever/metric. For RQ2, complete strategies may preserve or organize routing-relevant information differently; those assumptions must be reported rather than hidden.

## I3 Extraction Provenance

`I3` is an information layer, not one fixed extraction method. Use these suffixes when extraction provenance matters:

| Label | Meaning | Current status |
|---|---|---|
| `I3H` | Heuristic/section-based extraction from headings, explicit fields, and conservative sentence cues. | Current frozen-v0.4 local and SkillRouter-Eval-Core first-pass condition. |
| `I3V` | Model-assisted verification that a field exists, usually with evidence spans, but not necessarily used as the retrieval representation. | Done for the 460 imported public skills via DeepSeek-assisted audit. |
| `I3M` | Paid-provider model-parsed structured selection representation. | Local full-library DeepSeek/API run complete for 2433 skills; artifact: `skill_benchmark/representations/I3M_model_parsed.jsonl`. External SkillRouter-Eval-Core rows `0-2999` complete as an extraction-quality pilot. Treat I3M as a pass/feasibility attempt, not the headline route. |
| `I3C` | ChatGPT/Codex-subagent parsed structured selection representation, produced without a paid provider extraction API. | External SkillRouter-Eval-Core rows `3000-5999`, the 3284-row top-20 task-relevant pool, and the full 79,141-row Hard-tier `all_I2` library are complete and cleaned under the V2 prompt. Full-tier external I3C FTS/BM25 retrieval has been run. Local frozen-v0.4 I3C has not yet been produced. |

This distinction matters because the current `I3H` result tests a cheap deterministic extraction layer. Local `I3M` should not be silently merged with `I3H` or relabelled as `I3C`, because it was produced through a paid model route. `I3C` is useful because it tests whether the same seven-field information layer can be recovered by an interactive ChatGPT/Codex-style parser. Current external I3C V2 extraction and FTS retrieval QA are strong enough to support external verification claims, but I3C is still an `I3` field representation: it has not been converted into `I4` relation edges or `I5` hierarchy/tree structure.

## Axis 2: Retrieval And Encoding Strategies

| Strategy | What it consumes naturally | How it can use other information | Main failure mode to measure |
|---|---|---|---|
| Progressive disclosure | `I0` compact metadata in main-agent context | Cannot scale to all skills without context pressure. | Context overload, missed full-doc activation, expensive main-agent reasoning. |
| Lexical retrieval | Textual `I1`, `I2`, serialized `I3` | Relations/hierarchy must be serialized as text. | Keyword cueing, lexical leakage, poor paraphrase handling. |
| Dense embedding retrieval | Textual `I1`, `I2`, serialized `I3` | `I4/I5` can be converted into textual relation summaries, but embeddings do not natively traverse edges. | Semantic near-neighbour confusion and weak procedural ordering. |
| Learned reranking | Candidate text from `I1`, `I2`, or serialized `I3/I4` | Can implicitly learn which fields matter if those fields are present in the input. | Opaque use of cues, provider/name bias, cost, and candidate recall dependence. |
| Field-aware reranking | `I3` structured fields | Can use relation/hierarchy features as conditional bonuses or penalties. | Field extraction errors, over-weighting irrelevant fields, query underspecification. |
| Tree routing | `I5` hierarchy | Can attach summaries from `I1/I3` to branch nodes. | Early branch-exclusion failure; multi-domain skills do not fit one path. |
| DAG/graph retrieval | `I4` relations and `I5` grouping | Can seed from lexical/dense retrieval, then expand through relation edges. | Bad edge construction, relation over-generation, too many candidates after expansion. |
| Hybrid retrieval | Any combination | Usually dense/lexical seeding plus reranker or graph expansion. | Confounded attribution unless candidate source, information layer, and reranker are reported separately. |

## Why Graph/Tree Are Not The Same As Fields

Graph and tree methods should not be treated as merely another "representation" row that competes with embeddings. They organize routing-relevant information differently:

- graphs are best for relations such as dependency, composition, similarity, alternatives, prerequisite order, and resource links;
- trees are best for coarse-to-fine grouping, taxonomy, and scale reduction;
- fields are best for selector-visible attributes of one skill: task, input, output, workflow, dependencies, and boundaries.

Therefore, the fair comparison is not "embedding versus graph" in the abstract, nor is it automatically "I3 fields versus the same fields in graph form." The fair comparison is:

1. What information is available?
2. How is that information encoded for a method?
3. Does that method improve candidate recall, ranking, cost, or failure-mode attribution?

For now, graph/tree information design should be marked as planned/TBD. The active thesis work should not depend on graph/tree results until their information assumptions and leakage controls are explicitly specified.

## Current Benchmark Freeze

Active benchmark: `benchmark-v0.4-2026-06-16`.

Frozen inputs:

- 245 controlled prompts.
- 144 public-gold prompts.
- 12 low-information stress prompts.
- 2433 skills.

Freeze rule:

- Do not edit prompt files, gold labels, or skills for results reported under `v0.4`.
- If a gold-label or skill-definition error is discovered, create a new benchmark version.
- Low-information prompts remain a separate stress stratum and should not be merged into headline controlled/public-gold accuracy.

## Experimental Steps

### Step 1: Validate Benchmark Inputs

Done for frozen v0.4.

Done criteria:

- 100% prompt references resolve.
- Gold skills and alternatives exist.
- Public-gold targets are present in the full library.
- No duplicate prompt IDs.

### Step 2: Validate Procedural Distinctions

Done for frozen v0.4, with recorded residuals.

Done criteria:

- Each headline prompt has a defensible gold label.
- Gold and alternatives differ on at least one concrete axis: task/use condition, input/precondition, output artifact, workflow/procedure, dependency/resource, constraint/boundary, or success criterion.
- Human-readable rationales exist or can be produced for representative examples.
- Ambiguous alternatives are recorded as acceptable alternatives rather than hidden false positives.

### Step 3: Validate Semantic Confusability

Done for frozen v0.4.

Done criteria:

- Alternatives are semantically plausible, not random negatives.
- Cheap or embedding-based selectors sometimes confuse gold and alternatives.
- At least two plausible near-neighbour alternatives exist for most main prompts.

### Step 4: Freeze Information Layers

Done for `I1`, `I2`, `I3H`, local paid-model `I3M` feasibility, and external SkillRouter `I3C`; not done for local frozen-v0.4 `I3C` or `I4/I5`.

Done criteria:

- `I1`, `I2`, and `I3` are fully exported and documented.
- If `I3M` is discussed, label it as the paid-provider feasibility attempt and record the exact prompt, schema version, model, provider, temperature, JSON mode, input truncation rule, and cache key.
- If local `I3C` is used for final local reruns, create a distinct Codex/ChatGPT-style artifact first; do not reuse or relabel `I3M_model_parsed.jsonl`.
- `I4` relation schema is specified before graph experiments.
- `I5` hierarchy schema is specified before tree/DAG experiments.
- The thesis states how each layer is obtained: authored field, deterministic parse, LLM-assisted extraction, learned latent encoding, or relation construction.

### Step 5: Run Information-Layer Ablations

Done for the audited frozen-v0.4 `I1/I2/I3` method families; interpretation and thesis integration remain.

Done criteria:

- At least one fixed retrieval strategy compares `I1` vs `I2` vs `I3` on the same prompt stratum and skill library.
- Candidate recall, top-1, top-5, and MRR are reported.
- Controlled and public-gold strata are reported separately.
- Results are interpreted as information-layer effects only when model, candidate budget, and reranker are held fixed.

### Step 6: Run Retrieval-Strategy Comparisons

Done for the audited frozen-v0.4 `I1/I2/I3` method families; not done for `I4/I5`, M0, or downstream task execution.

Done criteria:

- For each headline strategy, record information layer, first-stage retriever, reranker, candidate budget, scoring rule, and model settings.
- Compare rerankers only when the candidate set and budget match.
- Report whether a failure is first-stage candidate miss or reranker ordering error.

### Step 7: Implement Relation And Hierarchy Tests

Not done yet.

Done criteria for `I4/M5` graph:

- Define edge types before running graph retrieval: `similar_to`, `belong_to`, `depend_on`, `compose_with`, `alternative_to`, and optional workflow/prerequisite edges.
- Explain how edges are produced: deterministic field match, embedding-neighbour proposal plus validation, or manual/public metadata.
- Compare graph retrieval against a text baseline that has access to a serialized version of the same relation information where feasible.
- Report candidate recall and whether graph expansion recovered semantically distant but functionally necessary skills.

Done criteria for `I5/M4` tree or DAG:

- Define hierarchy levels before running: domain, subdomain, task family, atomic skill.
- Measure branch recall: whether the gold skill remains reachable after top-1/top-3/top-5 branch routing.
- Report early branch-exclusion failures separately from final reranker errors.
- Prefer DAG over strict tree when a skill naturally belongs to multiple dimensions.

### Step 8: Scale And Cost Analysis

Partly done for context-size estimates; not complete for final cost/latency.

Done criteria:

- Report skill count, selector-visible token count, candidate budget, API/local runtime, and API call count where available.
- Separate cost of first-stage retrieval, reranking, field extraction, and main-agent full-doc loading.
- Do not claim a method is cheaper unless the cost components being compared are specified.

### Step 9: Failure-Mode Analysis

First-pass done for the main R2/I3 comparisons; per-source-family public-gold analysis and thesis examples remain.

Done criteria:

- Group errors into: representation loss, candidate-recall miss, reranker ordering error, field-extraction error, relation/hierarchy error, provider/name cueing, public-skill messiness, low-information query ambiguity, and unstable gold label.
- Provide representative examples in the thesis.
- Low-information prompts are treated as clarification/query-understanding stress tests, not forced top-1 headline results.

## Current Progress Summary

Done:

- Frozen v0.4 benchmark exists.
- Controlled and public-gold validation gates pass with caveats.
- Public skill audit supports the claim that many proposed fields are observed or extractable in public skills.
- `I1`, `I2`, and heuristic `I3H` have been tested with lexical, Qwen, SkillRouter, generic reranker, and field-aware methods.
- The consolidated `I1/I2/I3` information-layer matrix exists with candidate recall@20, bootstrap top-1 confidence intervals where available, and paired McNemar tests for fixed-method layer comparisons.
- First-pass failure-mode comparison exists for the main R2/I3 Qwen, SkillRouter, and SkillRouter+M6-v1 conditions.
- M6-v2 no-rewrite semantic field matcher exists as a diagnostic of field signal.
- SkillRouter-Eval-Core external validation has been downloaded and converted into I1, I2, and heuristic I3H; first FTS/BM25 external matrix has been run.
- SkillRouter-Eval-Core I3C V2 extraction is complete for the top-20 task-relevant pool and the full 79,141-row Hard-tier library, and full-tier FTS/BM25 external I3C retrieval has been run.

Partly done:

- Thesis integration of information-layer ablations across `I1/I2/I3`.
- Per-source-family and representative-example failure-mode analysis.
- Cost/context estimates.
- Public-gold per-source-family analysis.
- Statistical reporting beyond first-pass top-1 confidence intervals and McNemar tests, especially paired MRR/top-k if selected for final tables.

Not done:

- Public-gold original-source rerun. Existing public-gold `full` / `RFULL` rows that loaded normalized public wrappers are historical until rerun against upstream `source/SKILL.original.md` files.
- True local frozen-v0.4 `I3C` extraction and reruns. The existing local `I3M_model_parsed.jsonl` is the paid DeepSeek attempt and should not be used as I3C.
- External SkillRouter-Eval-Core fixed-candidate I3C reranking/selection over top-20/top-50 candidate pools, if needed. Full-tier FTS/BM25 I3C has been run.
- `I4` relation schema and graph retrieval.
- `I5` hierarchy/tree or DAG routing.
- Full-scale M0 progressive-disclosure rerun.
- Downstream task-success validation.
- Final cost/latency model.

## Current Decision Rules

- Use `information layer` in thesis prose.
- Keep `representation` only when referring to implementation artifacts such as `R1_flat_metadata.jsonl`.
- Do not present graph/tree as central unless they test `I4/I5` information that `I1/I2/I3` cannot represent cleanly.
- Do not present field-aware methods as final winners unless results hold under frozen weights or held-out selection.
- Do not merge low-information stress prompts into headline controlled/public-gold metrics.
- Do not add more methods unless they answer a new information-layer or retrieval-strategy question.
