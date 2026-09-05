# Benchmark Methodology Rubric

This note is the working rubric for deciding whether the benchmark and information layers are good enough for the thesis.

The thesis studies skill selection as a candidate-subsetting layer before the main agent loads full skill artifacts. The benchmark should therefore test whether different information layers help a selector surface the right procedural skill under semantic confusion and scale.

Active frozen benchmark version: `benchmark-v0.4-2026-06-16`.

Freeze manifest:

- `skill_benchmark/versions/benchmark-v0.4-2026-06-16.md`
- `skill_benchmark/versions/benchmark-v0.4-2026-06-16.json`

For this version, the benchmark inputs are frozen at 245 controlled prompts, 144 public-gold prompts, 12 low-information stress prompts, and 2433 skills. New selector outputs may be added under `frozen_v0_4`, but prompt/skill edits require a new benchmark version.

For the current source of truth on experiment method IDs, information-layer/retriever/reranker combinations, run commands, and fair-comparison rules, use `thesis_notes/current/Experiment Methodology Tracker.md`. For the current research framing, use `thesis_notes/current/Information Layer Framework.md`. This rubric defines validation criteria; the tracker defines the current experiment matrix.

For model-parsed I3 extraction, use `thesis_notes/current/I3 Model Extraction Protocol.md`. Do not run a large model-parsed I3 extraction until the prompt/schema in that file is approved and frozen.

For experiment sequencing, use `thesis_notes/current/Thesis Experiment Roadmap.md`. This rubric answers "is the benchmark valid enough?" The roadmap answers "what experiment should happen next?"

For the current risk register and mitigation choices, use `thesis_notes/current/Benchmark Risk Register and Mitigation Plan - 2026-06-06.md`.

## Core Claim To Test

A benchmark item is useful when several skills look semantically plausible from compressed metadata, but only one skill is procedurally correct once task/use condition, input, output, workflow, preconditions, dependencies, resources, boundaries, relations, or success criterion are considered.

Current thesis framing:

- The core object is **selection information**, not a specific architecture.
- Explicit fields are not claimed as the only possible solution. They are an inspectable information layer for testing which information matters.
- If an information type is retrieval-critical, a scalable system must obtain it somewhere: author-provided metadata, deterministic parsing, LLM-assisted extraction, learned encoders/rerankers, or graph/tree relation structure.
- Graph and tree methods are valid only when they test relation or hierarchy information that cannot be cleanly reduced to a flat text card.

Good benchmark pressure means:

- high surface similarity between gold and alternatives
- clear procedural divergence between gold and alternatives
- stable gold labels
- non-trivial retrieval difficulty
- measurable degradation under scale
- visible differences between representation methods

## Nine-Step Benchmark Loop

Use this staged loop for benchmark validation. Do not treat the selector-evaluation step as an invitation to test unlimited methods; final method selection is governed by the experiment roadmap.

1. Validate skill and prompt integrity.
2. Validate information-layer coverage and procedural requirement alignment.
3. Validate semantic confusability.
4. Validate gold-label stability and prompt-leakage risk.
4b. Manually audit cluster design before expanding test cases.
5. Build or refresh scale regimes.
6. Audit public/real-world skill artifacts for information-field validity.
6b. Validate public skills as gold-label retrieval targets.
6c. Validate external SkillRouter-Eval-Core as a portability check.
7. Run offline selectors, rerankers, information-layer ablations, and scale-sensitivity checks.
8. Run the M0 progressive-disclosure main-agent baseline.
9. Run candidate-subsetting plus main-agent downstream checks on a smaller sample.

Loop rule:

- If Step 1 fails, fix references/frontmatter before any retrieval claims.
- If Step 2 fails, rewrite skills or prompts so the gold label is procedurally justified.
- If Step 3 fails, add or revise alternatives so errors are plausible semantic confusions.
- If Step 4 fails, rewrite ambiguous or leaked prompts.
- If Step 4b fails, do not add more prompts to that cluster yet; first clarify the intended procedural distinction, revise alternatives, or mark the cluster as unsuitable for headline claims.
- If Step 5 fails, add realistic background/public skills before claiming scale behavior.
- If Step 6 shows our proposed fields are mostly absent or non-extractable in public skills, reframe the schema as a proposed information-normalization layer and report that adoption gap explicitly.
- If Step 6c conflicts with the controlled benchmark, treat it as external-validity evidence and failure-mode evidence, not as a replacement for the controlled benchmark.
- If Step 6b fails, keep public skills as background distractors and field-taxonomy evidence only; do not use them as gold-label evaluation cases.
- If Step 7 is near-perfect for all methods, harden the benchmark before claiming representation value.
- If Step 8 or Step 9 disagrees with offline selectors, inspect whether the main-agent prompt policy or downstream artifact task is masking retrieval errors.

## 2026-06-16 Expansion Snapshot

The active broad benchmark now has 401 prompts: 245 controlled prompts, 144 public-gold prompts, and 12 low-information stress prompts. The controlled set includes two new expansion files (`benchmark_expansion_clear_confusability.json` and `public_like_extra_confusability.json`), and public-gold includes `public_gold_expansion_confusability.json`.

Post-expansion gates: controlled integrity PASS, procedural distinctness PASS (245/245 prompts, 830/830 pairs), prompt-specific alignment 238/245, semantic confusability 243/245, leakage PASS with 0 critical/high. Public-gold integrity PASS, procedural distinctness PASS (144/144 prompts, 575/575 pairs), prompt-specific alignment 131/144, semantic confusability 144/144, leakage PASS with 0 critical/high.

Scale/background checks: 2433 skills, including 1800 generated background-scale skills and 460 imported public skills; R1 flat metadata is approximately 332,992 tokens. Controlled background competition is active under flat semantic cards and reduced under procedural comparison, supporting the use of the benchmark as a scalable semantic-confusion stress test.

Detailed checkpoint: `thesis_notes/checkpoints/benchmark_validation/Test Case Expansion Toward 400 - 2026-06-16.md`.

## Current Experiment Snapshot

Last refreshed on 2026-06-19 against frozen benchmark `benchmark-v0.4-2026-06-16`.

- Active benchmark inputs: 245 controlled prompts, 144 public-gold prompts, 12 low-information stress prompts, and 2433 skills.
- Active comparable information-layer matrix: I1/R1 flat cards, I3/R2 structured selection fields, and I2/full `SKILL.md` artifacts.
- Extraction provenance: current frozen-v0.4 I3 is heuristic/section-based (`I3H`), not uniformly model-parsed. DeepSeek public-skill work verifies field presence (`I3V`) but is not the canonical retrieval representation. Model-parsed I3 (`I3M`) and ChatGPT/Codex-subagent parsed I3 (`I3C`) are separate extraction conditions and must use the frozen seven-field schema in `thesis_notes/current/I3 Model Extraction Protocol.md`.
- Active method coverage: BM25, TF-IDF, Qwen embedding, Qwen embedding + Qwen rerank, Qwen embedding + local schema diagnostic, SkillRouter embedding, SkillRouter embedding + SkillRouter rerank, SkillRouter embedding + M6-v1 diagnostic, and M6-v2 fixed diagnostic summaries.
- Consolidated matrix: `skill_benchmark/outputs/frozen_v0_4_information_layer_matrix.md`.
- Matrix status: no missing I1/I2/I3 rows for the audited frozen-v0.4 method families.
- Statistical status: first-pass bootstrap top-1 confidence intervals and paired McNemar tests exist for fixed-method I1/I3/I2 comparisons. Add MRR/top-k uncertainty only if those metrics become final headline claims.
- Failure-mode status: first-pass comparison exists for the main R2/I3 Qwen, SkillRouter, and SkillRouter+M6-v1 rows on controlled and public-gold strata: `skill_benchmark/outputs/frozen_v0_4_failure_mode_comparison.md`.
- Interpretation: controlled prompts show the clearest I3-over-I1 benefit; public-gold is more mixed because public names/descriptions and provider cues often carry useful information; full skill text is not monotonically better because it adds noise and token cost.
- External SkillRouter-Eval-Core first pass: 75 scored tasks, 78,361 Easy skills, 79,141 Hard skills, and 780 Hard-only distractors. Disk-backed BM25 shows I2 full body strongest; heuristic I3H improves over I1 on Hard Hit@1 but not Recall@20 or FullCoverage@20. This motivates model-parsed I3 rather than proving current I3H is sufficient.
- External I3 extraction status: DeepSeek `I3M` is complete for rows `0-2999`; ChatGPT/Codex `I3C` is complete for rows `3000-5999`. These older slices are extraction-quality pilots, not retrieval results. The scored SkillRouter tasks use 186 unique gold skills at rows `27018-27213`, so retrieval claims must use the newly parsed task-relevant I3C pool or a full-library/tier parse under a declared selector-visible universe.
- I3C V2 pilot status: first 200 rows of the SkillRouter top-20 task-relevant pool passed with minor QA caveats: 200/200 rows, 0 parse failures, 0 missing skill ids, 100% exact evidence-match, and populated QA warnings. This justified scaling to the top-20 task-relevant pool rather than the full 79k library first.
- I3C V2 top-20 task-relevant pool status: complete and cleaned. The canonical file is `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_top20_pool/I3C_V2_top20_pool_cleaned.jsonl`: 3284 rows, 0 parse failures, 0 missing skill ids, 0 duplicate skill ids, 25544/25544 exact evidence matches, 0 heading-only evidence after cleaning, and 7 sparse rows with no selector-visible fields. This supports the next fixed-candidate external retrieval experiment; it is not itself a retrieval result.
- Full SkillRouter I3C V2 extraction target: parse `all_I2.jsonl` into I3C V2, seeded from the cleaned top-20 pool. This is required before claiming full-library or full-tier I3C evaluation. Do not mix older DeepSeek I3M or older I3C slices into the full V2 representation.

