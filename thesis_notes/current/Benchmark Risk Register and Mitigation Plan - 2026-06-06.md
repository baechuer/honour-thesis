# Benchmark Risk Register and Mitigation Plan

Date: 2026-06-23 refresh of the 2026-06-06 risk register

> **2026-08-02 RQ2 status.** RQ1a remains `REVIEWED / COMPLETE`. RQ2a is `CONFIRMATORY COMPLETE / USER-REVIEWED / THESIS-INTEGRATED`; all 13,200 primary rows, frozen paired inference, costs, cache checks, and failure analysis pass. The evidence rejects a universal field-heading advantage under Qwen single-vector selection and supports a narrower representation-retrieval compatibility claim. RQ2b is `B0F FROZEN / B0F-A1 APPROVED / B1X COMPLETE / B1S SEALED / B1R APPROVAL OUTSTANDING`, with no transfer or scientific result. Older architecture, graph/tree, and broad I1/I2/I3 risks below remain historical risks; active controls and gates are governed by the canonical RQ2 tracker and execution ledger.

Purpose: record the current interpretation of benchmark risks so later methodology work does not drift into either overclaiming the benchmark or treating every caveat as fatal. The benchmark should be framed as a controlled stress test for skill-selection confusability, with public-skill evidence used for external validity and field-taxonomy grounding.

## Current Framing

The benchmark is not intended to be a general-purpose public benchmark. It is a thesis-specific stress test for the following situation:

> A skill selector must choose among semantically plausible candidate skills under scale, where the correct skill depends on operational information such as input state, output artifact, workflow, tool dependency, resource requirement, boundary condition, side effect, or success criterion.

This means that "procedural information" should be read broadly. It does not only mean workflow steps. It includes any operational field that changes which skill should be selected.

## Current Benchmark Pros After Frozen v0.4 Expansion

Updated after freezing `benchmark-v0.4-2026-06-16` and generating the consolidated I1/I3/I2 information-layer matrix.

| Strength | Why it helps the thesis | Evidence |
|---|---|---|
| Controlled scale is now credible for an honours study | The benchmark is no longer a tiny toy library, and the selector ranks against thousands of skills. | 2433 total skills; 245 controlled prompts; 144 separate public-gold prompts; 12 low-information stress prompts. |
| Confusability is intentional rather than accidental | Clusters are designed so alternatives are plausible semantic neighbours but procedurally different. | Step 3 semantic confusability passes 243/245 controlled prompts and 144/144 public-gold prompts. |
| Procedural distinctness is explicitly checked | The benchmark does not only ask whether skills are phrased differently; it checks gold/alternative procedural axes. | Step 2 distinctness passes 245/245 controlled prompts with 830/830 controlled pairs, and 144/144 public-gold prompts with 575/575 public-gold pairs. |
| Gold fit is mostly stable under prompt-specific checking | The stricter check asks whether the prompt requirement aligns better with gold than listed alternatives. | Controlled prompt-specific alignment is 238/245; public-gold prompt-specific alignment is 131/144; residual reasons are recorded separately. |
| Public-style controlled skills reduce neat-schema co-adaptation | Raw skills are more prose-like and require field extraction before structured retrieval. | 8 public-style clusters, 32 skills, 64 prompts; all pass integrity/leakage/confusability gates. |
| Public skills ground the field taxonomy | Public skills are used as background and as a field-audit source, so the proposed fields are not only invented from controlled skills. | 460 imported public skills audited heuristically and with DeepSeek model-assisted verification. |
| Information-layer results show useful difficulty | The benchmark is not solved by simple methods, and I3 structured fields help most clearly on controlled prompts. | Frozen v0.4 controlled top-1: TF-IDF I1 53.9% vs I3 64.5%; Qwen rerank I1 51.4% vs I3 58.0%; SkillRouter rerank I1 65.7% vs I3 71.0%. |
| The benchmark supports failure-mode analysis | Wrong choices can be classified as candidate-miss, semantic near-neighbour, field extraction weakness, boundary misuse, or acceptable alternative. | First-pass R2/I3 failure comparison exists for Qwen, SkillRouter, and SkillRouter+M6-v1 on controlled and public-gold. |

