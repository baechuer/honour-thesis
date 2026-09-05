# Supervisor Feedback Response Plan - A3 to Current Thesis

Date: 2026-06-05

Purpose: preserve the Assignment 3 literature-review feedback and translate it into concrete thesis-methodology improvements.

## Supervisor Feedback To Address

The feedback asks for:

1. More concrete empirical details from the reviewed papers.
2. A clearer benchmark construction process.
3. A more specific experimental setup, including:
   - gold labels;
   - model settings;
   - prompts;
   - statistical comparison.

The thesis has progressed beyond A3, but these criticisms still apply to the current draft. They should be treated as writing and methodology-hardening requirements, not only as old assignment feedback.

## How This Changes The Thesis

### Literature Review

The literature review should not only say that prior work uses retrieval, skills, or agents. For each important paper, record:

- the task domain and benchmark;
- library size or action/skill/tool count;
- representation used for tools or skills;
- retriever/reranker architecture;
- model backbone;
- evaluation metrics;
- reported empirical results;
- limitation directly relevant to this thesis.

Minimum papers that need empirical-detail treatment:

- SkillRouter: skill-specific embedding and reranking setup, model choice, retrieval/reranking evaluation, and what it does not isolate about procedural fields.
- SkillRet or similar skill-retrieval benchmark papers: dataset size, query construction, metrics, and whether confusability is broad-scale or near-neighbour procedural confusion.
- SkillAct: skill representation format, environment, evaluation setup, and scalability limitation from prompt-time skill lists.
- Voyager: skill-library representation, embedding retrieval over skill descriptions/code, benchmark domain, and retrieval limitation.
- ToolLLM/ToolBench, ToolRerank, or other tool-retrieval work: tool count, retrieval representation, reranking setup, metrics, and why tool selection differs from procedural skill selection.
- Public-skill empirical analysis papers such as AgentSkillOS or agent-skill quality studies: corpus size, observed field/procedure/dependency properties, and how they support the field taxonomy.

Deliverable:

- Add a literature-review table with concrete empirical details.
- Add a synthesis paragraph after the table explaining the gap: prior work tests skill/tool retrieval at scale, but does not cleanly isolate which skill-artifact information distinguishes semantically similar, procedurally different skills.

### Benchmark Construction

The benchmark section must explain construction as a reproducible pipeline:

1. Define an atomic skill unit.
2. Build controlled confusable clusters.
3. For each prompt, assign one strict gold skill.
4. Record 2-4 closest alternatives.
5. Write a gold rationale and rejection rationale.
6. Annotate field axes that distinguish gold from alternatives.
7. Add public skills as background scale and field-taxonomy evidence.
8. Add a separate public-gold stratum only after manual atomization/adjudication.
9. Run validation gates: integrity, procedural alignment, semantic confusability, leakage, scale, public-field audit.

Deliverable:

- Add one methodology figure or table showing this pipeline.
- Include example prompt records with gold labels, alternatives, and field axes.

### Experimental Setup

Every final method table should specify:

- library size and prompt stratum;
- candidate representation;
- model/provider;
- embedding text source;
- candidate budget;
- reranker type;
- whether embeddings/calls were cached;
- scoring rule: strict gold or gold-or-acceptable;
- metrics: top-1, top-5, MRR, candidate recall, false-positive/failure type, cost/latency where available.

Deliverable:

- Add a final method configuration table in the methodology chapter.
- Add an experiment-run metadata appendix or table.

### Gold Labels

Gold labels need explicit documentation:

- strict gold skill;
- acceptable alternatives;
- rejection rationale for listed alternatives;
- revise/exclude status for unstable public-gold cases;
- manual adjudication date/status.

Deliverable:

- Public-gold cleanup must be applied before final public-gold results.
- Final results must report strict and acceptable scores separately.

### Prompts

Prompt documentation should include:

- prompt source/cluster;
- exact prompt text stored in benchmark files;
- whether the prompt is controlled, implicit-field, low-information, or public-gold;
- leakage check result;
- whether it names the gold skill or copies distinctive phrasing.

Deliverable:

- Expand Appendix B or benchmark chapter with representative prompt examples.

### Statistical Comparison

Final result tables need uncertainty:

- confidence intervals for top-1/top-5/MRR;
- paired McNemar tests for selected top-1 comparisons;
- paired bootstrap or randomization test for MRR/top-k;
- exact prompt-count differences alongside percentages.

Deliverable:

- Implement or run a statistical comparison script before final result tables.

## Current Status Against Feedback

| Feedback item | Current status | Action needed |
|---|---|---|
| Concrete empirical paper details | Partial | Add a literature-review empirical table and revise synthesis. |
| Benchmark construction clarity | Partial | Add reproducible construction pipeline and prompt-record example. |
| Gold labels | Partial | Controlled golds exist; public-gold cleanup still needed. |
| Model settings | Partial | Qwen/SkillRouter notes exist, but final method table needs standardized model settings. |
| Prompts | Partial | Prompt files exist; thesis writing needs clearer prompt strata and examples. |
| Statistical comparison | Not done | Add CIs and paired tests. |
| Candidate budget fairness | Partially fixed in writing | Need final result table discipline and possibly rerun SkillRouter top-100 or avoid unfair comparisons. |

## Next Writing Targets

1. Update Chapter 2 with empirical-detail table.
2. Update Chapter 4 with benchmark construction pipeline.
3. Update Chapter 5 with method configuration table and gold-label protocol.
4. Update Chapter 6 with strict/acceptable labels, candidate budgets, and statistical uncertainty.
5. Update Appendix B with representative prompt records.

