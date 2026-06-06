# Benchmark Risk Register and Mitigation Plan

Date: 2026-06-06

Purpose: record the current interpretation of benchmark risks so later methodology work does not drift into either overclaiming the benchmark or treating every caveat as fatal. The benchmark should be framed as a controlled stress test for skill-selection confusability, with public-skill evidence used for external validity and field-taxonomy grounding.

## Current Framing

The benchmark is not intended to be a general-purpose public benchmark. It is a thesis-specific stress test for the following situation:

> A skill selector must choose among semantically plausible candidate skills under scale, where the correct skill depends on operational information such as input state, output artifact, workflow, tool dependency, resource requirement, boundary condition, side effect, or success criterion.

This means that "procedural information" should be read broadly. It does not only mean workflow steps. It includes any operational field that changes which skill should be selected.

## Risk Register

| Risk | Why it matters | Current position | Mitigation / experiment |
|---|---|---|---|
| Co-adaptation between controlled skills and proposed fields | If controlled skills were authored around the exact fields being tested, field-aware methods may look better because the benchmark is shaped for them. | Real risk, especially for controlled schema-authored skills and `skill_representation_analysis`. | Add public-style controlled skills: generated/curated skills written in messy public `SKILL.md` style, then extract fields through the representation layer rather than hand-authoring neat schema fields. Keep implicit-field stress cases separate and expand them. |
| Gold-label instability under public/background competition | A background or public skill may sometimes be genuinely better than the designed gold, making a retrieval "failure" actually an annotation failure. | Still one of the most important validity risks. Some acceptable alternatives are already recorded, but stronger manual adjudication is needed for final examples and failure cases. | For top failures and non-core winners, manually inspect gold, predicted skill, and alternatives. Label each as wrong retrieval, acceptable duplicate, broad parent/router, better-than-gold, or prompt ambiguity. Strict and acceptable scoring must remain separate. |
| Prompt leakage | Exact name leakage is currently controlled, but prompts can still contain strong title-like cues or negative boundaries that make selection easier. | Exact/high-risk leakage passes, but medium cueing remains a design choice. Some boundary phrases are natural and necessary; not all cueing is invalid. | Add prompt-information levels: high-information explicit prompts, medium natural prompts, and low-information/underspecified prompts. Report them separately so the thesis can show when field-aware retrieval helps and when clarification is needed. |
| Platform-name bias | Provider/tool names such as Hugging Face, Figma, Shopify, Netlify, OpenAI, or Sentry can be legitimate selection evidence, but they can also make retrieval too easy. | Not a simple flaw. Tool/provider dependency is one of the information fields that can correctly determine skill choice. The risk is overrepresenting provider-name cases and calling them procedural reasoning. | Treat provider/tool as a valid `dependency_or_tool` field, but stratify results into provider-explicit versus provider-implicit cases. Add cases where the provider name is absent but workflow/output implies the dependency, and cases where provider name alone is insufficient. |
| Generated-background limitation | Generated background skills create scale pressure, but they may not match public-library messiness, duplication, hierarchy, and uneven quality. | Current scale is useful for context/candidate pressure, not enough for broad ecosystem claims. | Import more real public skills where possible, but do not automatically use them as gold labels. Use public skills first as background distractors and field-taxonomy evidence; promote them to public-gold only after manual atomization and acceptable-alternative review. |
| Public skill messiness | Public skills are broad, duplicated, hierarchical, platform-specific, and sometimes under-specified. | This cannot be fully "solved"; it is part of the phenomenon being studied. | Report public-gold separately from controlled. Use strict and acceptable scoring. Treat broad/hierarchical skills as router/parent candidates unless the request explicitly asks for routing or orchestration. |
| Semantic-check limitation | MiniLM semantic checks are useful for benchmark construction, but not a final authority on semantic confusability. | MiniLM validates construction, while Qwen/SkillRouter results provide stronger retrieval evidence. | Justify semantic confusion through multiple signals: manual cluster audit, local embedding similarity, stronger dense retriever top-k behaviour, and failure-mode analysis. Do not rely on one embedding model as the definition of semantic similarity. |
| Methodology conflation | Representation effects, retriever architecture, reranker architecture, candidate budget, prompt information, and public/controlled strata can be mixed together. | Current notes already identify this, but final tables must enforce it. | Use crossed design: representation layer x retriever/reranker x candidate budget x stratum. Compare horizontally within the same architecture and vertically within the same representation. Report cost/latency/token budget beside accuracy. |
| M6-v1-local lexical limitation | Current field-aware reranker uses cue extraction and lexical field overlap, not robust semantic entailment. | This is already recorded. Controlled gains are meaningful but should not be overclaimed as final structure-aware reasoning. | Audit request-field extraction manually. Implement or plan M6-v2: semantic/LLM-assisted field extraction and field matching, with evidence spans and contradiction/boundary handling. |
| Downstream task gap | Retrieval accuracy does not automatically imply better agent task success. | Planned, not done. | Run a small downstream validation after offline retrieval stabilizes: compare no-skill/wrong-skill/top-retrieved/oracle-gold conditions on selected high-confusion tasks. |

## Prompt Information Levels

To address leakage, platform cues, and underspecification without pretending they are the same problem, future prompts should be grouped into information levels:

| Level | Description | Purpose |
|---|---|---|
| L3 high-information | Prompt explicitly states artifact type, desired output, constraints, and sometimes "not X" boundaries. | Tests whether methods can use clearly available selection information. Good for controlled causal analysis. |
| L2 natural-information | Prompt resembles a normal user request with enough detail to infer the correct skill, but fewer explicit negations. | Best main benchmark condition. Tests realistic selection under semantic similarity. |
| L1 low-information | Prompt is short or underspecified, and several skills may be reasonable. | Tests clarification need and robustness. Should be scored separately; not all failures are retrieval failures. |
| Provider-explicit | Tool/provider name is directly mentioned. | Tests dependency/tool matching. Valid when provider is genuinely required. |
| Provider-implicit | Provider name is absent, but workflow or artifact implies the needed tool. | Tests whether representation and retriever infer operational fit beyond name matching. |

This lets the thesis avoid a false choice. Provider names and explicit boundaries are legitimate information, but they should be reported as different prompt conditions rather than mixed into one undifferentiated accuracy score.

## Public-Style Controlled Skills

Recommended next benchmark improvement:

1. Select 6-10 strong cluster families from the audit.
2. For each family, create or import skills written in public style: less structured, more prose, sometimes with examples/resources, but still atomic enough for gold labels.
3. Do not hand-author neat R2 fields in the raw skill.
4. Extract R2/R3 fields through the representation layer.
5. Validate whether the extracted fields match manual gold rationales.
6. Run the same methods on:
   - controlled structured skills;
   - public-style controlled skills;
   - public-gold skills.

This directly tests whether field-aware retrieval only works on neat schema-authored skills or whether the representation layer can recover useful information from messier artifacts.

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