## Model-Parsed / ChatGPT-Parsed I3 Gate

Use this gate before replacing heuristic I3H with model-parsed I3M or ChatGPT/Codex-parsed I3C in any headline result.

Pass requirements:

- The exact prompt/schema version is frozen as `I3_MODEL_EXTRACTION_V1` or a later named version in `thesis_notes/current/I3 Model Extraction Protocol.md`.
- Model settings are recorded: provider, model, base URL if applicable, temperature, JSON mode, max output tokens, input truncation rule, and retry/cache behavior.
- Every extracted item includes an exact evidence quote found in the source artifact.
- Multiple use conditions, inputs/preconditions, outputs, workflow steps, dependencies/resources, constraints/boundaries, and success criteria are preserved as numbered arrays within one skill-level I3 instance.
- A pilot parse has been completed before full parsing:
  - at least 20 local benchmark skills;
  - at least 20 imported public skills;
  - at least 20 SkillRouter-Eval-Core skills, including gold and hard-only distractor skills where possible.
- Pilot outputs pass JSON schema validation and evidence-span validation.
- At least 20 pilot outputs are manually inspected for over-inference, missing major fields, and excessive broad background extraction.
- Full I3M results are named separately from I3H results in reports.
- ChatGPT/Codex `I3C` results are named separately from DeepSeek/API `I3M` results in reports.
- `I3C` may be treated as the main practical extraction route only after it passes: 0 parse-failed rows, 0 missing skill ids, at least 95% exact evidence-match on extracted evidence strings, manual sample inspection with no severe systematic field misuse, successful re-extraction of the local controlled benchmark using the same worker prompt and merge normalizer, and QA warnings that record sparse/generic/missing-field cases without making them selector-visible.
- Future I3C runs must use `skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V2.md` or a later named prompt. V2 requires subagents to include only high/medium selector-usefulness field items and to record absent or weak fields in non-selector-visible `absent_fields`, `field_warnings`, and `qa_warnings`.
- For external SkillRouter-Eval-Core fixed-candidate experiments, use the cleaned I3C V2 file rather than the raw merge. The raw merge is retained for audit; the cleaned file removes heading-only evidence and records the removal in QA warnings.

Fail conditions:

- The model invents fields without direct evidence.
- Evidence quotes are frequently absent from the source artifact.
- The parser collapses multiple workflow steps into one vague summary.
- The parser turns broad background explanation into use conditions.
- The parser extracts every mentioned tool as a dependency without evidence that the skill uses or requires it.
- The parser fills fields with generic headings, checklist fragments, placeholders, examples, return literals, or non-required resources instead of recording QA warnings.
- Retrieval reports silently mix I3H and I3M.
- Retrieval reports silently mix I3M and I3C, or compare a partial I3C/I3M subset against full-library I1/I2 results as if the selector-visible skill universe were the same.

## Historical Validation Snapshot

Last refreshed on 2026-06-06 against the expanded 2433-skill library, including the new public-style controlled stratum, the expanded 120-case public-gold stratum, and a 333-prompt broad combined audit that also includes low-information stress prompts. This section is retained as development history and is superseded by the active frozen-v0.4 snapshot above.

- Step 1 integrity: PASS. 201 controlled prompts and 2433 skills resolve.
- Current composition: 169 controlled/evaluated skills including 10 implicit-field stress skills and 32 public-style controlled skills, 1800 generated background-scale skills, 460 public imported background skills, and 4 support email skills.
- Public imports: PASS. 460 public-source wrappers were created from OpenAI, Anthropic, `claude-office-skills`, Hugging Face, `akillness/oh-my-skills`, Addy Osmani skills, Matt Pocock skills, SWE-Skills-Bench, and other smaller public sources; 460/460 original `SKILL.md` files downloaded successfully.
- Step 2 procedural distinctness: PASS. 201/201 prompts pass; 646/646 gold/alternative pairs differ on primary procedural axes.
- Step 2 prompt-specific alignment: PASS WITH RECORDED RESIDUALS. On the 201-prompt public-style expansion, 199/201 prompts pass under the embedding requirement-alignment diagnostic, 657/659 gold/alternative pairs pass, strict gold is top-1 among listed candidates for 194/201 prompts, and gold-or-acceptable is top-1 for 199/201 prompts. The two residual cases are recorded as duplicate/boundary issues rather than forced prompt edits.
- Step 3 semantic confusability: PASS. The current embedding checkpoint has 182/201 prompts with at least two plausible listed alternatives, or 90.5%, above the 85% pass threshold. Remaining weak cases are retained as semantic residuals unless they dominate final selector failures.
- Step 4 prompt leakage: PASS. 0 critical exact-name leaks and 0 high-risk leaks.
- Step 5 scale regime: PASS. The 2433-skill condition remains a near-context-limit scale condition for compact metadata/progressive-disclosure style systems. R1 flat metadata should be recalculated after the public-style expansion before final context-cost claims.
- Step 6 public/real-world skill field audit: MOSTLY DONE. Current heuristic checkpoint audits 460/460 imported public `SKILL.md` files; DeepSeek model-assisted verification also covers 460/460 skills; a 10-skill subagent/manual calibration pilot and an 80-case disagreement packet exist.
- Step 6b public-skill gold validation: CLEANED / PASS WITH CAVEATS. A separate 120-prompt public-gold stratum now exists, giving 321 total evaluated prompts when combined with the 201 controlled prompts, or 333 prompts when low-information stress prompts are included. It passes Step 1 integrity, Step 2 procedural distinctness, Step 2 prompt-specific alignment, Step 3 semantic confusability, and Step 4 leakage thresholds after acceptable-alternative cleanup.
- Public-gold Step 1 integrity: PASS. 120 prompts and 2433 skills resolve; 0 missing references.
- Public-gold Step 2 procedural distinctness: PASS. 120/120 prompts pass; 459/459 gold/alternative pairs have at least one primary procedural differentiator; 417/459 pairs have two or more primary differentiators.
- Public-gold Step 2 prompt-specific alignment: PASS / residual hard cases. 115/120 prompts pass under the embedding requirement-alignment diagnostic; 510/517 pairs pass; strict gold is top-1 among listed candidates for 98/120 prompts and gold-or-acceptable is top-1 for 118/120 prompts.
- Public-gold Step 3 semantic confusability: PASS. 116/120 prompts have at least two plausible listed alternatives under the embedding diagnostic; 382/517 pairs are plausible semantic neighbours. Remaining weak cases are high-specificity public/provider tasks and should be retained as hard external-validity cases rather than overfit with weak distractors.
- Public-gold Step 4 leakage: PASS. 0 critical exact-name leaks and 0 high-risk leaks. Six provider/tool dependency cues are explicitly reclassified as low-risk dependency evidence rather than leakage.
- Public-gold label metadata: 80 stable strict public-gold cases, 37 stable cases with acceptable alternatives, and 3 hard public-label cases. Provider/tool cue status: 64 provider/tool-explicit and 56 provider-implicit or generic cases.
- Current residual validation note: `thesis_notes/checkpoints/benchmark_validation/Benchmark Residual Validation Reasons - 2026-06-06.md`.
- Combined broad audit: PASS on 333 prompts for integrity, procedural distinctness, semantic confusability, and leakage. Combined Step 2 requirement alignment is WARN at 298/333 prompts; the lower rate is expected because this audit includes low-information stress prompts.
- Step 4b manual cluster audit: FIRST PASS COMPLETE / USED FOR EXPANSION. Existing automated checks show the benchmark is usable, and the first manual audit now records controlled clusters and public-gold source families with intent, gold skill type, plausible alternatives, procedural differentiating axes, realism, ambiguity risk, and expansion priority. Audit artifact: `skill_benchmark/outputs/cluster_design_audit.md`. The 2026-06-06 public-style controlled expansion follows this audit; checkpoint: `thesis_notes/checkpoints/benchmark_validation/Public-Style Controlled Expansion Checkpoint - 2026-06-06.md`.
- Public-gold local selector check: HISTORICAL on the 82-prompt stratum. On that older `current_full` scale, strict top-1 ranged from 32.9% to 51.2%, accept top-1 from 47.6% to 67.1%, and top-5 from 64.6% to 86.6%. Superseded by the active frozen-v0.4 144-prompt public-gold matrix.
- Public-gold provider/SkillRouter check: HISTORICAL on the 82-prompt stratum. Best old public-gold result was Qwen R2 + Qwen rerank top-20 with 76.8% strict top-1, 90.2% accept top-1, 100.0% strict top-5, and 0.861 MRR. Superseded by the active frozen-v0.4 144-prompt public-gold matrix.
- Step 7 non-core semantic competition: PASS useful pressure, but the latest summarized non-core winner counts are from the older 85-prompt checkpoint. They are retained as diagnostic evidence and should be refreshed only if used as final headline counts.
- Step 7 all-non-core procedural competition: PASS with risks, but the latest summarized 14/85 procedural non-core-above-gold count is historical. These cases require manual adjudication before final claims.
- Step 7 local selector baselines: PASS useful pressure on the active benchmark. On the 2433-skill full library with 201 prompts, flat metadata ranges from 55.2% to 61.7% top-1, serialized schema/rerank methods reach 65.2-65.7% top-1, and M6-v1 local field-aware reranking reaches 72.1-72.6% top-1 at top-100 candidate budget.
- Step 7 Qwen provider update: HISTORICAL useful pressure for full-skill conditions on 2401/137. Qwen full-skill embedding reaches 52.5% top-1; Qwen full-skill plus local schema rerank reaches 77.4% at top-100. These provider results have not yet been rerun on the 201/2433 controlled benchmark.
- Implicit-field stress set: integrated into the main benchmark. Raw skills remain prose-only, while R2/R3 now use a conservative representation-layer extraction pass to recover procedural fields before retrieval.
- Historical 1006-skill results remain useful as a v1 comparison for Qwen R1/R2 variants.
- Low-information stress test: DONE separately, not merged into the main benchmark.
- Step 8 M0 progressive disclosure: previous core-only M0 trace remains the only completed M0 run. The full 2433-skill M0 condition is now mainly a context/cost stress test and has not been run.

