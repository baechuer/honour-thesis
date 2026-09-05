# RQ1 Field Targeted Test Plan

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `CURRENT_SUPPORTING`.** Its controlled field-isolation design remains current. Its dated public-RQ1 status sections are historical and are superseded by the Round-3 public-original SOP and result packet. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Last updated: 2026-08-25

> **2026-08-28 RQ1b active-method amendment.** RQ1b's current public
> experiment is no longer raw-artifact or winner-only primary-field masking.
> It is a source-grounded, all-candidate field-type availability ablation:
> `FULL` cards are compared with one-mask-per-operational-field conditions,
> with strict-gold card preservation, literal-source fidelity, per-field
> eligibility, and residual-redundancy gates preceding any score. It tests
> conditional contribution to gold-versus-neighbour routing separation, not a
> uniquely decisive field in a natural document. Authoritative protocol:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Public Field-Type Ablation Protocol - 2026-08-28.md`.
> Its six-family pre-scoring validation pilot passed all applicable source,
> literal-card, mask-mechanics, strict-gold-preservation, eligibility, and
> residual-ledger gates. It created no selector score, retrieval metric, API
> call, or external-text transfer. The upstream non-pilot C6 source roster had
> 193 paired strict routing families (386 prompts) across 74 unique candidate
> compositions. After literal source-card construction and the 2026-08-29
> surface-cue amendment, the active frozen input is 48 compositions, 128
> routing families, and 256 prompt variants: 38 cards are byte-identical, 10
> are literal-safe same-slot repairs, and 10 cue-affected compositions are
> strictly excluded. The next gate is two blinded FULL-card preservation
> reviews; no selector result exists.
> Checkpoint: `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_pilot_2026-08-28/RQ1B_FIELD_TYPE_ABLATION_PILOT_CHECKPOINT_2026-08-28.md`.

Status: `RQ1a REVIEWED / COMPLETE` for the seven operational-field suites. The completed public-original field recoverability audit is supporting context only, not an RQ1b result. `RQ1b WAVE 001 FROZEN / NATURAL_ORIGINAL_ONLY / NOT EXECUTED` is the naturalistic public-skill replication described in `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Naturalistic Public Skill Replication Protocol - 2026-08-24.md`. Keep completed RQ1a cluster content frozen except for proven errors. These reviewed propositions are the source for RQ2a matched-content representations; see `thesis_notes/current/RQ2 Current Status and Implementation Tracker - 2026-07-26.md`.

## Purpose

RQ1 asks:

> Which operational information types help distinguish semantically similar but procedurally distinct agent skills?

The existing frozen-v0.4 I1/I3/I2 matrix is historical exploratory RQ2-adjacent evidence because it compares complete representation/retrieval conditions and does not cleanly isolate one field. RQ1 therefore uses the completed field-labelled, field-specific suites below.

## Test Logic

For each prompt, the gold and alternatives should be semantically similar. The correct skill should be identifiable because one operational field resolves the ambiguity.

Important clarification, agreed 2026-06-23:

- RQ1 tests skill-side information, not whether vague prompts can be guessed.
- The user prompt should explicitly state the operational requirement: the object, input state, requested output, procedure, boundary, dependency, or success condition.
- The prompt is held fixed across ablations. It is not the experimental variable.
- The experimental variable is what matching information is exposed on the skill side.
- Avoiding leakage does not mean making the prompt vague. It means the baseline skill-side representation should not already reveal the `primary_distinguishing_field`.

Clean RQ1 comparison:

1. Use the same prompt, skill library, retriever, candidate budget, and metric.
2. Use a shared/domain baseline description that keeps the broad task context but removes the primary distinguishing field.
3. Compare this controlled baseline against baseline plus one operational field.
4. Group results by the prompt's `primary_distinguishing_field`.
5. Count a field as helpful only if it improves top-1/MRR or reduces hard-negative sibling errors on prompts where that field is the labelled distinction.

This means the baseline should not be so vague that a human cannot identify the gold skill. It should preserve the common cluster context while hiding the specific skill-side fact being tested.

Canonical condition names, agreed 2026-06-24:

| Condition | Selector-visible text | Thesis role |
|---|---|---|
| `shared_context_only` | The shared neutral skill-side context with the target field omitted. | Hidden-field baseline. Sibling skills are intentionally tied when all target information is removed. |
| `shared_context_plus_field` | The same shared context plus exactly one appended target field line, such as `Input / Precondition: ...` or `Output Artifact: ...`. | Main RQ1a exposed-field condition. This is the headline causal contrast. |
| `field_only` | Only the target field value. | Diagnostic: tests whether the field text alone is enough signal. |
| `full_skill_doc` | The whole generated skill artifact, including names, headings, all shared sections, and the target field. | Diagnostic: tests whether the signal survives whole-document noise/cost. Not the main RQ1a field-isolation claim. |

For every field suite, the thesis-facing table should therefore report `shared_context_only` versus `shared_context_plus_field` and the lift between them. `full_skill_doc` may be mentioned as a diagnostic, but it should not be treated as the clean RQ1 field-isolation condition.

Example:

| Role | Text | Why |
|---|---|---|
| Prompt | "Extract table rows from a scanned PDF image and return structured data." | Explicit and gold-stable. |
| Bad masked skill baseline | "Handles PDF document processing tasks." | Too vague; removes the task. |
| Better skill baseline | "Extracts structured information from PDF documents." | Keeps shared task context but hides scanned/native distinction. |
| Skill A input/workflow | "Works on scanned or image-based PDFs; runs OCR before table extraction." | Matching skill-side evidence. |
| Skill B input/boundary | "Works on native PDFs with selectable text; not for scanned PDFs requiring OCR." | Contrasting skill-side evidence. |

The proof is not that the prompt alone contains the answer. The proof is that the prompt requirement can only be matched to the correct near-neighbour skill when the skill-side representation exposes the corresponding operational field.

## RQ1 Test Unit

An RQ1 test unit is the smallest controlled comparison used to answer RQ1. It is not a whole retriever architecture and it is not a whole benchmark matrix. It is one prompt plus one near-neighbour skill pair or cluster where one operational field is the intended separator.

Each RQ1 test unit contains:

| Component | Meaning |
|---|---|
| Fixed prompt requirement | The user-side request, written clearly enough that the intended gold skill is stable. |
| Near-neighbour skill pair/cluster | Skills that share domain, nouns, and broad task family, so a short description can plausibly confuse them. |
| Shared neutral skill context | A controlled skill-side baseline that preserves the common task family but removes the target field value. |
| Target field values | The skill-side operational facts that differ between siblings, such as scanned vs native input, JSON table vs prose summary output, or local runtime vs Hugging Face Jobs. |
| Gold and hard-negative evidence | Exact skill evidence showing why the gold satisfies the target field and why alternatives do not. |
| Fixed retriever/metric | The retrieval method, candidate budget, and metrics held constant while field visibility changes. |

The unit therefore asks:

> If the prompt requires field value X, and the skill-side baseline hides X, does exposing the matching skill-side field help the selector choose the correct sibling?

This avoids mixing RQ1 with RQ2. RQ1 is about whether a field value is useful for distinguishing near-neighbour skills. RQ2 can later ask which representation/retrieval architecture best carries, organizes, or exploits those values.

## RQ1 Evidence Programme

The formal research question remains unchanged:

> Which operational information types help distinguish semantically similar but procedurally distinct agent skills?

It is answered by two complementary evidence lines with deliberately different claim strength:

**RQ1a: controlled individual-field sufficiency (`REVIEWED / COMPLETE`).**

Do operational field values such as input state, output artifact, workflow, dependency, boundary, or success criterion distinguish semantically similar skills when shared context is controlled? This is the completed field-isolation test. It establishes that an exposed field can resolve deliberately tied near-neighbour candidates; it does not estimate how often a field is the unique natural cue in public skill documentation.

**Supporting public-skill field-realism audit (`COMPLETE / CONTEXT ONLY`).**

Do original public skill artifacts contain recoverable evidence for those operational fields, and how often? The 460-file audit answers this grounding question only. It is not a routing-accuracy result, a causal field-ablation, or a naturalistic replication.

**RQ1b-N: naturalistic public-skill corpus and label frame (`FROZEN / NOT A SELECTOR RESULT`).**

The frozen public-source corpus provides the provenance-preserved strict clusters, prompts, labels, and cue-risk records for RQ1b. It is the ecological frame for the active study, not a raw-document causal mask comparison. The fixed 460-file field-realism audit remains historical support only. Source hashes, prompts, exact evidence maps, and model-assisted blind strict-label records remain frozen; they are not human annotation, selector results, or external-text results. Protocol: `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Naturalistic Public Skill Replication Protocol - 2026-08-24.md`.

**RQ1b-A: public field-type availability ablation (`ACTIVE / PILOT PASS / AMENDED INPUT FREEZE / FULL-CARD PRESERVATION PENDING`).**

The active ecological experiment projects each frozen public candidate into a source-grounded seven-slot card. It first requires the full card to preserve the sealed strict gold under selection-only blinded review. It then withholds one field type from every candidate card at a time and measures conditional Top-1 loss, rank/MRR movement, selector-native gold-versus-best-wrong margin change, post-mask winner identity, and cross-slot residual redundancy. This asks how much a field type contributes to public combined-information routing without assuming that it is the unique human decision rationale. It is a derivative-card field-availability test, not a claim about deleting text from raw public documents. Protocol: `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Public Field-Type Ablation Protocol - 2026-08-28.md`.

The six-family local pre-scoring pilot passed all applicable construction and
preservation gates. It is an instrument-validation checkpoint only: it created
no selector score, retrieval metric, API call, or external-text transfer. The
pilot is excluded from confirmatory effects. The active non-pilot input is
frozen after source-card construction and surface-cue remediation; its 128
routing families now await the full-card preservation gate.

**RQ1c: joint-field interaction (`DEFERRED`).**

Do not define or execute a combined-field interaction suite until RQ1b is reviewed. Combined all-field representations, graph/tree/grouping strategies, and retriever robustness remain RQ2 concerns unless the thesis framing is explicitly revised.

## RQ1 Closing Boundary And Transition To RQ2

Agreed 2026-07-24:

- RQ1a is the causal evidence for individual-field discriminability. It deliberately makes sibling skills identical apart from one target field, so it cannot be replaced by a natural public-skill comparison.
- The supporting public-skill field-realism audit is external-realism context only. It establishes that the same operational information is commonly present or recoverable from real artifacts, but it is not a routing-accuracy result and does not establish a field-specific causal effect.
- RQ1b-N supplies the ecological public-source frame. RQ1b-A tests field availability on a source-grounded derivative card rather than claiming a raw-document single-field effect. It reports both field contribution and cross-field redundancy, conditional on card-preservation gates.
- In naturally authored skills, operational facts are normally expressed jointly. A use condition may be repeated in the title, description, workflow and examples; output, workflow, dependency, boundary and verification can reinforce one another. This is expected, rather than a defect in the public corpus.
- The imported Notion knowledge-capture, meeting-intelligence and research-documentation skills are a qualitative example: all retrieve and create/update Notion pages, but their use condition, output artifact and workflow jointly distinguish wiki-style knowledge capture, meeting agendas/pre-reads, and cited research briefs/reports. They are not admitted as a new RQ1a single-field test because several fields already reveal the correct choice.

Therefore, RQ1 does not prescribe that a router should use only one field. It identifies operational information that must be available somewhere in a practical selection surface. RQ2 begins from that combined reality: it compares how skill representations and retrieval strategies preserve, organise and exploit jointly expressed information, with accuracy, candidate recall, selector-visible context, latency, construction cost and failure modes reported separately.

2026-07-01 status:

- RQ1a has complete controlled suites for `use_condition`, `input_precondition`, `output_artifact`, `dependency_resource`, `boundary_not_for`, `success_verification`, and `workflow_procedure`. The canonical contrast is still `shared_context_only` versus `shared_context_plus_field`.
- RQ1a also has a completed negative-control / composite suite for `examples_tests` at `skill_benchmark/rq1a_field_discriminability/examples_test/`. It is intentionally not counted as an eighth core operational field. In each cluster, all true operational fields are shared across sibling skills and only the examples/tests section differs. Gold labels are example-matched only. The suite separates `generic` prompts, where no example scenario is named, from `rare_exact_match` prompts, where the request deliberately resembles one stored example.
- The supporting public-skill field-realism audit covers 460 upstream public skill files. It reads `skill_benchmark/skills/public_imported_background/<skill>/source/SKILL.original.md`, not the normalized benchmark wrappers.
- Supporting-audit artifacts: `skill_benchmark/scripts/audit_rq1_public_field_realism.py`, `skill_benchmark/outputs/rq1_public_field_realism_audit.md`, `skill_benchmark/outputs/rq1_public_field_realism_audit.json`, and `skill_benchmark/outputs/rq1_public_field_realism_audit_rows.jsonl`.
- Public recoverability is high for all seven fields, but explicitness and routing cleanliness differ: use condition is universal; input, output, workflow, boundary, and dependency are commonly recoverable; success/verification is common but noisy; dependency/resource must be interpreted as hard capability compatibility rather than generic install/setup text.
- RQ1b public-source discovery used a 1,099-artifact local source corpus: 460 fixed historical originals, 168 separately staged Emmraan sources, and 471 separately staged Skill Me sources from MIT-licensed, commit-pinned upstream repositories. The historical 460-file audit is not recomputed or relabelled. The frozen strict natural-original clusters supply RQ1b-A inputs; its active field-card pilot has no selector, retrieval score, embedding, API, or external text transmission.

## Completed Negative-Control Suite: Examples / Tests

Status: complete multi-method negative-control run as of 2026-07-18.

Purpose:

- Public skills commonly include examples, sample prompts, expected outputs, small tests, or mini scenarios.
- These examples may help retrieval because they repeat concrete input/output/workflow/success terms.
- They do not necessarily define separate skill capability. They can also mislead a selector toward a skill whose example resembles the user request, even when sibling skills are operationally equivalent.

Design:

- Suite folder: `skill_benchmark/rq1a_field_discriminability/examples_test/`
- 50 clusters, 3 sibling skills per cluster, 100 prompt rows.
- All sibling skills share use condition, input/precondition, output artifact, workflow/procedure, boundary/not-for, dependency/resource, and success/verification.
- Only `Examples / Tests` differs.
- Gold labels are `example_matched_only`: the gold has the closest example to the `rare_exact_match` prompt, but all siblings should still be capable of the generic requested task.
- `generic` is the thesis-facing independent-value variant: "Review the provided artifact for evidence-backed issues and return the shared operational report."
- `rare_exact_match` is an upper-bound diagnostic: it deliberately names the scenario contained in one sibling's example.

Current multi-method result:

| Retriever | Prompt subset | Hidden examples top-1 | `shared_context_plus_field` top-1 | Lift | Interpretation |
|---|---:|---:|---:|---:|---|
| BM25 | Generic | 33.3% | 22.7% | -10.7pp | Non-matching examples do not help and can add noise. |
| BM25 | Rare exact match | 33.3% | 100.0% | +66.7pp | Exact example resemblance dominates lexical selection. |
| TF-IDF | Generic | 33.3% | 33.0% | -0.3pp | Non-matching examples are effectively chance-level. |
| TF-IDF | Rare exact match | 33.3% | 100.0% | +66.7pp | Same upper-bound exact-match effect. |
| Qwen embedding | Generic | 33.3% | 28.0% | -5.3pp | Non-matching examples do not help semantic retrieval. |
| Qwen embedding | Rare exact match | 33.3% | 100.0% | +66.7pp | Exact example resemblance also dominates semantic retrieval. |

Reasoning selector result:

| Selector | Condition | Prompt subset | Expected behavior rate | Ambiguous rate | Selection rate | Interpretation |
|---|---|---:|---:|---:|---:|---|
| DeepSeek `deepseek-v4-flash` | Hidden | Generic | 100.0% | 100.0% | 0.0% | Correctly refuses arbitrary selection. |
| DeepSeek `deepseek-v4-flash` | Hidden | Rare exact match | 100.0% | 100.0% | 0.0% | Correctly refuses without examples visible. |
| DeepSeek `deepseek-v4-flash` | + Examples | Generic | 100.0% | 100.0% | 0.0% | Correctly treats non-matching examples as insufficient. |
| DeepSeek `deepseek-v4-flash` | + Examples | Rare exact match | 100.0% | 0.0% | 100.0% | Selects only when request matches a stored example. |
| Codex subagent selector | Hidden | Generic | 100.0% | 100.0% | 0.0% | Correctly refuses arbitrary selection. |
| Codex subagent selector | Hidden | Rare exact match | 100.0% | 100.0% | 0.0% | Correctly refuses without examples visible. |
| Codex subagent selector | + Examples | Generic | 100.0% | 100.0% | 0.0% | Correctly treats non-matching examples as insufficient. |
| Codex subagent selector | + Examples | Rare exact match | 100.0% | 0.0% | 100.0% | Selects only when request matches a stored example. |

Thesis interpretation:

Artifacts:

- Multi-method summary: `skill_benchmark/outputs/rq1a_examples_test_multimethod_summary.md`
- BM25/TF-IDF result: `skill_benchmark/outputs/rq1a_examples_test_negative_control_local_lexical.md`
- Qwen embedding result: `skill_benchmark/outputs/rq1a_examples_test_negative_control_qwen_embedding.md`
- DeepSeek selector result: `skill_benchmark/outputs/rq1a_examples_test_llm_selector_deepseek.md`
- Codex subagent selector result: `skill_benchmark/outputs/rq1a_examples_test_subagent_selector.md`

This suite should be framed as a low-routing-value or cautionary field test. For the `generic` variant, there is no true operational gold because all sibling skills can perform the task; scoring against the inherited example-matched option only checks whether examples create arbitrary attraction. The corrected BM25, TF-IDF, Qwen, DeepSeek, and Codex subagent results support the claim that examples/tests have little independent routing value when the user request does not resemble a stored example. They become strong only under rare exact or near-exact example matches, which is better treated as possible example-attraction or misguidance than as a true skill capability distinction.

This is the clearest current negative-control evidence that field presence in a skill document does not automatically imply routing value. For the thesis, examples/tests should be treated primarily as workflow-support context: useful for execution, validation, onboarding, edge-case illustration, and downstream behavior after a skill has already been selected. This lets RQ1 separate primary selection signals, such as input, output, dependency, use condition, and boundary, from support/documentation content that should generally not drive first-pass routing.

## Completed RQ1a Suite 1: Input / Precondition

Status: complete for the input/precondition field as of 2026-06-24.

Artifacts:

- Suite folder: `skill_benchmark/rq1a_field_discriminability/input_precondition/`
- Aggregate prompts: `skill_benchmark/rq1a_field_discriminability/input_precondition/prompts.jsonl`
- Rubric summary: `skill_benchmark/rq1a_field_discriminability/input_precondition/rubric_summary.md`
- Runner: `skill_benchmark/scripts/run_rq1a_field_ablation.py`
- Main result: `skill_benchmark/outputs/rq1a_input_precondition_bm25_qwen_embedding.md`
- Machine summary: `skill_benchmark/outputs/rq1a_input_precondition_bm25_qwen_embedding.json`

Design:

- 50 near-neighbour clusters.
- 3 sibling skills per cluster: 1 gold and 2 hard negatives.
- 2 prompts per cluster: one direct prompt and one paraphrase-safe prompt.
- 100 evaluated prompt variants total.
- Non-target context is controlled: broad task, output, workflow, boundary, dependency, and success framing are shared or intentionally non-discriminative.
- The intended distinguishing signal is the skill-side `input_precondition` value.
- The hidden-field baseline uses only `shared_context_only`; the three sibling candidates are intentionally tied. Top-1 for this baseline is therefore reported as tie-aware expected top-1, 1/3.

Run command:

```bash
python3 skill_benchmark/scripts/run_rq1a_field_ablation.py \
  --retrievers bm25,qwen_embedding \
  --embedding-batch-size 4 \
  --output-prefix rq1a_input_precondition_bm25_qwen_embedding
