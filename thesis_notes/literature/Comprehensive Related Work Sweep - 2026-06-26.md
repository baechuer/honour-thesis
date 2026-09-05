# Comprehensive Related Work Sweep - 2026-06-26

Purpose: identify papers relevant to the thesis on agent-skill representation and retrieval, especially operational information, skill/tool/RAG representation, retrievers, rerankers, hierarchy, graphs, and semantic-confusability evaluation.

Current thesis framing:

- RQ1: Which operational information types help distinguish semantically similar but procedurally distinct agent skills?
- RQ2: How do representation and retrieval strategies preserve, organize, and exploit routing-relevant skill information, and what trade-offs do they create in accuracy, candidate recall, context cost, latency, and failure modes?

High-level conclusion:

The current thesis is still defensible, but the novelty claim must be narrow. The field now has several structured-skill and skill-routing papers. The safest contribution framing is not "structured skill representation improves retrieval" and not "first skill retrieval benchmark." The contribution is a controlled, field-level study of operational information under near-neighbour procedural confusability, with matched representation/retrieval comparisons and failure-mode analysis.

## Already Covered In Thesis References

These are already in `references.bib` or the current literature review:

| Paper | Current use | Relevance |
|---|---|---|
| Lewis et al., 2020, RAG | Foundation for retrieval-augmented external knowledge | Background only |
| Izacard et al., 2022, Atlas | Retrieval-augmented few-shot learning | Background only |
| Toolformer | Tool use as learned API calling | Tool-use background |
| Gorilla | Retrieval-aware API use at scale | Tool/API scaling analogy |
| ToolLLM / ToolBench | 16k+ real-world APIs and neural API retrieval | Strong tool-retrieval baseline analogy |
| SkillAct | Early textual skill abstractions | Shows skill utility but flat exposure |
| Voyager | Embedding retrieval over skill descriptions/code | Early skill-library architecture |
| SkillsBench | Skills help but larger/broader skill sets can be fragile | Skill-utility benchmark |
| When Single-Agent with Skills Replace Multi-Agent Systems and When They Fail | Scale and semantic confusability | Very strong motivation |
| AgentSkillOS | Hierarchical capability tree and DAG orchestration | M4/tree comparison |
| SkillNet | Relational skill graph and ecosystem-scale organization | M5/graph comparison |
| Claude skills data-driven analysis | Real public-skill ecosystem noise/redundancy | Public-skill motivation |
| SkillRouter | Large-scale skill retrieve-and-rerank; full body helps | Strong direct baseline |
| SkillRet | Large-scale skill retrieval benchmark | Scale benchmark; position our benchmark as diagnostic |
| Skill Retrieval Augmentation | Separates retrieval, incorporation, and execution | Supports staged architecture |
| SSL | Structured Scheduling-Structural-Logical skill representation | Closest representation prior |
| ToolRet | Generic retrievers are not automatically tool-aware | Tool-retrieval baseline logic |
| ToolRerank | Hierarchy-aware reranking for tools | Transferable method idea |
| SciToolAgent | Tool knowledge graph with dependency/safety relations | Structured tool graph analogy |
| LATTICE | LLM-guided hierarchical document retrieval | Transferable hierarchy/path-recall idea |

## Highest-Priority Additions

These are the strongest additions to the thesis now. They should be reviewed and added to `references.bib` before the next serious literature-review pass.

### 1. SkillResolve-Bench: Measuring and Resolving Same-Capability Ambiguity in Agent Skill Retrieval