Interpretation: the expanded benchmark is valid enough for local scale-sensitivity analysis. The main current risk is no longer lack of scale; it is gold-label stability under realistic public/generated competitors and whether extracted fields are used with sufficiently field-aware logic. Before final thesis claims, acceptable alternatives and revise/exclude decisions should be applied, and the current local schema reranker should be treated as a diagnostic method rather than the final structure-aware proposal.

## Methodology Hardening Gate

Added on 2026-06-05 after a detailed methods critique. These checks must pass before the final thesis treats a result as headline evidence.

1. Candidate-budget fairness:
   - Compare rerankers at the same candidate budget.
   - A top-100 M6-v1 result may be reported as a larger-budget result, but not as a direct win over a top-20 SkillRouter reranker unless SkillRouter is also run at top-100.

2. Strict versus acceptable labels:
   - Report strict gold metrics as the primary benchmark result.
   - Report gold-or-acceptable metrics separately.
   - Do not write "top-1 accuracy" as if strict and acceptable labels are the same scoring rule.

3. Statistical uncertainty:
   - Final tables should include confidence intervals or prompt-count differences.
   - Use paired tests for selected method comparisons: McNemar for top-1 and bootstrap/randomization for MRR or top-k.

4. Field-value versus length bias:
   - Cumulative field ablations must be interpreted cautiously because token counts grow with each added field.
   - Add at least one length-control check before claiming that a field identity, rather than extra text volume, caused a gain.

5. Field extraction validity:
   - Public-skill field claims require evidence spans, model-assisted extraction, or manual/sample calibration.
   - If public-gold remains weak, separate extraction failure from reranker failure instead of treating both as one retrieval failure.

6. M6-v1-local naming:
   - The current implemented M6-v1 is a local lexical field-aware prototype.
   - It uses request-side cue extraction and field-to-field lexical/token overlap. It is not yet a robust semantic field matcher.

7. Public-gold false-positive labels:
   - Do not use `non-main top-1` uncritically for public-gold, because public gold skills are often public/background skills.
   - Use stratum-aware categories such as wrong controlled skill, wrong public wrapper, broad parent/router, duplicate/acceptable, extraction failure, and candidate-recall failure.

8. Post-hoc field-set selection:
   - If the best field set is selected after trying many variants, label the result exploratory.
   - For a final claim, either freeze the field set before test reporting or use train/dev/test selection.

9. Supervisor-feedback experimental-detail gate:
   - The final methodology must specify gold-label construction, prompt strata, model settings, candidate budgets, scoring rules, and statistical comparisons.
   - Literature-review claims must include concrete empirical details from key papers, not only conceptual summaries.
   - Final tables must make clear whether a result is controlled-authored, public-gold, low-information, or downstream.
   - The corresponding response plan is `thesis_notes/assignments/Supervisor Feedback Response Plan - A3 to Current Thesis.md`.

## Benchmark Validation Rubric

### 1. Skill And Prompt Integrity

Checks:

- every prompt has a unique `id`
- every `gold_skill` exists as a `SKILL.md`
- every `closest_alternatives` entry exists
- every skill has frontmatter `name` and `description`
- public imports are separated from the controlled core

Pass:

- 100% prompt references resolve
- no duplicate prompt IDs
- no malformed skill frontmatter in evaluated families

Fail:

- missing gold skill
- duplicate prompt ID
- malformed metadata in a main evaluated skill

### 2. Procedural Requirement Alignment

This step has two layers. The first layer is a field audit: do the gold skill and alternatives expose different procedural fields? The second and stricter layer is prompt-specific requirement alignment: what concrete requirement in the prompt makes the gold skill correct and each alternative wrong?

For each gold/alternative pair, annotate which requirement axis differs:

- input type or input state
- output artifact
- workflow steps
- preconditions
- required tools or external dependencies
- optional resources
- success criterion
- side effects

Pass:

- every gold prompt has at least one concrete requirement that explains the gold label
- each listed alternative can be rejected because it misses a prompt requirement, produces the wrong artifact, follows the wrong workflow, assumes the wrong precondition, lacks a required dependency/resource, or optimizes for the wrong success criterion
- most high-value cases differ on two or more axes
- the differentiator is visible in a structured representation and does not depend only on `not_for` negation

Fail:

- gold and alternative are effectively interchangeable
- distinction depends only on wording preference
- gold label cannot be explained procedurally
- workflow fields are merely paraphrases and no prompt-specific requirement separates the skills

### 3. Semantic Confusability

Checks:

- compare prompt text with gold and alternative skill descriptions
- compare gold skill description with closest alternatives
- inspect lexical overlap, shared trigger words, TF-IDF/cosine similarity, and embedding similarity when an embedding backend is available

Pass:

- each main prompt has at least two plausible neighboring skills
- gold and closest alternatives share meaningful task vocabulary
- failures are plausible confusions, not random unrelated selections

Fail:

- gold skill is uniquely obvious from exact wording
- alternatives are semantically unrelated
- background distractors never appear in top-k under cheap selectors

### 4. Gold Label Stability

Checks:

- manual review of prompt and candidate skills
- optional independent annotation by another person or model
- agreement on gold skill and acceptable alternatives

Pass:

- annotators agree on gold for most prompts
- ambiguous prompts are rewritten or removed
- acceptable-but-not-ideal alternatives are documented

Fail:

- multiple skills are equally correct
- prompt requires hidden assumptions
- gold label changes depending on stylistic preference

### 4a. Prompt Leakage

Checks:

- exact gold skill ID or skill name appears in the prompt
- prompt uses distinctive gold title words much more than alternative title words
- prompt copies long phrases from the gold skill card
- selectors could win through label matching rather than procedural fit

Provider/tool-name rule:

- Provider and tool names are not automatically leakage. If a public skill is genuinely tailored to Hugging Face, Figma, Shopify, Netlify, GitHub, Playwright, or another provider/tool, naming that dependency can be part of the correct input requirement.
- A provider/tool cue becomes a leakage problem only when it is effectively the whole gold-label rationale and the prompt does not also justify the skill through input state, output artifact, workflow, side effect, resource, or success criterion.
- Record provider-explicit and provider-implicit prompts separately. Do not strip all provider names from provider-specific skills; instead, test whether the method can use provider cues together with procedural evidence.

Pass:

- zero exact gold skill-name leaks
- zero or very few high-risk title/phrase leaks
- any remaining medium-risk wording is documented and judged to be natural task vocabulary
- provider/tool names, when present, are justified as dependencies and not as copied skill-title leakage
- Step 2 procedural alignment remains passing after leakage reduction

Fail:

- prompt directly names the gold skill
- prompt contains copied gold-card phrasing that makes the answer obvious
- prompt uses only a provider/source cue while the gold and alternatives are not procedurally distinguishable
- removing leaked wording makes the gold label procedurally unstable

### 4b. Manual Cluster Design Audit

Purpose:

Check whether each cluster is a defensible semantic-confusion unit before adding more prompts or using it for headline claims. This step is deliberately manual because automated distinctness and similarity scores can miss the most important benchmark question: is the gold skill obviously better after careful procedural reading, while the alternatives remain plausibly tempting from compressed representations?

Run this step:

- before expanding controlled clusters;
- before adding public skills as gold-label targets;
- after major scale expansion if background/public skills start beating gold labels;
- before selecting representative examples for the thesis chapter.

Required cluster audit table:

| Field | What to record |
|---|---|
| `cluster_id` | Stable cluster or source-family name. |
| `cluster_intent` | The user workflow or intent family this cluster represents. |
| `gold_skill_type` | The intended atomic capability represented by the gold skill or gold group. |
| `skills_in_cluster` | Gold skills and listed near-neighbour alternatives. |
| `typical_prompt_pattern` | What kind of request should activate this cluster. |
| `main_confusion_source` | Why compressed text makes the alternatives look plausible. |
| `procedural_axes` | Which fields separate gold from alternatives: input state, precondition, workflow, output artifact, constraint, dependency, resource, success criterion, side effect, or avoid-condition. |
| `gold_rationale` | One to two sentences explaining why the gold skill is procedurally best. |
| `alternative_rejection_rationale` | Short reason each major distractor is plausible but wrong. |
| `realism_evidence` | Whether the cluster is grounded in public skills, observed agent workflows, assignment/literature examples, or generated stress cases. |
| `ambiguity_risk` | Low, medium, or high. Medium/high cases need acceptable alternatives, prompt rewrite, or exclusion from strict scoring. |
| `scale_risk` | Whether public/background skills may be genuinely better than the designed gold. |
| `expansion_decision` | Expand, revise first, keep but do not expand, or exclude from headline claims. |