```

Main result:

Prompt subset `Combined` pools the direct and paraphrase-safe prompt rows.

| Retriever | Prompt subset | Hidden field top-1 | `shared_context_plus_field` top-1 | Lift | MRR + field |
|---|---:|---:|---:|---:|---:|
| BM25 | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| BM25 | Paraphrase | 33.3% | 91.0% | +57.7pp | 0.953 |
| BM25 | Combined | 33.3% | 95.5% | +62.2pp | 0.977 |
| Qwen embedding | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| Qwen embedding | Paraphrase | 33.3% | 94.0% | +60.7pp | 0.970 |
| Qwen embedding | Combined | 33.3% | 97.0% | +63.7pp | 0.985 |

Additional diagnostic:

- BM25 `full_skill_doc` all top-1 is 96.0%, close to the compact `shared_context_plus_field` condition.
- Qwen `full_skill_doc` all top-1 is 94.0%, lower than compact `shared_context_plus_field` at 97.0%.
- This suggests that, for this controlled field-isolation suite, exposing the decisive field compactly can be at least as effective as embedding the full generated skill document.

Interpretation:

The suite supports input/precondition as a strong RQ1a field. Because both BM25 and Qwen embedding improve from chance-level hidden-field ties to high direct and paraphrase-safe accuracy, the result indicates that the input/precondition field carries routing-relevant information for semantically similar sibling skills. It does not yet establish the relative value of output, workflow, boundary, dependency, or success fields; those require separate suites with the same leakage controls.

## Completed RQ1a Suite 2: Output / Artifact

Status: complete for the output/artifact field as of 2026-06-24.

Artifacts:

- Suite folder: `skill_benchmark/rq1a_field_discriminability/output_artifact/`
- Aggregate prompts: `skill_benchmark/rq1a_field_discriminability/output_artifact/prompts.jsonl`
- Rubric summary: `skill_benchmark/rq1a_field_discriminability/output_artifact/rubric_summary.md`
- Runner: `skill_benchmark/scripts/run_rq1a_field_ablation.py`
- Main result: `skill_benchmark/outputs/rq1a_output_artifact_bm25_qwen_embedding.md`
- Machine summary: `skill_benchmark/outputs/rq1a_output_artifact_bm25_qwen_embedding.json`

Design:

- 50 near-neighbour clusters.
- 3 sibling skills per cluster: 1 gold and 2 hard negatives.
- 2 prompts per cluster: one direct prompt and one paraphrase-safe prompt.
- 100 evaluated prompt variants total.
- Non-target context is controlled: broad task, input/precondition, workflow, boundary, dependency, and success framing are shared or intentionally non-discriminative.
- The intended distinguishing signal is the skill-side `output_artifact` value.
- The hidden-field baseline uses only `shared_context_only`; the three sibling candidates are intentionally tied. Top-1 for this baseline is therefore reported as tie-aware expected top-1, 1/3.
- The main exposed-field condition is `shared_context_plus_field`, meaning the same shared context plus `Output Artifact: <skill-specific output/artifact>`.

Run command:

```bash
python3 skill_benchmark/scripts/run_rq1a_field_ablation.py \
  --suite-dir skill_benchmark/rq1a_field_discriminability/output_artifact \
  --retrievers bm25,qwen_embedding \
  --output-prefix rq1a_output_artifact_bm25_qwen_embedding
