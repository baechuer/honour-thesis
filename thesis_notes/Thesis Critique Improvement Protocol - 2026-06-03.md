# Thesis Critique Improvement Protocol - 2026-06-03

Purpose: convert the current skeptical critique into a more rigorous evaluation plan. The thesis should not be judged only by whether one retriever wins. It should be judged by whether it isolates which procedural information must be preserved for skill selection, and whether methods that use that information improve selection under semantic confusion.

## 1. Tightened Contribution Claim

Best current claim:

> Skill retrieval is an information-preservation problem. Dense retrieval can generate useful candidates, but final selection among semantically similar skills depends on preserving and using procedural evidence: use conditions, inputs/preconditions, expected outputs, workflow/procedure, dependencies/resources, constraints, negative boundaries, and task role.

Do not claim yet:

- Structure-aware retrieval is generally solved.
- Graph retrieval beats embedding retrieval.
- Schema text alone beats modern rerankers.
- Retrieval accuracy automatically implies downstream task success.

## 2. How To Improve The Disliked Issues

### Issue A: The project is too broad.

Fix:

- Make the core thesis about information fields and field-aware use.
- Treat M4 tree routing and M5 graph retrieval as architecture probes, not central contributions, unless they are fully implemented and ablated.
- Keep provider models as baselines, not the thesis novelty.

Pass condition:

- The thesis can be explained in one sentence: "Which skill information should be preserved, and does using it improve retrieval under semantic confusion?"

### Issue B: M6-v0 is too crude.

Current weakness:

- M6-v0 uses weighted lexical overlap over skill-side fields.
- It does not parse user requests into procedural fields.
- It can reward benchmark wording rather than genuine procedural matching.

Fix:

- Implement M6-v1 field-aware procedural reranking.
- Pipeline:
  1. first-stage retriever returns top-k candidates;
  2. request-side extractor parses the user request into action, input/precondition, desired output, workflow constraint, platform/tool requirement, exclusions, and success criteria;
  3. skill-side extractor parses or normalizes the same fields from SKILL.md;
  4. reranker compares field-to-field matches, not just global text overlap;
  5. report candidate recall separately from reranker accuracy.

Pass condition:

- M6-v1 improves top-1 or MRR over strong dense retrieval plus generic reranking on the controlled benchmark, while preserving high top-k recall.
- It should not collapse on public-gold cases after cleanup.

### Issue C: Public-gold currently weakens the schema claim.

Current weakness:

- Public-authored skills are broad, duplicated, hierarchical, and unevenly formatted.
- Naive schema overlap underperforms on public-gold results.

Fix:

- Keep public-gold as a separate external-validity stratum.
- Apply strict manual labels:
  - strict gold;
  - gold-or-acceptable alternative;
  - revise/exclude.
- For every public-gold failure, label the failure mode:
  - first-stage candidate miss;
  - reranker error;
  - field extraction error;
  - gold ambiguity;
  - broad parent skill beating atomic skill;
  - prompt under-specified.

Pass condition:

- Public-gold metrics are reported after removing revise/exclude cases.
- Acceptable alternatives are counted separately.
- The thesis claims public skills support field existence and extraction difficulty, not that schema overlap already solves public retrieval.

### Issue D: M4/M5 scope is unclear.

Fix for M4 tree routing:

- Only report M4 if there is a clear tree experiment:
  - branch accuracy;
  - candidate reduction;
  - gold-excluded-by-wrong-branch rate;
  - comparison with flat candidate retrieval at equal candidate budget.

Fix for M5 graph retrieval:

- Only report M5 if there is a clear edge-ablation experiment:
  - trigger/use-condition edges;
  - output edges;
  - workflow/procedure edges;
  - dependency/resource edges;
  - boundary/not-for edges;
  - full graph.

Pass condition:

- Tree/graph results explain failure modes or cost trade-offs. Otherwise they belong in future work.

### Issue E: Downstream validation is missing.

Fix:

- Run a small 12-20 case downstream validation.
- Conditions:
  - no skill;
  - oracle gold skill;
  - dense top-1 skill;
  - generic rerank top-1 skill;
  - M6-v1 top-1 skill.
- Metrics:
  - skill selection correctness;
  - task success;
  - tokens loaded;
  - latency;
  - error type.

Pass condition:

- Retrieval improvements should correlate with task success on at least a small, carefully chosen set.
- If downstream validation is not finished, thesis should only claim retrieval-quality evidence.

## 3. Stronger Evaluation Methodology

### Retrieval Decomposition

Every retrieval/reranking experiment should report:

- candidate recall@k before reranking;
- reranker top-1 among candidate set;
- final top-1;
- final top-5;
- MRR;
- non-core/public distractor top-1 rate;
- token cost of visible representation;
- latency/API cost where available.

This prevents confusion between "the retriever never found the gold skill" and "the reranker saw the gold skill but chose incorrectly."