Checks:

- Read the gold skill and its closest alternatives, not only the generated information-layer cards.
- Confirm the cluster is not just paraphrased versions of the same procedure.
- Confirm the prompt family requires a concrete operational distinction.
- Identify the minimal field or fields that a selector must preserve to choose correctly.
- Inspect whether public/background skills create a more appropriate gold label than the designed skill.
- Mark acceptable alternatives where human disagreement would be reasonable.
- Separate broad router/hierarchical skills from atomic skills unless the prompt explicitly asks for routing.
- Check whether the cluster tests the thesis claim or merely adds domain variety.

Pass:

- every audited cluster has a clear user-intent family;
- every headline cluster has at least one stable gold skill type and at least two plausible near-neighbour alternatives;
- the gold-vs-alternative distinction is procedural, not merely wording preference;
- at least one primary differentiating axis is visible or extractable in the proposed representation fields;
- ambiguity risk is low for strict-scored cases, or acceptable alternatives are explicitly recorded;
- no background/public skill is judged clearly better than the intended gold without being recorded as acceptable or revising the prompt.

Warning:

- cluster is realistic but broad, with several valid workflows;
- cluster relies heavily on negated `do not use when...` text rather than positive procedural fit;
- cluster has good procedural differences but weak semantic confusability;
- cluster is mostly generated and lacks public/literature grounding;
- gold skill is correct only because the prompt was over-specified.

Fail:

- alternatives are not genuinely plausible;
- gold and alternatives are effectively interchangeable;
- a human reader cannot explain why the gold skill is better without using hidden assumptions;
- a public/background candidate is clearly more suitable than the gold label;
- the cluster mainly tests exact keyword matching or exact skill-name matching;
- adding more prompts would multiply the same easy distinction rather than improve benchmark coverage.

Pass threshold before expansion:

- 100% of clusters selected for expansion must have a filled audit row.
- At least 80% of expanded clusters should be `low` ambiguity risk.
- Any `medium` ambiguity cluster must include acceptable alternatives or a prompt rewrite plan.
- Any `high` ambiguity cluster must not be used for strict headline scoring until revised.
- Each expanded cluster should identify at least two candidate prompt variants and at least two plausible distractors.

Expected evidence artifacts:

- cluster audit table, preferably `skill_benchmark/outputs/cluster_design_audit.md`;
- representative gold-label examples for thesis writing, linked to `thesis_notes/current/Gold Label Evidence Map.md`;
- list of clusters to expand, revise, freeze, or exclude;
- updated prompt files only after the audit decision is made.

### 5. Difficulty Calibration

Checks:

- run progressive-disclosure baseline on core library
- run cheap selectors on flat metadata
- inspect per-cluster confusion

Pass:

- not all methods score near-perfect
- not all methods fail randomly
- at least some clusters produce repeatable near-neighbor confusions

Warning:

- top-1 accuracy above 90% for all methods may mean the benchmark is too easy
- top-1 accuracy below 30% for humans or strong main-agent selection may mean the benchmark is ambiguous

### 6. Public/Real-World Skill Field Audit

Purpose:

Check whether the proposed representation fields are grounded in real skill artifacts rather than only in our generated controlled benchmark.

This step separates three claims:

- `observed field`: public skills already expose this information explicitly
- `extractable field`: public skills contain this information implicitly, but the information layer must parse, extract, or normalize it
- `proposed field`: public skills often lack this information, but the thesis argues it should be preserved for reliable retrieval

Checks:

- audit imported public skills for explicit headings and implicit evidence
- count fields such as routing trigger, inputs/preconditions, outputs, workflow/procedure, constraints/not-for, dependencies/tools, scripts/resources/references, examples, and tests
- run a model-assisted semantic extraction pass on a subset or the full public-skill sample, using a strict JSON schema with evidence spans
- compare heuristic and model labels to identify likely false positives and false negatives
- manually sample a small subset to check whether automated field tags are reasonable
- prioritize manual review of heuristic/model disagreement cases
- compare public-skill field prevalence with the controlled benchmark schema
- document public skills that are broad, hierarchical, underspecified, or difficult to atomize

Pass:

- the audit covers at least the current 460 imported public skills or a clearly defined public subset
- model-assisted extraction has been run on at least a checkpoint sample, or the thesis explicitly states why only deterministic extraction is used
- model outputs include quoted evidence spans or mark the field as missing
- heuristic/model disagreements are summarized by field
- each proposed representation field is classified as observed, extractable, or proposed
- the thesis can explain whether the field is an empirical artifact pattern or a retrieval-oriented normalization design
- public skills provide enough evidence that the schema is not only tailored to our generated skills

Fail:

- proposed fields appear only in our generated skills and not in public artifacts
- the model verifier asserts fields without evidence spans
- heuristic/model disagreement is high and no manual calibration is performed
- public skills are so broad or messy that field extraction cannot be meaningfully evaluated
- the thesis cannot explain whether structured fields are authoring requirements or representation-layer extraction targets

### 6b. Public-Skill Gold Validation

Purpose:

Turn a selected subset of externally authored public skills into evaluated gold-label benchmark cases. This is separate from Step 6. Step 6 asks whether public skills contain or imply our proposed fields. Step 6b asks whether public skills can serve as stable retrieval targets under the same semantic-confusability rubric as the controlled benchmark.

Why this matters:

- It tests whether the benchmark is overfitted to our authored skills.
- It checks whether the information layer and retrieval strategy can retrieve skills written by other authors, not only clean synthetic skills.
- It creates a harder realism layer where useful procedural information may be implicit in prose, examples, dependencies, or linked resources rather than clean headings.

Scope:

- Start with 30-50 public-gold prompts.
- Cover at least 6 public-skill clusters or source families.
- Prefer public skills that are atomic enough to test as one procedure.
- Keep broad, hierarchical, or router-like public skills as background unless they can be atomized into a single evaluated procedure.

Public-gold prompt record:

Each public-gold item must record:

- `gold_skill`: an imported public skill, not a generated controlled skill
- `user_request`: natural request text that does not name the exact skill or repository; provider/tool names are allowed when they are real task dependencies
- `closest_alternatives`: 2-4 semantically plausible competitors from public, controlled, or background skills
- `gold_rationale`: the concrete procedural reason the public skill is best
- `rejection_rationale`: why each alternative is plausible but not best
- `field_axes`: which fields make the distinction, such as input/precondition, output artifact, workflow/procedure, dependency/tool, resource/reference, boundary/side effect, or success criterion
- `acceptable_alternatives`: any near-equivalent skills that should count as acceptable rather than false positives
- `atomization_status`: atomic, atomized-from-broad-skill, or rejected-as-too-broad

Validation sequence:

1. Select candidate public skills from the imported corpus.
2. Screen each skill for atomization: reject broad/hierarchical skills unless the tested behavior is a single stable procedure.
3. Extract fields using the current information-layer extraction pipeline, then optionally verify with model-assisted extraction and evidence spans.
4. Write prompts that require the public skill's procedure without naming the exact skill. Keep provider/tool names when they are genuine dependencies, and record whether the case is provider-explicit or provider-implicit.
5. Choose semantic neighbours as alternatives.
6. Manually adjudicate whether the public skill is clearly best after careful reading.
7. Run Steps 1-4 on the public-gold subset separately.
8. Run selector evaluations on controlled-only, public-gold-only, and combined prompt strata.
9. Classify public-gold failures as candidate-recall failure, extraction failure, reranking failure, gold-label ambiguity, broad-skill/hierarchy issue, or acceptable-alternative issue.

Pass:

- at least 30 public-gold prompts exist for the initial validation, with a target of 50 if stable
- at least 6 clusters or source families are represented
- 100% prompt references resolve
- at least 85% of public-gold prompts have stable manual gold labels, with ambiguous cases removed or marked with acceptable alternatives
- at least 80% pass prompt-specific procedural alignment
- at least 70-80% pass semantic-confusability checks under a modern embedding model, or failures are documented as high-precision cases
- 0 critical or high-risk prompt leaks
- public-gold selector results show non-trivial method spread rather than all methods succeeding or all methods failing randomly
- structure-aware or extraction-aware methods improve top-1/top-k/MRR, reduce non-core/public false positives, or produce an interpretable failure-mode advantage over flat/dense baselines

Fail:

- the public skill is too broad, hierarchical, or conditional to be a stable atomic gold label
- the prompt tests a subskill that is only weakly present in the public artifact
- the public skill lacks enough procedural signal for any defensible extraction or manual rationale
- the prompt leaks the exact skill name, repository slug, distinctive copied wording, or copied text
- multiple alternatives are equally correct and no acceptable-alternative label is recorded
- results mostly reflect provider/source/name matching without input, output, workflow, dependency, or success-criterion support

Reporting rule:

Report public-gold results as a separate stratum:

- controlled-authored benchmark: clean and implicit designed confusions
- public-gold benchmark: externally authored skill-artifact validity
- combined benchmark: final scale and distractor pressure

Do not merge public-gold failures into the main score without explaining whether the failure came from retrieval behavior, field extraction, or instability in the public skill artifact itself.

Detailed planning note: `thesis_notes/benchmark/public_skills/Public Skill Gold Validation Plan.md`.

### 7. Offline Selectors, Information-Layer Ablations, And Scale Sensitivity

Checks:

- evaluate on at least two library sizes:
  - core only
  - core plus background/public skills
