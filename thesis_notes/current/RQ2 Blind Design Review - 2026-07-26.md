# RQ2 Blind Design Review - 2026-07-26

Status: `DESIGN INPUT / SUPERSEDED AS ACTIVE PROTOCOL`. Preserve this memo as an independent perspective, but do not implement it directly. Current authority: `thesis_notes/current/RQ2 Current Status and Implementation Tracker - 2026-07-26.md`.

## Purpose And Independence Boundary

This note preserves an independent experimental-design review requested on 2026-07-26. The contributing Sol agent was deliberately prevented from reading the local thesis, repository, existing RQ2 framing, trackers, methods, result tables, or implementation artifacts. It received only:

- the broad skill-routing problem;
- the completed RQ1 conclusion that use condition, input/precondition, output/artifact, workflow/procedure, dependency/resource, boundary/not-for, and success/verification can distinguish controlled semantic near-neighbours; and
- the observation that naturally authored public skills express these facts jointly, redundantly, and noisily.

It did not inspect any existing methodology. This note records a design proposal for evaluation and discussion. It is not an approved replacement for the thesis methodology and no experiment was launched from it.

## Independent Proposed Research Question

> Do explicit representations of operational facts improve skill reranking in realistic, noisy public-skill collections beyond what is achieved by full skill documents and equally concise unstructured summaries?

The proposed causal claim is deliberately narrow: given the same candidate set, model, information budget, and scoring protocol, an operational-fact representation may improve selection among compatible and semantically close skills. It does not claim universal superiority across models or corpora, first-stage retrieval improvement, independent causal effects of fields in natural documents, or a complete production routing architecture.

## Independent Primary Experiment

The proposal makes reranking, rather than full-corpus retrieval, the primary experiment. Each fixed candidate set contains the labelled gold skill, operationally incompatible near-neighbours, and unrelated distractors. The same query, candidate order randomisation, reranker, prompt template, decoding settings, and candidate-set size are used for every condition.

| Condition | Selector-visible candidate form | Main interpretation |
|---|---|---|
| Full document | Complete original skill text. | Whether natural full artifacts are sufficient. |
| Token-matched prose summary | Concise unstructured description at the approximate information budget of the fact representation. | Whether compression alone explains a gain. |
| Fielded operational facts | Use condition, input, output, workflow, dependency, boundary, and verification fields. | Whether explicit operational facts are selector-usable. |
| Flattened facts | The same extracted fact values without labels or field boundaries. | Whether field organisation adds value beyond the values themselves. |
| Full document plus facts | Full artifact plus an explicit fact card. | Whether explicitness adds value when raw information is retained. |

The intended headline contrast is fielded facts versus token-matched prose summary on hard near-neighbour candidate sets. Flattened facts are a crucial control: I1 versus I3 alone confounds information quantity with explicit organisation.

## Diagnostics Suggested By The Independent Design

- Field-label removal while retaining the same fact values.
- Leave-one-field-out ablations. In natural public skill artifacts, these are incremental-value diagnostics, not single-field causal proofs.
- One-field swaps/corruptions as an RQ2 robustness diagnostic only; they are not the main RQ1 test.
- Manual correction of a stratified subset of automatically extracted cards to estimate extraction-fidelity effects.
- An end-to-end secondary evaluation applying the selected reranker to candidate sets returned by one fixed first-stage retriever.
- Queries and gold labels created independently of fact extraction; record acceptable alternatives and `none applicable` where appropriate.

## Proposed Measurements

Primary metrics:

- Top-1 accuracy;
- MRR and Recall@3/5 or nDCG where multiple/graded relevance is appropriate;
- near-neighbour accuracy.

Secondary metrics:

- false-positive rate for explicitly incompatible skills;
- acceptable-alternative and abstention/`none applicable` accuracy;
- latency, reranker input tokens, and estimated inference cost;
- extraction fidelity by field;
- performance by ambiguity, document length, missing fields, candidate similarity, and source family.

The design recommends paired comparisons because every query is observed under every representation. Effect sizes and paired confidence intervals are more important than unpaired leaderboard-style claims.

## Suggested Scope

Minimal honours-scale version proposed by the agent:

- 150--250 public skills;
- 250--400 independently authored task queries;
- 5--10 candidates per query;
- one embedding retriever and one frozen LLM reranker;
- all four core representation conditions;
- field ablations for the seven RQ1 groups;
- manual extraction correction for approximately 20\% of skills; and
- one held-out repository or skill family.

This exact scale is a suggestion, not a committed thesis target. Existing public-gold prompts, acceptable alternatives, and annotation records should be audited before authoring new prompts. Any new human annotation or survey-like activity requires supervisor and ethics review before it is treated as research evidence.

## Graph/Tree Assessment

The independent design recommends that graph/tree methods are not central to this RQ2. They add new hypotheses about hierarchy construction, relation quality, traversal, and error propagation. A single-skill routing benchmark is also not naturally suited to proving composition or dependency-graph benefits. Graph/tree work may later become a separate RQ or a narrow extension for multi-skill, prerequisite, or composition tasks.

## Novelty Position

The novelty is not a new structured skill representation, retrieve-rerank pipeline, hierarchy, or graph. The defensible contribution is a field-grounded evaluation: operational distinctions first isolated in RQ1 are tested for incremental usefulness under naturally redundant skill artifacts through matched-compression, flattened-fact, ablation, extraction-fidelity, and near-neighbour controls.

## Comparison With The Existing Direction

The independent proposal converges with the current information-led thesis in one important respect: it treats RQ1 as the foundation for RQ2 and does not recommend graph/tree as an immediate core method.

It differs in emphasis:

| Current broad direction | Independent proposal |
|---|---|
| Full-corpus information-layer and retrieval matrix is central. | Fixed-candidate reranking is central, so first-stage recall cannot obscure the representation effect. |
| I1/I2/I3 contrasts are useful but can confound information quantity, formatting, and retriever. | Full, matched summary, fielded facts, and flattened facts explicitly separate these explanations. |
| Candidate recall, latency, and system cost appear in the main comparison. | They are a secondary end-to-end systems validation after the primary representation test. |
| Graph/tree remained possible RQ2 methods. | Graph/tree should be deferred unless the benchmark changes to relation-sensitive multi-skill routing. |

## Synthesis To Discuss Before Any Change

A potentially clearer thesis structure is:

1. **RQ1:** Which operational information distinguishes semantic near-neighbours under controlled conditions?
2. **RQ2a, primary causal representation study:** Given the same candidate set and information budget, does an explicit operational-fact representation help a fixed reranker distinguish naturally authored skills beyond full text, concise prose, or flattened facts?
3. **RQ2b, secondary systems study:** When the candidate set is not guaranteed, how do information layers and first-stage/re-rank pipelines trade off candidate recall, final ordering, selector-visible context, latency, and amortised cost?

This is a proposed restructuring for discussion only. It should not be inserted into the thesis or used to schedule reruns until the literature-overlap check, current-result provenance audit, and supervisor-facing scope decision are complete.
