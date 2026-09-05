# Current Results Summary

## Canonical RQ1 Snapshot - 2026-09-04

Status: RQ1 is scientifically complete and thesis-integrated; remaining RQ1 work is final submission editing only, and the active research focus moves to RQ2.

RQ1 is one question with two current experiments and one negative control. The controlled study contains 350 clusters and 750 prompts; all seven fields have positive hidden-to-exposed Top-1 intervals under BM25 and Qwen. The public-original study contains 1,078 clean composition-family cases and 2,156 prompt rows; use condition and success/verification are stable under both retrievers, four other individual fields are BM25-only, and boundary/not-for has no stable positive strict Top-1 effect. Task-specification and execution/verification joint removals are stable under both. Examples/tests are a controlled negative control. Full values and claim limits are in `thesis_notes/current/Results Writing Packet - 2026-09-04.md`.

Unblinded prospective researcher confirmation is complete across all 350 controlled, 194 public-gold, and 402 public-removal units (`946/946` approved). Reconciled counts are maintained in `skill_benchmark/rq1_human_review/2026-09-04/STATUS.md`, with exact batch decisions in the stream receipts. Frozen gold was visible in the controlled and public-gold confirmation packets, and intact/removed documents were visible in the removal-fidelity packets; this is not blinded or independent annotation. The upstream 199-family and 574-transformation counts describe wider processing pools. The chronological entries below are retained as history; their old `current`, `final`, or `pending` labels do not override this snapshot.

## Chronological Archive

> **2026-09-04 RQ1 thesis-facing public-result supersession.** RQ1 is reported as one question with two complementary experiments: controlled field isolation and public original-document removal. The source-original Round-3 twin replaces the 2026-08-30 derivative field-card ablation as the thesis-facing public evidence because it compares each preserved public original with the exact same document after cited source lines for a field are removed from every candidate. Across BM25 and Qwen, use condition and success/verification have stable positive Full-minus-removed strict Hit@1 effects. Task specification and execution/verification also have stable joint-removal effects in both retrievers. Other individual fields are retriever-conditional; boundary/not-for has no stable positive strict Top-1 result. The older field-card null result remains historical sensitivity and must not be pooled with this result. Examples/tests remain a controlled negative control, not a public-original removal condition. Source: `thesis_notes/checkpoints/methods/RQ1 Public Original Round 3 Twin Result and Failure Analysis - 2026-09-04.md`, the two Round-3 joint-group result checkpoints, and `thesis_notes/current/Results Writing Packet - 2026-09-04.md`.

> **2026-08-30 historical field-card result.** The former thesis-facing RQ1b
> public-card result is not the historical 460-file recoverability audit. Its
> source-grounded discovery frame contains 1,099 preserved original public
> artifacts, from which strict source, near-neighbour, evidence, prompt, and
> model-assisted singleton gates form the final 46-composition / 99-family /
> 198-prompt field-card experiment. The 460-file audit remains a historical
> supporting extraction record only. In the final public-card matrix, no
> statistically reliable individual-field Top-1 or MRR effect is detected:
> every composition-bootstrap interval includes zero. RQ1a remains distinct:
> its 350 controlled clusters are author-reviewed, mechanically checked
> field-sufficiency evidence, not independent annotation. Source: `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Public Field-Type Ablation Protocol - 2026-08-28.md`,
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_v3_final_2026-08-30/`, and
> `skill_benchmark/rq1a_field_discriminability/human_review_2026-08-30/author_review_confirmation_receipt.json`.

> **2026-08-29 RQ1b v2.1 public joint-field result.** The separately labelled
> prospective joint-mask extension is complete: 87 strict routing families,
> 174 prompts, three coherent all-candidate field-set masks and 696 rows per
> selector. Local BM25 and the separately authorised Qwen
> `text-embedding-v4` twin both pass integrity audit. Qwen transmitted only
> 402 new mask-derived candidate cards in 41/41 no-retry calls (95,694
> provider tokens); 174 query texts and 134 unchanged `FULL` cards were local
> cache hits. Every primary group-level `FULL-MASK` Top-1 and MRR bootstrap
> interval crosses zero for both selectors. Qwen's task-specification native
> cosine margin nevertheless falls by `+0.0241`, 95% CI `[+0.0045,+0.0445]`:
> the gold card becomes less separated from its nearest wrong candidate, but
> this does not yield a confirmed change in Top-1 winner. This does not confirm a
> non-redundant joint field-set effect: it is bounded evidence that combined
> public field cards can retain overlapping operational routing support after
> a coherent slot set is withheld. Detailed checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_qwen_2026-08-29/QWEN_RESULT_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b v2 public field-card result.** The source-grounded
> field-type availability experiment is complete for its frozen strict subset:
> 87 routing families, 174 direct/paraphrase prompts and 1,392 `FULL` versus
> seven candidate-synchronous-mask rows per selector. Local BM25 and the
> separately authorised Qwen `text-embedding-v4` single-vector twin both pass
> their integrity audits. Qwen completed 126/126 no-retry calls for 1,246 raw
> card/prompt texts and cached all embeddings locally. Across all-eligible
> composition-bootstrap estimates, every Qwen field-level `FULL-MASK` Top-1
> and MRR interval crosses zero; BM25 is likewise mixed. Qwen's
> success/verification cosine-margin interval is positive (`+0.0044`, 95% CI
> `[+0.0005,+0.0084]`), but the small separation signal does not yield a
> stable Top-1/MRR effect and is not a universal ranking claim. This is evidence that
> public field-card slots can be redundant when operational facts are combined,
> not a universal field ranking or a refutation of RQ1a's controlled
> field-sufficiency result. Detailed checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_qwen_2026-08-29/QWEN_RESULT_CHECKPOINT_2026-08-29.md`.

> **2026-08-22 RQ2 status.** RQ1a is `REVIEWED / COMPLETE`. RQ2a is `CONFIRMATORY COMPLETE / USER-REVIEWED / THESIS-INTEGRATED`: 280 confirmatory clusters, 600 prompts, 22 conditions, and 13,200 aligned primary rows passed the frozen matrix, statistical, cache, cost, and failure-analysis gates. A20 is complete and RQ2a remains closed. RQ2b is `PARTIAL`: its strict-only v1.1 execution overlay has 381 scored prompts and no acceptable endpoint because base-v1 B0G remains blocked. The frozen V3 corpus now has three completed B1 retrievers: local BM25, Qwen `text-embedding-v4`, and native `pipizhao/SkillRouter-Embedding-0.6B`; each has 1,524 strict rows and post-run integrity/warm-replay verification. In the native SkillRouter B1 condition, combined strict Hit@1/MRR@10 is I1 `0.656/0.780`, I2 `0.669/0.787`, I3-flat `0.661/0.779`, and I3C `0.664/0.782`. These are descriptive B1 results pending user review, not a complete RQ2b conclusion: field-aware B1E-F, the matched SkillRouter and Qwen rerankers, cross-condition statistics, and thesis integration remain separate gates. B0F-A2's generic Qwen reranker proposal is still not independently reviewed, sealed, or externally approved. Older I1/I2/I3, M6, external SkillRouter, graph/tree, and downstream evidence remains explicitly historical or exploratory.

> **2026-08-25 RQ1b status.** Wave 001 is `FROZEN / NATURAL_ORIGINAL_ONLY / NOT EXECUTED`, not a retrieval result. From the separate 1,099-artifact public-original corpus, 62 source-disjoint clusters with 129 unique candidates passed source-hash, prompt-overlap, source-evidence, and two-reviewer model-assisted blinded acceptable-set gates. Both prompt variants had an agreed singleton first skill in every packet. All 62 are `ORIGINAL_ONLY`: the relevant public-skill facts occur jointly across title, workflow, examples, and resources, so no causal masked-field comparison is valid. This meets the 50-cluster natural-original feasibility threshold. It does not establish selector accuracy, human label validity, causal field effects, or an external-text result; no BM25, embedding, API, selector, or external transfer has run.

RQ2a confirmatory answer: operational facts strongly beat `shared-only`, but literal field headings do not provide a universal organisation gain. Under Qwen single-vector selection, `same-facts-fielded - same-facts-flat = -6.7pp`, 95% cluster-bootstrap CI `[-9.9pp,-3.6pp]`, raw `p=0.0002`. The frozen Qwen `uniform-top-two` field-aware selector improves over the same fielded single-vector input by `+6.6pp`, CI `[+2.1pp,+11.1pp]`, Holm-adjusted `p=0.0204`, but its Top-1 `0.823` is nearly identical to flat Qwen `0.824`. The mechanism claim is therefore conditional: useful facts matter, and explicit field-wise use can recover a pooled-embedding penalty, but headings alone and the current uniform aggregation are not universal winners.

Selector clarification: RQ2a Qwen is a bi-encoder embedding condition (`text-embedding-v4`, one reusable vector per complete candidate). RQ2a SkillRouter is **not** SkillRouter embedding; it is direct joint query-candidate cross-encoder scoring with `pipizhao/SkillRouter-Reranker-0.6B`. SkillRouter reaches Top-1 `0.955` on flat, `0.951` on fielded, and `0.946` on prose, but novel-pair inference costs about 11.10 seconds per prompt locally. No SkillRouter-native field-aware condition was run.

Detailed thesis-facing analysis: `thesis_notes/current/RQ2a Confirmatory Results and Analysis - 2026-08-02.md`. Frozen machine evidence remains at `skill_benchmark/outputs/rq2a_matched_content/analysis/confirmatory-complete-v1/analysis.json`, the confirmatory cost ledger, and the deterministic failure report.

Current presentation update, 2026-07-18: Chapter 6 now moves the RQ1 field-isolation logic and synthesis ahead of the broader representation/retrieval tables. It uses `shared_context_only` versus `shared_context_plus_field` consistently, groups fields into claim tiers, and labels examples/tests as a negative-control/support-documentation result rather than a core routing field.

Current framing note, 2026-06-21: interpret result rows by information layer first, then retrieval strategy. Existing labels map as follows: `R1` = I1 flat card, `full`/`RFULL` = I2 full artifact, `R2/R3` = I3 structured selection fields. Planned I4 relation and I5 hierarchy results are not yet run. Canonical framing: `thesis_notes/current/Information Layer Framework.md`.

Operational boundary note, 2026-06-21: full SkillRouter embedding/reranker matrices should run on Hugging Face Jobs or an equivalent hosted GPU environment, not on the local laptop. Local SkillRouter execution is only for tiny smoke tests. Qwen/DeepSeek conditions are provider API orchestration, and I3C extraction is Codex-subagent parsing with evidence validation. The canonical run-boundary record is `thesis_notes/current/Experiment Methodology Tracker.md`.

External benchmark validity note, 2026-06-23: the SkillRouter-Eval-Core track is useful portability evidence, but it is not the same difficulty regime as the local frozen-v0.4 controlled benchmark. Static audit artifacts now exist at `skill_benchmark/outputs/skill_corpus_richness_audit.md` and `skill_benchmark/outputs/skill_corpus_richness_audit.json`, with checkpoint `thesis_notes/checkpoints/skillrouter/External SkillRouter Corpus Richness Audit - 2026-06-23.md`.

Public-original source correction, 2026-06-23: public-gold final reporting should use the upstream public `SKILL.md` files stored as `skill_benchmark/skills/public_imported_background/<skill>/source/SKILL.original.md`. The normalized top-level public wrappers remain provenance/import artifacts. The shared local full-text loader and representation exporter now prefer public originals. Local deterministic rows and Qwen provider rows have been refreshed after this correction; SkillRouter local rows generated before this correction remain historical/caveated until rerun with the original public artifacts. Checkpoint: `thesis_notes/checkpoints/public_gold/Public Original Skill Source Correction - 2026-06-23.md`.

Public-style controlled correction, 2026-06-23: the 32 synthetic public-style controlled skills were regenerated to be messier public-document-style artifacts while preserving the intended use/input/output/procedure/dependency signals. Checkpoint: `thesis_notes/checkpoints/benchmark/Public Style Controlled Messy Regeneration - 2026-06-23.md`.

RQ1a condition rule, 2026-06-24: every field-isolation result should be read as `shared_context_only` versus `shared_context_plus_field`. The hidden condition contains shared non-target skill context with the tested field omitted. The exposed condition contains the same shared context plus exactly one target field line, such as `Input / Precondition: ...` or `Output Artifact: ...`. This hidden-versus-exposed contrast is the thesis-facing RQ1a causal claim. `field_only` and `full_skill_doc` are diagnostics only; `full_skill_doc` tests whether the target signal survives whole-document noise and added selector-visible cost.

RQ1 extension checkpoint, 2026-08-25: the completed RQ1a suites remain controlled field-sufficiency evidence, and the 460-file public-original audit remains supporting field-recoverability context only. The new RQ1b naturalistic replication has frozen 62 source-disjoint natural-original clusters from the separate 1,099-artifact local corpus. Their source and prompt integrity, model-assisted blinded acceptable sets, and exact residual maps pass local curation gates; all are `ORIGINAL_ONLY`, so the wave supports a natural-original selection study but not a causal original-versus-masked field claim. The achieved 50-plus feasibility threshold does not permit a universal field ranking, because boundary/not-for has four clusters and success/verification two. No selector or external text transfer has occurred. RQ1c remains deferred. Protocol: `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Naturalistic Public Skill Replication Protocol - 2026-08-24.md`.