- compare accuracy, top-k recall, MRR, context cost, and background false positives
- inspect non-core skills that outrank gold skills to decide whether they are true procedural alternatives or only semantic distractors
- run information-layer and field ablations to test which information improves selection:
  - description only
  - description + use conditions
  - + input/precondition fields
  - + output artifact fields
  - + workflow/procedure fields
  - + constraints/not-for fields
  - + dependencies/resources
- distinguish information layers from algorithms:
  - I1 flat cards / R1
  - I2 full skill artifacts / RFULL
  - I3 extracted selection fields / R2-R3
  - I4 relation information / graph edges
  - I5 hierarchy or grouping / tree-DAG index
- distinguish first-stage retrieval from reranking:
  - embedding or lexical candidate generation
  - generic neural reranking
  - procedural field-aware reranking
  - graph expansion or diffusion
  - tree/DAG routing

Pass:

- larger library increases context cost or retrieval difficulty
- at least some background/public skills appear as plausible false positives
- information-aware methods degrade less than weaker information layers
- non-core winners are mostly procedurally wrong or documented as acceptable-but-not-gold borderline cases
- field ablation shows which information contributes to retrieval, or honestly shows that some fields add little
- field-aware reranking reports candidate recall separately from final top-1, so failures can be attributed to first-stage retrieval or reranking
- structure-aware methods show either accuracy gains, top-k recall gains, non-core false-positive reduction, cost/context reduction, or clearer failure-mode attribution
- if I4 graph is evaluated, the edge schema and edge-construction method are frozen before reporting results
- if I5 tree/DAG is evaluated, branch recall and early branch-exclusion failures are reported

Fail:

- adding background skills changes nothing
- background skills are all unrelated noise
- scale condition cannot be distinguished from core condition
- many background skills are equally or more procedurally correct than the gold labels without being documented as acceptable alternatives
- structured reranking wins only because our controlled skills expose hand-authored fields that public skills lack, with no audit or extraction argument
- extracted fields are only appended as extra text and the thesis then overclaims that the method used structured information

#### 7a. I4 Relation-Aware Graph Gate

Purpose:

Test whether explicit skill relations improve candidate subsetting beyond serialized skill text.

Allowed edge types:

- `similar_to`: skills that solve neighbouring tasks and are likely semantic confusions.
- `belong_to`: skill belongs to a domain, task family, platform, or capability group.
- `depend_on`: one skill requires another skill, tool, resource, or setup step.
- `compose_with`: skills are commonly used together in a workflow.
- `alternative_to`: skills are mutually plausible but differ in boundary, input, output, or workflow.
- `prerequisite_or_workflow`: one skill should precede another in a multi-step process.

Pass:

- edge types are defined before retrieval runs;
- graph construction is sparse and evidence-based, not dense all-pairs speculation;
- graph retrieval is compared against a text baseline that serializes the same relation information where feasible;
- graph results report candidate recall, top-1/top-5/MRR, and whether recovered candidates were semantically distant but functionally necessary;
- failures are classified as bad seed, missing edge, wrong edge, graph over-expansion, or reranker ordering error.

Fail:

- graph edges are generated without evidence or validation;
- graph wins only because it has extra information not available to the stated baseline;
- graph returns broad bundles that improve recall but make final selection harder without reporting the cost;
- relation information is actually just a category label and should have been treated as I5 hierarchy instead.

#### 7b. I5 Hierarchy / Tree-DAG Gate

Purpose:

Test whether hierarchical grouping helps scalability and whether simple grouping is sufficient for confusable skill selection.

Required hierarchy levels:

- domain or source family;
- subdomain or task family;
- atomic skill.

Pass:

- route decisions are recorded at each level;
- branch recall is reported for top-1, top-3, and top-5 branches;
- strict tree and DAG/multi-label grouping are separated if both are tested;
- early branch-exclusion failures are reported separately from final skill-ranking failures;
- the method reports the candidate-count reduction achieved by routing.

Fail:

- hierarchy is used only as a hidden filter and not reported;
- a single strict tree forces multi-domain skills into arbitrary branches;
- branch summaries leak exact gold skill names;
- the result is interpreted as evidence for procedural fields when it actually tests only category routing.

### 8. M0 Progressive Disclosure Baseline

Checks:

- expose all skill names/descriptions/compact metadata to the main agent
- record selected skills and full `SKILL.md` documents loaded
- record selector-visible token cost and final context cost
- compare core-only runs with the largest feasible library stress test

Pass:

- current prompt and skill versions are used
- every trace records selected skill, gold skill, loaded docs, and failure mode
- core runs are feasible and comparable with offline selector metrics
- token/context cost is recorded, approximated, or explicitly marked unavailable
- large-library runs either complete or are documented as context/cost infeasible

Fail:

- traces are stale relative to current prompts or skills
- selected skill cannot be recovered from logs
- M0 is reported as cost evidence without token/context cost

### 9. Downstream Candidate-Subset Validation

Checks:

- take a smaller sample of prompts after offline retrieval behavior is understood
- pass retrieved candidates to the main agent under a fixed prompt policy
- load only the selected full skill artifacts
- evaluate the final task artifact, not only the selected skill ID

Pass:

- retrieval success is separated from downstream artifact success
- task artifact is checked for required fields, workflow, dependency/resource use, and unsupported invention
- downstream failures can be traced back to retrieval, skill execution, or task ambiguity
- at least 12 representative prompts are used, including both easy-success and known-confusion cases
- each compared selector uses the same candidate budget, preferably top-5 for first validation
- gold-or-acceptable candidate recall is at least 85% for methods being taken into downstream execution, otherwise the downstream failure is labelled as retrieval failure
- artifact success is at least 80% for oracle-gold runs; if oracle-gold fails below this, the task prompt or skill itself is not stable enough for downstream evaluation

Fail:

- a good-looking final answer hides wrong-skill selection
- the main agent sees extra skill information that the method was not supposed to expose
- downstream task success is judged without checking whether the selected skill was procedurally appropriate

## Method Families

These are broad experimental families, not single algorithms. A method is a combination of candidate representation, first-stage selector, optional reranker, candidate budget, and final main-agent skill-loading policy.

The thesis should report methods in this form. Embedding retrieval is one scalable selector family, not the baseline. The baseline is normal progressive disclosure.

Current method decision:

- Keep the existing local schema reranker as `M6-v0`, a transparent diagnostic weighted-overlap method over extracted skill fields.
- Do not treat `M6-v0` as the final proposed structure-aware method.
- Build the next main method as `M6-v1`, a field-aware procedural reranker that parses the user request into requirements, compares those requirements with extracted skill fields, and handles dependencies, boundaries, and broad parent/router skills explicitly.
- Report Qwen reranking as a strong generic reranker baseline, not as evidence that the proposed procedural fields were used.

Updated method decision, 2026-06-18:

- Treat the implemented `M6-v1-local` as a lexical field-aware prototype, not as the final semantic field-aware method.
- Build `M6-v2` as the main no-rewrite semantic field-aware reranker. It should embed the raw user request and compare it against existing selector-visible skill fields using semantic similarity.
- Do not let `M6-v2` invent hidden workflow steps, optionality labels, or unstated user requirements. Explicit cue detection is allowed only for field activation and mismatch penalties.
- Any LLM query parser, query rewrite, or request-to-schema expansion must be labelled as a separate query-understanding ablation, because otherwise the experiment confounds representation usefulness with query interpretation.
- Multi-item fields such as workflow/procedure should be chunked at reranking time and scored by max or top-k average similarity rather than by summing all pairwise matches. This prevents longer procedural fields from winning simply because they contain more text.
- Boundary, negative-use-case, dependency, and side-effect mismatches should be penalties or clearly reported ablation components, not blindly concatenated as positive retrieval text.

## Embedding Model Policy

Use embedding models at two different levels.

### Construction / Validation Model

`sentence-transformers/all-MiniLM-L6-v2` is the current local validation model.

Purpose:

- cheap benchmark construction signal
- semantic-confusability sanity check
- prompt/skill similarity audit
- repeatable local validation on an 8 GB laptop

Do not treat MiniLM as the strongest embedding baseline. It is a benchmark-building instrument, not the main evidence against modern retrieval systems.

### Experimental Embedding Baselines

The final retrieval comparison should include stronger embedding/reranking systems where feasible.

Priority candidates:

- Qwen3 embedding model over description cards
- Qwen3 embedding model over full `SKILL.md` artifacts
- Qwen3 reranker over embedding shortlists
- SkillRouter-style embedding model, if the public fine-tuned model is accessible
- SkillRouter-style reranker, if the public fine-tuned model is accessible

Rationale:

- modern embedding models may already encode more procedural information than older sentence encoders
- full-skill embedding may reduce the weakness of description-only retrieval
- reranking is common in realistic retrieval pipelines and should not be ignored
- the thesis claim is stronger if schema/tree/graph-aware methods are compared against modern embedding and reranking baselines, not only against MiniLM

If stronger embedding/reranker baselines perform near-perfectly, revisit the benchmark before making a contribution claim. That may mean the current prompts leak too much information, the clusters are too easy, or the structured information layer has been given an unfair information advantage.

### M0: Progressive Disclosure Baseline

Selector-visible representation:

- all skill names and descriptions, possibly basic metadata, in the main agent context
- full `SKILL.md` loaded only after the main agent selects a skill

Purpose:

- realistic small/medium-library baseline
- shows context cost and scalability limit

Pass:

- can run on the core library
- reports selector-visible token/context cost
- produces selected-skill traces
- makes clear when the large-library version is infeasible or only a stress test

### M1: Flat Metadata Candidate Selection

Selector-visible representation:

- name
- description
- optional family/category only when explicitly testing category labels