```

Main result:

Prompt subset `Combined` pools the direct and paraphrase-safe prompt rows.

| Retriever | Prompt subset | Hidden field top-1 | `shared_context_plus_field` top-1 | Lift | MRR + field |
|---|---:|---:|---:|---:|---:|
| BM25 | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| BM25 | Paraphrase | 33.3% | 53.3% | +20.0pp | 0.723 |
| BM25 | Combined | 33.3% | 76.7% | +43.3pp | 0.861 |
| Qwen embedding | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| Qwen embedding | Paraphrase | 33.3% | 92.0% | +58.7pp | 0.957 |
| Qwen embedding | Combined | 33.3% | 96.0% | +62.7pp | 0.978 |

Additional diagnostic:

- BM25 `full_skill_doc` all top-1 is 88.8%, higher than compact `shared_context_plus_field` at 76.7%.
- Qwen `full_skill_doc` all top-1 is 94.0%, slightly lower than compact `shared_context_plus_field` at 96.0%.
- This diagnostic should be interpreted as whole-document signal survival/noise, not as the main RQ1a output-field causal comparison.

Interpretation:

The suite supports output/artifact as a strong RQ1a field, especially for semantic embedding retrieval. Direct prompts are solved by both BM25 and Qwen embedding, but paraphrase-safe prompts separate the retrievers: BM25 falls to 53.3% while Qwen remains at 92.0%. This suggests that output/artifact information is useful, and that semantic matching is important when the requested output is phrased without exact artifact keywords.

## Completed RQ1a Suite 3: Boundary / Not For

Status: complete for the boundary/not-for field as of 2026-06-25.

Artifacts:

- Suite folder: `skill_benchmark/rq1a_field_discriminability/boundary_not_for/`
- Aggregate prompts: `skill_benchmark/rq1a_field_discriminability/boundary_not_for/prompts.jsonl`
- Rubric summary: `skill_benchmark/rq1a_field_discriminability/boundary_not_for/rubric_summary.md`
- Implicit-authority analysis: `skill_benchmark/rq1a_field_discriminability/boundary_not_for/implicit_authority_analysis.md`
- Runner: `skill_benchmark/scripts/run_rq1a_field_ablation.py`
- Main result: `skill_benchmark/outputs/rq1a_boundary_not_for_bm25_qwen_embedding_with_implicit.md`
- Machine summary: `skill_benchmark/outputs/rq1a_boundary_not_for_bm25_qwen_embedding_with_implicit.json`

Design:

- 50 near-neighbour clusters.
- 3 sibling skills per cluster: 1 gold and 2 hard negatives.
- 3 prompts per cluster: one direct prompt, one paraphrase-safe prompt, and one `implicit_authority` prompt.
- 150 evaluated prompt variants total.
- Non-target context is controlled: broad task, input/precondition, output/artifact, workflow, dependency, and success framing are shared or intentionally non-discriminative.
- The intended distinguishing signal is the skill-side `boundary_not_for` value.
- The hidden-field baseline uses only `shared_context_only`; the three sibling candidates are intentionally tied. Top-1 for this baseline is therefore reported as tie-aware expected top-1, 1/3.
- The main exposed-field condition is `shared_context_plus_field`, meaning the same shared context plus `Boundary / Not For: <skill-specific boundary>`.

Prompt variant definitions:

| Variant | Meaning | Why reported separately |
|---|---|---|
| Direct | User explicitly states the boundary, often with "do not" wording. | Tests explicit exclusion or guardrail matching. |
| Paraphrase | Same boundary with reduced exact wording where safe. | Tests robustness beyond exact negative keywords. |
| Implicit authority | User asks for a constrained role such as an internal review note, triage packet, or evidence summary, without directly naming the excluded action. | Tests the realistic case where authority/scope is implied rather than explicitly negated. |
| Combined | Pools all three prompt variants. | Useful for overall result, but must not hide the weaker implicit-authority pattern. |

Run command:

```bash
python3 skill_benchmark/scripts/run_rq1a_field_ablation.py \
  --suite-dir skill_benchmark/rq1a_field_discriminability/boundary_not_for \
  --retrievers bm25,qwen_embedding \
  --conditions shared_context_only,shared_context_plus_field \
  --output-prefix rq1a_boundary_not_for_bm25_qwen_embedding_with_implicit