### Field Ablation

Required ablations:

- R1: name + description.
- R2-use: description + use conditions.
- R2-output: add output artifacts.
- R2-workflow: add workflow/procedure.
- R2-input: add inputs/preconditions.
- R3-dependency/resource: add dependencies/resources.
- R2-boundary: add constraints/not-for.
- Full artifact.

Expected result:

- Use conditions and output/workflow fields should improve controlled semantic-confusion performance.
- Dependencies/resources and boundaries may not behave as simple positive text; they should improve only when used conditionally.

### External Validity

Use public skills in three roles:

1. background distractors for scale;
2. audit corpus for field-existence claims;
3. separate public-gold evaluation stratum.

Public-gold results should not be merged with controlled results unless the gold labels are equally stable.

## 4. Comparison Against External Work

| Work | What it mainly tests | Relevance to this thesis | Remaining gap this thesis can own |
|---|---|---|---|
| SkillRouter | Large-scale retrieve-and-rerank skill routing; full skill body versus metadata | Direct competitor for scalable skill routing and progressive-disclosure weakness | Does not isolate which procedural fields inside the skill body matter most |
| SkillRet | Large-scale public skill retrieval benchmark with taxonomy and many queries | Shows skill retrieval is a standalone benchmark problem | Focuses on retrieval behavior at scale, less on semantic near-neighbour procedural field ablation |
| Skill Retrieval Augmentation | Retrieve, incorporate, and execute skills dynamically | Supports separating retrieval from incorporation/execution | Does not deeply test representation-field preservation |
| AgentSkillOS | Capability tree and DAG orchestration for skill ecosystems | Relevant to M4 tree routing and multi-skill orchestration | Tree routing should be an architecture probe, not assumed superior |
| SkillNet | Ontology/graph infrastructure for connecting skills | Relevant to M5 graph retrieval | Need edge-type ablations to show which relations matter for retrieval |
| SkillsBench | Benchmarks whether skills help across tasks | Warns that skills are not automatically useful | This thesis can focus before execution: selection quality under semantic confusion |
| SWE-Skills-Bench | Requirement-driven downstream utility of SWE skills | Strong caution: many skills do not improve pass rate | Downstream validation should be modest and explicit |
| ToolRerank | Hierarchy-aware reranking for tool retrieval | Strong baseline idea for tree/hierarchy signals | Tools are usually atomic; skills are procedural artifacts |
| ToolLLM/ToolBench | API/tool retrieval and tool-use training | Historical baseline for neural API retrieval | API retrieval differs from procedural skill retrieval |

## 5. Suggested Subagent Critique Prompt

Use this prompt when asking a subagent or reviewer to critique the thesis:

> Evaluate this thesis as a research-methods examiner. Do not only say whether the topic is good. Compare it against SkillRouter, SkillRet, SRA, AgentSkillOS, SkillNet, SkillsBench, SWE-Skills-Bench, ToolRerank, and ToolLLM/ToolBench. For each comparison, state whether the thesis has a distinct contribution or is duplicating prior work. Then evaluate whether the experiments can falsify the core claim: procedural information fields improve selection among semantically similar skills when used by field-aware retrieval/reranking. Separate evidence into benchmark validity, field taxonomy validity, retrieval performance, public-skill external validity, and downstream task validity. End with the minimum experiment set needed for a defensible honours thesis.

## 6. Minimum Experiment Set For A Defensible Thesis

Required:

1. Controlled benchmark validation on the 2401-skill library.
2. Public-skill field audit with evidence that proposed fields exist or can be extracted.
3. Field ablation over R1/R2/R3/Full.
4. Modern dense baseline and generic reranking baseline.
5. M6-v1 field-aware reranking.
6. Candidate-recall decomposition.
7. Clean public-gold reporting after manual adjudication.

Nice to have:

1. M4 tree routing probe.
2. M5 graph edge ablation.
3. 12-20 case downstream validation.

Do not add more scale or more providers until M6-v1 and public-gold cleanup are complete.

## 7. Sources To Revisit

- SkillRouter: https://arxiv.org/abs/2603.22455
- SkillRet: https://arxiv.org/abs/2605.05726
- Skill Retrieval Augmentation: https://arxiv.org/abs/2604.24594
- AgentSkillOS: https://arxiv.org/abs/2603.02176
- SkillNet: https://arxiv.org/abs/2603.04448
- SkillsBench: https://arxiv.org/abs/2602.12670
- SWE-Skills-Bench: https://arxiv.org/abs/2603.15401
- Agentic Skills in the Wild: https://arxiv.org/abs/2604.04323
- ToolRerank: https://aclanthology.org/2024.lrec-main.1413/
- ToolLLM/ToolBench: https://arxiv.org/abs/2307.16789
- Claude Code Skills docs: https://docs.claude.com/en/docs/claude-code/skills