RQ1 status update, 2026-07-01: the seven planned RQ1a field-isolation suites are complete and should be interpreted as the current answer to the individual-field part of RQ1. All seven fields improve over the intentionally tied hidden-field baseline, but not equally. Stronger first-pass routing signals are input/precondition, use condition, output/artifact under semantic retrieval, and dependency/resource when framed as external capability compatibility. Boundary/not-for is useful but weaker when the request only implies the authority or scope boundary. Success/verification and workflow/procedure are positive but weaker first-pass retrieval signals because their alternatives are semantically close and often need reasoning over acceptance gates or operation order.

RQ1b public-field realism audit, 2026-07-01: a focused audit over the 460 imported upstream public `source/SKILL.original.md` files now checks whether the seven RQ1 field types are explicit, implicit, missing, or noisy/mixed. This is external-validity support for RQ1a, not a routing accuracy run. Main artifacts:

- Script: `skill_benchmark/scripts/audit_rq1_public_field_realism.py`
- Markdown summary: `skill_benchmark/outputs/rq1_public_field_realism_audit.md`
- Machine summary: `skill_benchmark/outputs/rq1_public_field_realism_audit.json`
- Row cache: `skill_benchmark/outputs/rq1_public_field_realism_audit_rows.jsonl`

Headline public-original field recoverability:

| RQ1 field | Explicit | Present | Noisy / mixed | Interpretation |
|---|---:|---:|---:|---|
| Use condition | 460/460 (100.0%) | 460/460 (100.0%) | 0/460 (0.0%) | Public skills almost always carry a routing description or use condition. |
| Input/precondition | 103/460 (22.4%) | 416/460 (90.4%) | 0/460 (0.0%) | Usually recoverable, often embedded in prose rather than a clean heading. |
| Output/artifact | 208/460 (45.2%) | 422/460 (91.7%) | 0/460 (0.0%) | Common and often explicit enough to support output-oriented routing. |
| Workflow/procedure | 330/460 (71.7%) | 424/460 (92.2%) | 0/460 (0.0%) | Common in public skills, though not always in a neat single field. |
| Boundary/not-for | 190/460 (41.3%) | 357/460 (77.6%) | 20/460 (4.3%) | Present often enough to matter, but less universal than positive task fields. |
| Dependency/resource | 364/460 (79.1%) | 438/460 (95.2%) | 86/460 (18.7%) | Very common; normalize hard capability compatibility away from setup text. |
| Success/verification | 135/460 (29.3%) | 408/460 (88.7%) | 362/460 (78.7%) | Common but noisy; concrete acceptance gates need separation from generic quality language. |

Interpretation: RQ1a supplies the controlled causal test; RQ1b shows that the same field types are realistically recoverable from public skill artifacts, but dependency/resource and success/verification especially require normalization before they can be trusted as routing fields.

RQ1a input/precondition result, 2026-06-24: the first clean field-isolation suite is complete and run. It contains 50 near-neighbour input/precondition clusters and 100 prompts, with direct and paraphrase-safe variants for each cluster. In each cluster, siblings share the broad task, output, workflow, boundary, dependency, and success framing; only the input/precondition sentence is intended to distinguish the gold. The hidden-field baseline is intentionally tied across three siblings, so top-1 is reported with tie-aware scoring.

Main artifacts:

- Suite: `skill_benchmark/rq1a_field_discriminability/input_precondition/`
- Runner: `skill_benchmark/scripts/run_rq1a_field_ablation.py`
- BM25 + Qwen result: `skill_benchmark/outputs/rq1a_input_precondition_bm25_qwen_embedding.md`
- Machine summary: `skill_benchmark/outputs/rq1a_input_precondition_bm25_qwen_embedding.json`

Prompt subset `Combined` pools the direct and paraphrase-safe prompt rows.

| Retriever | Prompt subset | Hidden field top-1 | + input/precondition top-1 | Lift | MRR + field |
|---|---:|---:|---:|---:|---:|
| BM25 | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| BM25 | Paraphrase | 33.3% | 91.0% | +57.7pp | 0.953 |
| BM25 | Combined | 33.3% | 95.5% | +62.2pp | 0.977 |
| Qwen embedding | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| Qwen embedding | Paraphrase | 33.3% | 94.0% | +60.7pp | 0.970 |
| Qwen embedding | Combined | 33.3% | 97.0% | +63.7pp | 0.985 |

Interpretation: input/precondition is now supported as a strong RQ1a routing signal in controlled near-neighbour clusters. The paraphrase-safe rows remain high, reducing the risk that the result is only exact keyword matching. This is one completed field-specific RQ1a result, not an all-field RQ1 conclusion and not an RQ2 strategy comparison.

RQ1a output/artifact result, 2026-06-24: the second clean field-isolation suite is complete and run. It contains 50 near-neighbour output/artifact clusters and 100 prompts, with direct and paraphrase-safe variants for each cluster. In each cluster, siblings share the broad task, input/precondition, workflow, boundary, dependency, and success framing; only the output/artifact sentence is intended to distinguish the gold.

Main artifacts:

- Suite: `skill_benchmark/rq1a_field_discriminability/output_artifact/`
- Runner: `skill_benchmark/scripts/run_rq1a_field_ablation.py`
- BM25 + Qwen result: `skill_benchmark/outputs/rq1a_output_artifact_bm25_qwen_embedding.md`
- Machine summary: `skill_benchmark/outputs/rq1a_output_artifact_bm25_qwen_embedding.json`

Prompt subset `Combined` pools the direct and paraphrase-safe prompt rows.

| Retriever | Prompt subset | Hidden field top-1 | + output/artifact top-1 | Lift | MRR + field |
|---|---:|---:|---:|---:|---:|
| BM25 | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| BM25 | Paraphrase | 33.3% | 53.3% | +20.0pp | 0.723 |
| BM25 | Combined | 33.3% | 76.7% | +43.3pp | 0.861 |
| Qwen embedding | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| Qwen embedding | Paraphrase | 33.3% | 92.0% | +58.7pp | 0.957 |
| Qwen embedding | Combined | 33.3% | 96.0% | +62.7pp | 0.978 |

Interpretation: output/artifact is supported as a strong RQ1a routing signal, especially with semantic embedding retrieval. The direct prompts are easy for both retrievers, while paraphrase-safe prompts show a large gap between BM25 and Qwen embedding. This suggests that output/artifact information is useful, but lexical retrieval is much more sensitive to wording when the requested deliverable is paraphrased.

RQ1a boundary/not-for result, 2026-06-25: the third clean field-isolation suite is complete and run. It contains 50 near-neighbour boundary/not-for clusters and 150 prompts. Each cluster has direct, paraphrase-safe, and `implicit_authority` prompts. In each cluster, siblings share the broad task, input/precondition, output/artifact, workflow, dependency, and success framing; only the boundary/not-for sentence is intended to distinguish the gold. The implicit-authority prompt variant was added to test realistic scope/authority requests where the user asks for an internal review note, triage packet, or evidence summary without explicitly saying the excluded action.

Main artifacts:

- Suite: `skill_benchmark/rq1a_field_discriminability/boundary_not_for/`
- Implicit-authority analysis: `skill_benchmark/rq1a_field_discriminability/boundary_not_for/implicit_authority_analysis.md`
- Runner: `skill_benchmark/scripts/run_rq1a_field_ablation.py`
- BM25 + Qwen result: `skill_benchmark/outputs/rq1a_boundary_not_for_bm25_qwen_embedding_with_implicit.md`
- Machine summary: `skill_benchmark/outputs/rq1a_boundary_not_for_bm25_qwen_embedding_with_implicit.json`

Prompt subset `Combined` pools direct, paraphrase-safe, and implicit-authority prompt rows. For interpretation, keep the implicit-authority row separate because it is materially weaker than explicit boundary wording.

| Retriever | Prompt subset | Hidden field top-1 | + boundary/not-for top-1 | Lift | MRR + field |
|---|---:|---:|---:|---:|---:|
| BM25 | Direct | 33.3% | 98.0% | +64.7pp | 0.990 |
| BM25 | Paraphrase | 33.3% | 90.0% | +56.7pp | 0.943 |
| BM25 | Implicit authority | 33.3% | 62.0% | +28.7pp | 0.800 |
| BM25 | Combined | 33.3% | 83.3% | +50.0pp | 0.911 |
| Qwen embedding | Direct | 33.3% | 84.0% | +50.7pp | 0.917 |
| Qwen embedding | Paraphrase | 33.3% | 82.0% | +48.7pp | 0.907 |
| Qwen embedding | Implicit authority | 33.3% | 58.0% | +24.7pp | 0.777 |
| Qwen embedding | Combined | 33.3% | 74.7% | +41.3pp | 0.867 |

Interpretation: boundary/not-for is supported as useful, but conditionally. It is strong when the prompt explicitly states the exclusion or guardrail and remains positive under paraphrase. Under implicit authority, the field still improves above the tied hidden baseline, but by much less. This means boundary/not-for should be framed as a scope, authority, compatibility, or guardrail signal rather than as a simple positive matching field like input/precondition or output/artifact.

RQ1a use-condition result, 2026-06-27: the fourth clean field-isolation suite is complete and run. It contains 50 near-neighbour use-condition clusters and 100 prompts, with direct and paraphrase-safe variants for each cluster. In each cluster, siblings share the broad context, input/precondition, output/artifact, workflow, boundary, dependency, and success framing; only the use-condition sentence is intended to distinguish the gold. This field is close to a direct task-intent hint, so direct prompt rows are expected to be easy; the more useful robustness check is the paraphrase row.

Main artifacts:

- Suite: `skill_benchmark/rq1a_field_discriminability/use_condition/`
- Runner: `skill_benchmark/scripts/run_rq1a_field_ablation.py`
- BM25 + Qwen result: `skill_benchmark/outputs/rq1a_use_condition_bm25_qwen_embedding.md`
- Machine summary: `skill_benchmark/outputs/rq1a_use_condition_bm25_qwen_embedding.json`

Prompt subset `Combined` pools the direct and paraphrase-safe prompt rows.

| Retriever | Prompt subset | Hidden field top-1 | + use condition top-1 | Lift | MRR + field |
|---|---:|---:|---:|---:|---:|
| BM25 | Direct | 33.3% | 98.0% | +64.7pp | 0.987 |
| BM25 | Paraphrase | 33.3% | 71.0% | +37.7pp | 0.820 |
| BM25 | Combined | 33.3% | 84.5% | +51.2pp | 0.903 |
| Qwen embedding | Direct | 33.3% | 98.0% | +64.7pp | 0.990 |
| Qwen embedding | Paraphrase | 33.3% | 84.0% | +50.7pp | 0.920 |
| Qwen embedding | Combined | 33.3% | 91.0% | +57.7pp | 0.955 |

Interpretation: use condition is supported as a strong RQ1a routing signal, especially as a direct task-trigger cue. It is not perfectly robust under paraphrase, particularly for BM25, which suggests the field can behave like a lexical intent hint unless a semantic retriever is used. Qwen embedding retains stronger paraphrase performance than BM25.

RQ1a dependency/resource result, updated 2026-06-28: the dependency/resource suite has been narrowed and rerun to avoid conflating dependency with input availability. Dependency/resource is defined here as a required external capability, platform, tool, API, runtime, permission, version, or prior-artifact provenance. Headline clusters now use true near-neighbour capability contrasts such as PostgreSQL versus MySQL versus BigQuery SQL, GitHub Actions versus GitLab CI versus CircleCI, Chrome DevTools/Playwright-style browser inspection versus Selenium versus Cypress, AWS Cost Explorer versus GCP Billing versus Azure Cost Management, Hugging Face Jobs or Spaces GPU runtime versus local CUDA versus Modal GPU runtime, and version-specific compatibility such as React 18 versus React 17/16, Node.js 20 versus 18/16, SQLAlchemy 2.0 versus 1.4/1.3, and Next.js 13 versus 12/14. The suite records non-selector-visible subtypes (`platform`, `tool`, `runtime`, `version`) for later analysis; the subtype label is not shown to retrievers. The second prompt variant is now `contextual`, not paraphrase: the user request stays task-like while positive routing context exposes the available or required capability. This matches public-skill patterns where dependency is often carried by MCP tools, platform auth, runtimes, package versions, APIs, package metadata, or resource files rather than by a user saying "not X".

Main artifacts:

- Suite: `skill_benchmark/rq1a_field_discriminability/dependency_resource/`
- Generator: `skill_benchmark/rq1a_field_discriminability/build_remaining_strict_units.py`
- Cluster review: `skill_benchmark/rq1a_field_discriminability/dependency_resource/cluster_review.md`
- Runner: `skill_benchmark/scripts/run_rq1a_field_ablation.py`
- BM25 + Qwen isolation result: `skill_benchmark/outputs/rq1a_dependency_resource_isolation_bm25_qwen_embedding.md`
- Machine summary: `skill_benchmark/outputs/rq1a_dependency_resource_isolation_bm25_qwen_embedding.json`
- Subtype breakdown: `skill_benchmark/outputs/rq1a_dependency_resource_subtype_breakdown.md`
- Public-skill dependency audit: `skill_benchmark/outputs/public_dependency_signal_analysis.md`

This suite is reported as an individual field-discrimination test. All sibling skills share the same broad context and the same non-target operational fields; only the `Dependency / Resource` value differs. The thesis-facing contrast is therefore the canonical RQ1a comparison: `shared_context_only` versus `shared_context_plus_field`. Earlier no-I/O and identical-I/O runner variants are treated as exploratory diagnostics, not as separate thesis claims. For contextual rows, the runner embeds/searches the prompt plus its `routing_context`; direct rows use the prompt alone.

Public-skill grounding check, updated 2026-07-01: the focused RQ1b public-original audit over 460 imported public `SKILL.original.md` files shows that dependency/resource evidence is common but mixed. It detects dependency/resource evidence in 438 skills (95.2%). Within the kind breakdown, 332 skills contain hard capability evidence, 82 mix hard capability evidence with setup text, 4 contain only setup/execution style evidence, and 42 have no hard/setup kind, including 22 skills where the field is missing. The common public pattern is not "raw package download text"; it is capability compatibility: MCP/tool/server availability, provider/API identity, auth or credential boundary, runtime/platform requirement, version/stack constraint, or required resource/config/artifact. Generic `npm install`, `pip install`, or `npm ci` usually belongs to execution workflow after a skill is selected, not to first-pass routing unless it implies a named required capability.

Concrete examples for thesis wording: a line such as "Install dependencies: `npm install`" or a CI step such as `npm ci` is weak routing evidence by itself because many unrelated skills can contain the same setup instruction. A line such as "Requires the Chrome DevTools MCP server", `GH_TOKEN`, `GOOGLE_APPLICATION_CREDENTIALS`, Firebase CLI, React 18, or Node.js 20+ is stronger routing evidence because it constrains whether the skill is compatible with the available tool, provider, credential, runtime, version, or platform. The result should therefore be phrased conditionally: dependency/resource has a vital impact in differentiating semantically close skills when sufficient capability context is visible to the selector. That context may come from the user prompt, but in realistic routing it may need to be supplied from package manifests, configured tools, available credentials, project metadata, or runtime state.

| Retriever | Prompt subset | Hidden dependency top-1 | + dependency/resource top-1 | Lift | MRR + field |
|---|---:|---:|---:|---:|---:|
| BM25 | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| BM25 | Contextual | 33.3% | 100.0% | +66.7pp | 1.000 |
| BM25 | Combined | 33.3% | 100.0% | +66.7pp | 1.000 |
| Qwen embedding | Direct | 33.3% | 98.0% | +64.7pp | 0.990 |
| Qwen embedding | Contextual | 33.3% | 100.0% | +66.7pp | 1.000 |
| Qwen embedding | Combined | 33.3% | 99.0% | +65.7pp | 0.995 |

Subtype check after adding version cases: the suite now has 9 version clusters, 24 platform clusters, 10 tool clusters, and 7 runtime clusters. Under `shared_context_plus_field`, version rows are 100.0% for BM25 direct/contextual and 100.0% for Qwen contextual, but Qwen direct version rows are 88.9% because one React 18 accessibility prompt ranked the React 17 sibling first by a small margin. This is useful rather than fatal: version-only dependency is a harder semantic subtype, and routing context such as `package.json`, `.nvmrc`, or dependency metadata clarifies the version constraint.

Interpretation: narrowed dependency/resource is supported as an individual routing-discrimination signal under controlled shared context. The hidden-field baseline is the expected 1-of-3 tie because the sibling skills are intentionally indistinguishable without the target field. Exposing dependency/resource reaches 100% tie-aware top-1/MRR for BM25 and 99.0% combined top-1 for Qwen embedding after adding harder version-only cases. This supports dependency/resource as a capability-compatibility signal when the selector-visible skill representation includes the required external capability and the request/routing context provides the corresponding capability requirement. It does not mean every real prompt will naturally mention the dependency; the realistic claim is that dependency/resource can help when capability context is available through user wording, environment state, package metadata, MCP/tool availability, platform auth, or other routing context.

Result analysis / claim boundary: the dependency/resource result should be read as strong evidence for **capability compatibility**, not for raw dependency/setup text. The controlled suite shows that when the only discriminating skill-side field is a required platform, tool, API, runtime, permission, version, or resource, both lexical and semantic retrievers can use that field to break a near-neighbour tie. The public-skill audit explains why this field must be normalized before routing: real skills often mix hard requirements such as Chrome DevTools MCP, Firebase CLI, GitHub auth, Node/React versions, or package manifests with low-value setup text such as `npm install`, `pip install`, `npm ci`, build/test/lint commands, and general dependency hygiene advice. Generic setup text is therefore not treated as a positive RQ1 dependency signal unless it names a specific required capability or compatibility conflict. This also explains the direct/contextual split: direct rows model a user who names the capability; contextual rows model a router that obtains the cue from project files, configured tools, credentials, package metadata, or runtime state.

Deferred interaction test: a future suite may test whether dependency/resource adds value after input/output already narrow the candidate set but cannot fully resolve sibling ambiguity. That would require clusters where input/output differ enough to eliminate some candidates, while dependency/resource resolves the remaining near-neighbour choice. The current dependency/resource suite does not claim that richer interaction result.

RQ1a success/verification result, 2026-06-30: the success/verification field suite has now been refined and run. It contains 50 near-neighbour clusters and 100 direct/paraphrase-safe prompts where every sibling shares broad task context and all non-target operational fields; only the success/verification acceptance gate differs. Valid target values are concrete completion gates such as schema validation, threshold checks, evidence/source anchoring, unresolved finding state, rollback proof, reproducible failure, or runtime smoke checks. Weak alternatives such as polished writing, persuasive wording, broad style, generic presentation quality, or "better answer" preferences were removed. Main artifacts: `skill_benchmark/rq1a_field_discriminability/success_verification/`, `skill_benchmark/rq1a_field_discriminability/success_verification/cluster_review.md`, `skill_benchmark/rq1a_field_discriminability/success_verification/rubric_summary.md`, `skill_benchmark/outputs/rq1a_success_verification_bm25_qwen_embedding.md`, and `skill_benchmark/outputs/rq1a_success_verification_bm25_qwen_embedding.json`.

| Retriever | Prompt subset | Hidden field top-1 | + success/verification top-1 | Lift | MRR + field |
|---|---:|---:|---:|---:|---:|
| BM25 | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| BM25 | Paraphrase | 33.3% | 48.0% | +14.7pp | 0.703 |
| BM25 | Combined | 33.3% | 74.0% | +40.7pp | 0.852 |
| Qwen embedding | Direct | 33.3% | 70.0% | +36.7pp | 0.833 |
| Qwen embedding | Paraphrase | 33.3% | 48.0% | +14.7pp | 0.707 |
| Qwen embedding | Combined | 33.3% | 59.0% | +25.7pp | 0.770 |

Interpretation: success/verification is supported as a positive but comparatively weak RQ1a routing signal. It is strong for direct lexical criteria under BM25, but it degrades sharply under paraphrase and is weaker under Qwen embedding than the more object-like fields. This suggests success/verification often behaves as a late-stage completion or acceptance gate rather than a robust first-pass semantic discriminator. The thesis claim should be conditional: concrete success criteria can help distinguish near-neighbour skills when the request names the criterion clearly, but this field is more wording-sensitive and more semantically entangled with neighbouring criteria than input/precondition, output/artifact, use condition, or dependency/resource.

## 2026-06-23 Refreshed Local Matrix Rerun

This rerun uses the corrected public-original source policy and the messier public-style controlled skills. It refreshes local deterministic rows, Qwen embedding/rerank rows, Qwen local-schema diagnostics, and Qwen-only fixed M6-v2 task-heavy diagnostics. SkillRouter/HF local rows were **not** rerun in this pass and should remain caveated.

Main artifacts:

- Compact refreshed summary: `skill_benchmark/outputs/frozen_v0_4_refreshed_matrix_summary_2026_06_23.md`
- Checkpoint: `thesis_notes/checkpoints/benchmark/Local Matrix Rerun After Public Source Correction - 2026-06-23.md`
- Consolidated matrix: `skill_benchmark/outputs/frozen_v0_4_information_layer_matrix.md/json`
- Crossed lexical matrix: `skill_benchmark/outputs/frozen_v0_4_crossed_lexical_matrix.md/json`
- Qwen provider rows: `skill_benchmark/outputs/frozen_v0_4_{controlled,public_gold}_qwen_{r1,r2,full}_{embedding,qwen_rerank_top20,local_schema_top20}.json`
- Qwen-only fixed M6-v2 rows: `skill_benchmark/outputs/frozen_v0_4_m6v2_fixed_task_heavy.md/json`

Headline top-1 results:

| Stratum | Method | I1 | I3H/R2 | I2/full |
|---|---|---:|---:|---:|
| Controlled | BM25 | 55.1% | 58.0% | 66.5% |
| Controlled | TF-IDF | 52.6% | 59.6% | 69.4% |
| Controlled | Qwen embedding | 33.9% | 40.4% | 42.4% |
| Controlled | Qwen + Qwen rerank | 51.0% | 58.4% | 62.9% |
| Controlled | M6-v2 fixed task-heavy | 35.5% | 38.4% | 40.8% |
| Public-gold | BM25 | 55.6% | 54.9% | 59.0% |
| Public-gold | TF-IDF | 56.9% | 50.7% | 48.6% |
| Public-gold | Qwen embedding | 57.6% | 61.8% | 70.8% |
| Public-gold | Qwen + Qwen rerank | 73.6% | 70.8% | 72.9% |
| Public-gold | M6-v2 fixed task-heavy | 54.9% | 56.9% | 59.7% |

Current interpretation:

- Controlled Qwen rows still show I3H/R2 improves over I1, both embedding-only and embedding + learned rerank.
- Full text is now a stronger comparator than earlier wrapper-based runs, especially on controlled lexical and Qwen full-document conditions.
- Public-gold remains mixed: public names/provider cues make I1 strong under some rerankers, while I2/full is strongest for Qwen embedding and close to strongest for Qwen rerank.
- M6-v2 fixed task-heavy is useful as an interpretable field-use diagnostic, but it does not beat learned Qwen reranking and should not be sold as the final selector.
- The safe claim is now narrower: structured fields help over flat cards in several controlled and Qwen settings, but full documents are not a weak baseline; the thesis argument must include token/cost, fixed extraction/indexing cost, candidate recall, and corpus-difficulty caveats.

## 2026-06-23 SkillRouter-Eval-Core Corpus and Prompt Audit

This audit checks whether SkillRouter-Eval-Core skill bodies and prompts are structurally comparable to the local controlled benchmark. It is a static markdown/prompt audit, not a retrieval run.

Key skill-body findings:

| Corpus | Rows | Median tokens | H1 | Rich schema | Procedural |
|---|---:|---:|---:|---:|---:|
| SkillRouter all | 79141 | 726 | 95.0% | 27.6% | 78.8% |
| SkillRouter scored gold names | 533 | 885 | 98.5% | 27.4% | 79.2% |
| Local controlled gold+alts | 240 | 260.5 | 100.0% | 72.9% | 73.3% |

Frequent SkillRouter H2 headings include `overview` (13568), `best practices` (10567), `when to use` (10041), `when to use this skill` (9642), `examples` (6862), `workflow` (6442), `quick start` (6382), `resources` (6241), and `purpose` (5994). In the scored gold-name subset, common headings include `overview`, `best practices`, `quick start`, `dependencies`, `when to use this skill`, and `workflow`.

Prompt-side findings:

| Prompt set | Rows | Mean tokens | Median tokens | >=200 tokens | File/path refs | Explicit input | Explicit output | Numbered steps |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SkillRouter scored tasks | 75 | 198.4 | 169 | 41.3% | 97.3% | 92.0% | 85.3% | 40.0% |
| Local controlled prompts | 245 | 36.8 | 25 | 0.4% | 28.2% | 18.4% | 26.9% | 0.0% |
| Local public-gold prompts | 144 | 30.1 | 29 | 0.0% | 18.1% | 21.5% | 47.2% | 0.0% |

Interpretation:

- SkillRouter-Eval-Core is not uniformly "rich I3" data: only about 27% of all or scored gold-name skill bodies satisfy the strict rich-schema definition.
- It is still highly markdown-normalized: most scored gold skills have H1 titles and procedural sections, so full-body retrieval is often searching clean documentation sections rather than chaotic raw text.
- SkillRouter prompts are substantially more informative than local controlled prompts. A median of 169 rough tokens is paragraph-sized task text, often with file names, input explanations, output requirements, and numbered steps.
- Therefore, external SkillRouter-Eval-Core results should be reported as portability evidence and a corpus-difference caveat, not merged into the local controlled/public-gold result tables as if the difficulty profile were identical.

