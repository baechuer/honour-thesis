# Temporary Literature Collection: Skill Quality And Retrieval

Date: 2026-05-28

This is a temporary working collection of papers to inspect later for the thesis literature review. The focus is not general LLM agents, but agent skill artifacts, skill quality, skill retrieval, and what information should be preserved in skill representations.

Credibility labels:

- `peer-reviewed / workshop`: accepted to a named workshop or conference-adjacent venue; useful, but check whether it is archival.
- `preprint`: arXiv or similar; useful but not peer reviewed yet.
- `standard / docs`: not academic evidence, but useful for describing real system conventions.

## Highest Priority

| Paper | Status | Why It Matters | How We Use It |
|---|---|---|---|
| What Keeps Agent Skills from Being Reusable? Evidence from 138K SKILL.md Files | Agent Skills '26 poster, ACM CAIS workshop; likely workshop-reviewed but not necessarily archival | Directly analyzes public `SKILL.md` files at ecosystem scale. Provides a reusable-skill quality taxonomy covering routing, body design, resources, prohibited content, safety, portability, and scope/persona conflicts. Identifies high-quality traits such as trigger-complete descriptions, imperative/actionable body text, and project-specific procedural knowledge. | Use as the main external justification for the claim that real skill artifacts contain quality-relevant structural signals. Our thesis then asks whether preserving such signals improves retrieval. |
| Agent Skills: A Data-Driven Analysis of Claude Skills for Extending Large Language Model Functionality | arXiv preprint | Analyzes 40,285 public marketplace skills. Reports skill categories, adoption patterns, length distribution, redundancy/homogeneity, and safety risks. | Use to justify the scale, redundancy, and semantic-overlap problem in public skill ecosystems. |
| SkillRouter: Skill Routing for LLM Agents at Scale | arXiv preprint | Studies skill routing at ~80K scale. Finds that hiding the skill body and showing only name/description causes large routing degradation; proposes retrieve-and-rerank. | Use to justify why progressive disclosure metadata is insufficient and why full body/procedural information matters for routing. |
| SkillRet: A Large-Scale Benchmark for Skill Retrieval in LLM Agents | arXiv preprint | Contains 17,810 public skills with semantic tags and taxonomy, plus large training/evaluation data. Shows off-the-shelf retrievers struggle on realistic skill retrieval. | Use as evidence that skill retrieval is a distinct benchmark problem and not solved by generic semantic search. |
| SkillFlow: Scalable and Efficient Agent Skill Retrieval System | arXiv preprint | Builds a multi-stage retrieval pipeline over ~36K community `SKILL.md` files. Emphasizes retrieval scale, corpus quality, runnable code, and bundled artifacts. | Use to support multi-stage retrieval design and the claim that skill quality/resources affect downstream usefulness. |

## Skill Structure, Generation, And Quality

| Paper | Status | Why It Matters | How We Use It |
|---|---|---|---|
| SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks | arXiv preprint, benchmark with public site | Shows curated skills improve pass rate, self-generated skills do not reliably help, and focused skills outperform broad documentation. | Use to argue that skill quality and structure matter, not merely the existence of a skill file. |
| From Raw Experience to Skill Consumption: A Systematic Study of Model-Generated Agent Skills | arXiv preprint | Studies the skill lifecycle: experience generation, skill extraction, and skill consumption. Analyzes what properties characterize useful skills and negative transfer. | Use for discussion of skill quality and why representation should preserve utility-bearing properties. |
| SKILLFOUNDRY: Building Self-Evolving Agent Skill Libraries from Heterogeneous Scientific Resources | arXiv preprint | Says skills should encode task scope, inputs/outputs, execution steps, environment assumptions, provenance, and tests. | Very useful for justifying our procedural schema fields: scope, input, output, workflow, dependencies/environment, provenance/resources, tests. |
| Skill-Pro: Learning Reusable Skills from Experience via Non-Parametric PPO for LLM Agents | arXiv preprint | Defines reusable procedural skills through activation, execution, and termination conditions. | Use as conceptual support for preconditions/activation and procedure/termination-style fields. |
| Graph of Skills: Dependency-Aware Structural Retrieval for Massive Agent Skills | Hugging Face paper page / likely preprint | Constructs executable skill graphs and retrieves dependency-aware bundles under context budgets. | Use to motivate dependency/resource-aware and graph-based representations. |