Source: [arXiv 2606.10388](https://arxiv.org/html/2606.10388v1)

Why it matters:

- This is the closest new paper to the thesis's semantic-confusability framing.
- It studies same-capability helpful/risky sibling pairs rather than generic relevant-vs-irrelevant retrieval.
- It explicitly uses contract-profile cues including resource bindings, preconditions, API/temporal scope, output schema, and procedure indicators.
- It reports that generic lexical, SkillRouter, and BGE reranking retrieve relevant skills but expose risky siblings.

How to position:

- Very direct related work, possibly a "near competitor."
- It focuses on harmful/risky sibling exposure and representative selection within resolved capability families.
- Our thesis is broader and more diagnostic: it asks which operational fields help distinguish near-neighbour skills in general, including but not limited to risk/safety siblings.
- If cited well, it strengthens the argument that near-neighbour ambiguity is now recognized as a concrete skill-retrieval problem.

Suggested thesis wording:

> SkillResolve-Bench is the closest recent benchmark to the near-neighbour problem, because it evaluates same-capability helpful/risky sibling pairs under fixed-library pressure. Its emphasis on suppressing harmful sibling exposure differs from the present thesis, which uses semantic confusability to isolate the retrieval value of operational fields such as use conditions, inputs, outputs, workflows, dependencies, and boundaries.

Risk to novelty:

- Medium-high. It overlaps on "same-capability ambiguity," but its objective is safety/risky-sibling suppression, not field-level causal ablation across general procedural distinctions.

### 2. Graph-of-Skills: Dependency-Aware Structural Retrieval for Massive Agent Skills

Source: [arXiv 2604.05333](https://arxiv.org/html/2604.05333v3)

Why it matters:

- Builds a directed multi-relational graph over local skill packages.
- Uses semantic/lexical seeding plus reverse-aware Personalized PageRank and context-budgeted hydration.
- Directly argues that semantic retrieval may find topically relevant skills but miss prerequisites or workflow dependencies.
- Evaluates on SkillsBench and ALFWorld with token and reward trade-offs.

How to position:

- Essential for M5/graph retrieval.
- It should stop us from claiming novelty for graph retrieval over skill libraries.
- Our angle remains field-level: what information should become edges or graph features, and whether those fields actually distinguish confusable skills.

Suggested thesis wording:

> Graph-of-Skills shows that dependency-aware graph retrieval can outperform flat full-library prompting and vector retrieval when tasks require dependency-complete skill bundles. The present thesis treats this as evidence for structure-aware retrieval, but focuses on the prior question of which operational information types should be preserved or extracted before graph structure can be useful.

Risk to novelty:

- Medium. Strongly challenges any broad M5 novelty claim; less threatening to RQ1 field analysis.

### 3. Group of Skills: Group-Structured Skill Retrieval for Agent Skill Libraries

Source: [arXiv 2605.06978](https://arxiv.org/html/2605.06978v1)

Why it matters:

- Moves from individual skill retrieval to group-structured retrieval.
- Renders selected skill context with explicit Start, Support, Check, and Avoid fields.
- This is highly relevant to the thesis's output/workflow/boundary/success-criteria field groups.
- Evaluates on SkillsBench and ALFWorld under bounded context budgets.

How to position:

- Strong RQ2 evidence that "retrieval result presentation" matters, not just candidate ranking.
- It overlaps with our operational fields but uses them for context rendering and role-labeled execution support.
- Our thesis can cite it as evidence that field organization affects downstream execution and runtime, while our study isolates retrieval-side discriminative signal.

Risk to novelty:

- Medium. It is close to RQ2 context organization, but not RQ1 field-isolation retrieval.

### 4. Skill Is Not Document: A Query-Conditional Benchmark and Two-Stage Retriever for LLM Agent Skill Routing

Source: [arXiv 2606.03565](https://arxiv.org/html/2606.03565v2)

Why it matters:

- Makes the argument that skill retrieval is not document retrieval.
- Emphasizes query-conditional joint correctness: a retrieved set of skills must be compatible, not just individually relevant.
- Good support for separating skill retrieval from passage retrieval and for multi-skill candidate-set metrics.

How to position:

- Use in literature review where the thesis says skills are procedural capability units rather than ordinary documents.
- Especially useful for RQ2 if reporting candidate recall or multi-skill coverage.

Risk to novelty:

- Low-medium. It is a direct skill-routing paper but focuses on compatibility/joint retrieval, not our near-neighbour field ablations.

### 5. Multi-Field Tool Retrieval

Source: [arXiv 2602.05366](https://arxiv.org/html/2602.05366v1)

Why it matters:

- Very strong tool-side analogy for our RQ1.
- It argues that tool utility is multi-aspect, involving functionality, input constraints, output formats, and usage examples.
- It standardizes tool documentation into fields, rewrites queries into aligned fields, and adaptively weights field scores.
- It explicitly shows that masking different fields can have different positive/negative impacts.

How to position:

- Transferable evidence, not direct skill evidence.
- Strong support that "flat documentation as one text blob" is suboptimal for capability retrieval.
- The difference: tools are typically atomic operations; skills are procedural artifacts with workflows, boundaries, dependencies, resources, and success criteria.

Risk to novelty:

- Medium. It is very close methodologically, but in tool retrieval rather than skill retrieval.

### 6. Tools Are Under-Documented: Simple Document Expansion Boosts Tool Retrieval

Source: [arXiv 2510.22670](https://arxiv.org/abs/2510.22670)

Why it matters:

- Shows that incomplete/heterogeneous tool documentation harms tool retrieval.
- Introduces structured tool-profile expansion and dedicated embedding/ranking models.
- Reports field-contribution analysis.

How to position:

- Tool-side evidence for extracting/normalizing missing fields before retrieval.
- Useful support for why full artifacts or raw metadata may be inconsistent and why extracted procedural cards can be helpful.

Risk to novelty:

- Low-medium. Tool-side, not skill-side.

### 7. MCP Tool Descriptions Are Smelly

Source: [arXiv 2602.14878](https://arxiv.org/abs/2602.14878)

Why it matters:

- Empirical study of 856 MCP tools across 103 servers.
- Finds description-quality defects are widespread.
- Augmenting descriptions improves task success but increases execution steps and sometimes regresses performance.
- Component ablations show compact combinations can preserve reliability while reducing token overhead.

How to position:

- Very useful for the thesis claim that representation quality and context cost trade off.
- Also supports not naively appending every field as positive retrieval text.
- Tool descriptions are not skills, but both are agent-facing capability descriptions.

Risk to novelty:

- Low-medium. It reinforces our cost/field-ablation logic without directly studying skills.

### 8. How Well Do Agentic Skills Work in the Wild

Source: [arXiv 2604.04323](https://arxiv.org/abs/2604.04323)

Why it matters:

- Studies skill utility under more realistic settings where agents retrieve from a large collection of 34k real-world skills.
- Finds skill benefits are fragile and degrade as settings become more realistic.
- Query-specific refinement helps when initial skills are reasonably relevant/quality.

How to position:

- Strong support that "having skills" is not enough; selection and refinement matter.
- Use in motivation and limitations: retrieval gains should not automatically be overclaimed as downstream task success.

Risk to novelty:

- Low. It is broader skill utility, not controlled field disambiguation.

### 9. SkillsInjector: Dynamic Skill Context Construction for LLM Agents

Source: [arXiv 2605.29794](https://arxiv.org/html/2605.29794v1)

Why it matters:

- Treats skill context construction as adaptive: which skills, how many, and how they are presented.
- Finds that skill selection, adaptive budgeting, and set-aware rendering each contribute to gains.
- Very relevant to the thesis's context-cost and progressive-disclosure assumptions.

How to position:

- RQ2 support: retrieval policy and representation/rendering interact.
- Our thesis is more retrieval-diagnostic; SkillsInjector is a downstream context-construction system.

Risk to novelty:

- Medium for RQ2, low for RQ1.

### 10. Agent Skill Framework: Perspectives on Small Language Models in Industrial Environments

Source: [arXiv 2602.16653](https://arxiv.org/abs/2602.16653)

Why it matters:

- Separates skill selection/routing and execution correctness in industrial settings.
- Reports small models struggle with reliable skill selection, while moderate SLMs benefit more.
- Relevant to practical deployment constraints and model-size sensitivity.

How to position:

- Use as deployment motivation and as evidence that skill selection itself is measurable.

Risk to novelty:

- Low.

### 11. CUA-Skill: Develop Skills for Computer Using Agent

Source: [arXiv 2601.21123](https://arxiv.org/abs/2601.21123)

Why it matters:

- Encodes computer-use knowledge as structured skills with parameterized execution and composition graphs.
- Uses dynamic skill retrieval, argument instantiation, and memory-aware failure recovery.
- Good example of skills as structured, executable, parameterized artifacts.

How to position:

- Useful in "skills are richer than tools" section.
- Not central unless thesis discusses computer-use agents.

Risk to novelty:

- Low.

## Foundational Retrieval And RAG Papers To Add Or Mention

The current thesis cites RAG and Atlas, but the retrieval-method discussion would be stronger with a few standard IR/RAG anchors.

| Paper | Source | Why it matters to thesis |
|---|---|---|
| BM25 / Probabilistic Relevance Framework | Robertson and Zaragoza, 2009 | Justifies BM25/TF-IDF lexical baselines. |
| Sentence-BERT | [arXiv 1908.10084](https://arxiv.org/abs/1908.10084) | Foundation for sentence embeddings and semantic search. |
| Dense Passage Retrieval | [arXiv 2004.04906](https://arxiv.org/abs/2004.04906) | Foundation for dual-encoder dense retrieval. |
| ColBERT | [arXiv 2004.12832](https://arxiv.org/abs/2004.12832) | Late-interaction retrieval; useful contrast to single-vector dense embeddings. |
| BEIR | [arXiv 2104.08663](https://arxiv.org/abs/2104.08663) | Shows BM25 robustness and dense retriever OOD limits; supports benchmark discipline. |
| Lost in the Middle | [arXiv 2307.03172](https://arxiv.org/abs/2307.03172) | Supports context-budget argument: full-library prompting can bury relevant skill info. |
| Self-RAG | [arXiv 2310.11511](https://arxiv.org/abs/2310.11511) | Adaptive retrieval and self-critique; background for retrieval policy control. |
| CRAG | [arXiv 2401.15884](https://arxiv.org/abs/2401.15884) | Retrieval evaluator/corrector; transferable idea for candidate quality assessment. |
| GraphRAG | [arXiv 2404.16130](https://arxiv.org/abs/2404.16130) | Graph-structured retrieval over documents; useful analogy but not direct skill evidence. |

Use these sparingly. The thesis is not a general RAG thesis. They should support the method vocabulary and evaluation choices, not take over the literature review.

## Foundational Tool/Agent Papers To Add Or Mention

| Paper | Source | Why it matters |
|---|---|---|
| MRKL Systems | [arXiv 2205.00445](https://arxiv.org/abs/2205.00445) | Early modular LLM architecture with external modules; background for agents as systems. |
| ReAct | [arXiv 2210.03629](https://arxiv.org/abs/2210.03629) | Shows interleaved reasoning and acting; useful bridge from generation to agent action. |
| API-Bank | [arXiv 2304.08244](https://arxiv.org/abs/2304.08244) | Early runnable benchmark for planning, retrieving, and calling APIs. |
| ToolGen | [arXiv 2410.03439](https://arxiv.org/html/2410.03439v3) | Integrates tool retrieval and calling via generation; optional related work. |
| ToolReAGt | ACL KnowLLM 2025 | Tool retrieval via RAG/ReAct; useful but not essential unless tool-retrieval section is expanded. |
| PORTS | EMNLP 2025 | Preference-optimized retrievers for tool selection; optional method comparison. |

These are useful background, but the thesis should avoid getting dragged into all tool-use training literature. The key contrast is: tools/API calls are usually atomic callable operations; skills are reusable procedural artifacts.

## Skill Papers By Theme

### Skill Concept And Lifecycle

- SoK: Agentic Skills -- Beyond Tool Use in LLM Agents. Already cited. Use to argue skills are more than tools.
- Agent Skills from the Perspective of Procedural Memory. Already cited, but bibliographic details should be verified because the current `references.bib` author/title details may not match the latest survey landscape.
- A Comprehensive Survey on Agent Skills: Taxonomy, Techniques, and Applications. [arXiv 2605.07358](https://arxiv.org/html/2605.07358v1). Add as broad survey; it organizes representation, acquisition, retrieval, and evolution.
- Agent Skills for Large Language Models: Architecture, Acquisition, Execution, Evaluation, Security, and the Path Forward. [arXiv 2602.12430](https://arxiv.org/html/2602.12430v3). Useful as broad survey / architecture map.

### Skill Representation

- SSL. Already cited. Most direct structured representation prior.
- CUA-Skill. Add if discussing executable/parameterized skills.
- SkillX. [arXiv 2604.04804](https://arxiv.org/html/2604.04804v2). Automatically constructs skill knowledge bases with structured/hierarchical experience representations. Useful but less central.
- SkillSmith. [arXiv 2605.15215](https://arxiv.org/html/2605.15215v1). Compiles workflow skills into typed graphs and dispatcher/reference skills into other runtime forms. Useful if thesis discusses skill compilation, but probably secondary.

### Skill Retrieval And Routing

- SkillRouter. Already cited. Strong baseline.
- SkillRet. Already cited. Large-scale benchmark.
- SRA. Already cited. Retrieval/incorporation/execution pipeline.
- Skill Is Not Document. Add as direct argument that skill retrieval differs from document retrieval and needs query-conditional/joint correctness.
- SkillResolve-Bench. Add as closest same-capability ambiguity benchmark.
- Compositional Skill Routing / SkillWeaver. [arXiv 2606.18051](https://arxiv.org/html/2606.18051v1). Decompose complex queries, retrieve per subtask, compose. Useful for multi-skill routing but less central to RQ1 single-skill confusability.

### Structural Retrieval / Context Organization

- AgentSkillOS. Already cited.
- SkillNet. Already cited.
- Graph-of-Skills. Add as direct M5/graph retrieval comparator.
- Group-of-Skills. Add as direct context-organization / role-labeled retrieval comparator.
- SkillsInjector. Add for adaptive budgeting and rendering.

### Skill Utility In Realistic Settings

- SkillsBench. Already cited.
- How Well Do Agentic Skills Work in the Wild. Add; strong realism/fragility evidence.
- Agent Skill Framework. Add for industrial/SLM skill-selection evidence.
- SWE-Skills-Bench. Already cited in `references.bib`; use if software-engineering setting matters, but not central unless result chapter discusses code/SE skills.

## Tool-Side Representation Papers That Support RQ1

These are not direct skill papers, but they strongly support the idea that retrieval over capability artifacts should not treat documentation as undifferentiated text.

| Paper | Key idea | Thesis use |
|---|---|---|
| Multi-Field Tool Retrieval | Tool utility has multiple field-specific dimensions; field masking changes retrieval impact. | Strong support for RQ1 field framing, with tool/skill distinction. |
| Tool-DE | LLM-expanded structured tool profiles improve tool retrieval. | Supports extraction/normalization of sparse artifacts. |
| MCP Tool Descriptions Are Smelly | Tool descriptions often omit purpose, usage, limitations; augmentation improves performance but can increase cost/regressions. | Supports field quality, compactness, and cost trade-off. |
| ToolRet | Generic retrievers underperform on tool retrieval. | Already cited; supports domain-specific evaluation. |
| ToolRerank | Hierarchy-aware reranking improves tool retrieval and execution. | Already cited; supports hierarchy/reranking method family. |

Important caution:

Tool papers are not enough to justify a skill thesis by themselves. They show that structured capability descriptions matter, but skills add procedural workflow, success criteria, bundled resources, and negative boundaries. The thesis should keep saying this explicitly.

## RAG And Retrieval Concepts To Use Carefully

The thesis should use RAG/IR papers mainly to define method families and explain why skill retrieval cannot be reduced to ordinary document retrieval.

Useful claims:

- RAG externalizes knowledge/capabilities rather than relying only on model parameters.
- Dense retrieval, lexical retrieval, late interaction, and reranking have known trade-offs.
- BEIR shows that generic retrieval performance varies strongly across domains; BM25 can remain robust, and dense models can fail OOD.
- Lost-in-the-Middle supports selective loading instead of full skill-library context.
- Self-RAG/CRAG support adaptive retrieval and retrieval-quality checking, but they focus on documents/evidence, not executable skills.
- GraphRAG supports graph-structured retrieval as a document-side analogy, but skill graphs must encode executable or procedural relations rather than just semantic entities.

Avoid overclaiming:

- Do not say RAG literature "solves" skill retrieval.
- Do not treat documents/passages as equivalent to skills.
- Do not import GraphRAG claims as direct evidence for skill graph retrieval.

## Novelty Boundary After This Sweep

The thesis should not claim:

- First structured representation for agent skills. SSL and several skill-compilation/graph papers now exist.
- First large-scale skill retrieval benchmark. SkillRouter, SkillRet, SRA-Bench, and newer benchmarks cover this.
- First graph/tree skill retrieval. AgentSkillOS, SkillNet, Graph-of-Skills, and Group-of-Skills cover this territory.
- First evidence that fields matter for capability retrieval. MFTR and Tool-DE provide tool-side field evidence, while SSL provides skill-side representation evidence.

The thesis can still claim:

- A controlled near-neighbour benchmark focused on semantically similar but procedurally distinct skills.
- Field-level analysis of which operational information types are discriminative under confusability.
- A matched comparison of representation conditions such as flat metadata, full artifact, extracted procedural cards, dependency/resource-aware cards, and field-aware reranking.
- Failure-mode analysis that separates absent information, unused information, noisy information, boundary/dependency misuse, and first-stage recall failure.
- A bridge between skill-specific retrieval and tool/RAG retrieval literature, showing what transfers and what does not.

## Recommended Citation Priority

Add first:

1. SkillResolve-Bench.
2. Graph-of-Skills.
3. Group-of-Skills.
4. Skill Is Not Document.
5. Multi-Field Tool Retrieval.
6. MCP Tool Descriptions Are Smelly.
7. Tools Are Under-Documented / Tool-DE.
8. How Well Do Agentic Skills Work in the Wild.
9. Lost in the Middle.
10. BEIR and DPR, plus BM25 if BM25 is reported in methods.

Add if space allows:

- A Comprehensive Survey on Agent Skills.
- Agent Skills for LLMs survey.
- ReAct.
- API-Bank.
- MRKL.
- SkillsInjector.
- Agent Skill Framework.
- CUA-Skill.
- GraphRAG / Self-RAG / CRAG as method background only.

## Suggested Literature Review Insertions

### After SkillRouter / SSL

Add SkillResolve and Skill Is Not Document:

> More recent work further sharpens the retrieval target. Skill Is Not Document argues that skill retrieval requires query-conditioned compatibility rather than independent document-style relevance, because retrieved skills may need to collaborate as a set. SkillResolve-Bench moves even closer to the semantic-confusability problem by evaluating same-capability helpful/risky sibling pairs under fixed-library pressure. These papers reinforce the need to evaluate plausible near-neighbour mistakes rather than only broad topical retrieval.

### In Structure-Aware Retrieval

Add GoS and GoSkills:

> Graph-of-Skills and Group-of-Skills show that structural retrieval can use dependency, workflow, and role information to construct bounded skill contexts. Their focus is retrieval-time bundle construction and downstream execution. The present thesis instead treats dependency, workflow, boundary, and output information as operational variables whose discriminative value can be tested before committing to a particular graph or group structure.

### In Tool Retrieval Transfer Section

Add MFTR, Tool-DE, and MCP smells:

> Recent tool-retrieval work independently supports the field hypothesis. Multi-Field Tool Retrieval shows that tool utility depends on multiple dimensions such as functionality, inputs, outputs, and examples, and that field masking can change retrieval behavior. Tool-DE and the MCP tool-description study further show that raw tool descriptions are incomplete, heterogeneous, and costly to augment naively. These results are transferable but not decisive for skills, because skills contain richer procedural and resource-bounded execution guidance than atomic tool descriptions.

## Open Checks Before Final Thesis

- Verify final arXiv versions and author lists for all 2026 preprints.
- Decide whether to treat very new papers from June 2026 as core literature or late-breaking related work.
- Update `references.bib` with the high-priority additions.
- Rebuild the literature review so the new close papers do not appear as afterthoughts.
- Re-check whether any cited paper uses unreleased benchmark data or models that make results hard to compare.
- Keep the novelty claim narrow and explicit in introduction, methodology, and discussion.