## 2026-06-18 I3M Paid-Model Feasibility Attempt

Local full-library I3M extraction is complete for `benchmark-v0.4-2026-06-16`, but it is a DeepSeek/API-derived feasibility attempt rather than the thesis-facing extraction route. Do not use I3M as the headline condition unless the cost/budget decision changes.

Artifacts:

- Selector-facing I3M representation: `skill_benchmark/representations/I3M_model_parsed.jsonl`
- Full model-parse report: `skill_benchmark/outputs/i3m/local_i3m_full_model_parse_report.md`
- Full model-parse QA rows: `skill_benchmark/outputs/i3m/local_i3m_full_model_parse.jsonl`
- Checkpoint: `thesis_notes/checkpoints/methods/I3M Local Full-Library Parse Checkpoint - 2026-06-18.md`

Method condition, paid provider:

- Primary model: DeepSeek `deepseek-v4-flash`
- Fallback model: `deepseek-chat`
- Schema: `I3_MODEL_EXTRACTION_V1`
- Input cap: 22,000 characters; 0 truncated rows

Full local parse summary:

| Metric | Value |
|---|---:|
| Skills parsed | 2433 |
| Valid rows | 2333 (95.9%) |
| Parse-failed rows | 0 |
| Fallback-model rows | 1398 |
| Extracted items | 54,989 |
| Evidence exact match | 98.7% |
| Evidence case-insensitive / whitespace-insensitive match | 99.7% |

Field coverage:

| Field | Skills with field | Items |
|---|---:|---:|
| `use_conditions` | 2433 | 9198 |
| `input_preconditions` | 2425 | 10141 |
| `output_artifacts` | 2080 | 2499 |
| `workflow_steps` | 2007 | 9830 |
| `constraints_boundaries` | 2433 | 12844 |
| `dependencies_resources` | 2060 | 9455 |
| `success_criteria` | 604 | 1022 |

Interpretation:

- I3M shows that the proposed I3 information types are broadly recoverable from the local skill library with a paid model parser.
- Because this path depends on DeepSeek/API budget, it is now treated as a pass/feasibility attempt and supporting evidence, not the main thesis condition.
- The high fallback count is an operational caveat: model-parsed information layers need robust JSON/failure handling.
- The practical thesis-facing route is I3C. Local frozen-v0.4 I3C has not yet been produced, so local I3C retrieval reruns cannot be claimed yet.

## 2026-06-16 Test-Case Expansion Snapshot

The benchmark was expanded toward the requested ~400-prompt condition while keeping controlled, public-like, public-gold, and low-information strata separate. Current prompt counts are 245 controlled, 144 public-gold, and 12 low-information stress prompts, for 401 total broad prompts. The full library remains 2433 skills: 1800 generated background-scale skills, 460 imported public skills, and 32 public-style controlled skills.

Validation rerun: controlled Step 1 PASS (245 prompts), Step 2 procedural distinctness PASS (245/245 prompts; 830/830 pairs), Step 2 prompt-specific alignment 238/245 prompts with acceptable top-1 241/245, Step 3 semantic confusability 243/245, and leakage PASS with 0 critical / 0 high. Public-gold Step 1 PASS (144 prompts), Step 2 procedural distinctness PASS (144/144 prompts; 575/575 pairs), Step 2 prompt-specific alignment 131/144 prompts with acceptable top-1 138/144, Step 3 semantic confusability 144/144, and leakage PASS with 0 critical / 0 high.

Scale sanity: R1 flat metadata is now roughly 332,992 tokens, already above a 200k context budget by the crude chars/4 estimate. Controlled non-core competition remains active: flat semantic cards place a non-core skill top-1 for 56/245 prompts and a best non-core above gold for 88/245 prompts; structured procedural competition reduces this to 14/245 prompts.

New checkpoint: `thesis_notes/checkpoints/benchmark_validation/Test Case Expansion Toward 400 - 2026-06-16.md`. Background scale report: `skill_benchmark/outputs/background_scale_validation_2026_06_16.md`.

**Supersession note.** The 2026-06-16 snapshot above, plus the 2026-06-17 SkillRouter retry, is the active benchmark state. Older sections below are retained for history and may still mention previous 201-controlled, 120-public-gold, or 82-public-gold conditions unless explicitly labelled as refreshed. For the compact current source of truth, use `thesis_notes/current/Active Benchmark Snapshot.md`.

## 2026-06-18 M6-v2 Semantic Field-Matching Checkpoint

M6-v2 has now been implemented as a no-rewrite semantic field-aware reranker. It embeds the raw request with Qwen `text-embedding-v4`, compares it against existing selector-visible skill fields, and reranks a fixed top-20 candidate set. It does not invent workflow steps or rewrite underspecified requests into structured requirements.

Current output reports:

- `skill_benchmark/outputs/frozen_v0_4_qwen_m6v2_comparison.md`
- `skill_benchmark/outputs/frozen_v0_4_skillrouter_m6v2_comparison.md`

Qwen first-stage summary:

| Stratum | Representation | Best M6-v2 field set | M6-v2 Top-1 | Embedding-only Top-1 | Qwen-rerank Top-1 |
|---|---|---|---:|---:|---:|
| Controlled | R1 | task | 35.1% | 34.3% | 51.4% |
| Controlled | R2 | task | 41.6% | 40.0% | 58.0% |
| Controlled | Full | task | 43.3% | 44.1% | 58.8% |
| Public-gold | R1 | task | 59.0% | 57.6% | 74.3% |
| Public-gold | R2 | task | 62.5% | 63.2% | 72.9% |
| Public-gold | Full | task | 39.6% | 36.1% | 65.3% |

SkillRouter first-stage focused task-field summary:

| Stratum | Representation | M6-v2 task Top-1 | SkillRouter embedding Top-1 | SkillRouter rerank Top-1 |
|---|---|---:|---:|---:|
| Controlled | R1 | 60.4% | 62.9% | 65.7% |
| Controlled | R2 | 62.9% | 64.5% | 71.0% |
| Controlled | Full | 59.6% | 59.2% | 71.8% |
| Public-gold | R1 | 69.4% | 68.8% | 70.8% |
| Public-gold | R2 | 72.9% | 75.0% | 71.5% |
| Public-gold | Full | 72.2% | 75.0% | 70.1% |

Interpretation:

- M6-v2 is an interpretable semantic field-use diagnostic, not yet a learned reranker replacement.
- Task-only is the strongest M6-v2 field set in the Qwen sweep. Adding workflow, boundary, and dependency fields often hurts under the no-rewrite setting, which supports the claim that structured fields require selective use rather than naive positive concatenation.
- Qwen and SkillRouter learned rerankers remain strong baselines. M6-v2 helps slightly over embedding-only in some rows, but does not consistently beat learned reranking.
- Candidate recall remains a hard ceiling. For example, public-gold full-skill Qwen first-stage has only 81.2% candidate recall at top-20, so reranking cannot recover missing gold skills.
- Next hardening step: run failure analysis on M6-v2, calibrate field weights/penalties on a held-out development split, and only then decide whether to add a separate query-parser/rewrite ablation.

Fixed global M6-v2 policy update:

- The thesis-facing fixed method uses the same weights everywhere: 0.30 first-stage score, 0.70 semantic-field score, and 0.25 penalty/bonus adjustment.
- Fixed semantic-field weights after internal-weight ablation are task/use 0.50, output/artifact 0.20, workflow/procedure 0.15, input/precondition 0.10, and dependency/resource 0.05.
- After the 2026-06-23 rerun, refreshed Qwen-only fixed task-heavy R2 results are controlled 38.4% top-1 and public-gold 56.9% top-1.
- The corresponding field-only sensitivity check with base weight 0.00 remains worse than the 0.30 first-stage blend on Qwen rows, so a small first-stage prior still appears necessary for the current no-rewrite matcher.
- SkillRouter M6-v2 fixed rows from earlier files were not refreshed in this pass and should not be mixed into the refreshed Qwen-only M6-v2 table.

## 2026-06-18 Crossed Information-Layer and M6-v2 Calibration Update

Crossed lexical information-layer controls were refreshed on 2026-06-23 after correcting public-original source loading and regenerating the public-style controlled skills into messier public-document style. BM25 and TF-IDF now run over the same three implementation artifacts: I1/R1 flat metadata, I3H/R2 structured procedural cards, and I2/full source skill text. Output report: `skill_benchmark/outputs/frozen_v0_4_crossed_lexical_matrix.md`.

Controlled lexical results:

| Retriever | R1 Top-1 | R2 Top-1 | Full Top-1 | R1 Cand R@20 | R2 Cand R@20 | Full Cand R@20 |
|---|---:|---:|---:|---:|---:|---:|
| BM25 | 55.1% | 58.0% | 66.5% | 93.9% | 98.0% | 98.4% |
| TF-IDF | 52.6% | 59.6% | 69.4% | 91.4% | 95.5% | 97.5% |

Public-gold lexical results:

| Retriever | R1 Strict Top-1 | R2 Strict Top-1 | Full Strict Top-1 | R1 Cand R@20 | R2 Cand R@20 | Full Cand R@20 |
|---|---:|---:|---:|---:|---:|---:|
| BM25 | 55.6% | 54.9% | 59.0% | 87.5% | 97.2% | 99.3% |
| TF-IDF | 56.9% | 50.7% | 48.6% | 92.4% | 94.4% | 96.5% |

Interpretation:

- Controlled lexical results are now a source-policy warning: after the public-style controlled regeneration, full source text is strongest for BM25/TF-IDF top-1, while R2 still improves candidate recall over R1 but does not dominate full text.
- Public-gold remains mixed: BM25 full is now strongest at strict top-1 and candidate recall after switching to upstream originals, while TF-IDF still prefers R1 at top-1.
- Full skill text is therefore an important comparator, not a straw baseline. Its fixed indexing/context cost must be reported against the lower-token I3/I3C representations rather than assuming either side always wins.

M6-v2 fine blend sweep was also added. Output report: `skill_benchmark/outputs/frozen_v0_4_m6v2_blend_sweep_fine.md`.

Main calibration takeaways:

- The old default score was conservative and first-stage-heavy. The fine sweep confirms that this can underuse the field-aware second stage.
- For Qwen candidate sets, field-heavy or middle blends improve several rows, especially public-gold R2.
- For SkillRouter controlled candidates, first-stage-heavy blends often remain best, which means a strong skill-specific first stage should not be overwritten blindly.
- Tuned M6-v2 must be reported with dev/test or cross-validation. Full-set best weights are useful diagnostics, not final headline numbers.

M6-v2 explicit field-use sweep was then run over saved field-specific component scores. Output reports: `skill_benchmark/outputs/frozen_v0_4_m6v2_explicit_field_weight_sweep_narrow.md` and the focused R2 calibration `skill_benchmark/outputs/frozen_v0_4_m6v2_explicit_field_weight_sweep_r2_focused.md`.

R2 explicit field-use checkpoint:

| Candidate source | Stratum | Fixed field-specific top-1 | Tuned full-set top-1 | Dev-selected held-out top-1 | Main read |
|---|---|---:|---:|---:|---|
| Qwen | Controlled | 40.0% | 41.6% | 40.7% | Small full-set gain; held-out does not improve. |
| Qwen | Public-gold | 61.8% | 68.8% | 66.7% | Field scoring helps after calibration, but mostly through task evidence. |
| SkillRouter | Controlled | 64.5% | 66.1% | 63.6% | Extra fields help full-set tuning, but held-out remains lower. |
| SkillRouter | Public-gold | 73.6% | 76.4% | 71.8% | Full-set tuning helps but held-out score is lower. |

Interpretation:

- Field-specific matching makes the use of proposed information more explicit, because task, input, output, workflow, and dependency spans are compared to matching skill-side fields rather than every field receiving the whole request.
- The current result does not prove that all proposed fields should be treated as positive evidence. Most tuned R2 winners are still task-only or first-stage-heavy.
- The next methodological improvement should focus on field activation and mismatch handling, not just wider score sweeps.

## 2026-06-18 External SkillRouter-Eval-Core Checkpoint

This is an external validation track, not a replacement for the controlled frozen-v0.4 benchmark. It uses the public SkillRouter-Eval-Core benchmark to test whether the information-layer question transfers to a much larger public skill pool.

Important extraction note: this first external result uses heuristic I3 (`I3H`), not model-parsed I3 (`I3M`). No DeepSeek, Qwen, or other LLM API was used to produce this external I3 parse.

Artifacts:

- Preparation report: `skill_benchmark/external/skillrouter_eval_core/derived/README.md`
- External result report: `skill_benchmark/external/skillrouter_eval_core/outputs/skillrouter_eval_core_fts_information_layers.md`
- Checkpoint note: `thesis_notes/checkpoints/skillrouter/External SkillRouter Eval Core Checkpoint - 2026-06-18.md`

