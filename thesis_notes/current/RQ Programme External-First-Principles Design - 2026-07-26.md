# External First-Principles RQ Programme Design (2026-07-26)

Status: `DESIGN INPUT / SUPERSEDED AS ACTIVE PROTOCOL`. Preserve this memo as an independent perspective, but do not implement it directly. Current authority: `thesis_notes/current/RQ2 Current Status and Implementation Tracker - 2026-07-26.md`.

## Purpose and independence boundary

This memo records an independently commissioned design proposal. The reviewer was prohibited from inspecting any local file, conversation history, thesis draft, methodology, experiment, benchmark, result, or existing design. Its only premise was that a prior controlled study found several operational facts useful for distinguishing near-neighbour, pre-execution agent skills. It was allowed at most six web searches across relevant skill, tool-retrieval, RAG, reranking, and structured-retrieval literature.

## Reviewer memo

### Research aim

Determine whether explicitly representing operational facts improves selection of exactly one pre-execution skill when candidates share a topic but differ in applicability, requirements, procedure, or deliverable. The central distinction is between **information content** and merely making descriptions longer, cleaner, or easier for a particular model to parse.

### Proposed research questions

**RQ1: Which operational facts causally improve skill discrimination?**

Measure the individual and joint contribution of seven fact types: input/preconditions, output artifact, procedure, boundary/exclusion, dependency/resource, success/verification, and use condition. The reviewer expects boundary, precondition, output, and use-condition facts to be especially valuable for near-neighbour discrimination, while procedure may add topical vocabulary without reliably resolving applicability.

**RQ2: Does explicit structure help independently of information content?**

Compare identical facts expressed as natural prose, consistently ordered prose, labelled fields, and compact JSON. This separates gains from adding discriminative facts from gains caused by formatting, ordering, or compatibility with a retriever or reranker.

**RQ3: How do these effects interact with retrieval architecture, catalogue scale, and cost?**

Test whether structured operational facts still help across sparse, dense, hybrid, and reranked pipelines as distractor counts rise. The result should be a Pareto analysis of routing accuracy against latency, token use, and estimated monetary cost, rather than a claim that the most expensive pipeline is universally best.

### Proposed experiment matrix

Construct **SkillRoute-Hard**, a modest benchmark of approximately 120–180 public skills grouped into 30–45 near-neighbour families. Create 600–900 requests: authentic or lightly normalised examples, controlled paraphrases, and counterfactual minimal pairs that alter one operational requirement while preserving topic. Hold out whole skill families for testing so descriptions, templates, and paraphrases cannot leak across splits.

Use two transfer datasets: the single-tool portion of **ToolRet** and single-API examples sampled from **ToolBench**. Report them separately because APIs and skills are not identical objects.

For each skill, produce these information-controlled conditions:

| Block | Conditions |
|---|---|
| Content | original; topic-only summary; all seven facts; leave-one-fact-out; individual fact-only fields |
| Structure | shuffled prose; fixed-order prose; labelled Markdown; JSON |
| Retriever | BM25; one frozen general dense encoder; one tool-oriented dense encoder; BM25+dense reciprocal-rank fusion |
| Reranker | none; frozen cross-encoder; one fixed prompted LLM reranker |
| Scale | family only; 100, 500, 2,000, and maximum available distractors |
| Query | original; paraphrase; minimal-pair constraint change; underspecified request |

Do not run the full Cartesian product. First run content ablations with one fixed dense retriever and no reranker. Next test formatting while holding characters, facts, and field-order controls constant. Finally evaluate the strongest two content representations across the retrieval, reranking, and scale conditions.

### Gold policy and metrics

Gold must be defined by executable suitability rather than textual similarity. Two annotators independently select the one skill whose documented preconditions are satisfied and whose output matches the requested artifact. They should identify the decisive fact and allow “ambiguous/no valid skill”. Adjudicate disagreement and report agreement. Exclude genuinely multi-skill requests from primary top-one evaluation; retain ambiguous and no-match cases in a secondary abstention test. Hard negatives should come from the same family and differ in at least one adjudicated operational fact.

Primary metrics: Accuracy@1 and family-confusion rate. Secondary metrics: MRR, Recall@5, abstention F1, calibration, median/p95 latency, indexed characters, reranker tokens, and estimated cost. Use family-clustered bootstrap confidence intervals and a mixed-effects logistic model with request and skill family as random effects.

### Required controls

- Keep the underlying facts identical in structure experiments; otherwise structure is confounded with content.
- Match length through neutral padding or report length-stratified results.
- Freeze retriever checkpoints, embedding dimensions, prompts, candidate depth, and reranker temperature.
- Use the same candidate sets when comparing rerankers.
- Randomise field order separately from adding labels.
- Compare raw descriptions with cleaned prose to isolate noise removal.
- Sample distractors identically across systems and repeat scale experiments over several seeds.
- Report retrieval-only outcomes before downstream selection, so reranking cannot conceal candidate-recall failures.
- Maintain a cost ledger covering indexing, query embedding, retrieval, reranking, and prompt tokens.

### Bounded novelty claim

The reviewer’s suggested claim is:

> A controlled evaluation that separates operational-fact content from representation structure in single-skill, pre-execution retrieval under near-neighbour confusions, while retrieval and reranking components are held fixed.

This is **not** a new general retriever, a comprehensive agent benchmark, or proof that seven fields are universally sufficient.

Closest work proposed by the reviewer:

- [ToolRet](https://aclanthology.org/2025.findings-acl.1258/)
- [ToolLLM / ToolBench](https://arxiv.org/abs/2307.16789)
- [ToolRerank](https://aclanthology.org/2024.lrec-main.1413/)
- [Tool2Vec and ToolRefiner](https://arxiv.org/abs/2409.02141)
- [PORTS](https://aclanthology.org/2025.emnlp-main.507/)
- [ProTIP](https://arxiv.org/abs/2312.10332)
- [Multi-Meta-RAG](https://arxiv.org/abs/2406.13213)

### Risks and exclusions

Risks: subjective gold labels, synthetic-query artefacts, leakage between related skills, inconsistent public documentation, and model-specific sensitivity to JSON or field names. Mitigate through adjudication, family-held-out splits, authentic-query subsets, counterbalanced formats, and replication with at least one sparse and one dense system.

Exclude skill execution, multi-step planning, tool-argument generation, retriever training, large proprietary user logs, and a broad many-LLM comparison. They obscure the causal question and exceed a realistic honours scope.

## Integration note (not a decision)

The reviewer did not see the thesis or previous blind-review memo. Nevertheless, its RQ2 independently converges with both other reviews on the key experimental separation: preserve content, then test the representation/interface itself. Its suggested RQ3 is deliberately broader than the current proposed next step; it should be considered a future systems-validation layer rather than an automatic commitment for this honours thesis.