## Current Benchmark Risks After Public-Style Expansion

| Risk | Current severity | Why it remains | Current mitigation |
|---|---|---|---|
| Generated public-style skills are still designed by us | Medium-high | They are less schema-neat, but still generated to fit our hypothesis and cluster plan. | Report public-style controlled separately; use public-gold and public-field audit as external validity checks. |
| Weak requirement-alignment cases remain | Medium | 7/245 controlled prompts and 13/144 public-gold prompts do not cleanly pass the stricter Step 2 prompt-specific alignment check. | Manually audit weak prompts before final headline examples; record acceptable alternatives or revise only in a new benchmark version if needed. |
| Provider/tool dependency cues need careful interpretation | Medium | Hugging Face, GitHub, Playwright, Figma, and similar names are often real dependency requirements for provider-specific skills. They become a validity problem only when the provider name alone decides the label while input, output, workflow, or success criterion do not support it. | Keep provider/tool cues when they are part of the task. Stratify provider-explicit and provider-implicit prompts, and require gold rationales to cite at least one non-name procedural axis as well. |
| M6-v1-local is lexical | Medium-high | Current field-aware reranker still uses transparent token/field matching, not semantic entailment. | Treat as diagnostic prototype; M6-v2 semantic field matching exists but also needs activation/failure audit before being a final method. |
| Public-gold is messy and label-stability-sensitive | Medium-high | Public skills are broad, hierarchical, duplicated, or platform-specific; strict gold labels may be debatable. | Keep public-gold as separate stratum; use strict and acceptable metrics; manually adjudicate failures. |
| External SkillRouter-Eval-Core is cue-rich | Medium | The external benchmark is much larger and externally sourced, but its scored tasks average 198.4 rough tokens, have median 169 rough tokens, and usually include file/path, input, and output cues. Its skill bodies are also highly markdown-normalized, with frequent headings such as `overview`, `when to use`, `workflow`, `quick start`, and `dependencies`. | Use SkillRouter-Eval-Core as portability and scale evidence, not as a direct replacement for the local controlled semantic-confusability benchmark. Report corpus/prompt audit caveats beside external results. |
| Large JSON outputs are heavy for Git/reproduction | Low-method, medium-engineering | Generated result JSONs preserve evidence but make the repository large and slow to push. | Keep summary MD files for reading; consider Git LFS or compressed artifacts later if repo maintenance becomes painful. |
| Downstream task success is still untested | Medium | Retrieval accuracy does not automatically prove better agent execution. | Run Step 9 on a smaller high-confusion sample after offline retrieval stabilizes. |
| Graph/tree methods are still planned, not executed | Low-medium | The thesis discusses structure-aware alternatives, but current empirical evidence is mainly cards/rerankers. | Either implement a focused M4/M5 experiment or frame graph/tree as future work rather than a completed comparison. |
| RQ2a cost/latency is quantified, but end-to-end cost is not | Medium | RQ2a now separates one-time Qwen construction, cached online scoring, and novel-pair SkillRouter cross-encoder time. It still fixes three candidates and therefore does not measure full-library candidate-generation cost. | Report the completed RQ2a ledger with its fixed-candidate boundary; reserve full-library token, candidate-budget, and amortisation claims for reviewed RQ2b work. |

## Risk Register

