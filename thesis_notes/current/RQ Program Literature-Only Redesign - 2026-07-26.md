# Literature-Only RQ Programme Redesign (2026-07-26)

Status: `DESIGN INPUT / SUPERSEDED AS ACTIVE PROTOCOL`. Preserve this memo as an independent perspective, but do not implement it directly. Current authority: `thesis_notes/current/RQ2 Current Status and Implementation Tracker - 2026-07-26.md`.

## Purpose and independence boundary

This memo records an independent design critique requested on 26 July 2026. The reviewer was permitted to read **only** the introduction and literature-review chapters:

- `thesis_latex/chapters/01_introduction.tex`
- `thesis_latex/chapters/02_literature_review.tex`

It was expressly prohibited from reading local methodology, results, benchmarks, experiment trackers, datasets, scripts, or the existing implementation. It could browse external literature. The reviewer was asked to reconsider the research-question programme from first principles, including replacing the questions if appropriate.

## Reviewer memo

### Executive judgement

Retain the field-level theme of RQ1, but replace the current omnibus RQ2. It presently conflates information content, representation, retrieval, reranking, architecture, scale, cost, and failure analysis. The strongest honours thesis is a three-question causal chain:

> What information matters -> how it should be exposed -> whether a practical router can use it under confusability and scale.

The proposed central claim is: reliable routing among near-neighbour skills is first an information-adequacy problem, then a representation problem, and only then a retrieval-architecture problem.

### Proposed research questions

**RQ1: Operational evidence.** Which operational information types causally improve routing among semantically similar but procedurally distinct single skills, and when is the user request sufficiently specified for those signals to determine a correct route?

Study six principal fields: input/precondition, output artifact, workflow/procedure, dependency/resource, boundary/exclusion, and success/verification criterion. Treat a general “when to use” or intent summary as a positive control because it can simply restate the answer; treat setup snippets, examples, and background explanation as execution-support controls.

**RQ2: Representation and dilution.** How do explicit field organisation and information dilution affect selectors’ ability to exploit the routing signals identified in RQ1?

This asks about encoding, not competing architectures. It separates the value of the facts from the value of labels, ordering, compression, and reduced noise.

**RQ3: Pipeline generalisation.** Do RQ1-informed compact representations improve retrieve-then-rerank routing on held-out authored skill clusters as semantic confusability and irrelevant library size are varied independently, and at what retrieval and context cost?

RQ3 is the external-validity and systems test. Failure modes and costs should be analyses across all three RQs, not additional research questions.

### Proposed experiment programme

#### RQ1: Field-isolated causal benchmark

Construct controlled clusters of four skills that share topic, purpose, style, and non-target fields but differ on exactly one operational dimension. Example: four PDF-table skills differ only in required input state, output artifact, or verification standard.

For every cluster, create three query conditions:

- **Explicit:** states the decisive requirement.
- **Paraphrased:** preserves the requirement without lexical copying.
- **Underspecified:** omits it, making a unique route unjustified.

Cross these with four representation conditions:

- Common topical description only.
- Discriminating field only: a sufficiency test.
- Complete canonical card.
- Complete card with the discriminating field masked: a necessity test.

Use one preregistered, frozen primary selector and one architecturally different replication selector, plus a small blinded human ceiling. Randomise candidate and field order. Match candidate length and lexical overlap.

The reviewer suggests about 15–20 independent clusters per field (90–120 clusters overall), after a small pilot and power calculation. The cluster, rather than repeated model calls, is the inference unit. Underspecified cases must use set-valued relevance labels or “insufficient information / clarification required”, never an arbitrary single gold label.

#### RQ2: Same facts, different interface

Reuse held-out RQ1 clusters and freeze the underlying propositions. Compare:

- canonical, unlabelled prose;
- typed field card containing the same propositions;
- typed card with counterbalanced field ordering;
- the same decisive evidence embedded in increasing amounts of neutral execution text.

The flat-versus-typed comparison should be content- and approximately token-matched. The dilution experiment should add the same class and amount of irrelevant text to every candidate, with length-matched candidates inside each condition.

Use a fixed dense matcher and a fixed listwise or cross-encoder selector. The reviewer recommends manually verified “oracle” cards for the primary representation experiment, separating representation from extraction error.

#### RQ3: Authored skills and nested candidate pools

Build a separate natural benchmark of roughly 50–80 human-adjudicated near-neighbour clusters from public authored skills. Use held-out repositories or capability families. Query writers should not copy source wording; functionally equivalent skills should receive set-valued relevance labels.

Cross:

- representation: name + description, full body, and the RQ2-selected compact representation;
- first stage: BM25 and one frozen dense retriever;
- reranking: absent versus one fixed reranker;
- unrelated pool size: e.g. 50, 500, and full corpus;
- near-neighbour count: e.g. 0, 2, and 4 procedurally plausible distractors.

Vary pool size and near-neighbour count independently. If operational cards are automatically extracted, compare raw extracted cards against human-corrected cards; audit field precision/recall, unsupported additions, and omissions.

### Claimed contribution and novelty boundary

The defensible contribution is **causal separation**, not a universal schema or a state-of-the-art router:

1. A counterfactual near-neighbour benchmark in which one operational routing distinction changes at a time.
2. Estimates of each field’s sufficiency, incremental value, and dependence on query specification.
3. A matched-content test of whether typed organisation helps beyond merely adding text.
4. A decomposition of large-library performance into candidate-generation recall, conditional reranker success, and final routing accuracy.
5. Evidence separating near-neighbour density from unrelated-pool size.

Closest literature, according to the reviewer:

- [SkillRouter](https://arxiv.org/abs/2603.22455): full bodies carry decisive routing information at approximately 80K-skill scale, but body information is largely an aggregate signal.
- [SSL](https://arxiv.org/abs/2604.24026): structured, normalised skill views outperform text-only representations, but it compares bundles of fields rather than minimal counterfactual distinctions.
- [Tool-DE](https://arxiv.org/abs/2510.22670): add-one and one-out field analyses for atomic tools. The thesis must not claim the first field ablation for capability retrieval. The proposed distinction is procedural skills, controlled near-neighbour correctness, query-field interaction, and matched-content structure tests.
- [ToolRet](https://aclanthology.org/2025.findings-acl.1258/): ordinary IR competence does not guarantee capability-retrieval competence.
- [SkillRet](https://arxiv.org/abs/2605.05726): valuable large-scale ranking data, but its queries are synthetic and generated from skill names and descriptions; use only as a portability appendix, not body-field evidence.
- [Skill Retrieval Augmentation](https://arxiv.org/abs/2604.24594): retrieval, incorporation, and execution are separable bottlenecks, supporting a scoped routing claim.

### Scope discipline

The reviewer recommends excluding from the core thesis:

- multi-skill decomposition, composition, and DAG planning;
- tree/graph/taxonomy/dependency-traversal/ontology construction;
- skill generation, acquisition, refinement, memory evolution, or library maintenance;
- full execution and task-success evaluation;
- runtime safety, side-effect prediction, and malicious-skill detection;
- training a new foundation retriever or running a broad model leaderboard;
- any claim that selected fields form a universal schema;
- monetary cost as a primary outcome (report reproducible tokens and compute quantities instead).

### Evidence standards and metrics

For RQ1, use top-1 routing accuracy and paired change from field inclusion/masking as primary; report cluster-bootstrap 95% confidence intervals, mixed-effects odds ratios, and Holm-corrected field comparisons. For ambiguity, report clarification/abstention precision, recall, and selective risk.

For RQ2, report Hit@1, MRR, calibration or Brier score, selector-visible tokens, and accuracy-context Pareto curves. Do not collapse quality and cost into one arbitrary ratio.

For RQ3, report first-stage Recall@K, conditional Hit@1 given gold inclusion, end-to-end Hit@1/MRR, and error destination (near-neighbour, unrelated distractor, abstention). Report index size, offline normalisation cost, online tokens, and median/p95 latency separately.

Require dual independent gold annotation with adjudication; cluster/repository/domain-disjoint splits; set-valued gold where appropriate; blinded topical-plausibility checks; frozen prompts, versions, truncation rules, and seeds; a preregistered primary comparison per RQ; and explicit null results.

### Suggested narrative

1. Skills require procedural suitability, not merely topical relevance.
2. Prior work shows full bodies and structure can help, but does not isolate decisive operational evidence.
3. RQ1 identifies when routing is informationally possible and which fields make it possible.
4. RQ2 tests whether the same evidence is accessed more reliably when explicit and undiluted.
5. RQ3 tests whether the interface survives authored noise, near-neighbour competition, and large candidate pools.
6. Failure analysis follows the causal chain: underspecified request; absent evidence; evidence diluted; gold omitted; or gold misranked.
7. Conclude with bounded design guidance for single-skill, pre-execution routing.

## Integration note (not a decision)

This is independent advice, not yet an approved change. Its proposed RQ2 aligns strongly with the separate blind review saved in `RQ2 Blind Design Review - 2026-07-26.md`: both recommend holding candidate sets fixed and comparing representations before making architecture claims. It differs from the current broad RQ2 by splitting the public/end-to-end systems question into a possible RQ3. Any thesis reframing requires user approval.