```

Main result:

| Retriever | Prompt subset | Hidden field top-1 | `shared_context_plus_field` top-1 | Lift | MRR + field |
|---|---:|---:|---:|---:|---:|
| BM25 | Direct | 33.3% | 98.0% | +64.7pp | 0.990 |
| BM25 | Paraphrase | 33.3% | 90.0% | +56.7pp | 0.943 |
| BM25 | Implicit authority | 33.3% | 62.0% | +28.7pp | 0.800 |
| BM25 | Combined | 33.3% | 83.3% | +50.0pp | 0.911 |
| Qwen embedding | Direct | 33.3% | 84.0% | +50.7pp | 0.917 |
| Qwen embedding | Paraphrase | 33.3% | 82.0% | +48.7pp | 0.907 |
| Qwen embedding | Implicit authority | 33.3% | 58.0% | +24.7pp | 0.777 |
| Qwen embedding | Combined | 33.3% | 74.7% | +41.3pp | 0.867 |

Usage note:

- The Qwen embedding run made 35 embedding API calls with approximately 57,784 embedded tokens.

Interpretation:

The suite supports boundary/not-for as a useful but conditional RQ1a field. It is strong when the prompt explicitly states the constraint and remains positive under paraphrase. Under implicit-authority prompts, however, the lift is much smaller: BM25 rises from 33.3% to 62.0%, and Qwen embedding rises from 33.3% to 58.0%. This means boundary/not-for should not be described as a simple positive matching field like input or output. It behaves partly as a compatibility, authority, or guardrail signal. Final thesis reporting should keep the implicit-authority subset visible and avoid overclaiming that boundary fields alone solve realistic scope-control cases.

## Prompt Annotation Schema

Each RQ1 case should record:

| Field | Meaning |
|---|---|
| `prompt_id` | Stable prompt identifier. |
| `gold_skill` | Correct skill. |
| `confusing_alternatives` | Semantically plausible but procedurally wrong skills. |
| `primary_distinguishing_field` | Main field that should decide the choice. |
| `secondary_distinguishing_fields` | Optional supporting fields. |
| `prompt_requirement` | Phrase in the request that requires the primary field. |
| `field_evidence_gold` | Exact evidence in the gold skill. |
| `field_evidence_alternatives` | Why alternatives are weaker or conflicting. |
| `controlled_baseline_description` | Broad cluster/task description with the primary distinguishing field removed. |
| `baseline_leakage_status` | `clean`, `leaky_original_description`, `too_vague`, or `multi_field`. |
| `rq_use` | `rq1`, `rq2`, or `both`. |

Allowed primary fields:

- `use_condition`
- `input_precondition`
- `output_artifact`
- `workflow_procedure`
- `boundary_not_for`
- `dependency_resource`
- `success_verification`

Prompts with multiple equally decisive fields should be labelled `multi_field` and used for RQ2/failure analysis, not for clean RQ1 field ranking.

## Leakage And Stability Rules

RQ1 cases must satisfy both sides:

1. Prompt stability: the prompt must explicitly state the requirement that makes the gold skill correct.
2. Skill-side non-leakage: the controlled baseline skill description must not already contain the primary distinguishing field.

Do not use prompts such as "help with this PDF" for RQ1. They are under-specified and cannot support stable gold labels.

Do not use a baseline description such as "Extracts native PDF tables into JSON with page anchors" for an input/output test. It already leaks the tested information.

Use a controlled skill-side baseline such as "Extracts structured information from PDF documents" when testing native-vs-scanned input or JSON-table output. This keeps the shared semantic cluster visible while removing the target distinguishing field.

If the original skill description already contains the target field, keep it as a realistic RQ2 baseline but create a controlled masked version for RQ1. If a controlled masked version becomes too vague, mark that case as `too_vague` and do not use it for clean RQ1 field ranking.

## Shared Context Non-Leakage Rule

The shared neutral context is allowed to say the broad domain and broad task family. It should make the siblings comparable, not empty.

Allowed shared context examples:

- "PDF information extraction skill."
- "Dataset quality task."
- "API work skill."
- "Browser page evaluation skill."
- "Experiment execution skill."
- "Policy/compliance document skill."

Not allowed in shared context:

- the target field value itself, such as scanned/native, JSON/prose, validate/repair, no-legal-advice/legal-advice, HF Jobs/local, or visual-evidence/data-scrape;
- direct synonyms that would let a human pick the gold using the shared context alone;
- unique phrases copied from one skill's title, heading, or example;
- target-specific procedure words when `workflow_procedure` is being tested.

Leakage checklist for every unit:

1. Does the shared context contain the target field term or a close synonym?
2. Does the shared context imply the target field through a unique phrase?
3. Could a human distinguish the siblings using the shared context alone? If yes, rewrite it or mark the unit `leaky_original_description`.
4. Is the shared context so vague that a human cannot tell what task family is being tested? If yes, mark the unit `too_vague`.
5. Does the prompt name the skill or copy a unique skill phrase? If yes, the unit fails prompt leakage control.

## Optional RQ1 Diagnostic: Isolated Corruption

Isolated corruption is optional diagnostic evidence, not the main RQ1 test.

Purpose:

> Test whether a retriever is actually sensitive to the examined skill-side field.

Condition:

- Use the same fixed prompt, skill pair/cluster, retriever, candidate budget, and metrics as the main RQ1 field test.
- Keep all non-target skill-side fields controlled and non-discriminative, just as in the main RQ1 test.
- Corrupt or swap only the `primary_distinguishing_field`.
- Ensure no other field accidentally exposes the correct selection signal.
- Do not use multi-field conflict corruption as RQ1 evidence. If several fields support one skill and one corrupted field supports another, that is an RQ2 robustness/conflict-resolution test.

Expected interpretation:

- If the ranking flips or degrades after isolated corruption, the retriever is using that field.
- If the ranking does not change, the field may be human-meaningful but not used by that retriever.
- This diagnostic does not prove that the field should dominate all other fields in real selection.

Example for `input_precondition`:

| Condition | Skill A | Skill B |
|---|---|---|
| Controlled base | Same shared PDF extraction description and same non-target fields. | Same shared PDF extraction description and same non-target fields. |
| Correct target field | `input_precondition`: scanned/image PDF. | `input_precondition`: native/selectable PDF. |
| Corrupted target field | `input_precondition`: native/selectable PDF. | `input_precondition`: scanned/image PDF. |

If the prompt asks for scanned PDF extraction and the ranking follows the swapped input field, that shows input/precondition is influential for that retriever. It should be reported as field sensitivity, not as a realistic robust-selection result.

## Explicit Case Patterns

| Primary field | Gold vs alternatives | Prompt shape | What it tests |
|---|---|---|---|
| `use_condition` | OpenAPI contract reviewer vs API integration planner vs webhook planner. | "Review this existing OpenAPI contract for schema/status/auth/client compatibility." | Review versus planning intent. |
| `input_precondition` | Native PDF extractor vs PDF OCR vs PDF Q&A. | "Extract selectable text, table cells, and metadata from a non-scanned PDF." | Input state matters: native PDF, not scanned PDF. |
| `output_artifact` | PDF table extractor vs PDF summarizer vs PDF converter. | "Return structured JSON/CSV tables with page anchors, not a prose summary." | Same input, different artifact. |
| `workflow_procedure` | Dataset validator vs dataset repairer vs anomaly explainer. | "Check schema/ranges/missingness and report validation failures before changing the file." | Procedure order matters. |
| `boundary_not_for` | Compliance triage vs legal advice writer vs policy summarizer. | "Flag compliance risks without giving legal advice." | Negative boundary excludes plausible sibling. |
| `dependency_resource` | HF Jobs runner vs local experiment runner vs model-card writer. | "Run this experiment on Hugging Face Jobs with GPU and persist artifacts." | Required platform/resource decides the skill. |
| `success_verification` | Browser visual QA vs browser scraper vs UI debugger. | "Verify rendered page layout and capture evidence of no overlapping text." | Success criterion differs from same-domain web tasks. |

## Few-Shot RQ1 Test Units

These are not final benchmark cases. They are templates for future cluster design.

### Input / Precondition

| Component | Example |
|---|---|
| Prompt requirement | "Extract tables from a scanned PDF image." |
| Shared neutral context | "PDF table extraction skill." |
| Gold target field | `input_precondition`: scanned or image-based PDF; OCR required before extraction. |
| Hard-negative target field | `input_precondition`: native PDF with selectable text; not for scanned PDFs requiring OCR. |
| What must be hidden in shared context | scanned, image-based, OCR, native, selectable text. |

### Output / Artifact

| Component | Example |
|---|---|
| Prompt requirement | "Extract PDF content into JSON table rows with page references." |
| Shared neutral context | "PDF information extraction skill." |
| Gold target field | `output_artifact`: JSON table rows with page or cell references. |
| Hard-negative target field | `output_artifact`: prose summary with citations. |
| What must be hidden in shared context | JSON, table rows, page anchors, prose summary. |

### Workflow / Procedure

| Component | Example |
|---|---|
| Prompt requirement | "Check a dataset for schema and range violations and report issues without modifying the file." |
| Shared neutral context | "Dataset quality task." |
| Gold target field | `workflow_procedure`: validate and report only. |
| Hard-negative target field | `workflow_procedure`: repair data and write corrected output. |
| What must be hidden in shared context | validate-only, report-only, repair, modify, corrected output. |

### Use Condition

| Component | Example |
|---|---|
| Prompt requirement | "Review an existing OpenAPI contract for schema, status-code, auth, and client-compatibility issues." |
| Shared neutral context | "API work skill." |
| Gold target field | `use_condition`: review existing API contracts. |
| Hard-negative target field | `use_condition`: plan a new API integration or webhook. |
| What must be hidden in shared context | review, existing contract, integration planning, webhook planning. |

### Boundary / Not-For

| Component | Example |
|---|---|
| Prompt requirement | Direct: "Summarize compliance risks without giving legal advice." Implicit authority: "Prepare an internal compliance-risk briefing for a reviewer who will pass legal questions to counsel." |
| Shared neutral context | "Policy/compliance document skill." |
| Gold target field | `boundary_not_for`: flags risks without legal advice. |
| Hard-negative target field | `boundary_not_for` or `use_condition`: drafts legal recommendations or advice. |
| What must be hidden in shared context | no legal advice, risk-only, legal recommendation, legal advice. |

Completed suite status, updated 2026-06-25:

- Suite folder: `skill_benchmark/rq1a_field_discriminability/boundary_not_for/`
- Generated by: `skill_benchmark/rq1a_field_discriminability/boundary_not_for/build_strict_units.py`
- Generated artifacts: 50 cluster folders, 150 prompt rows, 150 controlled sibling skill documents.
- Prompt variants: `direct`, `paraphrase`, and `implicit_authority`.
- Mechanical rubric: `skill_benchmark/rq1a_field_discriminability/boundary_not_for/rubric_summary.md`, 50/50 `accepted_strict`.
- Thesis-facing result: `skill_benchmark/outputs/rq1a_boundary_not_for_bm25_qwen_embedding_with_implicit.md`.
- Detailed implicit-authority interpretation: `skill_benchmark/rq1a_field_discriminability/boundary_not_for/implicit_authority_analysis.md`.
- Main exposed condition remains `shared_context_plus_field`, meaning shared non-target context plus exactly one `Boundary / Not For: ...` line.
- Interpretation rule: report `implicit_authority` separately from `combined`, because it shows boundary/not-for is much weaker when authority/scope is implied rather than explicitly stated.

### Dependency / Resource

| Component | Example |
|---|---|
| Prompt requirement | Direct: "Run this experiment on Hugging Face Jobs with GPU and persist artifacts." Contextual: "Run the compute-heavy review and save the produced files," with routing context stating that Hugging Face Jobs/Spaces GPU and Hub artifact upload are available. |
| Shared neutral context | "Experiment execution skill." |
| Gold target field | `dependency_resource`: Hugging Face Jobs and GPU execution. |
| Hard-negative target field | `dependency_resource`: local CUDA runtime or Modal GPU runtime. |
| What must be hidden in shared context | Hugging Face Jobs, GPU, local runtime, artifact upload. |

Version-compatibility example:

| Component | Example |
|---|---|
| Prompt requirement | Direct: "Use React 18 compatibility, including createRoot behavior." Contextual: task prompt asks for interface review, while routing context says `package.json` pins React 18 and the app uses `createRoot`. |
| Shared neutral context | "Interface review skill." |
| Gold target field | `dependency_resource`: React 18 compatibility and `createRoot`. |
| Hard-negative target field | `dependency_resource`: React 17 legacy `ReactDOM.render` or React 16 legacy lifecycle compatibility. |
| What must be hidden in shared context | React 18, React 17, React 16, createRoot, ReactDOM.render. |

Completed suite status, updated 2026-06-28:

- Suite folder: `skill_benchmark/rq1a_field_discriminability/dependency_resource/`
- Generated by: `skill_benchmark/rq1a_field_discriminability/build_remaining_strict_units.py`
- Generated artifacts: 50 cluster folders, 100 prompt rows, 150 controlled sibling skill documents.
- Prompt variants: `direct` and `contextual`.
- Mechanical rubric: `skill_benchmark/rq1a_field_discriminability/dependency_resource/rubric_summary.md`, 50/50 `accepted_strict`.
- Human review aid: `skill_benchmark/rq1a_field_discriminability/dependency_resource/cluster_review.md`.
- Thesis-facing result: `skill_benchmark/outputs/rq1a_dependency_resource_isolation_bm25_qwen_embedding.md`.
- Main exposed condition remains `shared_context_plus_field`, meaning shared non-target context plus exactly one `Dependency / Resource: ...` line.
- Interpretation rule: report dependency/resource as external capability compatibility. Direct rows name the required capability in the request. Contextual rows keep the request task-like and attach positive routing context for required capability; they must not select by negating sibling alternatives.
- Version subtype: 9 clusters now test package/framework/runtime version compatibility: React 18, Node.js 20, SQLAlchemy 2.0, and Next.js 13 against adjacent version alternatives.
- Public-skill grounding: dependency/resource in real public skills appears in several roles. Use hard capability requirements for routing tests: MCP/tool/server availability, provider/API identity, auth/credential boundary, runtime/platform, package/framework version, or required resource/config/artifact. Do not treat generic package-download or workflow commands (`npm install`, `pip install`, `npm ci`, build/test/lint steps) as strong dependency routing evidence unless the command itself identifies the required capability. Keep dependency-hygiene/concept text separate from this field unless the cluster is explicitly about dependency-management work.
- Example boundary: `npm install` and `npm ci` normally describe setup after selection; Chrome DevTools MCP, `GH_TOKEN`, `GOOGLE_APPLICATION_CREDENTIALS`, Firebase CLI, React 18, and Node.js 20+ describe capability compatibility that can affect selection before execution.
- Claim boundary: dependency/resource is strong only when the selector sees sufficient capability context. That context can be explicit in the user request, but may also come from routing context such as package manifests, configured MCP/tools, available credentials, runtime metadata, provider configuration, or project files.

### Success / Verification

| Component | Example |
|---|---|
| Prompt requirement | "Verify the rendered page layout and capture evidence that no text overlaps." |
| Shared neutral context | "Browser page evaluation skill." |
| Gold target field | `success_verification`: visual layout evidence and no-overlap check. |
| Hard-negative target field | `success_verification`: scrape returned values or inspect network/data only. |
| What must be hidden in shared context | rendered layout, no overlap, screenshot evidence, data scrape. |

Completed suite status, updated 2026-06-30:

- Suite folder: `skill_benchmark/rq1a_field_discriminability/success_verification/`
- Generated by: `skill_benchmark/rq1a_field_discriminability/build_remaining_strict_units.py`
- Generated artifacts: 50 cluster folders, 100 prompt rows, 150 controlled sibling skill documents.
- Prompt variants: `direct` and paraphrase-safe.
- Mechanical rubric: `skill_benchmark/rq1a_field_discriminability/success_verification/rubric_summary.md`, 50/50 `accepted_strict`.
- Human review aid: `skill_benchmark/rq1a_field_discriminability/success_verification/cluster_review.md`.
- Thesis-facing result: `skill_benchmark/outputs/rq1a_success_verification_bm25_qwen_embedding.md`.
- Machine summary: `skill_benchmark/outputs/rq1a_success_verification_bm25_qwen_embedding.json`.
- Refinement rule: success/verification must be a concrete acceptance gate, such as threshold checks, schema validation, evidence/source anchoring, unresolved finding state, rollback proof, reproducible failure, or runtime smoke check.
- Excluded weak forms: polished writing, broad presentation style, generic quality preference, persuasive wording, and other output-quality preferences that do not define a distinct completion criterion.
- Main exposed condition remains `shared_context_plus_field`, meaning shared non-target context plus exactly one `Success / Verification: ...` line.
- Interpretation rule: success/verification is a positive but comparatively weak and wording-sensitive field. Direct criteria can be very useful, but paraphrase rows degrade sharply; treat this field more like a late-stage acceptance/completion gate than a robust first-pass object discriminator.

Prompt subset `Combined` pools the direct and paraphrase-safe prompt rows.

| Retriever | Prompt subset | Hidden field top-1 | `shared_context_plus_field` top-1 | Lift | MRR + field |
|---|---:|---:|---:|---:|---:|
| BM25 | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| BM25 | Paraphrase | 33.3% | 48.0% | +14.7pp | 0.703 |
| BM25 | Combined | 33.3% | 74.0% | +40.7pp | 0.852 |
| Qwen embedding | Direct | 33.3% | 70.0% | +36.7pp | 0.833 |
| Qwen embedding | Paraphrase | 33.3% | 48.0% | +14.7pp | 0.707 |
| Qwen embedding | Combined | 33.3% | 59.0% | +25.7pp | 0.770 |

## Construction Plan

1. Derive candidate field labels from existing frozen-v0.4 artifacts:
   - controlled prompt JSON;
   - public-gold prompt `field_axes`;
   - `procedural_distinctness_report.json`;
   - `procedural_requirement_alignment_report.json`;
   - R2/R3 representation files.
2. Keep prompts with a clear primary field.
3. Mark ambiguous multi-field prompts as `multi_field`.
4. For each candidate, create or derive a controlled baseline skill-side description that keeps shared task context but masks the primary field.
5. Mark original descriptions that already contain the primary field as `leaky_original_description`.
6. Count coverage per primary field and domain.
7. Author a small new benchmark version only for missing fields/domains, rather than editing frozen-v0.4 inputs.
8. Run field ablations grouped by primary field.
9. Report field-specific deltas, hard-negative sibling errors, within-cluster top-1/MRR, and visible-token cost.

Cluster design status, 2026-07-18: input/precondition, output/artifact, boundary/not-for, use-condition, narrowed dependency/resource, success/verification, and workflow/procedure suites are authored, rubric-checked, run, and thesis-facing. Use condition is a strong but partly direct task-intent signal; its paraphrase drop, especially under BM25, should be interpreted as wording sensitivity and possible need for semantic intent reasoning. Dependency/resource is treated narrowly as required platform, tool, API, runtime, permission, version, or prior-artifact provenance. Its clean RQ1a design is an individual field-discrimination test: non-target fields are fixed or intentionally non-discriminative, and only dependency/resource differs across sibling skills. Dependency/resource uses direct plus contextual prompt variants, where contextual rows add positive routing context for the required capability and do not name or negate sibling alternatives. Version-compatibility dependency is now explicitly included as a harder subtype. The thesis-facing result is hidden dependency/resource versus exposed dependency/resource. A future interaction suite may test whether input/output can partially narrow the candidate set while dependency/resource resolves the remaining ambiguity, but that is not part of the current dependency/resource claim. Success/verification was refined into concrete acceptance-gate contrasts only and run on BM25/Qwen; it is positive but much weaker under paraphrase, so it should be framed as a conditional completion-gate signal. Workflow/procedure is also positive but heterogeneous: wrong-order, swapped-step, validate-before-modify, and missing-prerequisite cases are clearer than missing-branch, missing-verification, evidence-timing, or substitute-method cases. Examples/tests are complete as a negative-control/support suite, not a core operational field.

## Definition Of Done

- At least five usable prompts per primary field, preferably across more than one domain.
- Every RQ1 case has gold evidence and alternative rejection evidence.
- Every RQ1 case has an explicit, gold-stable prompt and a controlled skill-side baseline.
- Field-specific result table exists.
- No field is claimed generally useful unless it improves its labelled subset or explains a meaningful reduction in sibling errors.
- RQ2 strategy comparisons are kept separate from RQ1 field ranking.