| Risk | Why it matters | Current position | Mitigation / experiment |
|---|---|---|---|
| Co-adaptation between controlled skills and proposed fields | If controlled skills were authored around the exact fields being tested, field-aware methods may look better because the benchmark is shaped for them. | Real risk, especially for controlled schema-authored skills and `skill_representation_analysis`. | Add public-style controlled skills: generated/curated skills written in messy public `SKILL.md` style, then extract fields through the information-layer pipeline rather than hand-authoring neat schema fields. Keep implicit-field stress cases separate and expand them. |
| Gold-label instability under public/background competition | A background or public skill may sometimes be genuinely better than the designed gold, making a retrieval "failure" actually an annotation failure. | Still one of the most important validity risks. Some acceptable alternatives are already recorded, but stronger manual adjudication is needed for final examples and failure cases. | For top failures and non-core winners, manually inspect gold, predicted skill, and alternatives. Label each as wrong retrieval, acceptable duplicate, broad parent/router, better-than-gold, or prompt ambiguity. Strict and acceptable scoring must remain separate. |
| Prompt leakage | Exact skill-name leakage is controlled, but prompts can still contain title-like cues, copied phrases, or negative boundaries that make selection easier. | Exact/high-risk leakage passes, but medium cueing remains a design choice. Some boundary phrases are natural and necessary; not all cueing is invalid. Provider/tool names are not automatically leakage when they are genuine task dependencies. | Add prompt-information levels: high-information explicit prompts, medium natural prompts, and low-information/underspecified prompts. Report them separately so the thesis can show when field-aware retrieval helps and when clarification is needed. |
| Provider/tool dependency cues | Provider/tool names such as Hugging Face, Figma, Shopify, Netlify, OpenAI, or Sentry can be legitimate selection evidence because many public skills are provider-tailored. | Not a simple flaw. Tool/provider dependency is one of the information fields that can correctly determine skill choice. The risk is overrepresenting provider-name cases and then calling the result evidence for broader procedural reasoning. | Treat provider/tool as a valid `dependency_or_tool` field. Keep provider names when the user task genuinely requires that provider. Stratify provider-explicit versus provider-implicit cases, and require gold rationales to also identify input/output/workflow/success-criterion evidence. |
| Generated-background limitation | Generated background skills create scale pressure, but they may not match public-library messiness, duplication, hierarchy, and uneven quality. | Current scale is useful for context/candidate pressure, not enough for broad ecosystem claims. | Import more real public skills where possible, but do not automatically use them as gold labels. Use public skills first as background distractors and field-taxonomy evidence; promote them to public-gold only after manual atomization and acceptable-alternative review. |
| Public skill messiness | Public skills are broad, duplicated, hierarchical, platform-specific, and sometimes under-specified. | This cannot be fully "solved"; it is part of the phenomenon being studied. | Report public-gold separately from controlled. Use strict and acceptable scoring. Treat broad/hierarchical skills as router/parent candidates unless the request explicitly asks for routing or orchestration. |
| Semantic-check limitation | MiniLM semantic checks are useful for benchmark construction, but not a final authority on semantic confusability. | MiniLM validates construction, while Qwen/SkillRouter results provide stronger retrieval evidence. | Justify semantic confusion through multiple signals: manual cluster audit, local embedding similarity, stronger dense retriever top-k behaviour, and failure-mode analysis. Do not rely on one embedding model as the definition of semantic similarity. |
| Methodology conflation | Information-layer effects, retriever architecture, reranker architecture, candidate budget, prompt information, and public/controlled strata can be mixed together. | Current notes already identify this, but final tables must enforce it. | Use crossed design: information layer x retriever/reranker x candidate budget x stratum. Compare horizontally within the same architecture and vertically within the same information artifact. Report cost/latency/token budget beside accuracy. |
| M6-v1-local lexical limitation | Current field-aware reranker uses cue extraction and lexical field overlap, not robust semantic entailment. | This is already recorded. Controlled gains are meaningful but should not be overclaimed as final structure-aware reasoning. | Audit request-field extraction manually. Implement or plan M6-v2: semantic/LLM-assisted field extraction and field matching, with evidence spans and contradiction/boundary handling. |
| Downstream task gap | Retrieval accuracy does not automatically imply better agent task success. | Planned, not done. | Run a small downstream validation after offline retrieval stabilizes: compare no-skill/wrong-skill/top-retrieved/oracle-gold conditions on selected high-confusion tasks. |

## Prompt Information Levels

To address exact leakage, provider/tool dependency cues, and underspecification without pretending they are the same problem, future prompts should be grouped into information levels:

| Level | Description | Purpose |
|---|---|---|
| L3 high-information | Prompt explicitly states artifact type, desired output, constraints, and sometimes "not X" boundaries. | Tests whether methods can use clearly available selection information. Good for controlled causal analysis. |
| L2 natural-information | Prompt resembles a normal user request with enough detail to infer the correct skill, but fewer explicit negations. | Best main benchmark condition. Tests realistic selection under semantic similarity. |
| L1 low-information | Prompt is short or underspecified, and several skills may be reasonable. | Tests clarification need and robustness. Should be scored separately; not all failures are retrieval failures. |
| Provider-explicit | Tool/provider name is directly mentioned. | Tests dependency/tool matching. Valid when provider is genuinely required by the skill or user task. |
| Provider-implicit | Provider name is absent, but workflow, artifact, API surface, or deployment target implies the needed tool. | Tests whether representation and retriever infer operational fit beyond name matching. |

This lets the thesis avoid a false choice. Provider names, tool names, and explicit boundaries are legitimate information when they represent real dependencies or task constraints. They should be reported as prompt conditions, not erased from the benchmark and not treated as automatic leakage.

## Public-Style Controlled Skills

Recommended next benchmark improvement:

1. Select 6-10 strong cluster families from the audit.
2. For each family, create or import skills written in public style: less structured, more prose, sometimes with examples/resources, but still atomic enough for gold labels.
3. Do not hand-author neat R2 fields in the raw skill.
4. Extract I3/R2-R3 fields through the information-layer pipeline.
5. Validate whether the extracted fields match manual gold rationales.
6. Run the same methods on:
   - controlled structured skills;
   - public-style controlled skills;
   - public-gold skills.

This directly tests whether field-aware retrieval only works on neat schema-authored skills or whether the information-layer pipeline can recover useful information from messier artifacts.

## Semantic Confusability Evidence

Semantic confusion should be justified with converging evidence:

- manual cluster audit: alternatives are plausible after reading names/descriptions;
- local embedding check: gold and alternatives are close enough under a simple model;
- strong embedding check: Qwen/SkillRouter first-stage retrieval places alternatives near gold;
- failure analysis: wrong top-ranked skills are often semantically plausible rather than random;
- human rationale: gold skill remains procedurally better after careful inspection.

The strongest argument is not "MiniLM says they are similar." The stronger argument is: multiple selectors and human inspection show near-neighbour pressure, while procedural fields explain why one skill should win.

## Cost And Economic Choice

The thesis should not only ask which method is most accurate. It should ask which representation/retrieval choice gives the best trade-off:

- selection accuracy;
- top-k recall;
- MRR;
- strict versus acceptable top-1;
- context tokens exposed to the main agent;
- retrieval/reranking latency;
- API or GPU cost;
- engineering cost of maintaining the representation;
- downstream task success.

This makes the contribution more practical. A field-rich representation may be justified if it improves selection enough to reduce wrong-skill downstream failures. A graph/tree method may only be justified if it reduces candidate cost without excluding the gold skill early.

## Graph/Tree Clarification

Graph/tree methods should not be framed as "an agent wanders through the graph" unless that is the actual experiment. More defensible options:

- Tree routing: classify request into a capability branch, then retrieve within that branch. Main risk is early wrong-branch exclusion.
- Graph expansion: retrieve seed candidates, then expand to neighbours connected by dependency, alternative, resource, family, or output-similarity edges. Main risk is noisy edges.
- Graph reranking: use edge features as additional signals for reranking. Main risk is overfitting graph construction.

The key metric for graph/tree methods is not only top-1. It is also branch recall, gold-exclusion rate, candidate reduction, latency, and whether the graph helps beyond the field-aware reranker.

## Working Thesis Claim

The safest claim is:

> The benchmark shows that skill retrieval should be treated as an information-preservation problem. Flat metadata and full-document embeddings expose different parts of the skill artifact, but neither guarantees that operational distinctions are preserved. Structured procedural fields can improve selection when they are extracted and matched reliably, especially in controlled near-neighbour clusters. Public-style and public-gold cases are necessary to test whether those fields generalize beyond neatly authored skills.

Avoid claiming:

- all structure-aware methods beat embeddings;
- public skills already cleanly support strict gold labels;
- M6-v1-local is a final semantic matcher;
- retrieval improvements automatically imply downstream task success.