Selectors may include:

- lexical/BM25
- LLM router over compact metadata

Purpose:

- scalable compressed baseline using the same broad information exposed by progressive disclosure
- tests what happens when candidate subsetting is separated from the main agent but procedural details remain hidden

Pass:

- exports one record per skill
- does not expose full skill bodies, workflow, resources, or schema fields
- reports top-k recall and top-1 accuracy over the same skill library as other scalable methods

### M2: Embedding-Based Skill Retrieval

Embedding retrieval is a method family with variants.

Variants:

- `M2a description-card embedding`: embed only name plus description, optionally family.
- `M2b full-skill embedding`: embed the complete `SKILL.md` text.
- `M2c chunked full-skill embedding`: embed sections/chunks of full skill artifacts, then aggregate or rerank candidate skills.
- `M2d schema-card embedding`: embed structured cards after M3 fields exist.
- `M2e skill-router embedding`: use a skill-routing-tuned embedding model if an accessible public model is available.

Reranking options:

- no reranker
- cross-encoder reranker
- LLM listwise reranker
- Qwen3 reranker
- SkillRouter-style reranker if accessible
- procedural/schema reranker after embedding shortlist

Model tiers:

- MiniLM: construction validator and weak local reference point only
- Qwen3-class embedding: main modern open embedding baseline
- SkillRouter-style embedding: prior-work-aligned skill retrieval baseline if accessible
- API-hosted embedding/reranker: acceptable for stronger comparison if local 8 GB memory is insufficient

Purpose:

- tests dense semantic retrieval under near-neighbor skill descriptions
- tests the claim from skill-routing literature that description-only embeddings can miss procedural distinctions
- tests whether structured information layers still help against modern full-skill embeddings and rerankers

Pass:

- reports first-stage top-k recall separately from reranked top-1 accuracy
- compares description-card and full-skill variants
- includes at least one modern stronger embedding baseline beyond MiniLM where feasible
- separates embedding model effects from representation effects
- reports context/storage cost of full-skill or chunked embeddings

### M3: Schema-Enriched Skill Cards

Selector-visible representation:

- name
- description
- input type or input state
- output artifact
- preconditions
- workflow summary
- success criterion
- avoid / not-for boundaries
- optional dependency/resource fields as an ablation

Selectors may include:

- lexical or embedding over serialized fields
- field-weighted scoring
- LLM router over structured cards
- reranker that compares prompt requirements against procedural fields

Purpose:

- tests whether preserving procedural information reduces semantic confusion
- tests a proposed representation format rather than relying only on existing flat descriptions

Pass:

- each main evaluated skill has extractable procedural fields
- fields explain the gold/alternative distinction
- context cost is measured separately from accuracy
- dependency/resource fields are evaluated as ablations, not as an unfair advantage for tool-heavy skills

### M4: Tree / Hierarchical Routing

Selector-visible representation:

- family/category tree
- optional subcategory nodes
- skill leaves
- category summaries

Selectors may include:

- LLM route-to-family then route-to-skill
- lexical or embedding selection at each tree level
- top-n branch routing to reduce early-decision brittleness

Purpose:

- tests an efficient and interpretable scale strategy
- exposes a known weakness: early branch errors can exclude the correct skill

Pass:

- reports branch accuracy separately from final skill accuracy
- reports cases where the gold skill was excluded by an early routing decision
- compares single-branch routing against multi-branch routing

### M5: Graph-Based Skill Retrieval

Selector-visible representation:

- nodes:
  - skill
  - family
  - input type
  - output artifact
  - workflow step
  - tool/dependency
  - resource
  - success criterion
  - avoid condition
- edges:
  - `belongs_to_family`
  - `expects_input`
  - `produces_output`
  - `requires_tool`
  - `uses_resource`
  - `has_precondition`
  - `has_workflow_step`
  - `optimized_for`
  - `avoid_when`
  - `confusable_with`
  - `derived_from_public_skill`

Selectors may include:

- graph filtering by matched input/output/tool nodes
- graph expansion from prompt-derived requirements
- graph-aware reranking over candidate skills
- hybrid retrieval: flat or embedding shortlist followed by graph-based reranking

Purpose:

- tests whether explicit relational structure improves selection beyond serialized text

Pass:

- edges are meaningful and not arbitrary
- graph fields can be ablated
- graph representation improves at least one of top-1, MRR, background false-positive rate, or branch-exclusion recovery without unreasonable context cost

Detailed M4/M5 methodology is recorded in `thesis_notes/methodology/M4 M5 Structure-Aware Architecture Plan.md`.

### M6: Hybrid Retrieval And Reranking

Hybrid methods combine a cheap first-stage selector with a richer precision layer.

Examples:

- flat metadata/BM25 shortlist, schema reranker
- description embedding shortlist, full-skill reranker
- full-skill embedding shortlist, schema reranker
- tree route to branches, graph reranker inside branches
- graph filter, LLM listwise reranker

Purpose:

- tests realistic retrieval architecture where a fast candidate generator is followed by a more expensive reranker

Pass:

- reports candidate recall before reranking
- reports reranker rescue rate
- reports cost/latency added by reranking
- improves rank placement without hiding full-library context in the final agent prompt

### M7/M8: Provider Neural Retrieval And Reranking

M7 uses a modern API embedding model as the candidate-subsetting layer. M8 adds a neural reranker over the top-k candidate set.

Implemented examples:

- Qwen `text-embedding-v4` over full `SKILL.md` files
- Qwen `text-embedding-v4` over I1/R1 and I3/R2 cards
- Qwen `text-embedding-v4` first stage plus `qwen3-rerank` over top-20 candidates
- OpenAI `text-embedding-3-small` or `text-embedding-3-large` as embedding-only baselines

Implemented SkillRouter-specific baseline:

- `pipizhao/SkillRouter-Embedding-0.6B` over full `SKILL.md` files as a domain-specific first-stage skill retriever
- `pipizhao/SkillRouter-Reranker-0.6B` over the top-20 or top-50 candidates as a domain-specific neural skill reranker
- same prompt sets, same library scale, same gold labels, and same candidate budgets as Qwen-backed M7/M8 where possible
- local smoke test first; Hugging Face Jobs hosted execution if local execution is too slow or memory-limited

Purpose:

- tests whether the benchmark remains difficult under stronger modern neural retrieval models
- separates information-layer questions from weak-local-model artifacts
- gives a realistic comparison against current retrieve-then-rerank systems such as SkillRouter-style pipelines

Pass:

- reports provider, model, representation, candidate budget, cache state, and approximate input tokens
- runs a smoke test on a small prompt subset before full-library evaluation
- compares M7/M8 against local M1-M6 on the same prompt set and library scale
- treats API cost, latency, and provider model choice as implementation details, not as the thesis contribution
- if SkillRouter is used, reports whether it is local Transformers, Hugging Face Inference Endpoint, or another hosted GPU endpoint; do not mix these results with API-only Qwen results without noting hardware and latency differences

## Information-Layer Implementation Artifacts

The current implementation exports artifacts that instantiate information layers. These artifacts are not final methods by themselves.

### Exported Components

- `R1_flat_metadata.jsonl`: name, family, description. Used by M1 and M2a.
- `R2_structured_procedural.jsonl`: parsed use cases, avoid conditions, preconditions, workflows, outputs, and writing rules. Used by M3 and M6.
- `R3_dependency_resource_aware.jsonl`: R2 plus dependency profiles, external dependencies, resource signals, public-source metadata, and resource files. Used as an M3/M5 ablation.
- `R4_graph_edges.jsonl`: graph edge view derived from R2/R3 fields. Used by M5.

What can change:

- embedding model
- description-only versus full-document embedding
- chunking strategy
- schema field weights
- graph edge types and traversal strategy
- reranker type and candidate budget
- whether family/category labels are exposed
- API provider and model, when testing M7/M8

What should not change during a controlled comparison:

- prompt text
- gold labels
- skill library for the scale condition
- whether full skill artifacts are visible before candidate selection, unless that is the method being tested
- final main-agent downstream prompt policy for post-selection runs

## Reranker Families

Reranking should be included because real retrieval systems rarely stop at first-stage retrieval.

Possible variants:

- no reranker
- cross-encoder reranker
- LLM listwise reranker
- pairwise tournament reranker
- structured procedural reranker
- dependency/resource-aware reranker
- graph-aware reranker

When reporting results, separate:

- first-stage recall: did the gold skill enter the candidate set?
- reranking quality: did the reranker move the gold skill toward rank 1?

## Evaluation Metrics

### Retrieval Metrics

- top-1 accuracy
- top-k recall, especially top-3 and top-5
- mean reciprocal rank
- NDCG if alternatives are graded as partially relevant
- confusion matrix by cluster
- background false-positive rate
- public-import false-positive rate

### Efficiency Metrics

- selector-visible token count
- main-agent context tokens after candidate selection
- number of full skill docs loaded
- latency
- approximate cost

### Benchmark Pressure Metrics

- semantic similarity between gold and alternatives
- procedural divergence score
- ambiguity rate
- prompt leakage score
- scale degradation from core to large library
- reranker rescue rate

### Downstream Metrics

Run downstream checks on a smaller sample after retrieval behavior is understood.

- correct artifact type
- required fields included
- unsupported fields not invented
- workflow followed
- dependency/resource used when required
- human judgment of task success

## Expected Results

The benchmark is doing its job if:

- progressive disclosure works reasonably on the core but becomes costly or unstable at larger scale
- flat metadata scalable selectors confuse semantically similar skills
- description-card embeddings underperform full-skill or schema-card variants on procedural near-neighbors
- stronger Qwen3/SkillRouter-style embedding baselines improve over MiniLM but still leave some procedural near-neighbor errors
- first-stage retrieval often has higher top-k recall than top-1 accuracy
- rerankers improve rank placement when the gold skill is in the candidate set
- schema-enriched cards reduce near-neighbor confusions
- dependency/resource fields help only when tool, file, public-source, or external-service requirements matter
- tree routing is efficient but shows branch-exclusion errors
- graph-based methods help only when edges capture real procedural distinctions

The benchmark is weak if:

- every method performs near-perfectly
- every method fails randomly
- background skills never compete with gold skills
- public imported skills add only noise and no dependency/resource pressure
- structured fields do not explain or improve any difficult cases
- annotators cannot agree on gold labels
- modern full-skill embedding plus reranking solves almost every prompt without needing procedural structure

## Immediate Refinement Steps

1. Integrate `frozen_v0_4_information_layer_matrix.md` into the thesis results chapter using information-layer-first grouping.
2. Add candidate recall and failure-mode companion tables so first-stage exclusion is separated from reranker ordering failure.
3. Report public-gold by source family, provider/tool cue status, and acceptable-alternative status.
4. Audit M6-v1/M6-v2 request-field activation on a labelled sample if either diagnostic is used as thesis evidence.
5. Run length-control or field-dropout ablations to separate field identity from extra-token effects if making strong field-causality claims.
6. Add a thesis-ready experimental setup table: gold labels, prompt strata, model settings, candidate budget, reranker, cache/cost, and metrics.
7. Add a literature-review empirical-detail table for key papers.
8. Decide whether SkillRouter, M4 tree routing, or M5 graph retrieval adds a genuinely new information-layer claim; otherwise defer graph/tree to discussion/future work.
9. Measure top-20/top-50/top-100 latency and cost for final candidate budgets.
10. Rerun or simulate M0 progressive-disclosure baseline with exact context-token/cost instrumentation; use the 2433-skill library mainly as a context stress test if feasible.
11. Run downstream candidate-subset validation on a smaller sample after offline retrieval behavior is stable.
12. If all stronger embedding/reranking methods perform near-perfectly in a future benchmark version, revisit cluster difficulty and prompt leakage before claiming information-layer improvement.

## Current Implementation Status

2026-06-18 active-status override:

- Current frozen benchmark is `benchmark-v0.4-2026-06-16`: 245 controlled prompts, 144 public-gold prompts, 12 low-information stress prompts, and 2433 skills.
- The compact source of truth is `thesis_notes/current/Active Benchmark Snapshot.md`.
- The method source of truth is `thesis_notes/current/Experiment Methodology Tracker.md`.
- The crossed information-layer comparison source is `thesis_notes/current/Representation Layer Horizontal Comparison.md` until the filename is changed.
- BM25 and TF-IDF have now been run over R1/R2/full as lexical representation controls. Report: `outputs/frozen_v0_4_crossed_lexical_matrix.md`.
- Qwen and SkillRouter embedding/rerank families have R1/R2/full frozen-v0.4 coverage.
- M6-v2 no-rewrite semantic field matching has R1/R2/full frozen-v0.4 coverage over fixed Qwen and SkillRouter top-20 candidates.
- M6-v2 fine blend calibration is complete. Report: `outputs/frozen_v0_4_m6v2_blend_sweep_fine.md`.
- M6-v2 field-specific request-to-skill matching and explicit field-weight calibration are complete for Qwen and SkillRouter R1/R2/full top-20 candidate sets. Report: `outputs/frozen_v0_4_m6v2_explicit_field_weight_sweep_narrow.md`.
- Focused R2 M6-v2 explicit-use tuning is complete. Report: `outputs/frozen_v0_4_m6v2_explicit_field_weight_sweep_r2_focused.md`. Current interpretation: useful field signal exists, but held-out R2 results do not yet show a clean win over strong learned reranking. Treat M6-v2 as a calibrated diagnostic until field activation, mismatch penalties, and dev/test selection are hardened.
- M6-v2 fixed internal-weight ablation is complete. Reports: `outputs/frozen_v0_4_m6v2_internal_weight_ablation_fixed.md` and `outputs/frozen_v0_4_m6v2_internal_weight_ablation_fixed_detailed.md`.
- M6-v2-fixed task-heavy policy is complete and should be used as the clean thesis-facing fixed method. Report: `outputs/frozen_v0_4_m6v2_fixed_task_heavy.md`. Field-only sensitivity report: `outputs/frozen_v0_4_m6v2_fixed_task_heavy_field_only.md`. Fixed policy: 0.30 first-stage score, 0.70 semantic-field score, 0.25 penalty/bonus adjustment, and field weights task 0.50, output 0.20, workflow 0.15, input 0.10, dependency 0.05.
- Remaining major gaps are thesis integration of the statistical/failure-mode reports, per-source-family public-gold failure slicing, cost/latency reporting, full-scale M0 progressive disclosure, optional M4/M5 graph/tree methods, and downstream task-success validation.

- `scripts/export_skill_representations.py` exports R1-R4 implementation artifacts for the information layers.
- `representations/R1_flat_metadata.jsonl` stores name, family, and description.
- `representations/R2_structured_procedural.jsonl` stores parsed `Use when`, `Not for`, workflow, output, preconditions, and writing rules.
- `representations/R3_dependency_resource_aware.jsonl` adds dependency profiles, external dependencies, resource signals, public-source metadata, and bundled resource files.
- `representations/R4_graph_edges.jsonl` stores graph edges derived from procedural and dependency/resource fields.
- The exported components support method families M1-M8, but do not by themselves implement retrieval, tree routing, graph traversal, reranking, provider API calls, or progressive disclosure evaluation.
- `scripts/analyze_procedural_distinctness.py` implements the first-pass Step 2 field-difference audit over gold/alternative prompt pairs.
- `scripts/analyze_requirement_alignment.py` implements the stricter Step 2 prompt-requirement alignment check.
- `scripts/analyze_semantic_confusability.py` implements Step 3 semantic-confusability reporting with `sentence-transformers/all-MiniLM-L6-v2` when the validation environment is installed, otherwise a local TF-IDF fallback.
- `scripts/analyze_prompt_leakage.py` implements the prompt-leakage check for exact gold-name leakage, dominant gold title-word overlap, and copied gold-card phrases.
- `scripts/validate_benchmark_integrity.py` implements Step 1 as a reproducible report.
- `scripts/audit_public_skill_fields.py` implements the resumable Step 6 public-skill field audit over imported public `SKILL.md` artifacts.
- `scripts/build_public_skill_manual_review_packet.py` builds a stratified manual review packet from the public-skill field audit output.
- `scripts/model_verify_public_skill_fields.py` implements the model-assisted Step 6 semantic verification pass with strict JSON output and required evidence spans.
- `scripts/compare_public_skill_field_audits.py` compares heuristic labels against model labels and produces the Step 6 disagreement report.
- `scripts/build_public_skill_disagreement_review_packet.py` builds a prioritized Step 6 disagreement packet for targeted manual adjudication.
- Step 6b public-skill gold validation is implemented as a separate draft stratum, not yet merged into the main benchmark:
  - `scripts/generate_public_gold_validation.py`
  - `prompts_public_gold/public_gold_validation_confusability.json`
  - `annotations/public_gold_acceptable_alternatives.json`
  - `outputs/public_gold_*`