## Security, Risk, And Operational Quality

| Paper | Status | Why It Matters | How We Use It |
|---|---|---|---|
| Towards Secure Agent Skills: Architecture, Threat Taxonomy, and Security Analysis | arXiv preprint | Defines a lifecycle for Agent Skills and a threat taxonomy across creation, distribution, deployment, and execution. | Use as supporting evidence for preserving safety-relevant constraints, dependencies, and execution boundaries. |
| Quality in the Agent Skills Ecosystem: A Structural, Behavioral, ... | status unclear; PDF found online | Appears to analyze skill ecosystem quality, reference files, contamination, and security/structural defects. | Inspect later before citing. Do not rely on it until authorship, venue, and methodology are verified. |

## Standards And System Conventions

| Source | Status | Why It Matters | How We Use It |
|---|---|---|---|
| SkillsBench docs / contributing guide | public benchmark docs | Shows real benchmark tasks use `SKILL.md`, optional `scripts/`, and optional `references/`; also emphasizes distractor skills and skill composition. | Use as system/design context, not as peer-reviewed evidence. |
| SKILL.md open-standard/spec pages | standard/docs/blog ecosystem | Useful for the practical file format: frontmatter, description, body, scripts/resources/references. | Use sparingly as format/context evidence, not academic support. |
| Agent Skills '26 workshop site | ACM CAIS workshop site | Gives venue context: 103 submissions, 45 posters, 6 oral presentations, topics include design, evaluation, optimization, safety, and skill ecosystem infrastructure. | Use to show the field is emerging and active, but do not overclaim peer-reviewed archival status. |

## Credibility Notes

At the moment, many of the strongest skill-specific papers are very recent and appear as arXiv preprints or workshop papers. This is normal for a fast-moving 2026 topic, but the thesis should be careful:

- Treat workshop papers as stronger than blog posts, but weaker than established archival conference/journal papers unless proceedings status is confirmed.
- Treat arXiv preprints as useful technical evidence, but describe them as preprints if no venue is listed.
- Use the most credible papers for the core literature claims:
  - `What Keeps Agent Skills from Being Reusable?` for public skill quality and common defects.
  - `SkillRouter`, `SkillRet`, and `SkillFlow` for skill retrieval at scale.
  - `SkillsBench` for skill efficacy and curated-vs-generated skill quality.
  - `SkillFoundry` for a field taxonomy close to our representation schema.

## Draft Literature Framing

Prior work now gives us a stronger foundation:

1. Skill benchmark work shows that curated procedural skills can improve agent performance, but skill quality is uneven.
2. Public-skill ecosystem analyses show that real `SKILL.md` artifacts contain recurring structural and quality signals, including routing descriptions, body organization, resources, portability issues, safety boundaries, and project-specific procedural knowledge.
3. Retrieval papers show that large skill libraries make full-context enumeration infeasible and that name/description metadata alone is often insufficient.
4. Skill construction papers suggest that useful skills encode scope, inputs, outputs, procedures, environment assumptions, provenance, and tests.

Gap for this thesis:

> Existing work studies skill usefulness, ecosystem quality, and large-scale retrieval, but there is still limited controlled evidence about which preserved information fields help distinguish semantically similar but procedurally different skills at retrieval time.

That lets us position the thesis as building on, not replacing, the new ecosystem-quality papers.

## Links

- What Keeps Agent Skills from Being Reusable?: https://openreview.net/forum?id=n0AIlfxDU0
- Agent Skills '26 workshop: https://www.agentskills-workshop.org/
- Agent Skills data-driven analysis: https://arxiv.org/abs/2602.08004
- SkillRouter: https://arxiv.org/abs/2603.22455
- SkillRet: https://arxiv.org/abs/2605.05726
- SkillFlow: https://arxiv.org/abs/2504.06188
- SkillsBench: https://arxiv.org/abs/2602.12670
- SkillFoundry: https://arxiv.org/abs/2604.03964
- From Raw Experience to Skill Consumption: https://arxiv.org/abs/2605.23899
- Towards Secure Agent Skills: https://arxiv.org/abs/2604.02837
