# External Methodology Critique and Contribution Comparison - 2026-06-03

Role: skeptical but constructive research-methods examiner.

Scope: honours thesis on LLM agent skill retrieval. This note compares the current thesis framing against recent skill/tool retrieval work and proposes a stricter evaluation methodology. It intentionally does not edit the LaTeX thesis.

## 0. Executive Verdict

The current thesis is promising, but the contribution must be tightened.

The strongest contribution is not "structure-aware retrieval beats embeddings" and not "graph retrieval is the future." Those claims are too broad and too easy for recent papers to challenge.

The strongest defensible contribution is:

> Skill retrieval is an information-preservation problem. Under semantic confusion, compact skill descriptions and full-text embeddings can both lose or dilute procedural evidence. The thesis identifies which procedural fields are most useful for skill selection, tests whether those fields improve retrieval and reranking under scale, and analyses when field extraction, hierarchy, or graph structure helps or fails.

This is credible because SkillRouter and SkillRet already establish large-scale skill retrieval as important, while your thesis can offer a more controlled analysis of *which information inside a skill representation* matters.

## 1. Prior-Work Comparison Matrix

| Work | What it studies | Scale / dataset | Representation used | Retrieval / reranking strategy | Does it study procedural fields directly? | Gap remaining for this thesis |
|---|---|---:|---|---|---|---|
| [Claude Skills docs](https://claude.com/docs/skills/overview) | Product-level skill packaging and progressive disclosure | Product docs, not benchmark | Skill name, description, `SKILL.md`, optional resources | Metadata loaded first; full skill and resources loaded when activated | Partly, as authoring convention, not experimentally | Gives the practical baseline: compact metadata is used before full artifacts, but does not test failure under semantic confusion. |
| [SkillRouter](https://arxiv.org/abs/2603.22455) | Retrieve-and-rerank skill routing at scale | Around 80K skills, 75 expert queries | Metadata and full skill body | Bi-encoder retrieval plus reranker | Indirectly: finds full body is decisive, but does not isolate which fields in the body matter | Direct competitor. Your thesis must avoid claiming novelty for retrieve-and-rerank. Your contribution should be field-level explanation and controlled confusability. |
| [SkillRet](https://arxiv.org/abs/2605.05726) | Large-scale skill retrieval benchmark | 17,810 public skills, 63,259 train samples, 4,997 eval queries | Public skills with semantic tags and two-level taxonomy | Off-the-shelf retrievers plus task-specific fine-tuning | Only indirectly; focuses on benchmark/training rather than procedural field ablation | Strong scale benchmark. Your thesis should be positioned as smaller but more diagnostic: near-neighbour procedural confusion and information ablation. |
| [Skill Retrieval Augmentation / SRA](https://arxiv.org/abs/2604.24594) | Retrieve, incorporate, and apply skills from external corpora | SRA-Bench, external skill corpora | Retrieved skill corpora | Pipeline separating retrieval, incorporation, and execution | Partly; separates stages but not detailed field taxonomy | Supports your separation of retrieval from main-agent execution. You should also separate candidate recall, reranker success, and downstream task success. |
| [AgentSkillOS](https://arxiv.org/abs/2603.02176) | Ecosystem-scale skill organization and orchestration | Ecosystem-scale skill framework | Capability tree / structured skill organization | Tree selection plus DAG orchestration | Some procedural organization, but more system-level than field-level | Challenges your M4. If you evaluate tree routing, report branch recall and gold-excluded-by-branch, otherwise leave M4 as future work. |
| [SkillNet](https://arxiv.org/abs/2603.04448) | Creating, evaluating, and connecting skills | Claims large skill infrastructure and multi-domain evaluation | Ontology plus relation graph | Graph-based skill connection and reuse | Yes at ecosystem level, but not a clean field-ablation retrieval study | Challenges your M5. Your graph method must show edge ablations, not just "graph exists." |
| [Graph of Skills](https://arxiv.org/abs/2604.05333) | Dependency-aware structural retrieval for massive agent skills | Evaluated on SkillsBench and ALFWorld | Dependency-aware skill graph | Structural retrieval / graph-based selection | Yes, especially dependencies and structure | Very relevant. If included in final literature review, M5 should be framed as a controlled replication/ablation idea, not a novel graph proposal. |
| [SkillsBench](https://arxiv.org/abs/2602.12670) | Whether skills improve agents across tasks | 86 tasks across 11 domains, deterministic verifiers | Curated and self-generated skills | Skills injected into agents; not primarily retrieval | Not retrieval-focused, but tests skill usefulness and abstraction level | Supports downstream validation and warns that skills can hurt. Your retrieval gains should not be overclaimed as task-success gains without paired execution tests. |
| [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401) | Whether software-engineering skills improve real repositories | 49 public SWE skills, about 565 task instances | Public skills plus repository tasks | With/without skill injection, deterministic tests | Focuses on utility, fit, and compatibility, not retrieval | Strong warning: correct-looking skills may provide little marginal utility. Add a small downstream validation or avoid final task-success claims. |
| [ToolRerank](https://aclanthology.org/2024.lrec-main.1413/) | Adaptive and hierarchy-aware reranking for tool retrieval | ToolBench-style tool retrieval | Tool descriptions and hierarchy | Adaptive truncation plus hierarchy-aware reranking | Tool-level, not skill-level; hierarchy-aware rather than procedural-field-aware | Strong baseline idea for M4/M6: reranking should evaluate hierarchy and seen/unseen tool behavior. Your thesis should use it as transferable method evidence, not direct skill evidence. |
| [ToolLLM / ToolBench](https://arxiv.org/abs/2307.16789) | Tool use over real-world APIs | 16,464 APIs across 49 categories | API/tool descriptions | Neural API retriever plus tool-use agent | No; APIs are atomic tools, not procedural skills | Supports retrieval over large capability pools, but your thesis must explain why skill artifacts are richer and harder than API descriptions. |
| [ToolRet](https://arxiv.org/abs/2503.01763) | Benchmarking tool retrieval for LLMs | 43K tools, 7.6K retrieval tasks | Heterogeneous tool descriptions | Retrieval benchmark over tools | No; focuses on tool retrieval model weakness | Useful baseline logic: off-the-shelf retrievers are not automatically tool/skill-aware. But it is not enough to justify a skill-field taxonomy. |
| [Gorilla](https://arxiv.org/abs/2305.15334) | LLMs connected to massive APIs | APIBench across ML APIs | API documentation plus retriever | Retrieval-aware API call generation | No, tool/API-focused | Transferable evidence that retrieval over capability documentation reduces hallucination, but not a direct skill-selection solution. |
| [LATTICE hierarchical retrieval](https://arxiv.org/abs/2510.13217) | LLM-guided hierarchical retrieval over corpora | Document corpora | Semantic tree over documents | Calibrated path traversal | No; document retrieval | Good caution for M4: tree traversal must be evaluated by path recall and branch-exclusion, because a wrong early route can destroy recall. |

## 2. What This Comparison Means For Novelty

### What is not novel enough to claim

- "Skill retrieval is important at scale." SkillRouter and SkillRet already show this.
- "Retrieve-and-rerank improves skill selection." SkillRouter and tool-retrieval work already cover this broadly.
- "Graph or hierarchy can organize skills." AgentSkillOS, SkillNet, Graph of Skills, ToolRerank, and LATTICE-like retrieval already make this plausible.
- "Full skill bodies are useful." SkillRouter makes this a central result.

### What can still be novel and credible

- A controlled benchmark of semantically similar but procedurally distinct skill clusters.
- A field-level taxonomy of procedural information needed for disambiguation.
- Field ablations showing which information types improve retrieval and which add noise.
- Candidate-recall versus reranker-success decomposition under scale.
- A direct comparison between generic neural reranking and field-aware procedural reranking.
- External-validity analysis showing that the proposed fields are observed or extractable in public skills, while public skills also expose weakness in naive schema methods.

## 3. Stronger Evaluation Methodology

The evaluation should be split into six tests. Each test should have a clear pass/fail rule and should map back to the thesis claim.

### Test A: Benchmark Validity Under Semantic Confusion

Question: Does the benchmark actually test semantic confusion rather than arbitrary label noise or keyword leakage?

Metrics:

- Integrity: percent of prompts, gold labels, alternatives, and skill paths resolving.
- Procedural alignment: percent of prompts where the gold skill is manually or rubric-adjudicated as procedurally better than listed alternatives.
- Semantic confusability: percent of prompts with at least two plausible alternatives above a semantic-similarity threshold.
- Leakage: exact skill-name leaks, distinctive phrase leaks, and source/repository-name leaks.
- Non-core better-than-gold rate: percent of cases where a background/public skill is judged genuinely better than the gold.

Pass thresholds:

- Integrity: 100%.
- Procedural alignment: >= 90% strict pass; remaining cases must be acceptable-alternative or excluded.
- Semantic confusability: >= 80% of controlled prompts have at least two plausible alternatives.
- Leakage: 0 critical/high-risk leaks.
- Non-core better-than-gold: <= 5% strict; if higher, gold labels/prompt wording must be cleaned.

Supports thesis if:

- The benchmark has high procedural validity and semantic confusability while avoiding leaks.

Falsifies or weakens thesis if:

- Many failures are caused by bad gold labels, prompt leaks, or background skills that are actually better targets.

### Test B: Representation Information Ablation

Question: Which fields must the selection representation preserve?

Compare these representation conditions under the same retrieval/scoring family:

- R1: name + description + family.
- R2a: R1 + use conditions.
- R2b: R2a + output artifacts.
- R2c: R2b + workflow/procedure.
- R2d: R2c + inputs/preconditions.
- R2e: R2d + boundaries/not-for.
- R3: R2e + dependencies/resources.
- Full: full `SKILL.md`.

Metrics:

- Top-1, top-5, MRR.
- Non-core top-1.
- Visible token cost.
- Marginal gain per added 1K visible tokens.
- Field-specific failure reduction, especially plausible-but-wrong same-family errors.

Pass thresholds:

- R2 core fields should improve over R1 by >= 8 percentage points top-1 or >= 0.05 MRR on controlled cases.
- Use/output/workflow should account for most stable gain.
- Added fields should be justified by either accuracy gain, false-positive reduction, or interpretable failure-mode reduction.
- If dependencies/resources add tokens without gain, they must be treated as conditional feasibility fields, not positive retrieval text.

Supports thesis if:

- R2 fields improve controlled selection and reduce near-neighbour false positives.

Falsifies or weakens thesis if:

- R1 or full embeddings consistently match or exceed R2/R3 after comparable retrieval and reranking, or fields only help because of benchmark wording leakage.

### Test C: Candidate Recall Versus Reranking Quality

Question: Are failures caused by first-stage retrieval missing the gold, or by reranking misordering plausible candidates?

For each two-stage method, report:

- First-stage top-20/top-50/top-100 candidate recall.
- Reranker conditional top-1 given gold-in-candidate-set.
- Reranker loss rate: gold was in candidate set but moved below wrong skill.
- Candidate budget sensitivity: top-20, top-50, top-100.

Pass thresholds:

- A proposed reranker must be evaluated only where first-stage recall is adequate.
- For final M6-v1, first-stage top-100 recall should be >= 90% on controlled benchmark.
- M6-v1 should improve conditional top-1 by >= 5 percentage points over generic reranking on controlled near-neighbour clusters, or reduce non-core top-1 by >= 30% relative.

Supports thesis if:

- Dense retrieval has good candidate recall but poor final precision, and field-aware reranking improves final selection.

Falsifies or weakens thesis if:

- Candidate recall is poor and reranker gains only occur on easy retained cases, or generic neural reranking solves the same cases better.

### Test D: Public-Skill External Validity

Question: Are the proposed fields real/extractable in public skills, and do they help on externally authored skill targets?

Metrics:

- Field audit prevalence: explicit, extractable, absent.
- Manual/model agreement on field presence for a calibrated sample.
- Public-gold strict top-1/top-5/MRR.
- Public-gold gold-or-acceptable top-1/top-5/MRR.
- Extraction failure rate by field.
- Broad parent/router selection rate.
- Duplicate/equivalent skill ambiguity rate.

Pass thresholds:

- At least 50 public-gold cases after cleanup, or clearly state public-gold is pilot evidence only.
- >= 80% of public-gold prompts survive manual adjudication as strict or acceptable.
- Primary fields should be explicit or extractable in >= 70% of audited public skills:
  - use/routing trigger;
  - output artifact;
  - workflow/procedure;
  - input/precondition.
- For manual/model field audit, primary-field precision should be >= 0.75 on a sample of at least 50 skills if used quantitatively.

Supports thesis if:

- Fields are usually present or recoverable, and cleaned public-gold results show either improved retrieval or clear explanation of why naive schema fails.

Falsifies or weakens thesis if:

- Public skills rarely contain or imply the proposed fields, or field-aware methods fail because extraction is too noisy.

### Test E: M4 Tree And M5 Graph Scope Control

Question: Do hierarchy or graph structure add something beyond fields-as-text and field-aware reranking?

M4 tree metrics:

- Family top-1 accuracy.
- Family top-n recall.
- Gold-excluded-by-branch rate.
- Candidate reduction ratio.
- Final skill top-1/top-5/MRR.
- Latency/context cost.

M4 pass threshold:

- Multi-branch family routing should reduce candidate set by >= 50% while keeping gold branch recall >= 90%.
- Gold-excluded-by-branch should be <= 10% for top-n family routing.

M5 graph metrics:

- Edge ablations: family only; trigger; trigger+output; trigger+output+workflow; +input; +dependency/resource; +boundary penalties; full graph.
- Graph-only retrieval top-1/top-5/MRR.
- Hybrid graph reranking conditional top-1.
- Edge-extraction error rate.
- Broad parent/router penalty effect.

M5 pass threshold:

- M5 must beat serialized R2/M6-v1 by >= 3-5 percentage points top-1 or show a clear efficiency/failure-mode advantage.
- If M5 does not beat M6-v1, report it as evidence that fields matter more than graph architecture for this benchmark.

Supports thesis if:

- Tree/graph expose new failure modes or efficiency trade-offs, not merely extra method names.

Falsifies or weakens thesis if:

- M4/M5 are implemented without branch/edge ablations, because then they do not answer a research question.

### Test F: Downstream Task Validation

Question: Do retrieval improvements change actual task success?

Minimal design:

- 12-20 tasks sampled from high-confusion clusters.
- Compare four conditions:
  - oracle gold skill;
  - dense top-1 skill;
  - generic neural rerank top-1 skill;
  - M6-v1 top-1 skill.
- Keep main agent, prompt, and tool availability fixed.

Metrics:

- Task success / pass rate.
- Wrong-skill misuse rate.
- Need for clarification.
- Token cost.
- Execution latency.
- Artifact quality or deterministic verifier result where possible.

Pass threshold:

- M6-v1 should reduce wrong-skill misuse or improve task success relative to dense top-1 and generic rerank on the sampled tasks.
- If task success does not improve, claims must stop at retrieval quality and representation analysis.

Supports thesis if:

- Better retrieval translates into fewer wrong-skill task failures.

Falsifies or weakens thesis if:

- Retrieval top-1 improves but task success does not change or worsens due to extra context/cost/noise.

## 4. Concrete Improvements To Current Disliked Issues

### Issue 1: Overbreadth

Problem:

The thesis currently names many method families: M0, M1, M2, M3, M4, M5, M6, M7/M8, public-gold, downstream validation. This looks like a method zoo unless each method has a narrow role.

Fix:

Make the final thesis contribution two-layered:

1. Main contribution: information taxonomy and field-ablation evidence.
2. Main method: M6-v1 field-aware procedural reranking.

Move M4 and M5 into "architecture probes" unless fully implemented with branch/edge ablations.

Recommended final method table:

| Role | Keep? | Why |
|---|---|---|
| M0 progressive disclosure | Yes, baseline/cost | Shows normal skill exposure behavior and context pressure. |
| M1 flat lexical | Yes, control | Detects keyword/wording cue effects. |
| M2 dense R1/full | Yes, strong baseline | Tests whether embeddings/full artifacts already solve it. |
| M3 structured-card retrieval | Yes | Tests whether preserving fields helps before reranking. |
| Generic neural reranker | Yes | Strong "modern model can solve this" baseline. |
| M6-v0 | Yes, diagnostic only | Transparent but not final method. |
| M6-v1 | Yes, central proposed method | Directly tests field-to-field procedural matching. |
| M4 tree | Optional/future unless branch metrics complete | Scalability and branch-exclusion analysis. |
| M5 graph | Optional/future unless edge ablations complete | Tests relation structure beyond serialized fields. |

### Issue 2: M6-v0 Weakness

Problem:

M6-v0 uses lexical overlap over fields. If it performs well, critics can say the benchmark was authored to reward field wording. If it performs poorly on public skills, critics can say the schema idea fails.

Fix:

Build M6-v1 as a controlled procedural reranker:

1. Parse the request into field requirements.
2. Compare request fields to skill fields field-by-field.
3. Use semantic similarity within fields, not raw whole-card similarity.
4. Treat dependencies/resources conditionally.
5. Penalize `not_for`, broad parent/router skills, and hierarchy delegation mismatch.
6. Report candidate recall separately from reranker precision.

Minimum variants:

- M6-v1a deterministic: embedding/lexical field similarities plus transparent weights.
- M6-v1b LLM-assisted optional: same JSON fields, but an LLM judges field compatibility over top-20 candidates.

Do not tune weights repeatedly on final test results. Use a development subset or fixed prior weights, then freeze.

### Issue 3: Public-Gold Weakness

Problem:

Current public-gold results do not prove schema helps. They show that public artifacts are messy, broad, duplicated, and often implicit. Qwen generic rerank currently does best on public-gold top-1.

Fix:

Report public-gold as a separate external-validity stratum, not as merged evidence.

Clean first:

- Remove or revise the 4 unstable public-gold cases.
- Add acceptable alternatives for the 7 ambiguous cases.
- Expand public-gold to 50 if possible; otherwise explicitly call it a 32-case pilot.
- Report strict, gold-or-acceptable, and cleaned-strict results separately.

Then test:

- Qwen R1.
- Qwen R2.
- Qwen full.
- Qwen generic rerank.
- M6-v1 field-aware rerank.

Interpret carefully:

- If M6-v1 improves public-gold, strong evidence.
- If M6-v1 does not improve public-gold, but controlled improves, the thesis can still claim public skill extraction is the bottleneck.
- If generic rerank remains best, claim that procedural fields are useful for analysis but final public skill retrieval may need trained/LLM rerankers.

### Issue 4: M4/M5 Scope

Problem:

Tree and graph methods can look impressive but become vague. Existing work already covers hierarchies and skill graphs.

Fix:

Use M4 and M5 only if they answer architecture-specific questions:

- M4: Does hierarchical routing reduce candidate cost without excluding gold skills?
- M5: Do typed edges improve over serialized fields?

If not implemented fully, write:

> M4 and M5 are not claimed as completed contributions. They are planned architecture probes motivated by AgentSkillOS, SkillNet, Graph of Skills, ToolRerank, and LATTICE-like hierarchical retrieval.

If implemented:

- M4 must report branch accuracy and gold-exclusion.
- M5 must report edge ablations and compare against M6-v1.

### Issue 5: Downstream Validation Absence

Problem:

Offline retrieval metrics do not prove the agent completes tasks better.

Fix:

Add a small downstream validation, or explicitly bound claims.

Small feasible downstream validation:

- 12-20 prompts.
- Fixed agent and fixed skill-loading protocol.
- Compare dense top-1, generic rerank top-1, M6-v1 top-1, and oracle skill.
- Use deterministic artifact checks where possible.

If not completed:

- State clearly that the thesis evaluates retrieval and representation quality, not full end-to-end agent reliability.

## 5. Recommended Final Contribution Statement

Recommended claim:

> This thesis investigates skill retrieval as an information-preservation problem. It constructs a controlled benchmark of semantically similar but procedurally distinct skill clusters at public-expanded scale, audits whether proposed procedural fields occur in public skill artifacts, and compares retrieval/reranking strategies under different representation conditions. The thesis shows which procedural fields most improve skill selection, where flat and dense retrieval fail, and what additional evidence is required for structure-aware reranking to generalize to public skills.

Stronger version if M6-v1 succeeds:

> The results show that request-side field extraction plus field-to-field procedural reranking improves selection accuracy and reduces non-core false positives compared with flat metadata, dense full-artifact retrieval, and generic reranking on controlled near-neighbour skill clusters, while public-gold cases reveal extraction and broad-skill handling as the main remaining bottlenecks.

Do not claim:

- "Graph retrieval solves skill retrieval" unless M5 beats M6-v1 with edge ablations.
- "Structure-aware methods always beat embeddings" because public-gold currently contradicts the naive version.
- "Downstream agent performance improves" unless downstream validation is completed.
- "Large-scale SOTA skill retrieval benchmark" because SkillRet and SkillRouter are much larger.
- "Public skills already contain clean fields" because many fields are extractable or implicit rather than explicit.

## 6. Recommended Final Experimental Report Layout

1. Benchmark validation:
   - integrity, semantic confusability, procedural alignment, leakage, scale, non-core adjudication.
2. Information ablations:
   - R1 -> use -> output -> workflow -> preconditions -> boundaries -> dependencies/resources -> full.
3. First-stage retrieval:
   - lexical, dense R1, dense R2, dense full, candidate recall at top-20/50/100.
4. Reranking:
   - generic rerank versus M6-v0 versus M6-v1.
5. Public-gold stratum:
   - strict, acceptable, cleaned-strict.
6. Failure modes:
   - first-stage miss, reranker misweighting, boundary failure, broad parent, duplicate/acceptable alternative, extraction error, underspecified request.
7. Optional architecture probes:
   - M4 branch metrics and/or M5 edge ablations.
8. Downstream validation:
   - if completed, otherwise clearly framed as future work.

## 7. What Results Would Support Or Falsify The Thesis

### Strong support

- R2 use/output/workflow fields improve top-1 by >= 8 pp over R1 on controlled prompts.
- Dense full retrieval has high top-100 recall but lower top-1, showing reranking need.
- M6-v1 beats generic rerank on controlled near-neighbour prompts or reduces non-core false positives substantially.
- Public-skill audit shows primary fields are explicit/extractable in >= 70% of public skills.
- Public-gold cleaned results improve with M6-v1 or reveal clear extraction/hierarchy bottlenecks.
- Downstream validation shows fewer wrong-skill task failures.

### Partial support

- R2 fields help controlled prompts, but public-gold remains weak.
- M6-v1 improves non-core false positives but not top-1.
- Generic rerank performs best, but field-ablation and failure analysis show why certain fields matter.

This still supports an information-analysis thesis, but not a proposed-method thesis.

### Weak or falsifying evidence

- R1/full embeddings and generic rerank outperform M6-v1 across controlled and public-gold cases.
- Field ablations show no stable gains from use/output/workflow.
- Public skills rarely contain or imply the proposed fields.
- Non-core/background skills are often genuinely better than the designed gold labels.
- Downstream tasks do not improve and wrong-skill selections do not harm task outputs.

## 8. Citation / Source Use Plan

Use these sources as follows:

1. [Claude Skills overview](https://claude.com/docs/skills/overview) - Cite for the real-world progressive-disclosure design: metadata is visible first, full skill and resources load later.
2. [SkillRouter](https://arxiv.org/abs/2603.22455) - Cite as the strongest direct prior work on skill retrieve-and-rerank at large scale and as evidence that metadata alone under-specifies skill selection.
3. [SkillRet](https://arxiv.org/abs/2605.05726) - Cite as the current large-scale skill-retrieval benchmark; use it to position your benchmark as smaller but more controlled and diagnostic.
4. [Skill Retrieval Augmentation](https://arxiv.org/abs/2604.24594) - Cite for the stage separation between retrieval, incorporation, and execution.
5. [AgentSkillOS](https://arxiv.org/abs/2603.02176) - Cite for ecosystem-scale hierarchy/orchestration and as a comparison point for M4 tree routing.
6. [SkillNet](https://arxiv.org/abs/2603.04448) - Cite for ontology/graph-based skill organization and as a comparison point for M5.
7. [Graph of Skills](https://arxiv.org/abs/2604.05333) - Cite as the strongest direct structural-retrieval challenge to your M5 idea; use it to justify edge ablations rather than vague graph claims.
8. [SkillsBench](https://arxiv.org/abs/2602.12670) - Cite for evidence that skills can help but effects vary and focused skills can outperform broad documentation.
9. [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401) - Cite as a caution that injected skills often do not improve downstream SWE success, so retrieval metrics must not be overclaimed.
10. [ToolRerank](https://aclanthology.org/2024.lrec-main.1413/) - Cite for hierarchy-aware reranking and adaptive truncation as transferable tool-retrieval methods.
11. [ToolLLM / ToolBench](https://arxiv.org/abs/2307.16789) - Cite for retrieval and evaluation over large API/tool spaces, while emphasizing that skills are richer procedural artifacts.
12. [ToolRet](https://arxiv.org/abs/2503.01763) - Cite for the finding that off-the-shelf retrieval models are not automatically tool-aware; use as support for domain-specific retrieval evaluation.
13. [Gorilla](https://arxiv.org/abs/2305.15334) - Cite for retrieval-aware API/tool use and mitigation of API hallucination.
14. [LATTICE](https://arxiv.org/abs/2510.13217) - Cite cautiously as document-retrieval evidence that hierarchical traversal requires calibrated path scoring and path-recall evaluation.

## 9. Bottom-Line Recommendation

The thesis should move forward, but the next work should not be "add more baselines." The next work should be:

1. Clean public-gold cases.
2. Report candidate recall versus reranker precision.
3. Implement M6-v1.
4. Run field ablations under frozen conditions.
5. Decide whether M4/M5 are full experiments or future-work probes.
6. Add a small downstream validation or explicitly limit claims.

The cleanest final story is:

> Embedding retrieval is a useful first-stage filter. Full skill text helps candidate recall but can be noisy. The critical issue is what procedural evidence survives into the selection representation and how the selector uses it. Use conditions, output artifacts, and workflow/procedure are currently the strongest positive fields; dependencies/resources and boundaries need conditional handling. The proposed method should therefore be field-aware reranking, not naive schema text retrieval.
