# Skeptical Research Methods Critique - 2026-06-03

Role: skeptical research-methods critic for the current honours thesis framing.

## 1. What I Like

The thesis has a real and timely problem. Recent systems and papers increasingly treat skills as reusable procedural capability units rather than simple tool calls. The current framing correctly separates the stored skill artifact, the selection representation, and the retrieval policy. That separation is strong because it prevents the common confusion between "we used a better retriever" and "we preserved better skill information."

The benchmark target is also sensible: semantically similar but procedurally different skills. This is more interesting than broad-domain retrieval. A system that can distinguish PDF OCR, PDF table extraction, PDF field extraction, and PDF question answering is testing a more realistic failure mode than a system that only distinguishes "PDF" from "GitHub."

The public-skill audit is a strong move. It helps defend the field taxonomy against the criticism that the benchmark was authored to reward the proposed schema. The manual public-gold adjudication is also good research hygiene: 21 strict keep, 7 acceptable-alternative cases, and 4 revise/exclude cases is much more credible than pretending all public targets are clean.

## 2. What I Dislike / Think Is Risky

The project is still at risk of overbreadth. Flat metadata, dense embeddings, structured fields, procedural reranking, tree routing, graph retrieval, generic reranking, public-gold validation, downstream task success, and field taxonomy are each publishable-sized subproblems. For an honours thesis, the core should be: which information fields help, and does a field-aware reranker use them better than flat/full-text retrieval? M4 tree and M5 graph should remain optional unless they answer a very specific follow-up.

The current schema reranker, M6-v0, is too weak to support the final claim. It uses weighted lexical overlap, so if it wins on controlled clusters, a critic can say the benchmark rewarded your hand-authored schema wording. If it loses on public-gold cases, a critic can say the extracted fields are not robust. The thesis should explicitly label M6-v0 as diagnostic and make M6-v1 the real test.

The public-gold results currently weaken the strongest version of the claim. Qwen generic reranking performs best on public-gold top-1, while naive schema overlap struggles. This does not kill the thesis, but it means the final argument cannot simply be "structured fields beat embeddings." It should be "fields help when they are extracted accurately and used with field-aware matching; naive structured text is not enough."

The benchmark scale is defensible but not enormous relative to new papers. SkillRet has 17,810 public skills and SkillRouter studies around 80K skills. Your 2401-skill library is still fine for honours work, but the claim should be "controlled scalable setting" rather than "large-scale benchmark comparable to current SOTA datasets."

## 3. Are The RQs Novel And Credible?

Yes, with tighter wording. RQ1 is the strongest: "What information must skill representations preserve?" This is novel enough because SkillRouter and SkillRet show retrieval is hard, but do not deeply isolate which fields inside the artifact matter.

RQ2 is credible, but too broad if it promises tree and graph as fully evaluated. Reframe it as comparing retrieval strategies over the same information conditions, with M4/M5 as planned or optional architecture probes. The thesis should not imply that graph retrieval is a central completed contribution unless it is implemented with edge ablations.

## 4. Is The Method Comparison Too Broad?

Currently, yes. The final comparison should be:

1. M0 progressive disclosure baseline, mainly for realism and cost.
2. M1 flat metadata lexical control.
3. M2 modern dense retrieval over R1 and full artifacts.
4. M3 structured-card retrieval over R2.
5. Generic neural reranker as strong baseline.
6. M6-v1 field-aware procedural reranker as the proposed method.

M4 tree routing should be reported only if you can show branch accuracy, candidate reduction, and gold-excluded-by-branch failures. M5 graph retrieval should be reported only if you can run edge ablations such as trigger-only, trigger+output, trigger+output+workflow, and full graph. Otherwise, keep them in methodology/future work.

## 5. Missing Evidence Before Final Writing

The biggest missing evidence is M6-v1. Without it, the thesis has good evidence that fields are useful, but not yet a clean demonstration that a method using those fields improves selection.

The second missing piece is cleaned public-gold reporting. The 4 revise/exclude cases need removal or prompt updates, and acceptable alternatives should be applied before final public-gold metrics.

The third missing piece is candidate-recall decomposition. For every reranker result, report whether the gold skill was in the first-stage top-k. Otherwise failures blur together: retrieval failure, reranker failure, extraction failure, and gold-label ambiguity.

The fourth missing piece is downstream validation. A small 12-20 case study is enough. It should compare oracle-gold, dense top-1, generic rerank top-1, and M6-v1 top-1 or top-k. If downstream execution is not done, the thesis must avoid claiming agent task-success improvement.

## 6. Sources To Cite / Use

- SkillRouter: https://arxiv.org/abs/2603.22455 - strongest direct support for full-body skill routing and progressive-disclosure limitations.
- SkillRet: https://arxiv.org/abs/2605.05726 - large-scale public skill retrieval benchmark; useful scale comparison.
- Skill Retrieval Augmentation: https://arxiv.org/abs/2604.24594 - frames retrieval, incorporation, and execution as separate stages.
- AgentSkillOS: https://arxiv.org/abs/2603.02176 - tree-based skill management and orchestration at ecosystem scale.
- SkillNet: https://arxiv.org/abs/2603.04448 - ontology/graph view of skills as connected assets.
- SkillsBench: https://arxiv.org/abs/2602.12670 - shows curated skills help unevenly and focused skills can beat broad documentation.
- Claude Skills overview: https://claude.com/docs/skills/overview - primary source for progressive disclosure.
- Claude Code Agent Skills docs: https://docs.claude.com/en/docs/claude-code/skills - primary source for SKILL.md, descriptions, and optional resources.
- ToolRerank: https://aclanthology.org/2024.lrec-main.1413/ - hierarchy-aware reranking baseline from tool retrieval.
- SWE-Skills-Bench: https://arxiv.org/abs/2603.15401 - cautionary evidence that skills do not automatically improve downstream task success.

## Verdict

The thesis is promising, but the contribution should be narrowed. The best version is not "graph beats embedding" or "schema beats Qwen." The best version is: skill retrieval fails when compressed representations lose procedural evidence; use conditions, outputs, and workflow are the strongest positive signals; boundaries and dependencies need conditional handling; and field-aware reranking is a principled way to use those signals under semantic confusability.