Dataset conversion:

- 87 total tasks; 75 default scored tasks after excluding `generic_only`.
- Easy pool: 78,361 skills.
- Hard pool: 79,141 skills.
- Hard-only distractors: 780, computed as `hard_skill_ids - easy_skill_ids`.
- I3H parsing completed in 16 fixed chunks of up to 5,000 skills.

First external lexical/BM25 results:

| Tier | Layer | Hit@1 | MRR@10 | Recall@20 | FullCoverage@20 | Approx tokens |
|---|---|---:|---:|---:|---:|---:|
| Easy | I1 metadata | 36.0% | 0.448 | 48.3% | 32.0% | 5,488,975 |
| Easy | I2 full body | 48.0% | 0.558 | 57.4% | 42.7% | 152,669,986 |
| Easy | I3H heuristic extracted fields | 38.7% | 0.453 | 46.0% | 29.3% | 63,119,911 |
| Hard | I1 metadata | 28.0% | 0.373 | 46.1% | 30.7% | 5,536,118 |
| Hard | I2 full body | 44.0% | 0.525 | 55.7% | 41.3% | 153,155,878 |
| Hard | I3H heuristic extracted fields | 36.0% | 0.439 | 45.1% | 28.0% | 63,232,478 |

Interpretation:

- I2 full body is strongest on this external benchmark under disk-backed SQLite FTS5 BM25. This is consistent with SkillRouter's emphasis on full skill bodies.
- I3H improves over I1 on Hard Hit@1, which suggests extracted fields can reduce some hard-distractor top-rank errors.
- I3H does not yet improve Recall@20 or FullCoverage@20 and remains much larger than I1. The current heuristic external I3H parser is too broad and does not recover dependency/resource fields from this dataset.
- The external checkpoint therefore strengthens the thesis as a cautious information-preservation argument, not a simple "structured fields always win" claim.
- The next comparison was retrieval-side evaluation of ChatGPT/Codex-parsed I3C under a declared candidate universe. The full-tier external I3C FTS rerun has now been run; see the 2026-06-21 section below.

## 2026-06-19 External I3M / I3C Extraction Status

These are extraction-quality checkpoints for SkillRouter-Eval-Core, not retrieval results yet.

| Extraction | Row range | Rows | Parse failures | Evidence exact match | Notes |
|---|---:|---:|---:|---:|---|
| DeepSeek/API I3M | 0-2999 | 3000 | 0 latest failed | strict selector-valid rows 2997/3000 | Strong evidence grounding; 3 QA residues recorded. |
| ChatGPT/Codex I3C | 3000-5999 | 3000 | 0 | 98.66% | Good practical candidate after QA; manual samples show heterogeneous extraction style. |

Coverage check:

- SkillRouter-Eval-Core has 75 scored tasks and 186 unique core gold skills.
- Those gold skills occur at rows `27018-27213` in `all_I2.jsonl`.
- Therefore, current I3M/I3C slices cover `0` scored gold skills.

Interpretation:

- I3M is viable as a paid-model feasibility attempt, but the practical route for thesis claims is I3C.
- I3C should be treated as a candidate practical extraction method only with QA gates, not as unchecked ground truth.
- Future I3C runs should use `skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V2.md`, which requires selector-usefulness checks and records absent/weak/generic fields in QA metadata instead of selector-visible fields.
- The top-20 task-relevant SkillRouter pool and full Hard-tier library have now been parsed as cleaned I3C V2. The full-tier external FTS/BM25 I3C condition has been evaluated; fixed-candidate top-20/top-50 reranking remains separate future work. The top-50 I2 pool is not separately materialized as a cleaned top-50 I3C file, but its rows are covered by the full-all I3C V2 artifact and can be filtered from it.

I3C V2 pilot:

- First 200 rows of the SkillRouter top-20 task-relevant pool were extracted with 2 subagents, 100 skills per subagent.
- Result: 200/200 rows, 0 parse failures, 0 missing skill ids, and 1184/1184 exact evidence matches.
- QA warnings are now populated (`broad_skill`, `field_absent`, `generic_fragment_skipped`, `limited_selector_content`, `sparse_artifact`).
- Status: pass with minor QA caveats. Checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 Pilot First 200 - 2026-06-19.md`.

I3C V2 top-20 task-relevant pool:

- Full top-20 task-relevant pool extraction is complete: 33 subagent chunks, mostly 100 skills each, final chunk 84 skills.
- Clean canonical output: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_top20_pool/I3C_V2_top20_pool_cleaned.jsonl`.
- Result: 3284/3284 rows, 0 parse failures, 0 missing skill ids, 0 duplicate skill ids, 25544/25544 exact evidence matches, and 0 heading-only evidence after cleaning.
- QA caveat: 7 sparse public-skill artifacts have no selector-visible fields after conservative extraction; they are retained with QA metadata rather than overfilled.
- Checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 Top20 Pool Extraction Checkpoint - 2026-06-19.md`.

I3C V2 full-all SkillRouter library:

- Full SkillRouter-Eval-Core Hard-tier I3C V2 extraction is complete over `all_I2.jsonl`.
- Canonical output: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/I3C_V2_full_all_cleaned.jsonl`.
- Raw audit output: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/I3C_V2_full_all_merged.jsonl`.
- Result: 79141/79141 rows, 0 parse failures, 0 missing skill ids, 0 duplicate skill ids, 498836/498836 exact evidence matches, and 0 heading-only evidence after cleaning.
- Merge provenance: 3284 cleaned top-20 seed rows plus 75857 newly extracted missing rows across 759 chunks.
- QA caveat: 875 sparse artifacts have no selector-visible fields after conservative extraction; they are retained with absence/QA metadata rather than overfilled.
- Checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 Full-All Extraction Completion - 2026-06-20.md`.

Task-relevant pool prepared:

| Pool | Effective candidate budget per task/source | Skills to parse | Artifact |
|---|---:|---:|---|
| top-20 union + gold | 20 | 3284 | Parsed as cleaned I3C V2: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_top20_pool/I3C_V2_top20_pool_cleaned.jsonl` |
| top-50 union + gold | 50 | 7113 | Prepared as an I2 candidate pool: `skill_benchmark/external/skillrouter_eval_core/derived/representations/skillrouter_task_relevant_pool_top50_I2.jsonl`. I3C rows are available by filtering the full-all cleaned artifact; no separate top-50 cleaned file exists yet. |
| full Hard library | full tier | 79141 | Parsed as cleaned I3C V2: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/I3C_V2_full_all_cleaned.jsonl` |

The pool is built from existing full-library BM25 rankings over I1/I2/I3H plus all gold skills. It supports a fixed-candidate external reranking/ablation experiment, not a full-library first-stage retrieval claim.

## 2026-06-21 External SkillRouter-Eval-Core I3C V2 FTS Rerun

This is the first external retrieval result using the cleaned full-all I3C V2 structured fields. The thesis-facing primary comparison evaluates I1, I2, and I3C under the same SQLite FTS5 BM25 retriever and the full Easy/Hard candidate tiers. The older heuristic extracted-field condition remains an archival construction/debug artifact, not a primary thesis condition.

Artifacts:

- Field-only I3C FTS builder: `skill_benchmark/scripts/build_i3c_v2_fts_representations.py`
- Generated Easy I3C representation: `skill_benchmark/external/skillrouter_eval_core/derived/representations/easy_I3C.jsonl`
- Generated Hard I3C representation: `skill_benchmark/external/skillrouter_eval_core/derived/representations/hard_I3C.jsonl`
- Generation summary: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_fts_representation_summary.json`
- Primary result report: `skill_benchmark/external/skillrouter_eval_core/outputs/skillrouter_eval_core_fts_information_layers_i3c_v2_primary.md`
- Primary result JSON: `skill_benchmark/external/skillrouter_eval_core/outputs/skillrouter_eval_core_fts_information_layers_i3c_v2_primary.json`

External FTS/BM25 results:

| Tier | Layer | Hit@1 | MRR@10 | Recall@20 | FullCoverage@20 | Approx tokens |
|---|---|---:|---:|---:|---:|---:|
| Easy | I1 metadata | 36.0% | 0.448 | 48.3% | 32.0% | 5,488,975 |
| Easy | I2 full body | 48.0% | 0.558 | 57.4% | 42.7% | 152,669,986 |
| Easy | I3C V2 structured fields | 53.3% | 0.586 | 60.5% | 44.0% | 15,677,596 |
| Hard | I1 metadata | 28.0% | 0.373 | 46.1% | 30.7% | 5,536,118 |
| Hard | I2 full body | 44.0% | 0.525 | 55.7% | 41.3% | 153,155,878 |
| Hard | I3C V2 structured fields | 45.3% | 0.527 | 59.2% | 40.0% | 15,833,065 |

Interpretation:

- I3C V2 is the strongest Easy-tier condition across Hit@1, MRR@10, Recall@20, and FullCoverage@20 while using about 10% of the I2 token volume.
- On Hard, I3C V2 narrowly beats I2 on Hit@1, MRR@10, and Recall@20, while I2 remains slightly better on FullCoverage@20.
- The result supports the RQ1 claim that task/input/output/workflow/dependency/boundary/success information can help when recovered cleanly.
- This is external verification of the information-field claim, not evidence that I3C has been rerun locally. Local frozen-v0.4 still lacks a true I3C artifact; the existing local `I3M_model_parsed.jsonl` is the paid DeepSeek attempt.
- Corrected external SkillRouter-Eval-Core neural job `6a3773a1953ed90bfb9469b7` was cancelled to stop Hugging Face GPU spend. It emitted only Easy/I1 embedding and Easy/I1 rerank rows before spending several hours on the next full-document condition, and no Hub result files were uploaded. Recovered rows are stored under `skill_benchmark/external/skillrouter_eval_core/outputs/skillrouter_eval_core_skillrouter_neural_i3c_v2_corrected_4096_partial_recovered.*`. The earlier neural job `6a373487953ed90bfb94663e` remains diagnostic only. The I3C-vs-FULL neural question is still unanswered and needs a split rerun.


Historical consolidation baseline, 2026-06-18:

The remaining sections retain older benchmark and retrieval notes for provenance. Treat them as historical unless a section explicitly says it has been refreshed for frozen-v0.4.

Methodology hardening update, 2026-06-05:

- Treat `M6-v1-local` as a lexical field-aware prototype, not a finished semantic field matcher.
- Compare rerankers at equal candidate budgets. The fair SkillRouter comparison is top-20 versus top-20; the M6-v1 top-100 result is a larger-budget condition.
- Report strict-gold and gold-or-acceptable metrics separately.
- Do not use `non-main top-1` as a headline metric for public-gold, because public-gold targets are themselves public/background skills.
- Add confidence intervals or paired tests before final headline claims.
- See `thesis_notes/methodology/Methodology Deep Critique and Improvement Plan - 2026-06-05.md`.

Supervisor feedback update, 2026-06-05:

- Assignment 3 feedback requested more concrete empirical details from reviewed papers, clearer benchmark construction, and a more specific experimental setup covering gold labels, model settings, prompts, and statistical comparison.
- This is now tracked in `thesis_notes/assignments/Supervisor Feedback Response Plan - A3 to Current Thesis.md`.
- Current status against that feedback:
  - empirical literature details: partial, needs a thesis-ready table;
  - benchmark construction: partial, needs a clear pipeline in the benchmark chapter;
  - gold labels: partial, controlled golds exist and public-gold cleanup plus provider reruns are done; strict versus acceptable labels must be explained clearly;
  - model settings: partial, provider notes exist but final method table needs standardized settings;
  - prompts: partial, files exist but thesis needs clearer prompt strata and examples;
  - statistical comparison: first-pass top-1 confidence intervals and paired McNemar tests exist in the frozen-v0.4 information-layer matrix; final MRR/top-k uncertainty remains optional depending on headline metrics.

## Historical Scale Update

This section is retained for the earlier 201-controlled / 2433-skill checkpoint. It is superseded by the frozen-v0.4 condition: 245 controlled prompts, 144 public-gold prompts, 12 low-information prompts, and 2433 skills.

Current library:

- 2433 total skills.
- 169 controlled/evaluated skills plus additional controlled prompt expansions.
- 144 cleaned public-gold prompts as a separate external-validity stratum.
- 389 total controlled + public-gold prompts if combined.
- 401 prompts in the broad combined validation audit when low-information stress prompts are included.
- 1800 generated background-scale skills.
- 460 public imported background skills.
- 4 support/email skills.
- 245 controlled/evaluated prompts, including implicit-field, clear-confusability, and public-style controlled prompt families.

Current validation:

| Step | Status | Result |
|---|---|---|
| Step 1 integrity | Done | PASS: 245 controlled prompts, 144 public-gold prompts, 12 low-information prompts, and 2433 skills resolve. |
| Step 2 procedural alignment | Done with residual cases recorded | Controlled procedural distinctness passes 245/245 prompts and 830/830 pairs; public-gold procedural distinctness passes 144/144 prompts and 575/575 pairs. |
| Step 3 semantic confusability | Done | Controlled semantic confusability passes 243/245 prompts; public-gold passes 144/144 prompts. |
| Step 4 prompt leakage | Done | PASS: 0 critical exact-name leaks; 0 high-risk leaks. |
| Step 5 scale regime | Done | PASS: 2433-skill public-expanded library constructed. |
| Step 6 public-skill field audit | Mostly done | 460/460 imported public skills audited heuristically and with DeepSeek model-assisted verification; 80-case disagreement packet generated for manual taxonomy review. |
| Step 6b public-skill gold validation | Expanded separate stratum | 144 public-gold prompts; integrity PASS, procedural distinctness 144/144, requirement alignment 131/144, semantic confusability 144/144, leakage PASS. |
| Step 7 information-layer matrix | Current frozen-v0.4 matrix done | PASS: local, Qwen, SkillRouter, M6-v1 diagnostic, and M6-v2 diagnostic families have I1/I3/I2 coverage where audited. |
| Step 7 statistical/failure companion | First pass done | Bootstrap top-1 CIs, paired McNemar tests, and compact R2/I3 failure-mode comparison exist for frozen v0.4. |
| Step 7 field ablation | Done | Local BM25/TF-IDF ablations show use conditions, outputs, and workflow/procedure drive most retrieval gains; naive not-for/dependency concatenation can hurt. |
| Step 7 M6-v1 field-aware reranker | First prototype done | `M6-v1-local` parses request-side fields and reranks fixed candidate sets by field-to-field matching. Controlled results support task/output/workflow as strong fields; public-gold remains weak and needs semantic field matching. |
| Step 7 non-core competition | Needs adjudication | 33/85 semantic non-core-over-gold cases; 16/85 procedural non-core-over-gold cases. |

Historical 2433/201 local lexical/schema selector results:

| Method | Full Top-1 | Full Top-5 | MRR | Full Non-Core Top-1 |
|---|---:|---:|---:|---:|
| M1 BM25 flat | 61.7% | 88.1% | 0.727 | 9.0% |
| M1 TF-IDF flat | 55.2% | 86.1% | 0.689 | 15.4% |
| M3 TF-IDF schema | 65.2% | 94.0% | 0.778 | 8.0% |
| M6 BM25 -> schema rerank | 65.7% | 93.5% | 0.781 | 3.0% |
| M6 TF-IDF -> schema rerank | 65.7% | 91.5% | 0.773 | 3.5% |

Current interpretation:

- The expanded benchmark now creates real scale and confusability pressure: flat metadata top-1 falls to 55-62%, and structure-aware local methods are not near-perfect.
- Description-only and flat retrieval remain fragile under scale; dense/MiniLM evidence is retained from the 2089 checkpoint.
- Schema-aware and hybrid methods degrade less on the controlled benchmark and produce fewer non-core top-1 false positives.
- The current local schema reranker should be treated as `M6-v0`: a diagnostic weighted-overlap method over extracted fields, not the final proposed structure-aware method.
- `M6-v1` and `M6-v2` should be treated as field-use diagnostics unless further auditing shows they are robust final methods. The thesis contribution is the information-layer comparison, not necessarily a new winning reranker.
- Tree routing (`M4`) and graph retrieval (`M5`) remain planned structure-aware architectures. They should be added only if they answer a specific question: tree routing tests scale/branch exclusion, while graph retrieval tests whether explicit relations among inputs, outputs, tools, workflows, resources, and families help beyond serialized structured cards.
- The main next validation step is targeted second-pass adjudication of non-core winners and strongest-method failures, especially in `documents_files`, `skill_lifecycle`, `deployment_browser_qa`, and `api_backend_design`.
- The historical 2433/201 local rerun preserves the main result: task/use, output, and workflow fields help, while naive use of all fields can add noise.

Method cleanup note:

- `thesis_notes/methodology/Final Method Set and Information-Use Plan.md`

Manual public-gold adjudication note:

- `thesis_notes/benchmark/public_skills/Public Gold Manual Adjudication - 2026-06-01.md`

Current validation residual note:

- `thesis_notes/checkpoints/benchmark_validation/Benchmark Residual Validation Reasons - 2026-06-06.md`

Current 2089-scale MiniLM/local selector results, retained for comparison:

| Method | Core Top-1 | Full Top-1 | Full Top-5 | Full Non-Core Top-1 |
|---|---:|---:|---:|---:|
| M2a MiniLM description | 67.1% | 49.4% | 77.6% | 31.8% |
| M2b MiniLM full skill | 71.8% | 64.7% | 83.5% | 15.3% |
| M6 MiniLM full -> schema rerank | 90.6% | 82.3% | 89.4% | 5.9% |

Historical 2401/137 Qwen provider results, superseded for active claims by the frozen-v0.4 information-layer matrix:

| Method | Candidate Budget | Top-1 | Top-5 | MRR | Public Top-1 | Non-Core Top-1 |
|---|---:|---:|---:|---:|---:|---:|
| Qwen full-skill embedding only | none | 52.5% | 73.7% | 0.617 | n/a | 26.3% |
| Qwen full-skill + Qwen generic rerank | 20 | 62.0% | 75.2% | 0.684 | n/a | 24.8% |
| Qwen full-skill + local schema rerank | 100 | 77.4% | 91.2% | 0.840 | n/a | 8.0% |

Historical 2433/201 M6-v1-local field-aware reranker results:

| First stage | Best field set | Top-1 | Top-5 | MRR | Candidate R@100 | Conditional top-1 | Non-Main Top-1 |
|---|---|---:|---:|---:|---:|---:|---:|
| TF-IDF flat | core | 72.6% | 94.0% | 0.824 | 96.0% | 75.6% | 3.5% |
| TF-IDF flat | core + boundary | 72.6% | 94.5% | 0.822 | 96.0% | 75.6% | 3.5% |
| BM25 flat | core + boundary | 72.1% | 95.0% | 0.825 | 97.0% | 74.4% | 3.5% |

Field-set pattern on 2433/201:

- TF-IDF first stage improves from 65.2% with task-only fields to 71.6-72.6% when output/workflow/core fields are added.
- BM25 first stage improves from 63.7% with task-only fields to 72.1% with core + boundary fields.
- All-fields scoring is weaker than the best selective field set, which supports the claim that the information layer needs field-aware use, not just longer skill text.

Interpretation:

- `M6-v1-local` is a better diagnostic than `M6-v0` because it reports candidate recall and compares request fields to skill fields.
- Qwen generic reranking is a useful neural baseline, but on the controlled benchmark it improves less than the procedural field-aware rerankers.
- The strongest controlled field set is not "all available structure"; it is task/use condition + output + workflow, with input sometimes helping and boundary/dependency/hierarchy needing conditional handling.
- The current M6-v1 matcher is still mostly lexical. It should be treated as the first deterministic field-aware prototype, not the final field-aware architecture.

Current SkillRouter update:

- SkillRouter full-skill embedding is now the strongest first-stage skill-specific retrieval baseline on the controlled benchmark.
- SkillRouter + SkillRouter rerank top-20 reaches 83.2% top-1, 97.8% top-5, and 0.898 MRR.
- SkillRouter + M6-v1-local task/output/workflow top-20 reaches 83.2% top-1, 95.6% top-5, and 0.895 MRR.
- SkillRouter + M6-v1-local task/output/workflow top-100 reaches 86.9% top-1, 98.5% top-5, and 0.927 MRR.
- Interpret this carefully: top-20 is the budget-fair reranker comparison; top-100 is evidence about the value of a larger high-recall candidate pool plus field-aware ordering.

Current implicit-field interpretation:

- The 10 implicit-field cases are now included in the 137-prompt main benchmark.
- Raw implicit skills remain prose-only.
- The representation exporter now performs conservative prose-to-field extraction before building R2/R3.
- This better matches the thesis claim: structure-aware retrieval should include an extraction/normalization layer, not assume all skill authors provide clean headings.

Current Qwen interpretation:

- Qwen flat-card retrieval is highly fragile under public-expanded scale.
- R2 structured cards substantially improve over R1, which supports the claim that representation content matters even with a strong embedding model.
- Qwen's generic reranker improves top-1 but still leaves many non-core/public false positives.
- Qwen full-skill retrieval plus local procedural schema reranking is currently the strongest 2401-scale provider result.
- The strongest method still has 13 strict top-1 failures; several are first-stage candidate-recall failures, so final reporting should separate candidate recall from reranking accuracy.

## Public-Gold Cleaned Stratum

Current status:

- 144 cleaned public-gold prompts now exist as a separate external-validity stratum.
- They should not be blindly merged with the controlled 245-prompt benchmark, because public-gold tests public-wrapper messiness and externally authored skill artifacts.
- Acceptable alternatives are recorded in `skill_benchmark/annotations/public_gold_acceptable_alternatives.json`.
- Total evaluated prompt pool is now 389 if combined for reporting: 245 controlled plus 144 public-gold. The broad combined validation audit includes 401 prompts after adding the 12 low-information stress prompts.

Validation:

| Gate | Result |
|---|---|
| Step 1 integrity | PASS: 120 prompts, 0 missing references. |
| Step 2 procedural distinctness | PASS: 120/120 prompts; 459/459 pairs with at least one primary differentiator; 417/459 with two or more. |
| Step 2 requirement alignment | PASS with residual hard cases: 115/120 prompts; 510/517 pairs; 98/120 strict top-1 and 118/120 gold-or-acceptable top-1 among listed candidates. |
| Step 3 semantic confusability | PASS: 116/120 prompts; 382/517 plausible semantic-neighbour pairs. |
| Step 4 leakage | PASS: 0 critical exact-name leaks; 0 high-risk leaks. |

Interpretation:

- Public-gold is valuable as an external-validity stratum, but controlled clusters remain the cleaner basis for causal field-use claims.
- Remaining weak requirement-alignment cases are Shopify automation, public security review, webhook automation, job description, and expense tracker. These are retained as public hard cases rather than overfit with artificial wording.
- Remaining weak semantic-confusability cases are Claude API, Ghost Admin API endpoint, security ownership map, and DocuSign automation; these are high-specificity public/provider tasks with too few natural close neighbours in the current library.
- Public-gold results should be reported in strict and gold-or-acceptable forms.
- The `core` scale is not meaningful for public-gold selector evaluation because public target skills are not present in the controlled-core candidate pool; use `current_full`.

Historical public-gold local selector results after the 82-case cleanup on `current_full`:

| Method | Top-1 | Top-5 | MRR | Interpretation |
|---|---:|---:|---:|---|
| M1 BM25 flat | 51.2% strict / 67.1% accept | 86.6% strict / 92.7% accept | 0.659 strict / 0.784 accept | Lexical control remains competitive; useful warning about wording cues. |
| M1 TF-IDF flat | 50.0% / 63.4% | 86.6% / 91.5% | 0.649 / 0.751 | Similar flat-card baseline. |
| M2a MiniLM description | 48.8% / 59.8% | 81.7% / 87.8% | 0.626 / 0.718 | Dense description retrieval is comparable to lexical flat cards. |
| M2b MiniLM full skill | 35.4% / 47.6% | 64.6% / 72.0% | 0.494 / 0.604 | Full public artifacts are noisy for small local embeddings. |
| M3 TF-IDF schema | 40.2% / 51.2% | 79.3% / 89.0% | 0.567 / 0.668 | Naive extracted schema is not enough on public-authored skills. |
| M6-v0 local schema rerank | 32.9-36.6% / 51.2-57.3% | 74.4-85.4% / 85.4-92.7% | 0.503-0.558 / 0.653-0.716 | Diagnostic reranker; current scoring is too crude for public-gold. |

Historical cleaned 82-case public-gold provider results:

| Method | Top-1 | Accept Top-1 | Top-5 | Accept Top-5 | MRR | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| Qwen R1 embedding | 62.2% | 72.0% | 84.2% | 89.0% | 0.720 | Flat public cards are strong on public-authored skills. |
| Qwen R1 + Qwen rerank top-20 | 74.4% | 85.4% | 96.3% | 97.6% | 0.837 | Strong generic reranking recovers many strict public labels. |
| Qwen R2 embedding | 59.8% | 73.2% | 82.9% | 87.8% | 0.714 | Structured cards do not beat R1 by embedding alone on public-gold. |
| Qwen R2 + Qwen rerank top-20 | 76.8% | 90.2% | 100.0% | 100.0% | 0.861 | Best current public-gold provider result. |
| Qwen full-skill embedding | 31.7% | 50.0% | 58.5% | 69.5% | 0.448 | Full public artifacts are noisy for direct embedding. |
| Qwen full-skill + Qwen rerank top-20 | 68.3% | 79.3% | 80.5% | 87.8% | 0.739 | Reranking helps but full-skill first stage is weaker here. |
| SkillRouter full embedding | 68.3% | 79.3% | 95.1% | 97.6% | 0.790 | Strong first-stage domain-specific retrieval. |
| SkillRouter + SkillRouter rerank top-20 | 64.6% | 73.2% | 92.7% | 95.1% | 0.778 | SkillRouter rerank does not improve public-gold top-1 in this run. |

Historical cleaned 82-case public-gold M6-v1-local results:

| First stage | Field set | Top-1 | Accept Top-1 | Top-5 | Accept Top-5 | MRR | Candidate R@100 |
|---|---|---:|---:|---:|---:|---:|---:|
| Qwen full-skill | task only | 54.9% | 65.8% | 79.3% | n/a | 0.663 | 95.1% |
| Qwen full-skill | task + output + workflow | 47.6% | 67.1% | 80.5% | n/a | 0.609 | 95.1% |
| Qwen full-skill | core | 48.8% | 67.1% | 79.3% | n/a | 0.619 | 95.1% |
| Qwen full-skill | core + boundary | 48.8% | 67.1% | 82.9% | n/a | 0.617 | 95.1% |
| Qwen full-skill | all fields | 43.9% | 63.4% | 81.7% | n/a | 0.604 | 95.1% |
| SkillRouter full-skill | task only | 68.3% | 78.1% | 90.2% | 95.1% | 0.788 | 98.8% |
| SkillRouter full-skill | core | 63.4% | 79.3% | 92.7% | 97.6% | 0.762 | 98.8% |

Public-gold interpretation:

- These results do not prove that extracted fields improve public-skill retrieval.
- These 82-case selector tables must be rerun before being used as evidence for the expanded 120-case public-gold stratum.
- They show that a lexical field-aware reranker is insufficient when public skills are broad, implicit, duplicated, wrapper-like, or heavily source/lexical cued.
- Qwen R2 + Qwen rerank is currently the best public-gold method, which means strong semantic reranking is a serious baseline.
- Candidate recall is high for Qwen full-skill and SkillRouter first stages, so many public-gold failures are reranker/field-matching/extraction failures rather than pure first-stage retrieval failures.
- This strengthens the thesis if framed carefully: field information may matter, but the final method must use it through robust semantic field matching rather than simple lexical overlap.

## Public-Skill Field Audit

Current status:

- Scope: 460 imported public `SKILL.md` files.
- Originals used: 460/460.
- Mean words per skill: 1194.02.
- Median words per skill: 1141.
- Manual review packet: 15 sampled skills for the expanded public set.

Field prevalence:

| Field | Explicit | Explicit or Extractable | Provisional Read |
|---|---:|---:|---|
| routing trigger | 100.0% | 100.0% | observed |
| input/precondition | 25.2% | 81.5% | often extractable |
| output artifact | 45.2% | 85.2% | observed/extractable |
| workflow/procedure | 71.7% | 84.4% | observed/extractable |
| constraints/boundaries | 41.3% | 77.6% | partially observed/extractable |
| dependencies/tools | 72.8% | 85.0% | observed |
| resources/references | 66.7% | 82.0% | observed/extractable |
| examples/tests | 63.5% | 93.9% | observed/extractable |
| safety/side effects | 11.3% | 37.0% | proposed or weakly observed |
| portability/environment | 62.2% | 80.7% | observed/extractable |
| hierarchy/links | 25.2% | 31.1% | partially observed |

Interpretation:

- Public skills do contain many of the procedural signals used by the structured representation, especially triggers, workflows, outputs, dependencies, and examples.
- Some signals are often implicit rather than cleanly fielded, which supports the idea of an information layer that extracts or normalizes them.
- Safety/side-effect information is weak in the sampled public corpus. Treat this as a proposed field or a quality gap, not a mature public-skill convention.
- The current audit is heuristic. The 20-skill manual review packet must be checked before using these numbers as final thesis evidence.
- A model-assisted semantic verification layer has been added and implemented. The DeepSeek checkpoint now covers the full 460-public-skill subset and is recorded in `thesis_notes/checkpoints/public_skill_audit/Public Skill Model Verification Checkpoint - 460 Skills.md`.
- A 10-skill subagent/manual calibration pilot is complete. It confirms the main pattern but warns that resources, examples/tests, output artifacts, workflow, and dependencies can be overcounted if keyword matching is too loose.
- A targeted disagreement adjudication note is recorded in `thesis_notes/benchmark/public_skills/Public Skill Disagreement Adjudication - Step 6.md`. Its main conclusion is that public skills contain recoverable procedural signals, but the information-layer extraction pipeline must normalize them rather than assuming clean author-provided schema fields.
- A draft final taxonomy is recorded in `thesis_notes/methodology/Final Representation Field Taxonomy - Draft.md`. It separates primary retrieval fields from secondary feasibility, boundary, and downstream fields.
- The public-expanded validation checkpoint is recorded in `thesis_notes/checkpoints/benchmark_validation/Public Expansion 2349 Validation Checkpoint.md`.

Model-assisted field prevalence on 460 public skills:

| Field | Model-present rate | Interpretation |
|---|---:|---|
| `workflow_procedure` | 90.4% | strongly observed |
| `dependencies_tools` | 89.6% | strongly observed |
| `examples_tests` | 87.6% | strongly observed |
| `routing_trigger` | 85.7% | observed, but broad descriptions need care |
| `output_artifact` | 80.2% | observed/extractable |
| `resources_references` | 77.2% | observed/extractable |
| `constraints_boundaries` | 75.2% | observed but definition-sensitive |
| `portability_environment` | 74.1% | observed/extractable |
| `input_precondition` | 68.3% | often implicit/extractable |
| `hierarchy_links` | 51.7% | partially observed |
| `safety_side_effects` | 29.8% | weakly observed/proposed |

## Benchmark Status

The following section records the earlier 1006-skill v1 state.

Library:

- 1006 total skills.
- 67 controlled core skills.
- 920 generated background-scale skills.
- 15 public imported background skills.
- 4 support/email skills.
- 67 evaluated prompts.

Validation:

| Step | Status | Result |
|---|---|---|
| Step 1 integrity | Done | PASS: 67 prompts and 1006 skills resolve. |
| Step 2 procedural alignment | Done | PASS: 67/67 prompts pass field audit; 65/67 pass stricter prompt-specific alignment. |
| Step 3 semantic confusability | Done | PASS: 61/67 prompts pass local MiniLM semantic-confusability check. |
| Step 4 prompt leakage | Done | PASS: 0 critical exact-name leaks; 0 high-risk leaks. |
| Step 5 scale regime | Done | PASS: 1006-skill library constructed. |
| Step 7 local selectors | Done | PASS: useful spread from 47.8% to 80.6% top-1. |
| Step 7 Qwen provider selectors | Done | PASS: Qwen embedding and reranking tested on R1, full skill, and R2. |
| Low-information stress test | Done separately | Performance drops sharply; confirms schema reranking depends on explicit procedural evidence. |
| Failure mode analysis | Done for current strongest method | 10 failures: 4 first-stage exclusions, 6 reranking/boundary/annotation failures. |
| Step 8 M0 progressive disclosure | Done on core | PASS as baseline trace; not yet full-library stress test. |
| Step 9 downstream task validation | Not done | Plan exists; artifact generation/evaluation still pending. |

## Local Selector Results

Core scale means 67 controlled skills. Full scale means 1006 skills.

| Method | Representation | Core Top-1 | Core Top-5 | Full Top-1 | Full Top-5 | Full MRR | Full Non-Core Top-1 |
|---|---|---:|---:|---:|---:|---:|---:|
| M1 BM25 flat | R1 flat metadata | 67.2% | 94.0% | 64.2% | 86.6% | 0.733 | 16.4% |
| M1 TF-IDF flat | R1 flat metadata | 68.7% | 92.5% | 58.2% | 85.1% | 0.697 | 16.4% |
| M2a MiniLM description | R1 description embedding | 61.2% | 91.0% | 47.8% | 74.6% | 0.603 | 25.4% |
| M2b MiniLM full skill | Full `SKILL.md` embedding | 64.2% | 92.5% | 61.2% | 82.1% | 0.717 | 9.0% |
| M3 TF-IDF schema | R2 structured procedural | 74.6% | 100.0% | 71.6% | 95.5% | 0.808 | 9.0% |
| M6 BM25 -> schema rerank | Flat shortlist + schema rerank | 77.6% | 95.5% | 71.6% | 92.5% | 0.815 | 7.5% |
| M6 TF-IDF -> schema rerank | Flat shortlist + schema rerank | 80.6% | 97.0% | 70.2% | 85.1% | 0.778 | 10.4% |
| M6 MiniLM full -> schema rerank | Full-skill shortlist + schema rerank | 89.6% | 100.0% | 80.6% | 91.0% | 0.856 | 7.5% |

Best local method:

- M6 MiniLM full-skill retrieval plus deterministic schema reranking.
- Full-library top-1: 80.6%.
- Full-library top-5: 91.0%.

## Historical Qwen Provider Results

The following Qwen full-library runs use the historical 1006-skill scale. The active 2089-scale Qwen full-skill results are listed near the top of this file.

| Method | Representation | Top-1 | Accept Top-1 | Top-5 | Accept Top-5 | MRR | Non-Core Top-1 |
|---|---|---:|---:|---:|---:|---:|---:|
| Qwen embedding only | R1 flat card | 35.8% | 35.8% | 56.7% | 59.7% | 0.449 | 43.3% |
| Qwen embedding + rerank | R1 flat card | 64.2% | 67.2% | 67.2% | 70.2% | 0.649 | 31.3% |
| Qwen embedding only | Full `SKILL.md` | 46.3% | 47.8% | 71.6% | 74.6% | 0.574 | 29.8% |
| Qwen embedding + rerank | Full `SKILL.md` | 61.2% | 65.7% | 65.7% | 70.2% | 0.644 | 37.3% |
| Qwen embedding only | R2 structured card | 47.8% | 47.8% | 65.7% | 67.2% | 0.563 | 31.3% |
| Qwen embedding + rerank | R2 structured card | 65.7% | 67.2% | 71.6% | 73.1% | 0.688 | 26.9% |

## Qwen + Local Schema Reranker

This ablation uses Qwen `text-embedding-v4` for first-stage retrieval, then uses our deterministic schema reranker instead of Qwen `qwen3-rerank`.

| Method | Candidate Budget | Top-1 | Top-5 | MRR | Non-Core Top-1 |
|---|---:|---:|---:|---:|---:|
| Qwen R1 + local schema | 20 | 58.2% | 67.2% | 0.622 | 25.4% |
| Qwen full + local schema | 20 | 68.7% | 74.6% | 0.715 | 22.4% |
| Qwen full + local schema | 50 | 80.6% | 88.1% | 0.834 | 11.9% |
| Qwen full + local schema | 100 | 85.1% | 91.0% | 0.878 | 9.0% |
| Qwen R2 + local schema | 20 | 64.2% | 73.1% | 0.687 | 22.4% |
| Qwen R2 + local schema | 50 | 70.2% | 79.1% | 0.746 | 14.9% |
| Qwen R2 + local schema | 100 | 79.1% | 89.5% | 0.838 | 10.4% |

Qwen core smoke test:

- Scale: 67 controlled core skills.
- Prompts: first 5 prompts.
- Method: full `SKILL.md` embedding plus Qwen rerank.
- Result: 100.0% top-1 and 100.0% top-5.

Main Qwen interpretation:

- Qwen reranking improves top-1 over embedding-only for every representation.
- The best Qwen condition is R2 structured card plus rerank at 65.7% top-1.
- Qwen does not solve the full benchmark.
- Qwen's generic reranker underperforms the best local structure-aware M6 result.
- Qwen embeddings combined with the local schema reranker now produce the strongest current result: 85.1% top-1 with full-skill Qwen retrieval and top-100 schema reranking.

## M0 Progressive Disclosure Baseline

M0 is the normal-agent baseline where the main agent sees skill cards and chooses which full skill documents to load.

Current run:

- Scale: 67 controlled core skills.
- Strict top-1: 61.2%.
- Strict any-hit: 64.2%.
- No explicit skill loaded: 31.3%.
- Mean full skill docs loaded: 0.78.

Interpretation:

- M0 is useful as a realistic main-agent behavior baseline.
- It is not a clean retriever-only measure because the agent sometimes answers directly without loading a skill.
- Full 1006-skill M0 has not been run and should be treated as a context/cost stress test rather than a necessary immediate result.

## Step 9 Candidate Readiness

Step 9 downstream artifact generation has not been executed. A 12-prompt readiness check exists. The underlying files still use `step8` in their names from the earlier numbering.

| Method | Top-1 Gold/Accept | Top-5 Gold/Accept |
|---|---:|---:|
| M1 BM25 flat | 75.0% | 91.7% |
| M1 TF-IDF flat | 41.7% | 100.0% |
| M2b MiniLM full skill | 50.0% | 83.3% |
| M3 TF-IDF schema | 66.7% | 91.7% |
| M6 BM25 -> schema rerank | 75.0% | 91.7% |
| M6 TF-IDF -> schema rerank | 50.0% | 91.7% |
| M6 MiniLM full -> schema rerank | 83.3% | 91.7% |

Interpretation:

- Downstream validation is only fair when the correct or acceptable skill is in the candidate set.
- Missing top-5 cases should be treated as retrieval failures before judging generated artifacts.

## Low-Information Stress Test

This separate 12-prompt set uses less explicit user requests. It is not mixed into the main benchmark.

Best strict top-1 results:

- M2b MiniLM full skill: 41.7%.
- M6 MiniLM full -> schema rerank: 33.3%.
- Qwen full + qwen3-rerank: 33.3%.
- Qwen full + local schema rerank, top-100: 25.0%.

Interpretation:

- This is an anti-cheating check.
- The schema reranker does not infer hidden intent from vague prompts.
- It works best when the user request contains enough procedural evidence to match structured fields.
- Very underspecified requests may need a clarification or query-understanding stage before retrieval.

Detailed report: `thesis_notes/results/Low Information Stress Test.md`.

## What The Results Currently Show

1. Flat metadata is weak under scale.
2. Description-only embedding is especially fragile.
3. Full skill text helps compared with short descriptions, but does not fully solve procedural confusion.
4. Structured procedural information is useful.
5. Reranking helps when the correct skill is already in the candidate set.
6. Stronger provider embeddings/rerankers do not remove the need for good representation.
7. The strongest controlled-benchmark result comes from Qwen broad semantic retrieval plus the current local schema reranker, but that reranker is now treated as `M6-v0` diagnostic rather than the final proposed method.
8. Field ablations show the most retrieval-critical information is use conditions, output artifacts, and workflow/procedure; not-for and dependency/resource fields need field-aware handling because naive text concatenation can add noise.

## Current Critique And Validity Risks

The formal critique/action plan is recorded in `thesis_notes/methodology/Critique Response and Validity Improvement Plan.md`.

Main risks:

- Benchmark construction and schema scoring may be co-adapted.
- Some non-core winners may be genuinely acceptable or better than the intended gold skill.
- 85 evaluated prompts supports a controlled honours-scale benchmark, but not broad universal claims.
- Generated background skills create scale pressure but not full real-world messiness.
- MiniLM semantic-confusability checks are useful construction evidence, not final semantic authority.
- The public-skill audit grounds the field taxonomy but is not a full human annotation study.
- Downstream task success is not yet demonstrated.

Planned response:

- Freeze the representation-field taxonomy and method set before further tuning.
- Run targeted second-pass adjudication over non-core winners and strongest-method failures.
- Report public-skill findings as observed/extractable/proposed, not as clean ecosystem-wide schema prevalence.
- Keep the cleaned public-gold validation subset separate from controlled gold skills; use it as external-validity evidence and as a failure-mode source for extraction noise.
- Run small Step 9 downstream validation before claiming agent reliability benefits.

## Public-Gold Validation

Current status:

- Public-gold candidate prompts: 120 cleaned prompts.
- Gold labels: imported public skills.
- Current location: `skill_benchmark/prompts_public_gold/public_gold_validation_confusability.json`.
- Checkpoint outputs: `skill_benchmark/outputs/public_gold_step*.md`. Older 82- and 120-prompt selector outputs are historical; frozen-v0.4 public-gold selector outputs now use 144 prompts.

Validation gates:

| Gate | Result |
|---|---:|
| Step 1 integrity | PASS, 120/120 references resolve |
| Step 2 procedural distinctness | PASS, 120/120 prompts |
| Step 2 prompt-specific alignment | PASS, 115/120 prompts |
| Step 3 semantic confusability | PASS, 116/120 prompts |
| Step 4 prompt leakage | PASS, 0 critical, 0 high-risk |

Historical public-gold local selector read on the older 82-prompt stratum:

| Method | Strict Top-1 | Accept Top-1 | Strict Top-5 | Accept Top-5 | Strict MRR |
|---|---:|---:|---:|---:|---:|
| M1 BM25 flat | 51.2% | 67.1% | 86.6% | 92.7% | 0.659 |
| M1 TF-IDF flat | 50.0% | 63.4% | 86.6% | 91.5% | 0.649 |
| M2a MiniLM description | 48.8% | 59.8% | 81.7% | 87.8% | 0.626 |
| M2b MiniLM full skill | 35.4% | 47.6% | 64.6% | 72.0% | 0.494 |
| M3 TF-IDF schema | 40.2% | 51.2% | 79.3% | 89.0% | 0.567 |
| M6 BM25 -> schema rerank | 35.4% | 57.3% | 85.4% | 92.7% | 0.558 |
| M6 TF-IDF -> schema rerank | 36.6% | 52.4% | 81.7% | 89.0% | 0.556 |
| M6 MiniLM full -> schema rerank | 32.9% | 51.2% | 74.4% | 85.4% | 0.503 |

Historical 32-case public-gold Qwen provider read:

| Method | Top-1 | Top-5 | MRR |
|---|---:|---:|---:|
| Qwen R1 flat-card embedding | 59.4% | 87.5% | 0.716 |
| Qwen R2 structured-card embedding | 59.4% | 87.5% | 0.732 |
| Qwen full-skill embedding | 28.1% | 65.6% | 0.469 |
| Qwen R1 + local schema rerank top-100 | 40.6% | 90.6% | 0.616 |
| Qwen R2 + local schema rerank top-100 | 46.9% | 90.6% | 0.653 |
| Qwen full-skill + local schema rerank top-100 | 25.0% | 78.1% | 0.482 |
| Qwen full-skill + Qwen rerank top-20 | 68.8% | 84.4% | 0.763 |

Interpretation:

- Public-gold cases now satisfy the Step 6b construction rubric as a cleaned 120-case stratum.
- Unlike the controlled benchmark, naive schema extraction underperforms flat/description retrieval on this public-only stratum.
- This supports a more careful thesis claim: structure-aware retrieval depends on the quality of the extraction/normalization layer when skills are authored by others.
- BM25 is kept as a lexical control, not as the thesis method. Its relatively strong result on public-gold cases helps diagnose how much exact wording and source-artifact wording still influence the benchmark. Wrapper-based public full-text rows remain historical until rerun against upstream originals.
- This historical 82-case provider note is superseded for current frozen-v0.4 reporting by the 2026-06-23 refreshed 144-case Qwen matrix. Keep it only as earlier diagnostic history.

## Current Strongest-Method Failure Analysis

Target:

- Qwen full `SKILL.md` embedding.
- Top-100 candidate pool.
- Local schema reranker.

Failure split:

- 10 strict top-1 failures out of 67 prompts.
- 4 first-stage exclusions where Qwen did not place the gold skill in top-100.
- 6 reranking, boundary, or annotation failures where the gold was inside the top-100 but did not rank first.

Main failure types:

- first-stage embedding confuses task object with required procedure;
- schema reranker overweights secondary terms;
- negation and `not_for` handling is too weak;
- meta-skill tasks such as editing/evaluating a skill are confused with using the named skill;
- one domain-specific extractor may need acceptable-alternative adjudication.

Detailed report: `thesis_notes/results/Failure Mode Analysis - Qwen Full Local Schema Top100.md`.

## Historical Not-Done List (Superseded)

- Thesis integration of the frozen-v0.4 information-layer matrix.
- Per-source-family public-gold failure-mode analysis and representative examples.
- Targeted second-pass adjudication over non-core winners and strongest-method failures.
- Refinement of `M6-v1` field-aware procedural reranking, especially public-skill extraction/matching and failure analysis.
- Latency/cost comparison for top-20, top-50, and top-100 candidate budgets.
- Hybrid Qwen candidate text experiments, such as R2 first-stage plus full-skill rerank text.
- SkillRouter local smoke test: runner implemented at `skill_benchmark/scripts/run_skillrouter_selectors.py`. Local attempts on 2026-06-05 reached model loading but did not complete a tiny one-prompt CPU/MPS smoke test within a practical window on the 8 GB laptop. Treat local full-scale SkillRouter as currently impractical unless quantized or run on stronger hardware.
- SkillRouter hosted test: completed via Hugging Face Jobs on 2026-06-05 using `t4-small` after uploading a private 5.6 MB benchmark snapshot to `baechuer1/honour-thesis-skillrouter-benchmark-snapshot`. The reranker is not available as a normal Hugging Face Inference Provider model, so this was run as a custom GPU job rather than an ordinary provider API call.
- M4 tree routing.
- M5 graph retrieval.
- Full 1006-skill M0 cost/context stress test.
- Step 9 downstream artifact generation and grading.
- Final thesis results tables and written discussion.

## Historical Next Step (Superseded)

The text below records the pre-2026-07-26 plan. The current next step is to implement RQ2a A0-A14 from the canonical RQ2 tracker; do not use this historical list as an implementation queue.

Specifically:

- classify public-skill fields as observed, extractable, or proposed normalization using the completed heuristic/model disagreement adjudication;
- use the completed field-ablation results to freeze the final representation-field set;
- use the cleaned 144-prompt public-gold stratum for any final public-gold claims, with strict and acceptable labels separated;
- refine `M6-v1`, especially request-side extraction, public-skill field normalization, and field-to-field matching;
- run targeted second-pass adjudication on non-core winners and strongest-method failures;
- compare top-20, top-50, and top-100 latency/cost;
- decide whether top-100 is acceptable as a retriever/reranker budget;
- decide whether to add acceptable alternatives for domain-specific near-equivalents;
- then move to Step 9 downstream validation.

## SkillRouter Hosted Results

Run date: 2026-06-05. Hardware: Hugging Face Jobs `t4-small`. Models: `pipizhao/SkillRouter-Embedding-0.6B` and `pipizhao/SkillRouter-Reranker-0.6B`. Representation: full skill artifact. Rerank budget: top-20.

| Prompt set | Method | Top-1 | Accept top-1 | Top-5 | Accept top-5 | MRR | Non-main top-1 |
|---|---|---:|---:|---:|---:|---:|---:|
| Controlled, 137 prompts | SkillRouter full embedding | 73.0% | 75.9% | 94.2% | 94.9% | 0.827 | 14.6% |
| Controlled, 137 prompts | SkillRouter full embedding + SkillRouter rerank top-20 | 83.2% | 83.2% | 97.8% | 98.5% | 0.898 | 4.4% |
| Public-gold, 32 prompts | SkillRouter full embedding | 65.6% | 75.0% | 96.9% | 96.9% | 0.770 | 84.4% |
| Public-gold, 32 prompts | SkillRouter full embedding + SkillRouter rerank top-20 | 65.6% | 68.8% | 93.8% | 96.9% | 0.788 | 87.5% |

Interpretation:

- SkillRouter embedding alone is much stronger than generic Qwen full-skill embedding on the controlled set, which means the benchmark remains meaningful under a skill-specific dense retriever.
- SkillRouter reranking is now the strongest controlled result so far: 83.2% top-1 and 97.8% top-5.
- On public-gold cases, SkillRouter embedding is already strong. The reranker improves MRR slightly but does not improve strict top-1, and it lowers top-5 from 96.9% to 93.8%.
- This suggests that learned skill-routing models can capture substantial procedural signal from full artifacts, but they still do not eliminate all semantic/procedural confusion.
- The proposed field-aware methods should now be interpreted against SkillRouter as a strong domain-specific retrieve-and-rerank baseline.

## SkillRouter + M6-v1 Field-Aware Hybrid

Run date: 2026-06-05. Hardware: Hugging Face Jobs `t4-small`. First stage: `pipizhao/SkillRouter-Embedding-0.6B` over full skill artifacts. Reranker: local deterministic M6-v1 field-aware matcher. Summary artifact: `skill_benchmark/outputs/m6v1_skillrouter_hybrid_summary_2026_06_05.md`.

Best results:

| Prompt set | Candidate budget | Best field set | Top-1 | Top-5 | MRR | Non-main top-1 |
|---|---:|---|---:|---:|---:|---:|
| Controlled, 137 prompts | top-20 | `task_output_workflow` | 83.2% | 95.6% | 0.895 | 5.1% |
| Controlled, 137 prompts | top-100 | `task_output_workflow` | 86.9% | 98.5% | 0.927 | 0.7% |
| Public-gold, 32 prompts | top-20 | `task` / `core_boundary` | 62.5% | 93.8-96.9% | 0.765 / 0.762 | 62.5-68.8% |
| Public-gold, 32 prompts | top-100 | `task` | 62.5% | 93.8% | 0.765 | 68.8% |

Interpretation:

- This is now the strongest controlled result currently recorded.
- SkillRouter embedding gives excellent candidate recall, and explicit `task + output + workflow` field-aware reranking improves final top-1 beyond SkillRouter's own neural reranker on the controlled benchmark.
- The same reranker does not improve public-gold top-1. This is an important limitation: the current deterministic field matcher works well on controlled/extracted procedural fields, but it is not robust enough for messy externally authored skills.
- This strengthens the thesis direction: the contribution should not be "fields always win"; it should be "which procedural information helps, under which representation/extraction conditions, and where learned retrieval still needs interpretable procedural matching."