- `scripts/run_field_ablation_selectors.py` implements Step 7 local representation field ablations over cumulative and single-field views.
- `scripts/generate_background_scale_skills.py` now generates 1800 background-scale skills: 80 hand-written broad background skills plus 1720 deterministic domain/procedure skills with dependency and resource signals.
- `scripts/import_public_background_skills.py` now discovers public `SKILL.md` files from selected OpenAI, Anthropic, Hugging Face, `claude-office-skills`, `akillness/oh-my-skills`, Addy Osmani, Matt Pocock, SWE-Skills-Bench, and smaller repositories, while preserving curated metadata overrides for key public skills.
- `scripts/generate_core_v2_clusters.py` generates the current controlled-core v2 expansion: office artifact workflows, deployment/browser QA, and API/backend design.
- `scripts/analyze_non_core_competition.py` checks whether background/public/support skills semantically outrank the gold core skill under description-card similarity.
- `scripts/run_offline_selectors.py` implements the shared offline selector/evaluator harness for M1, M2, M3, and M6 local baselines, with M0 trace-summary support.
- Current `M6-v0` rerankers use a first-stage candidate set followed by deterministic schema-aware reranking. Candidate budgets tested include top-20, top-50, and top-100 in different runs. The v0 reranker combines normalized first-stage score with a weighted schema score over description, `use_when`, output shape, preconditions, workflow, dependency/resource fields, and a mild `not_for` penalty.
- `scripts/run_provider_selectors.py` implements optional M7/M8 provider-backed baselines: OpenAI-compatible embedding retrieval and Qwen `qwen3-rerank` over a first-stage top-k candidate set. It requires API keys and caches calls under `runtime/provider_cache`.
- SkillRouter-specific M7/M8 is implemented in `scripts/run_skillrouter_selectors.py`. Local CPU/MPS execution on the 8 GB laptop was impractical, but Hugging Face Jobs `t4-small` completed the full 2401-skill evaluation on 2026-06-05. Results: controlled SkillRouter full embedding reaches `73.0%` top-1, `94.2%` top-5, and `0.827` MRR; controlled SkillRouter full embedding plus SkillRouter rerank top-20 reaches `83.2%` top-1, `97.8%` top-5, and `0.898` MRR. The older cleaned 82-prompt public-gold rerun completed via Hugging Face Jobs job `6a22ef1cece949d7b3dca3a2`: SkillRouter full embedding reaches `68.3%` top-1, `95.1%` top-5, and `0.790` MRR; SkillRouter rerank top-20 reaches `64.6%` top-1, `92.7%` top-5, and `0.778` MRR. These numbers are historical; use `frozen_v0_4_information_layer_matrix.md` for active SkillRouter I1/I3/I2 results.
- SkillRouter first-stage plus M6-v1 field-aware reranking is implemented through `scripts/run_m6v1_field_aware_reranker.py --first-stage skillrouter_full`. Hosted results on 2026-06-05 show the strongest controlled result so far: `86.9%` top-1, `98.5%` top-5, and `0.927` MRR using top-100 SkillRouter candidates and the `task_output_workflow` field set. The same hybrid does not improve public-gold top-1, so public-skill extraction/field matching remains a limitation.
- `notes/provider_api_baselines.md` records current provider choices, API key setup, expected cost controls, and recommended run order.
- `scripts/analyze_m0_manifest.py` implements the dedicated Step 8 M0 progressive-disclosure report with strict top-1, acceptable top-1, any-hit, no-skill, multi-skill, family-level, and prompt-level breakdowns.
- `outputs/step8_downstream_validation_plan.md` records the planned Step 9 downstream sample, conditions, artifact grading rubric, and pass thresholds. The filename still says `step8` from the earlier numbering.
- `scripts/prepare_step8_candidate_report.py` and `outputs/step8_candidate_readiness_report.md` implement the pre-downstream top-5 candidate recall check for the planned Step 9 sample. The filenames still say `step8` from the earlier numbering.
- MiniLM is currently used as a local construction/validation model only. It should not be treated as the main modern embedding baseline in final experiments.
- Stronger embedding/reranking baselines now include Qwen `text-embedding-v4` full-skill retrieval, Qwen `qwen3-rerank`, SkillRouter embedding, and SkillRouter reranking. The current `M6-v0` reranker is deterministic and local, not a neural cross-encoder. `M6-v1-local` is implemented as a lexical field-aware prototype; the next possible methodological improvement is `M6-v2`, a semantic or LLM-assisted field matcher.
- Current Step 1 integrity result: PASS. 201 prompts and 2433 skills resolve.
- Current representation coverage result: PASS. R1-R4 export covers the 2433-skill library, including 169 evaluated skills, the integrated implicit-field stress set, and the public-style controlled stratum.
- Current Step 2 field-audit result: 201/201 prompts pass, and 646/646 gold/alternative pairs have two or more primary procedural differentiators in the structured representation. Treat this as schema coverage only.
- Current stricter Step 2 requirement-alignment result: PASS with recorded residuals. The embedding diagnostic passes 199/201 prompts and 657/659 pairs.
- Current Step 3 semantic-confusability result: PASS. The embedding diagnostic reports 182/201 prompts, or 90.5%, with at least two plausible alternatives.
- Current Step 4 gold-label stability result: PASS after manual review of `web_p5_frontend_debugging`, `doc_p2_document_rewriter`, `obs_p5_root_cause`, `reply_p2_polish_supervisor`, `sec_p2_security_code_review`, and post-leakage weak cases `sec_p1_threat_model` and `skill_p2_install_existing`. No reviewed case was removed as ambiguous.
- Current prompt-leakage result: PASS. 0 critical exact-name leaks and 0 high-risk leaks.
- Current Step 5 scale result: PASS. The large condition is now 2433 skills: 169 controlled/evaluated skills including 10 implicit-field stress skills and 32 public-style controlled skills, 1800 generated background-scale skills, 460 public imported background skills, and 4 support email skills. 460/460 public imports have downloaded original `SKILL.md` files.
- Current Step 6 public-skill field audit result: MOSTLY DONE. A 460/460 public-skill heuristic checkpoint has been generated, plus a 15-skill manual review packet. The DeepSeek `deepseek-v4-flash` model-assisted checkpoint has now been run on the full 460-skill public subset, producing `public_skill_field_model_audit.jsonl` and `public_skill_field_agreement_report.md`; a prioritized 80-case disagreement packet is ready for targeted manual taxonomy adjudication.
- Current Step 6b public-skill gold validation result: EXPANDED / PASS WITH CAVEATS. The active 144-prompt public-gold stratum passes automated construction gates: Step 1 integrity 144/144 over the 2433-skill library, Step 2 procedural distinctness 144/144, Step 2 prompt-specific alignment 131/144, Step 3 semantic confusability 144/144, and Step 4 leakage 0 critical/high-risk with provider/tool dependency cues recorded separately. Local/provider/SkillRouter selector results are current for frozen v0.4; older 82- and 120-prompt public-gold notes are historical.
- Current Step 7 non-core semantic competition result: PASS useful pressure under TF-IDF fallback. A non-core skill is top-1 for `26/85` prompts and the best non-core skill scores above gold for `30/85` prompts. Previous MiniLM/embedding results remain historical/comparison evidence.
- Current Step 7 non-core procedural review result: PASS with caveat under TF-IDF fallback. `14/85` prompts have at least one non-core skill above gold. These cases need manual adjudication before final claims.
- Historical Step 7 offline selector result: PASS useful pressure. On the 2433-skill / 201-prompt condition, flat metadata reaches `61.7%` top-1 for M1 BM25 and `55.2%` for M1 TF-IDF; serialized schema/rerank reaches `65.2-65.7%`; M6-v1 local field-aware reranking reaches `72.1-72.6%` at top-100 candidate budget.
- Historical Step 7 field ablation result: DONE and supported by the 2433/201 M6-v1 rerun. Description/flat retrieval is weaker than selective use of task, output, and workflow/procedure fields. Naive all-field scoring can hurt top-1, so fields should be treated with field-aware scoring/reranking rather than appended as plain text.
- Historical 1006-scale Qwen provider result: PASS useful pressure. On the 1006-skill condition, Qwen `text-embedding-v4` reaches `35.8%` top-1 on R1 flat cards, `46.3%` on full `SKILL.md`, and `47.8%` on R2 structured cards. Qwen `qwen3-rerank` over top-20 improves these to `64.2%`, `61.2%`, and `65.7%` respectively. Qwen full-skill embeddings combined with the local schema reranker reach `68.7%` top-1 at top-20, `80.6%` at top-50, and `85.1%` at top-100. Use this only as historical comparison.
- Current 2089-scale Qwen update: Qwen full-skill embedding-only reaches `50.6%` top-1 and `69.4%` top-5; Qwen full-skill plus Qwen `qwen3-rerank` over top-20 reaches `63.5%` top-1 and `69.4%` top-5; Qwen full-skill plus local schema rerank reaches `80.0%` top-1 at top-50 and `84.7%` top-1 at top-100. R1/R2 Qwen variants remain historical 1006-scale unless rerun.
- Current low-information stress-test result: DONE separately. On 12 less-informative prompts, the best strict top-1 is `41.7%` for MiniLM full-skill embedding; Qwen full + local schema top-100 reaches `25.0%` top-1 and `66.7%` top-5. This should be reported as a robustness/limitation check, not folded into the main benchmark.
- Current strongest-method failure analysis: DONE. Qwen full-skill embedding plus local schema reranking over top-100 candidates has 10 strict top-1 failures: 4 first-stage exclusions and 6 reranker/boundary/annotation failures. The report is `thesis_notes/results/Failure Mode Analysis - Qwen Full Local Schema Top100.md`.
- Current scale-sensitivity read: PASS. Relative to core, M2a description-card MiniLM drops `-17.6` top-1 points and `-12.9` top-5 points; M1 TF-IDF flat drops `-16.5` top-1 points; M3 TF-IDF schema drops `-5.9` top-1 points; M6 MiniLM full -> schema rerank drops `-8.2` top-1 points but remains strongest at `82.3%` full-library top-1.
- Current Step 8 M0 result: historical core selection trace with cost caveat. The completed progressive-disclosure run covers the older 67-prompt/67-skill controlled core. M0 strict top-1 is `61.2%`, strict any-hit is `64.2%`, no explicit skill is loaded for `31.3%` of prompts, and the mean number of full skill docs loaded is `0.78`. The active 245-prompt / 2433-skill condition has not yet been run through M0.
- Current full-library M0 result: not run. Full progressive disclosure over 2433 skills should be treated as a context/cost stress test rather than a necessary first retrieval result.
- Current Step 9 downstream result: planned, not executed. The downstream sample, conditions, artifact rubric, and pass thresholds are recorded in `outputs/step8_downstream_validation_plan.md` under the old filename. The top-5 readiness check on the 12-prompt sample gives `91.7%` for M1 BM25 flat, `100.0%` for M1 TF-IDF flat, `83.3%` for M2b MiniLM full-skill, `91.7%` for M3 TF-IDF schema, `91.7%` for M6 BM25 -> schema rerank, `91.7%` for M6 TF-IDF -> schema rerank, and `91.7%` for M6 MiniLM full -> schema rerank. Execution should start with a small local dry run, then be repeated after stronger embedding/reranking methods are added.
- Remaining Step 3 weak confusability cases are mostly highly specific extraction/debugging/observability prompts where the gold skill is intentionally clearer than the alternatives.

Next refinement target:

- freeze the final representation-field taxonomy and final method set, then measure top-20/top-50/top-100 latency and cost before Step 9 downstream validation
