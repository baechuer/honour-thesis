# Thesis Experiment Roadmap

> **2026-09-08 RQ2 formal plan approved.** The new master research plan is `thesis_notes/current/RQ2 Approved Research Plan - 2026-09-08.zh-CN.md`. First complete B36+C6 on the frozen 3,798-candidate / 1,077-query V7 scope; consider wiki/graph/tree and the optional small system afterwards. Approximately 20k additional background skills are a prospective scale-out study, not a current commitment or result. Actual local I1/I2 materialisation has started and replayed at 3,798 rows per view; continue I3/representation QA and runtime sealing before formal inference. Earlier discussion drafts remain provenance.

> **2026-09-08 RQ2b V7 frozen; core-first experiment preparation.** Final-freeze replay confirms 1,077 retained groups and 149 exclusions; all 3,798 primary source hashes replay from the prepared checkout. User priority is the 36-configuration first matrix, followed by six fixed-candidate diagnostics, then wiki/graph/tree extension assessment, then the optional self-designed system. No need to repeat acceptable-set review. Remaining work is V7-complete four-representation QA, dependency/exposure and runtime/budget sealing before inference. See `thesis_notes/current/RQ2 First Matrix and Architecture Extension Roadmap - 2026-09-08.md`. RQ1 and RQ2a results are unchanged; optional systems need not win or be built for the core comparison research to stand.

Date: 2026-09-04

> **RQ1 CLOSED; RQ2 IS THE NEXT ACTIVE RESEARCH STAGE (2026-09-04).** Selector execution, result analysis, researcher confirmation, thesis integration, concrete example insertion, and independent advisory review are complete. All 350 controlled, 194 scored public strict-gold, and 402 scored public removal-fidelity rows were approved (`946/946`), with exact decisions preserved under each stream's `decision_receipts/` directory in `skill_benchmark/rq1_human_review/2026-09-04/`. The workflow was unblinded: frozen labels were visible for controlled/public-gold confirmation and intact/removed documents were visible for removal fidelity. No further RQ1 experiment is required under the current scope. Remaining RQ1 tasks are final submission editing only: the formal AI-use declaration, optional relocation or compression of historical manuscript detail, and a final citation/count/claim check. The upstream counts 199 families and 574 transformations are processing pools, not the human-review denominators. Canonical status: `thesis_notes/current/RQ1/README.md`; completion checkpoint: `thesis_notes/checkpoints/methods/RQ1 Prospective Researcher Confirmation Complete - 2026-09-04.md`. Older dated roadmap entries below are retained for provenance and do not reopen RQ1.

> **2026-09-04 unified RQ1 reporting (`THESIS LATEX/PDF UPDATED / COMPILE AND VISUAL CHECK PASS`).** The final RQ1 presentation uses two complementary experiments: controlled field isolation establishes that each tested operational field can supply a near-neighbour distinction when it is the only candidate-specific information; the Round-3 public original-document intervention tests whether removing cited information from natural artifacts weakens strict routing. The thesis-facing public result is the latter, not the earlier derivative field-card ablation. The evidence boundary is field-tiered: use condition and success/verification are cross-retriever stable individual removals; task specification and execution/verification are cross-retriever stable joint removals; other individual fields are retriever-conditional; boundary/not-for has no stable positive strict Top-1 effect. Examples/tests are a controlled negative control only. The field-card result remains historical sensitivity and is not pooled with the original-document result. Canonical synthesis: `thesis_notes/current/Results Writing Packet - 2026-09-04.md`.

> **2026-09-04 RQ1 public-original group-removal extension (`HISTORICAL PRE-CLOSURE CHECKPOINT / SUPERSEDED BY RQ1 CLOSURE`).** The current source-original twin is single-field only; this separate supporting extension tests task specification (use/input/output), execution/verification (workflow/success) and applicability/capability (boundary/dependency) as three exact-union source-document deletions. The independently validated freeze has 99, 138 and 132 composition-family cases respectively (369 total; 1,476 paired ranking rows per retriever). BM25 finds positive Full-minus-Removed Hit@1 effects for all three: +0.266 [+0.196, +0.336], +0.176 [+0.094, +0.262] and +0.136 [+0.087, +0.186]. The authorised Qwen dense twin finds +0.088 [+0.005, +0.162], +0.074 [+0.007, +0.141] and +0.014 [-0.043, +0.062]. Task specification and execution/verification are therefore stable under both first-stage retrievers; applicability/capability remains retriever-conditional. Qwen sent only the 342 preflight-missing group documents, no queries, in 35 successful no-retry calls; 283,526 provider-reported input tokens. At this checkpoint the package still awaited user review and thesis writing; the closure block above records their later completion. This is not the completed August extracted-card group study and cannot attribute a joint effect to one member. SOP: `thesis_notes/current/RQ1/protocols/RQ1 Public Original Round 3 Joint Group Extension SOP - 2026-09-04.md`; checkpoints: `thesis_notes/checkpoints/methods/RQ1 Public Original Round 3 Joint Group BM25 Result - 2026-09-04.md`, `thesis_notes/checkpoints/methods/RQ1 Public Original Round 3 Joint Group Qwen Result - 2026-09-04.md`.

> **2026-09-04 RQ1 public-original clean-only twin (`HISTORICAL PRE-CLOSURE CHECKPOINT / SUPERSEDED BY RQ1 CLOSURE`).** The frozen source-original RQ1 removal experiment completed two independently validated first-stage retrieval twins: local BM25 and DashScope international Qwen `text-embedding-v4` (1024). Both score the same 1,078 composition-family cases, direct/paraphrase pairs, candidate order and singleton golds, comparing an exact original public source to its exact one-field-removed Round-3 mask. Qwen completed under the explicitly authorised sealed payload with 1,898 newly embedded texts, 190 successful no-retry calls and local persistent caching. At composition level, use condition and success/verification show stable positive Full-minus-Removed Hit@1 effects under both retrievers; BM25 also shows stable positive effects for input/precondition, output/artifact, workflow/procedure and dependency/resource. Boundary/not-for is not stably positive in either twin. At this checkpoint the result still awaited user review; the closure block above records its later review and thesis integration. The retriever scores remain separate and are not pooled. Evidence: `thesis_notes/checkpoints/methods/RQ1 Public Original Round 3 Twin Result and Failure Analysis - 2026-09-04.md`.

> **2026-09-04 RQ1 public-original Qwen twin (`F2 PREFLIGHT COMPLETE / HISTORICAL PRE-EXECUTION STATE`).** The dense twin had a sealed local-only payload from the identical Round-3 clean-only freeze: 1,510 unique full/masked candidate documents plus 388 unique frozen queries, 1,898 total cache-miss texts, local token proxy 1,341,769, maximum 190 no-retry requests, and payload SHA-256 `38a8bab9938f884390caae6c0c062aac7ff7d08510b7e380156cf7fa6dba16d2`. It passed hash/inventory/zero-network validation before execution. This historical status is superseded by the F1--F3 completion entry above. Evidence: `thesis_notes/checkpoints/methods/RQ1 Public Original Round 3 Qwen Preflight - 2026-09-04.md`.

> **2026-09-04 RQ1 public-original clean-only BM25 (`F1 COMPLETE / QWEN TWIN NEXT`).** The frozen local BM25 test has completed and its 4,312 result rows plus composition-level paired analysis passed independent validation. Full-document removal is associated with 0.091--0.151 Hit@1 reductions for use condition, input/precondition, output/artifact, workflow/procedure, success/verification and dependency/resource; all corresponding 95% paired-bootstrap intervals are positive. Boundary/not-for is a non-stable Top-1 result (+0.024, [-0.014, 0.064]) even though its lexical margin declines. This is the first retriever-specific RQ1 evidence, not a final cross-retriever claim. Next: build an unsent, exact Qwen preflight from the identical freeze, obtain explicit payload authorisation, run the dense twin, then compare retrievers without pooling their native scores. Evidence: `thesis_notes/checkpoints/methods/RQ1 Public Original Round 3 BM25 Result - 2026-09-04.md`.

> **2026-09-04 RQ1 public-original clean-only scoring frame (`F0 FREEZE COMPLETE / LOCAL BM25 NEXT`).** The method decision is now frozen: do not perform a fourth forced-removal round. Test only field-specific composition-family cases in which all candidates are canonical Round-3 `CLEAR`, exact original/mask hashes validate, and the old strict roster provides one frozen singleton gold with both direct and paraphrase prompts. This yields 1,078 composition-family cases / 2,156 prompt rows, corresponding to 49--69 independent source compositions per field; direct/paraphrase and multiple families are repeated structure, not independent samples. The primary analysis will average within composition then use a composition-clustered paired bootstrap for `FULL_ORIGINAL - REMOVE_<FIELD>_R3`. The deterministic local BM25 runner has passed a synthetic test and a no-scoring dry run planning 4,312 paired ranking rows. Next: run it against the frozen inputs, validate full paired row coverage, then prepare an unsent Qwen payload for separate approval. Protocol: `thesis_notes/current/RQ1/protocols/RQ1 Public Original Round 3 Clean-Only Scoring Freeze and Test SOP - 2026-09-04.md`; checkpoint: `thesis_notes/checkpoints/methods/RQ1 Public Original Round 3 Clean-Only Scoring Freeze - 2026-09-04.md`.

> **2026-09-04 RQ1 exhaustive public-original ablation (`FORCED-REMOVAL ROUND 3 COMPLETE / NO SCORING`).** The fresh blind Round-3 ledger now covers the entire 82-composition frame: 574/574 field units and 1,855/1,855 candidate cards. Parent validation found exactly one canonical record per expected unit, zero identity/field/candidate-label discrepancies, and 574/574 individual schema/evidence validation passes. Candidate judgments are 1,609 `CLEAR`, 232 `RESIDUAL`, and 14 `UNCERTAIN`; 439 units are fully clear across all candidates. The field-specific fully-clear counts are 77 boundary/not-for, 55 dependency/resource, 58 input/precondition, 55 output/artifact, 65 success/verification, 62 use-condition and 67 workflow/procedure, each out of 82. This clears the audit stage but is not an effect estimate. It shows that repeated evidence-cited deletion can increase the candidate-card clearance rate while some public-document field overlap remains. No retrieval, external API, hosted work, metric calculation or thesis/PDF result writing is authorised. A next scoring step needs a separately frozen clean-only denominator; an additional forced-removal round would need a distinct method decision. Checkpoint: `thesis_notes/checkpoints/methods/RQ1 Public Original Exhaustive Ablation Forced Removal Round 3 Completion - 2026-09-04.md`.

> **2026-09-04 RQ1 exhaustive public-original ablation (`FORCED-REMOVAL ROUND 3 TECHNICAL MATERIALISATION COMPLETE / FRESH BLIND CLEARANCE ACTIVE / NO SCORING`).** The Round-3 representation deletes only the 573 exact lines cited by the 383 canonical Round-2 `RESIDUAL` records. It covers all 574 units / 1,855 candidate cards. Round-2 `CLEAR` (1,464 cards) and `UNCERTAIN` (8 cards) are copied byte-for-byte; only cited residual cards are changed. The local exact-diff audit found zero failures. This is still a routing-only transformation: it may damage a skill document and does not prove all target information is gone. Fresh prompt/gold/source-map/selector-blind clearance is now active. Routing, external APIs, hosted work, metrics, and thesis/PDF writing remain locked until a later complete-case decision. SOP: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/FORCED_REMOVAL_ROUND3_SOP.md`; checkpoint: `thesis_notes/checkpoints/methods/RQ1 Public Original Exhaustive Ablation Forced Removal Round 3 Technical Materialisation - 2026-09-04.md`.

> **2026-09-04 RQ1 exhaustive public-original ablation (`FORCED-REMOVAL ROUND 2 COMPLETE / NO SCORING`).** The complete fresh blind ledger covers all 574 units / 1,855 cards from the 82-composition frame. Parent validation passed all canonical records: 1,464 `CLEAR`, 383 `RESIDUAL`, and 8 `UNCERTAIN`; 377 units are clear for every candidate. Round 2 is a clearance result only: it shows that all known Round-1 residual spans can be removed deterministically but that public-document field overlap remains in 383 line-addressable and 8 uncertain cases. The next local-only step is Round-3 materialisation from the 383 cited spans, followed by a new exact-diff audit and fresh blind clearance. No retrieval, API, hosted, metric, or thesis/PDF action is authorised. Checkpoint: `thesis_notes/checkpoints/methods/RQ1 Public Original Exhaustive Ablation Forced Removal Round 2 Completion - 2026-09-04.md`.

> **2026-09-04 RQ1 exhaustive public-original ablation (`FORCED-REMOVAL ROUND 2 SERVICE-BLOCKED PARTIAL CLEARANCE / NO SCORING`).** Fresh blind clearance has been validated and canonicalised for `OR82-001--070`: 490/574 field units, 70/82 compositions, and 1,589/1,855 candidate cards. The verified partial ledger contains 1,229 `CLEAR`, 358 `RESIDUAL`, and 2 `UNCERTAIN` candidate decisions; 312 units have every candidate clear. The remaining `OR82-071--082` (84 units / 266 cards) are unreviewed and cannot be inferred in either direction. On 2026-09-04, all new fresh-reviewer launches failed before packet access with the same Codex backend `404`; no failed agent wrote an output. This blocks only the remaining clearance work. It is not an experimental finding and does not authorise retrieval, API, hosted, metric, or thesis/PDF action. Resume with fresh reviews for the 12 missing compositions, then build a Round-3 deletion plan from canonical Round-2 residual evidence. Checkpoint: `thesis_notes/checkpoints/methods/RQ1 Public Original Exhaustive Ablation Forced Removal Round 2 Service-Blocked Checkpoint - 2026-09-04.md`.

> **2026-09-03 RQ1 exhaustive public-original ablation (`FULL BLIND CLEARANCE ROUND 1 COMPLETE / NO SCORING`).** The frozen primary frame contains 82 compositions, 265 source artifacts, and 574 composition-field units. It retains 265 paths and 264 unique byte hashes because one pair is byte-identical. Full local materialisation created 574 single-field and 246 joint conditions (2,650 candidate masks), all exact-diff-audited with zero unlogged edits. Independent prompt/gold/source-map-blind clearance now covers all 574/574 units and 1,855 candidate masks: 710 `CLEAR`, 1,145 `RESIDUAL`, 0 `UNCERTAIN`; every canonical record passed the exact-span validator before ingest, and the canonical output directory has 574 files. W015-B01 remains a recorded non-adopted duplicate. No-op and near-empty masks remain in the audit rather than being excluded. Retrieval and external execution remain locked: clearance is not a routing result or a frozen scoring denominator. See `thesis_notes/checkpoints/methods/RQ1 Public Original Exhaustive Ablation Full Clearance Round 1 Completion - 2026-09-03.md` and the full-clearance SOP.

> **2026-09-03 RQ1 exhaustive public-original ablation (`FORCED-REMOVAL ROUND 2 IN FRESH CLEARANCE / NO SCORING`).** The new Round-2 routing-only representation takes each immutable Round-1 mask and deletes every exact residual span independently cited in the completed Round-1 ledger. All 574 units / 1,855 candidate cards were materialised; all 1,145 Round-1 residual cards were processed, deleting 6,480 evidence-cited lines. An independent exact-diff audit passed with zero failures: every cited span matched before deletion, every required line was blanked, and no non-ledgered Round-1 text changed. This transformation can make a skill damaged or non-executable by design; it tests whether the removed information has routing value, not whether the edited artifact can run. Fresh anonymous prompt/gold/source-map/selector-blind clearance is now required before any clean-isolation selector score, with non-cleared cards retained as an overlap stratum. SOP: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/FORCED_REMOVAL_ROUND2_SOP.md`; materialisation ledger: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/forced_round2_masks/FORCED_ROUND2_MASK_MANIFEST.json`; local audit: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/forced_round2_masks/audit/exact_diff_audit.json`.

> **2026-09-03 RQ1 exhaustive public-original ablation (`FORCED-REMOVAL ROUND 2 PARTIAL FRESH-CLEARANCE CHECKPOINT / NO SCORING`).** The shared-output blind-review and main-thread revalidation procedure has canonicalised 98/574 units, covering 322 candidate cards. The current verified subset contains 245 `CLEAR`, 77 `RESIDUAL`, and 0 `UNCERTAIN` candidate decisions; 58 unit cards are fully clear across all candidates. This is a partial audit checkpoint only. It confirms that known Round-1 residual deletion is useful but not complete: new target-field values are still recoverable in some cards and require separately cited, future forced removal. It does not authorise BM25, Qwen, APIs, hosted work, metrics, or thesis/PDF result writing. The next bounded protocol task is to complete fresh clearance for the remaining 476 units, starting by re-running OR82-001--OR82-005 under the shared-output implementation, then continuing OR82-020 onward. Canonical evidence: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/forced_round2_clearance/canonical_round2/`.

> **Historical pilot only (`SUPERSEDED AS THE PRIMARY STATUS`).** The 14-unit / 49-candidate target-clear pilot is retained for development provenance but is not the current public-original denominator or a completion claim. The full 574-unit clearance status above controls all next steps.

> **2026-08-31 RQ1 public-corpus consolidation.** Future public RQ1 cluster
> work starts from one 82-composition source registry, not separate V2 and V3
> pools. Every new method first applies its own fixed eligibility audit to that
> registry, then freezes one complete-case scoring subset; no completed matrix
> may be silently enlarged. The currently completed public-card result remains
> 46 scored compositions / 99 routing families / 198 prompts. See
> `thesis_notes/current/RQ1/supporting/RQ1 Public Corpus Consolidation Policy - 2026-08-31.md`.

> **2026-08-31 RQ1 merged-registry parse (`S0 COMPLETE / LOCAL ONLY`).** A new,
> non-overwriting parse root contains the canonical 82 source compositions and
> 265 verified original documents. The 76 historical source-only parses are
> reused only after hash, source identity and seven-field schema checks; the
> six V3 additions have fresh source-only evidence extraction. The completed
> ledger has 1,860 exact evidence spans and a zero-failure source hash/schema/
> line-range/quote-substring audit. This is a
> preparation and eligibility step, not a mask, retrieval, embedding or
> routing-result stage. The two V3 partial-prompt compositions remain in the
> source parse but cannot enter a later complete-case selector denominator
> without a separately frozen decision. Root:
> `skill_benchmark/rq1_public_original_removal_v3_82_registry/`.

> **2026-08-31 RQ1 original-document 82-registry eligibility (`S1 COMPLETE / SOURCE-ONLY / NO SCORING`).** The candidate-field removal-map gate completed across the merged 82/265 original-source frame. Mappers saw only anonymous originals and exact direct-value evidence. Mechanical validation produced 21 map-ready use-condition, 19 input/precondition, 25 output-artifact, 22 workflow/procedure, 32 success/verification, 37 boundary/not-for and 27 dependency/resource composition-field conditions. All remaining conditions are retained as `ORIGINAL_ONLY` or `NO_EDITABLE_VALUE`, not silently repaired. `MAP_READY` remains only a materialisation prerequisite: exact-diff auditing, independent prompt/gold-blind residual review, strict-family linkage and a frozen complete-case denominator are still required before any BM25 or Qwen experiment can be proposed. The earlier 76-composition redaction closure remains historical feasibility evidence; this new pass does not erase it. Protocol: `thesis_notes/archive/RQ1/original-document-lineage/RQ1 Public Original-Document 82 Registry Removal Amendment - 2026-08-31.md`; checkpoint: `thesis_notes/checkpoints/methods/RQ1 82 Registry S1 Eligibility Closure - 2026-08-31.md`.

> **2026-08-31 RQ1 original-document 82-registry materialisation (`S2 COMPLETE / LOCAL TECHNICAL ONLY / PENDING BLIND RESIDUAL REVIEW`).** All 750 candidate-mask rows passed independent source-hash, reconstruction and no-unlogged-diff checks. The single fields cover 19--37 compositions; technical group materialisations cover 5 task-specification, 18 execution/verification and 22 applicability/capability compositions, with one task-specification edit conflict excluded. This is implementation integrity only, not a claim that a field has been semantically removed. S3 now reviews anonymous single-field masks without prompt/gold/source-map access; a group can survive only when all audited component singles survive. SOP: `thesis_notes/archive/RQ1/original-document-lineage/RQ1 Public Original-Document S3 Blind Residual Review SOP - 2026-08-31.md`.

> **2026-08-31 RQ1 original-document 82-registry residual closure (`S3 COMPLETE / FEASIBILITY CLOSED / NO SCORING`).** The prompt/gold/source-map-blind residual audit reviewed all 183 materialised single-field composition conditions in 61 canonical batches. Only 33 conditions cleared: 2 use-condition, 2 input/precondition, 3 output-artifact, 0 workflow/procedure, 11 success/verification, 15 boundary/not-for and 0 dependency/resource. No task-specification, execution/verification or applicability/capability group survives because each group includes at least one non-clear component field. The frozen full-original intervention therefore has no adequate complete-case denominator for the intended seven-field/three-group BM25 or Qwen comparison; strict-family linkage and selectors are not run. This says that semantic field deletion from natural full documents is difficult under the non-broadening rule, not that those fields lack routing value. Evidence: `skill_benchmark/rq1_public_original_removal_v3_82_registry/blind_residual_ledger/`; checkpoint: `thesis_notes/checkpoints/methods/RQ1 82 Registry S3 Blind Residual Closure - 2026-08-31.md`.

> **2026-08-31 RQ1 public-original information-removal feasibility audit (`CLOSED / NO SCORING`).** This full-document extension attempted to remove a field's documented candidate-distinguishing values from hash-verified public originals without widening capability. A source-only first pass found `35 residual / 7 clear` across 42 stratified composition-condition items. The 35 residual items received a second source-only mapping pass: 3 were unsafe mixed carriers, 1 had an edit conflict, and 31 rebuilt masks passed exact-diff audit. A fresh prompt/label-blind residual review then found `28 residual / 3 clear`. The clean count is inadequate for the planned single-field/group BM25 or Qwen denominators, so selector stages are not run. This audit does not estimate routing effects and does not replace the completed derivative public-card RQ1b experiment. See `thesis_notes/checkpoints/methods/RQ1 Public Original-Document Redaction Feasibility Closure - 2026-08-31.md` and `thesis_notes/archive/RQ1/original-document-lineage/RQ1 Public Original-Document Information-Removal Execution SOP - 2026-08-31.md`.

> **2026-08-31 RQ1 public-original information-removal execution (`S0 SOURCE-ONLY PARSE ACTIVE / NO SELECTOR OR EXTERNAL EMBEDDING EXECUTION`).** The public RQ1 comparison will remove explicit candidate-distinguishing values for one field from complete frozen originals while retaining task/method identity. The edited document may no longer be executable: RQ1 asks whether removing that documented information weakens routing, not whether the edited document can still run. A removal may not invent a broader capability, such as replacing a PDF-only requirement with “any file.” S0 now materialises anonymous, hash-verified source packets and parses the seven fields without prompts, gold labels, or results. Single-field removals, group removals, retrieval, and external embedding remain later gated steps. See `thesis_notes/archive/RQ1/original-document-lineage/RQ1 Public Original-Document Redaction Amendment - 2026-08-31.md` and `thesis_notes/archive/RQ1/original-document-lineage/RQ1 Public Original-Document Information-Removal Execution SOP - 2026-08-31.md`.

> **2026-08-31 CFTC-001 original-document feasibility gate (`FIELD_MASK_REJECT / NO SCORING`).** The first fresh prompt-blind intake was rejected before masks were drafted. Two of its three public candidates encode the target PDF/input property in their skill identity, title, trigger, and core workflow, so a full-document input mask would create a different skill. This is retained as an auditable feasibility rejection rather than an experimental data point. Future source-only intakes must require a separately documented operational requirement that can be neutralised without redefining the candidate task. Evidence: `skill_benchmark/rq1_public_original_mask_v1/formal_queue/CFTC-001_input_precondition/INDEPENDENT_FEASIBILITY_REVIEW.md`.

> **2026-08-31 CFTC-002 original-document feasibility gate (`FIELD_MASK_REJECT / NO SCORING`).** A second prompt-blind triad from molecular pathway analysis also failed before mask drafting. Its gene-list, ranked-score, expression-matrix, group-file, and saved-result requirements define the methods' executable modes, so removing every input cue would create an incoherent or different skill. CFTC-002 confirms that the strict full-document `input_precondition` intervention needs redesign rather than a larger source sweep. It is a feasibility finding only; no selector, external service, or thesis/PDF result was run. Evidence: `skill_benchmark/rq1_public_original_mask_v1/formal_queue/CFTC-002_input_precondition/MAPPER_RUN_RECORD.md`.

> **2026-08-30 RQ1 public-original masking pilot (`USER-APPROVED / LOCAL ONLY`).** The user approved the CFTC-064 full-original `input_precondition` masking convention after inspecting original documents, masks, source spans, and residual-cue checks. It will test complete frozen `SKILL.original.md` documents, not derivative cards, by comparing each intact original with a version where all mapped target-field evidence is removed or minimally neutralised from every candidate document. CFTC-064 remains technical only because pilot selection was not prompt-blind. The next permitted action is a fresh source-only, prompt-blind mapping packet followed by a separate residual review and user-facing composition review. No retrieval, embedding, external transfer, hosted work, or thesis/PDF write is in scope. It does not alter existing card-mask outputs. Protocol and approved pilot: `thesis_notes/archive/RQ1/original-document-lineage/RQ1 Public Original-Document Field-Masking Pilot Protocol - 2026-08-30.md` and `skill_benchmark/rq1_public_original_mask_v1/pilot/CFTC-064_input_precondition/`.

> **2026-08-30 RQ1b V3 Wave 034 public-source intake.** Thirty-six
> navigation leads produced 17 commit-pinned roots, a deterministic 456-path
> roster and 456 exact-once public raw captures (all successful; zero retry).
> Frame-wide SHA-256 deduplication retained 342 historical aliases and froze
> 114 byte-distinct public originals. These additions are only an auditable
> provenance pool under prompt-free source-only T0 review; they do not change
> the live strict V3 cohort of **37 frozen compositions / 231 prompt cases**.
> Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 034 Public Source
> Intake - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 033 C4A--C6 strict closure.** A pathway-input
> triad completed source-only C1 evidence, six low-risk C2/C3 prompt cases,
> literal seven-slot cards, two key-blind C4B adequacy reviews, C5 sealed
> target reconciliation and C6 lineage freezing. The original canonical-card
> fidelity failure and a malformed builder schema return are retained; only an
> r1 exact-builder-quote amendment enters the passing chain. It records 6/6
> singleton agreements and target matches, with six low-risk cases and zero
> exclusions. V3 is now **37 frozen compositions / 231 strict prompt cases**.
> This is curation only, not a human-label, selector, metric or retrieval
> result. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 033 C4A-C6
> Strict Freeze - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 032 C4A--C6 strict closure.** The security,
> user-research, and visual/documentation survey triad completed literal
> seven-slot card preservation, two key-blind C4B adequacy reviews, C5 sealed
> target reconciliation and C6 source/ledger freezing. The original C4A
> nonliteral-quote failures and initial C4B trailing-space audit failure are
> retained; only exact-span source cards and a mechanical evidence-space
> amendment entered the passing chain. The r1 audit records 6/6 singleton
> agreements, 6/6 target matches, six low-risk strict cases and zero
> exclusions. V3 is now **36 frozen compositions / 225 strict prompt cases**.
> This is curation only, not a human-label, selector, metric or retrieval
> result. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 032 C4A-C6
> Strict Freeze - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 032 multi-root public-source intake.** Five
> commit-pinned roots produced 171 one-shot raw captures; SHA-256 deduplication
> froze 85 byte-distinct public originals (80 historical aliases and 6
> within-wave aliases retained). Five source-only T0 groups covering 19
> artifacts are in independent structural review. This is no prompt/no-label
> provenance and triage work, not a cluster or result; at its intake closure
> V3 was **35 frozen compositions / 219 strict cases**. Evidence:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 032 Public Source Intake - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 031 C1--C3 curation closure.** Two framework
> compositions passed source-only evidence but neither met complete C2/C3
> candidate symmetry needed for C4 strict adequacy: orchestration had 0/6
> cue-safe task positions, and RAG had 2/6. They are retained as a negative
> strict-public-cluster feasibility result only; no selector or RQ1 effect was
> estimated, and the V3 count remains **35 / 219**. Evidence:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 031 C1-C3 Curation Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 031 pinned public-source intake.** Four
> commit-pinned public roots yielded 482 body-free `SKILL.md` paths and a
> deterministic 313-path roster. The one-shot raw capture completed 313/313;
> full-frame byte deduplication admitted 100 original bodies and retained 213
> aliases. A source-only local inventory, lexical reading aid and ten
> non-overlapping prompt-free T0 triads now support bounded structural review.
> This does not create a cluster or result; V3 remains **35 frozen
> compositions / 219 strict cases**. The unexpectedly single-root novel-body
> origin is a discovery-diversity limitation to address before a later source
> wave. Evidence:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 031 Public Source Intake Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 029 C4A--C6 closure.** The UI-design triad
> completed C4A canonical source cards, anonymous C4B two-reviewer adequacy
> review, C5 sealed-target reconciliation and C6 source/ledger hash freeze.
> One non-exact reviewer quote received a preserved, single-packet fresh
> key-blind correction; the amended audit has 6/6 exact singleton agreements,
> 6/6 target matches, six low-risk strict prompt cases and zero exclusions.
> The V3 source-frame cohort now contains **35 frozen compositions / 219
> strict prompt cases**. This is curation only, not a human-label, selector,
> metric or retrieval result; it is not combined with the historical
> cross-source-campaign count. Evidence:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 029 C4A-C6 Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 030 broad multidomain intake.** M0 preserved 285
> public navigation leads across 16 lanes and six one-shot 403 failures;
> M1 pinned 21 roots and observed 453 paths without reading bodies. A
> deterministic 108-body capture then froze 53 byte-distinct originals after
> 55 clean-frame aliases. The local lexical list is descriptive only. No D1,
> prompt, gold, selector or metric work exists; strict total remains 34/213.
> Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 030 Broad Multidomain Public Source Intake - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 029 targeted supplemental intake.** Five
> one-shot public `SKILL.md` captures passed local byte rehash, full clean-frame
> SHA-256 deduplication and additive source-frame freeze (5 novel, 0 aliases,
> 0 failures). The W27/W29 UI-design triad reached audited D1 `READY_FOR_C1`
> consensus and one prompt-free C1 packet with a passing source-binding and
> principal literal-chain finaliser. C2 binding passed six source-informed
> drafts. Both blind C3 reviewers required cue-only shortening of bundled
> source details; both fresh C3R1 reviewers allowed all six revised requests
> as low-risk operational wording. C4A is now pending under the unchanged
> shared-template/mixed-domain exclusions. Wave 028 remains quarantined. No
> strict label, selector or metric work was started; total remains 34/213.
> Evidence:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 029 Targeted Supplemental Public Source Intake - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 028 capture quarantine.** A 243-URL public-source
> intake was contaminated when a detached capture process overlapped its
> resume: the manifest holds 362 records and 119 duplicate URLs. It is
> retained for audit but contributes zero frozen sources, cluster candidates,
> prompts, golds, selectors, metrics or results. The official strict total
> remains 34 compositions / 213 packets. Resume recruitment only from clean
> prior amendments; a later discovery wave needs non-overlapping capture.
> Record: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 028 Capture Quarantine - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 027 intake status.** A targeted pinned-repository
> route captured 289 public originals once and froze 235 byte-distinct source
> additions after full-frame SHA-256 deduplication (54 prior aliases, zero
> within-wave aliases). The local inventory and lexical pretriage are
> descriptive only. No D1/C1 composition, prompt, gold, selector, metric or
> retrieval result exists. The official strict total remains 34 compositions /
> 213 packets. Continue discovery-first recruitment under unchanged C1--C6
> gates. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 027 Targeted Public Source Intake - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 026 intake status.** A new broad pinned-repository
> route captured 197 public originals once and froze 172 byte-distinct source
> additions after full-frame SHA-256 deduplication (25 prior aliases, zero
> within-wave aliases). The local inventory and lexical pretriage are
> descriptive only. No D1/C1 composition, prompt, gold, selector, metric or
> retrieval result exists. The official strict total remains 34 compositions /
> 213 packets. Continue discovery-first recruitment under unchanged C1--C6
> gates. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 026 Broad Public Source Intake - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 025 intake status.** A broad pinned-repository
> route captured 230 public originals once and froze 198 byte-distinct source
> additions after full-frame SHA-256 deduplication (31 prior aliases, one
> within-wave alias). The local lexical pretriage is descriptive only. The
> health-digest family closed before D1 because valid, convergent source-only
> evidence was unavailable; short-form product ads are `LIKELY_NONPARALLEL`,
> and frame-extraction/analysis/transcription is component/granularity-
> confounded. No new cluster, prompt, gold, selector, metric or retrieval
> result exists. The official strict total remains 34 compositions / 213
> packets. Continue discovery-first recruitment under unchanged C1--C6 gates.
> Records:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 025 Broad Public Source Intake - 2026-08-30.md`
> and `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_025_2026-08-30/source_only_triage/HEALTH_DIGEST_TRIAD_CLOSURE_2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 024 closure.** This large public-source intake
> yielded 87 additive original artifacts, not 87 clusters. The only
> source-only triad reaching C4A failed closed: two independent, literal-valid
> anonymous builder cards jointly omitted a qualifying original workflow span,
> so the v1.2 completeness rule prohibits canonical-card repair and C4B--C6.
> The concurrent-capture incident is explicitly quarantined and provenance
> closure rehashes the 232 permitted bodies. The official strict total remains
> 34 compositions / 213 packets. Continue discovery-first recruitment with
> unchanged C1--C6 gates; do not relax card completeness to increase yield.
> Record: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 024 Source Intake And C4A Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 023 source-intake closure.** An alternate,
> pinned-repository public-source route completed 145 successful raw captures
> without executing source code. Byte-level deduplication left one new
> healthcare router and 144 already-frozen aliases. The new router is retained
> as provenance but has no same-wave 3--4 peer composition, so it enters no
> D1/C1 review. The official strict total remains 34 compositions / 213
> packets. Continue fresh public discovery under unchanged peer-role and
> singleton gates. Record:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_023_2026-08-30/README.md`.

> **2026-08-30 RQ1b V3 Wave 021 strict-screen closure.** Seventy-one
> byte-distinct public additions supplied a large source pool, not 71 clusters.
> Eight source-only screens rejected containers, lifecycle components, broad
> substitutes and unrelated deliverables. The sole finance triad to enter C1
> had literal support but an unresolved Controller--FP&A peer-role conflict;
> it was rejected fail-closed before prompt construction. Thus 0 C2--C6
> advances and the official strict total remains 34 compositions / 213 packets.
> Continue public-source discovery under unchanged peer-role rules. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 021 D1-C1 Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 022 navigation status.** Targeted public-source
> metadata discovery produced 644 M0 leads, but all 40 predeclared M1 tree
> attempts failed and were retained without retry. No skill body, source-frame
> amendment or candidate composition exists in Wave 022. Use a later distinct
> discovery route rather than rerunning these failed M1 attempts. Record:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_022_2026-08-30/README.md`.

> **2026-08-30 RQ1b V3 Wave 019 C1--C4A closure.** Eighty-four byte-distinct
> source additions supported two carefully screened candidate compositions.
> Both passed source-only C1 and C3 cue control, but both stopped at C4A when
> two independent conformance reviews found that literal-valid cards did not
> preserve all qualifying workflow, verification or boundary evidence from the
> original artifacts. This is an evidence-card completeness stop, not a claim
> against the source skills or a retrieval result; no C4B/C5/C6 case exists.
> The official strict total remains 34 compositions / 213 packets. Continue
> discovery-first recruitment under unchanged completeness gates. Checkpoint:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 019 C1-C4A Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 020 initial triage.** The 78 additive public
> originals are an intake pool, not a count of valid clusters. Five initial
> source-only groups were rejected before C1 as lifecycle stages, components
> or distinct deliverables; continued public-source search and local triage is
> the current gate. Log:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_020_2026-08-30/source_only_triage/W20_INITIAL_TRIAGE_LOG.md`.

> **2026-08-30 RQ1b V3 Wave 018 duplicate-only intake result.** Thirty public
> Kubernetes/platform-operation originals were captured once and all 30 were
> byte-identical to source bodies already frozen in the immutable frame plus
> Waves 009--017. This produces no amendment and no D1/C1--C6 candidate: it is
> a provenance deduplication result, not a routing or cluster-quality result.
> The official strict total remains 34 compositions / 213 packets. Continue
> fresh-source discovery rather than treating an alias capture as new evidence.
> Record: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 018 Duplicate-Only Source Intake Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 017 source-screen result.** Nineteen public
> sources were captured once: seven byte-distinct originals enter a separate
> provenance amendment and 12 are already-frozen aliases. The source-only
> screen rejects five plausible families before C1 because they are pairs
> without a natural third peer, containers, downstream uses, or nonparallel
> input/output routes. The official strict total remains 34 compositions / 213
> packets. Continue discovery-first recruitment without turning any pair or
> component into a strict triad. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 017 Source Intake and Triage Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 016 C4A feasibility closure.** One GitHub
> Actions triad passed C1 and C3, but failed C4A: both literal-valid anonymous
> source-card builders omitted qualifying original-source spans, and two
> independent conformance reviewers rejected the packet because v1.2 forbids
> inventing or principal-repairing those spans. It creates no C4B review, C5
> seal, C6 case, strict label, representation, selector input or metric. The
> official strict total remains 34 compositions / 213 packets. Continue
> cross-origin discovery without loosening field-card completeness. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 016 C1-C4A Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 013 strict-screen result.** A new 56-lead,
> cross-origin intake completed single-attempt byte capture and source-frame
> deduplication: 37 are existing aliases and 19 are additive, byte-distinct
> public originals. Three source-bound compositions advanced to C1, but all
> were rejected: security review mixed two adequate end-to-end reviews with a
> scanner; compliance mixed overlapping GDPR routes with a broad container;
> presentation authoring mixed a PPTX parent container with two deck routes.
> Thus 0 C2 advances and 0 new C1--C6 parents exist. Continue discovery-first
> recruitment without lowering strict peer or singleton rules. Full record:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 013 Cross-Origin Source Discovery and C1 Checkpoint - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 012 strict-screen result.** Thirty new
> cross-origin public leads were fetched once: 29 readable sources yielded 11
> byte-distinct additions after deduplication against all frozen frames, while
> one 404 remains as a retained non-retried failure. Two D1 compositions reached
> source-only C1 (generic code review and data visualisation). Both were
> rejected because broad task similarity concealed containers, implementation
> architectures, or operating modes rather than parallel peer routes. No C2
> prompt construction, strict label, representation, selector, metric or
> retrieval result follows from this screen. Evidence:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_012_2026-08-30/`
> and `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_012_2026-08-30/`.

> **2026-08-30 RQ1b V3 Waves 009--011 discovery checkpoint.** The additive
> source frame has gained 100 byte-distinct public originals (88 in Wave 009,
> six in Wave 010, and six in Wave 011). This is not progress toward a count
> of 100 valid clusters. The only two new D1 drafts advanced to source-only C1
> were rejected as non-parallel: their artifacts differed as broad containers,
> specialised implementations, or preparation workflows. Wave 011's entire
> public catalog added only six unique files and all were from one origin, so it
> supplied no same-wave cross-origin composition. Continue discovery with
> cross-origin, common-envelope candidates; C1--C6 remain unchanged and no
> prompt, strict label, selector, metric or retrieval input has been created.
> Records: `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_009_2026-08-30/`,
> `d1_source_intake_wave_010_2026-08-30/`, and
> `d1_source_intake_wave_011_2026-08-30/`.

> **2026-08-30 RQ1b V3 priority gate.** Pause new public-source recruitment
> and first finish C4A--C6 on the nine already materialised anonymous packets.
> This is now complete: C6 froze 14 strict prompt cases across three parents,
> with only one parent fully covered across all targets and direct/paraphrase
> variants. All frozen cases retain high/medium cue-risk annotations, so they
> are not implicit-semantic or retrieval evidence. D1 source discovery may now
> resume under unchanged gates. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 C4A v1.2 Priority Execution - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 009 source-frame amendment.** Public discovery
> retrieved 199 raw Markdown originals once. Exact local byte rehashing found
> 88 novel artifacts and 111 duplicates already present in the immutable
> 2026-08-29 source frame. The 88 are preserved in a separate, additive source
> frame amendment. This is only provenance and source-pool expansion: it does
> not create D1/C1 eligibility, a parent cluster, prompt, target, strict label,
> representation, selector input, metric or retrieval result. Next is local
> source-only triage, followed by unchanged D1/C1--C6 gates for any candidate
> composition. Record:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_009_2026-08-30/`.

> **2026-08-28 active RQ1b execution amendment.** The current public RQ1b
> experiment is `RQ1b Public Field-Type Ablation`: a source-grounded,
> seven-slot field-card representation is first required to preserve the
> sealed strict gold under blinded selection-only review. It then masks one
> field type from **every** candidate card at a time and measures the resulting
> gold-versus-neighbour routing change. It does not require a unique
> primary/decisive field. The new protocol, validation gates, per-field
> eligibility, residual-redundancy audit, selector boundary, native-margin
> analysis, and stop rules are authoritative at
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Public Field-Type Ablation Protocol - 2026-08-28.md`.
> The six-family pre-scoring validation pilot passed on 2026-08-28: 5/6
> families met every applicable gate; `FTA-004` was excluded after both source
> card builders failed literal evidence audit. The instrument has no selector,
> embedding, retrieval, metric, API, or thesis/PDF result. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_pilot_2026-08-28/RQ1B_FIELD_TYPE_ABLATION_PILOT_CHECKPOINT_2026-08-28.md`.

> **2026-08-29 RQ1b-A active-input freeze.** The non-pilot source-card build
> completed under a pre-review surface-cue amendment. Of 58 initially
> materialised compositions, 10 have literal-safe same-slot repairs and 10 are
> strictly excluded; 38 remain byte-identical. The active amended freeze holds
> 48 public candidate compositions, 128 strict routing families and 256 prompt
> variants, with 109--126 field-eligible families depending on field. The next
> gate is two blinded FULL-card preservation reviews. These are construction and
> review inputs only, not selector, retrieval, embedding, metric or thesis
> results. Checkpoint: `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_SURFACE_CUE_AMENDMENT_COMPLETION_2026-08-29.md`.

> **2026-08-29 RQ1b-A FULL-card preservation Wave 001.** Eighteen anonymous
> packets have now completed two independent model-assisted blind reviews and
> sealed-label adjudication. Six families passed for both direct and paraphrase
> prompts; twelve are excluded from later masked-field scoring because nine
> were judged `NONE_ADEQUATE`, two had reviewer disagreement, and one was
> multi-adequate. This is a strict gold-eligibility gate, not a retrieval,
> embedding, selector, field-effect or thesis result. The ordered first wave is
> not a pass-rate estimate. Evidence: `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_001_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A FULL-card preservation Wave 002.** The next 18 ordered
> packets added 13 valid strict-gold families and excluded five. Cumulatively,
> 36 families are adjudicated: 19 strict-preserved, 17 excluded, 92 pending.
> These remain validity-control counts only, with no selector, retrieval,
> embedding, metric, field-effect or thesis result. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_002_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A FULL-card preservation Wave 003.** Another 18 packets
> were dual-reviewed, evidence-audited and adjudicated: 12 pass and six strict
> exclusions. Cumulatively, 54 are adjudicated (31 strict-preserved, 23
> excluded, 74 pending). Four invalid response files were retained but replaced
> by independent valid reviewers before adjudication. These remain
> benchmark-validity controls only, not selector or field-effect results.
> Checkpoint: `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_003_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A FULL-card preservation Wave 004.** Seventeen validly
> double-reviewed packets added 14 pass and three exclusion. Cumulatively, 71
> families are adjudicated (45 strict-preserved, 26 excluded); `CFTF-099` is a
> separate unadjudicated format hold after three invalid A-side evidence
> responses, and 56 families remain undispatched. This is validity bookkeeping,
> not a model or field-effect result. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_004_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A FULL-card preservation Wave 005.** The fifth 18-packet
> wave added 15 strict-preserved and three excluded families. Cumulatively, 89
> families are adjudicated (60 pass, 29 excluded), 38 are undispatched and one
> is held for mechanical review-format failure. This remains a strict-label
> gate, not selector, retrieval or field-effect evidence. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_005_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A FULL-card preservation Wave 006.** Wave 006 added 13
> strict-preserved families and five exclusion. Cumulative gate state: 107
> adjudicated, 73 pass, 34 exclusion, 20 undispatched and one format hold. This
> remains validity control, not a selector, retrieval or field-effect result.
> Checkpoint: `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_006_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A FULL-card preservation Wave 007.** Eighteen packets
> added 12 strict-preserved and six excluded families. The cumulative
> construction gate is 125 adjudicated: 85 pass, 40 exclusion, two
> undispatched, and the separate `CFTF-099` format hold. Ten A-side and four
> B-side mechanically invalid evidence payloads were independently replaced
> before adjudication. This remains validity control, not a selector, retrieval
> or field-effect result. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_007_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A FULL-card preservation completed.** The active 128
> packet population is exhausted: 87 dual-review strict-gold preservations, 40
> strict exclusions, and the separate `CFTF-099` format hold. Input integrity,
> packet bindings and all 127 adjudicated review/audit chains validate locally.
> The scoreable field coverage is 77--86 preserved families depending on field.
> Residual-redundancy audit is now the remaining local pre-scoring gate. No
> selector, retrieval, embedding, metric, external transfer or thesis result
> exists. Completion checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_COMPLETION_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual-redundancy Wave 001.** Six opaque,
> source-card-only packets (124 targets) now have two valid independent
> residual reviews: 58 `none`, 35 `partial`, three `substantial`, and 28
> retained disagreements. It documents cross-slot redundancy only; it neither
> adjudicates routing nor estimates a field effect. Forty-two packets remain.
> Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_001_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual-redundancy Wave 002.** Six further packets
> complete 142 source-card-only targets: 43 `none`, 54 `partial`, 14
> `substantial`, and 31 disagreements. The cumulative local audit is 12/48
> packets and 266/994 targets, still without selector or field-effect scoring.
> Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_002_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual-redundancy Wave 003.** Six packets add 117
> targets (28 `none`, 44 `partial`, 19 `substantial`, 26 disagreements), for
> 18/48 packets and 383/994 targets. This is still no retrieval scoring.
> Checkpoint: `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_003_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual-redundancy Wave 004.** Six source-card-only
> packets add 123 targets (26 `none`, 48 `partial`, 13 `substantial`, 36
> disagreements), bringing the local redundancy ledger to 24/48 packets and
> 506/994 targets. Invalid response-schema or literal-quote payloads were
> retained and independently replaced before consensus; this is not a
> source-card, strict-gold, selector, or field-effect finding. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_004_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual-redundancy Wave 005.** Six source-card-only
> packets add 113 targets (47 `none`, 26 `partial`, nine `substantial`, 31
> disagreements), for 30/48 packets and 619/994 targets. Replacement reviews
> address only response-schema or literal-quote mechanics; no selector,
> retrieval, embedding, or field-effect finding exists. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_005_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual-redundancy Wave 006.** Six source-card-only
> packets add 120 targets: 54 `none`, 25 `partial`, 12 `substantial`, and 29
> disagreements. Cumulative local coverage is 36/48 packets and 739/994
> targets. The 91 exact independent-review agreements and any replacement
> payloads are redundancy-audit mechanics only; no selector, retrieval,
> embedding, metric, external API, or thesis result exists. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_006_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual-redundancy Wave 007.** Six source-card-only
> packets add 128 targets: 83 `none`, 24 `partial`, eight `substantial`, and
> 13 disagreements. Cumulative coverage is 42/48 packets and 867/994 targets.
> The 115 exact agreements and replacement reviews remain audit mechanics only;
> no selector, retrieval, embedding, metric, external API, or thesis result
> exists. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_007_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual-redundancy completion and pre-BM25 gate.** The
> final six packets complete 48/48 source-card-only packets and 994/994 target
> fields: 391 `none`, 287 `partial`, 97 `substantial`, and 219 disagreements
> (775 exact agreements). The immutable opaque core, packet binding, input
> integrity, 48-card condition materialisation amendment, and all
> candidate-synchronous mask checks pass. The primary strict subset is 87
> preserved families, with 77--86 eligible families per field; 40 strict
> failures and one format hold remain excluded. This is readiness, not a
> selector result. BM25 is the next local step and awaits explicit user
> approval. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_LOCAL_PRE_BM25_READINESS_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A execution order and post-v2 decision hold.** The user
> authorised the frozen v2 local BM25 run. It must consume only the
> ledger-defined 87-family strict subset, report the seven `FULL` versus
> candidate-synchronous `MASK_*` contrasts, and preserve all exclusions. Qwen
> dense retrieval is next, but only after a local payload/cost preflight
> defines the exact external-text scope and the user approves that scope. A
> larger `RQ1b v3` public-cluster cohort and a separate source-stratified
> public-field prevalence audit are recorded as post-v2 decisions, not changes
> to the frozen v2 corpus or its confirmatory analysis. Decision note:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Public Extension and Field Prevalence Decision Note - 2026-08-29.md`.

> **2026-08-29 RQ1b V3 current discovery state.** The separate, frozen public
> source frame has 29,292 hash-unique local public originals. It is an auditable
> structural/recoverability frame, not a claim to cover all public skills or a
> routing benchmark by itself. D1 Wave 005 has now completed C1: five of seven
> source-only drafts have C2 permission; the other two are rejected before any
> prompt. Their 30 C2 packets have completed C3 cue control with 25 low, one
> medium and four high residual-risk annotations; this is not a strict label or
> routing result. Meanwhile C4A remains on a source-card schema-calibration
> hold because two independent natural-source card builders disagree on joint
> trigger-action-artifact slot placement. No V3 selector, embedding, metric or
> thesis result has been added. The next work is fresh v1.1 C4A construction
> and literal audit, not retrieval execution.

> **2026-08-29 RQ1b V3 source-frame consolidation.** A local provenance audit
> maps every one of the historical campaign's 76 frozen candidate compositions
> (408 primary records) into the new 29,292-item frame by exact SHA-256. This
> is source inclusion, **not a protocol merge**: old model-assisted C3/C4
> records do not become V3 labels or V3 retrieval evidence. Separately, a
> seventh and eighth C0 queues of 30 disjoint triads / 90 originals each were
> materialised. Wave 008 is now closed: 29 triads reject before C1 and its
> only C1 permission rejects as a component-parent-downstream Figma chain.
> Wave 009 is now closed: all 30 source-disjoint triads reject before C1
> (22 component/container/nonparallel, two insufficient contrast, six no
> common envelope). Wave 010 repeats this outcome across 30 new triads (21
> component/container/nonparallel, two insufficient contrast, seven no common
> envelope). Neither item changes the C4A card-schema hold
> or authorises selector execution. Evidence:
> `thesis_notes/checkpoints/methods/RQ1b V3 Legacy Mapping And Wave 007 Discovery Checkpoint - 2026-08-29.md`.
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 008 Source-Only Materialisation Checkpoint - 2026-08-29.md`.
> `thesis_notes/checkpoints/methods/RQ1b V3 C0 Wave 008 and C1 Wave 003 Closure - 2026-08-29.md`.
> `thesis_notes/checkpoints/methods/RQ1b V3 C0 Wave 009 Closure - 2026-08-29.md`.
> `thesis_notes/checkpoints/methods/RQ1b V3 C0 Wave 010 Closure - 2026-08-29.md`.
> The separate local-only D1 Wave 006 source-semantic recruitment is now closed:
> five lanes proposed three cross-source, source-grounded peer-route candidates
> without prompts, labels, selectors or retrieval. W6r2 passes only mechanical
> source/literal binding; C1 rejects the deployment and CI trios for insufficient
> operational contrast and the SAST trio for a broad multi-tool container. It
> does not relax C1--C6, creates zero C2 permissions and is not a field or
> routing result. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 D1 Wave 006r2 And C1 Closure - 2026-08-29.md`.

> **2026-08-30 V3 D1 Wave 007r1 closure and next gate.** A five-lane,
> source-only pass over the frozen 29,292 originals retained five literal-bound
> triads. C1 advances only database-distribution migration and workflow-
> orchestration migration to C2 prompt construction; proposal writing,
> compliance and video derivatives fail the strict peer-route test. The next
> gate is local C2 roster and cue-controlled direct/paraphrase drafting for
> those two compositions only. It does not yet create a prompt result, gold
> label, field effect, selector input, metric or retrieval result. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 D1 Wave 007r1 And C1 Closure - 2026-08-30.md`.

> **2026-08-30 V3 D1 Wave 007r1 C2-C3 closure.** Both C1 permissions entered
> local cue-controlled construction. Of twelve source-bound prompt drafts,
> eight retain only low-risk operational wording; four workflow-migration
> prompts are unsafe even after an immutable cue-only r1 rewrite and therefore
> stop before C4. The surviving eight are not valid clusters or labels and
> cannot bypass the independent C4A source-card schema hold. No selector,
> embedding, external transfer, metric or routing experiment has begun.
> Record: `thesis_notes/checkpoints/methods/RQ1b V3 D1 Wave 007r1 C2-C3 Closure - 2026-08-30.md`.

> **2026-08-30 V3 D1 Wave 008 source-first expansion registered.** Five local,
> source-only lanes now search unused members of the frozen 29,292-artifact
> public-original frame for natural cross-origin peer-route triads or quartets.
> This expands candidate discovery rather than changing the RQ1b construct:
> C1--C6, cue control, strict singleton review, and the global C4A hold remain
> in force. It does not create a valid cluster, label, field effect, selector
> input, metric, or retrieval result.

> **2026-08-30 V3 D1 Wave 008 C1 closure.** Five source-only lanes recruited
> no C2-eligible composition: one returned `NO_CANDIDATE`, two rejected before
> materialisation, and two source-hash/literal-span-valid triads both rejected
> at prompt-free C1 for generic-specialist/nonparallel scope. This is an
> auditable discovery negative, not a finding about field value or a routing
> result. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 D1 Wave 008 And C1 Closure - 2026-08-30.md`.

> **2026-08-29 RQ1b-A local BM25 completed.** The ledger-defined strict v2
> subset produced 1,392 locally audited BM25 rows (`87 * 2 * 8`), with zero
> network calls and no thesis writing. Use condition had the largest
> directional `FULL-MASK` Top-1 difference (composition mean 0.068, 95% CI
> `[-0.018, 0.165]`), but the interval crosses zero; all other field contrasts
> were smaller or mixed. This is not a universal field ranking. Full results,
> residual strata and transition failures are checkpointed at
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_bm25_2026-08-29/BM25_RESULT_CHECKPOINT_2026-08-29.md`.
> Qwen remains unexecuted pending its exact local payload/cost preflight and
> external-text approval.

> **2026-08-29 RQ1b-A Qwen preflight.** The local-only preflight passed for a
> Qwen `text-embedding-v4` single-vector counterpart: 1,072 source-grounded
> candidate-condition cards plus 174 original prompts (1,246 unique texts,
> 1,414,939 UTF-8 bytes, 197,099 local lexical-token proxy, and at most 126
> no-retry calls). An execution attempt was blocked before process start
> because the exact egress scope was not specifically approved; at that
> preflight checkpoint, no text, API request, cache entry, charge or Qwen
> result existed. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_qwen_preflight_2026-08-29-v2/QWEN_PREFLIGHT_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A Qwen completed.** After exact user authorisation, Qwen
> `text-embedding-v4` ran once on the frozen 1,246-text payload: 126/126
> serial calls succeeded with zero automatic retries, all first-run embeddings
> were cached locally, and the 1,392-row output passed independent local
> integrity audit. In the all-eligible composition-bootstrap analysis, every
> field's `FULL-MASK` Top-1 and MRR interval crosses zero. This does not negate
> RQ1a controlled sufficiency; it shows that naturally combined public field
> cards often retain redundant support after one whole slot is withheld. The
> strict v2 result is complete and awaits user review; no thesis LaTeX/PDF was
> changed. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_qwen_2026-08-29/QWEN_RESULT_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b v2.1 joint-mask amendment.** A separately labelled,
> prospective-before-joint-results extension now fixes three coherent all-card
> masks: task specification (use/input/output), execution/verification
> (workflow/success), and applicability/capability (boundary/dependency). It
> tests whether a field **set** has non-redundant routing support after the
> remaining public-card information is retained. It does not retroactively
> preregister v2 or identify a decisive member field. Local freeze/mechanics
> validation and BM25 are next; Qwen requires a new exact cache-aware payload
> preflight and separate approval. Protocol:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Joint Field-Set Availability Amendment - 2026-08-29.md`.

> **2026-08-29 RQ1b v2.1 local BM25 and Qwen gate.** The prospective joint
> freeze passed on 87 strict families/42 compositions and fixed denominators of
> 73 task-specification, 77 execution/verification and 70
> applicability/capability families. Local BM25 produced and passed audit for
> 696 rows with zero network calls. All three composition-bootstrap Top-1
> intervals cross zero; task specification is directionally largest at `+0.089`
> (95% CI `[-0.005, 0.188]`). Qwen preflight reuses all cached query/FULL
> embeddings and would send only 402 new joint-mask card texts in at most 41
> no-retry calls. This was the pre-execution gate. Checkpoints:
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_{bm25_2026-08-29,qwen_preflight_2026-08-29}/`.

> **2026-08-29 RQ1b v2.1 joint-mask completed.** The separately authorised
> Qwen `text-embedding-v4` twin completed its exact scope: 402 new
> candidate-card texts only, 41/41 no-retry successful calls and 95,694
> provider tokens; 308 query/FULL texts were local cache hits. Its receipt and
> cache recovery produced 696 rows and passed an independent audit. All three
> Qwen primary `FULL-MASK` Top-1 and MRR composition-bootstrap intervals cross
> zero, matching the local BM25 claim boundary. RQ1b v2.1 therefore records a
> bounded combined-information redundancy/uncertainty result, not a confirmed
> joint field-set effect or a field-level causal ranking. No thesis LaTeX/PDF
> changed. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_qwen_2026-08-29/QWEN_RESULT_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b v3 public-source expansion started.** V2/v2.1 remain
> frozen and are not being pooled with V3. V3 begins with a local,
> hash-deduplicated canonical public source frame and then a separately frozen
> 3--4-candidate near-neighbour cohort targeting at least 100 candidate
> compositions. The source frame will support bounded recoverability and
> co-occurrence evidence; it cannot be described as every public skill or as
> the origin of the field taxonomy. No selector, embedding, external transfer,
> metric, or thesis result exists for V3. Protocol:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V3 Public Source Frame and Cluster Discovery Protocol - 2026-08-29.md`.

> **2026-08-29 RQ1b v3 D1 Wave 004r1 C1 complete.** Three cross-origin,
> source-only compositions passed the exact evidence-card gate and may now
> receive C2 direct/paraphrase construction: agreement review, structured-data
> visualisation and presentation authoring. This is only a C2 permission, not
> a strict cluster, gold label, representation, selector input or result. The
> initial W4 literal-formatting failure remains preserved; W4r1 changes only
> cited spans. C2/C3/C4/C5/C6 remain required under
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V3 C2 Prompt Construction and Cue-Control Handoff SOP - 2026-08-29.md`.

> **2026-08-29 RQ1b v3 C2-C3 Wave 001 complete.** Four C1-approved
> compositions now have 24 cue-controlled direct/paraphrase packets. One
> cue-only r1 change removed a copied Seaborn phrase; C3 permits all 24 to C4
> while retaining 20 `high` and four `medium` residual-cue-risk annotations.
> This is neither cue-safety proof nor a strict label, source card, selector
> input, metric or routing result. The next work is exact-evidence seven-slot
> card construction followed by two source-deidentified C4 singleton reviews:
> `thesis_notes/checkpoints/methods/RQ1b V3 C3 Wave 001 Cue Gate Checkpoint - 2026-08-29.md`.

> **2026-08-29 RQ1b v3 C4A packet materialisation complete.** Four anonymous
> packets bind 12 rehashed originals to the frozen C2/C3 lineage for
> exact-evidence seven-slot card transcription. The packets contain neither
> prompts nor title/source maps nor sealed targets. Two independent builders and
> literal/identity-line audits remain required before any C4B adequacy review;
> no card, gold, selector input or result yet exists.

> **2026-08-29 RQ1b v3 D1 Wave 003r1 completed gate status.** Three newly materialised
> source-only triads are at C1: source-language Spark migration, PDF output
> conversion, and jurisdiction-bounded privacy rights. The first W3 attempt
> failed closed on one nonliteral LGPD excerpt; W3r1 changes only that exact
> span and passed rehash/literal binding for all nine originals. C1 rejects all
> three: one retained migration chain, one generic parser container, and one
> broad-programme/specialist-workflow asymmetry. No prompt, gold label,
> selector, embedding, external transfer or result is authorised or present.
> A future C1 advance would permit only C2 prompt construction, not a valid
> cluster.

> **2026-08-29 RQ1b v3 directed-discovery amendment.** The lexical C0 queue
> remains a separately reported feasibility audit because same-topic lexical
> neighbours frequently form a container/component chain. A prospective D1
> local source-only path will instead prioritise real source-to-target,
> provider/interface, and explicit prerequisite/boundary contrasts while
> retaining the unchanged C1--C6 strict gates. D1 screening counts will never
> be pooled with lexical C0 or reported as valid clusters. Protocol:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V3 D1 Directed Public-Source Discovery Amendment - 2026-08-29.md`.

> **2026-08-29 RQ1b v3 C0 Wave 006 completed.** The final frozen lexical
> calibration wave rehashed 90 unique originals and screened 30 unseen triads.
> It advanced none: 24 were nonparallel/component/container structures, five
> lacked a common envelope, and one lacked operational contrast. The result
> calibrates title/local-FTS discovery only; it is not a valid-cluster or
> routing result. The lexical path now totals 180 screened triads and 25 C1
> source-evidence candidates. The next discovery activity is the separate D1
> directed, source-evidence-first queue under unchanged C1--C6 gates. Evidence:
> `skill_benchmark/rq1b_v3_public_source_frame/c0_source_review_wave_006_2026-08-29/C0_SOURCE_REVIEW_WAVE_006_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 C0 Wave 007 completed.** Thirty new source-only lexical
> triads passed binding and zero-reuse audit. Two may proceed only to C1
> source-evidence construction: performance-decay diagnosis and
> threat-intelligence workflows. Eighteen reject as nonparallel/component or
> container, two for insufficient operational contrast and eight for no common
> envelope. The lexical calibration therefore contains 27 C1 permissions from
> 210 screened triads; this is not a valid-cluster count, a prompt/gold result,
> a selector input or retrieval result. C1 must specifically test overlap of
> traffic/content decay and producer-consumer containment in the threat triad.
> Evidence:
> `skill_benchmark/rq1b_v3_public_source_frame/c0_source_review_wave_007_2026-08-29/C0_SOURCE_REVIEW_WAVE_007_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 C1 Wave 002 completed.** The two C0 Wave 007
> permissions were source-bound, independently reviewed and rejected before
> prompt construction. Organic traffic/content diagnosis and paid-ad creative
> rotation do not share one bounded envelope; threat intelligence enrichment,
> product production and SIEM hunting are an explicit lifecycle chain. The
> result is zero C2 permissions, not a field-effect or retrieval result.
> Evidence:
> `skill_benchmark/rq1b_v3_public_source_frame/c1_source_evidence_wave_002_2026-08-29/C1_SOURCE_EVIDENCE_WAVE_002_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 D1 Wave 001 materialised.** Four directed, local
> source-only triad drafts now have exact evidence and rehash bindings across
> 12 artifacts. They remain discovery packets for independent C1 review, not
> valid clusters or strict labels; all retain same-origin/cue-risk annotations.
> No prompt, selector, embedding or transfer has occurred. Evidence:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_001_2026-08-29/D1_DIRECTED_DRAFT_MATERIALISATION_AUDIT.json`.

> **2026-08-29 RQ1b v3 D1 Wave 001 C1 complete.** Of four independently
> source-reviewed triads, only typed PDF/DOCX/XLSX-to-Markdown conversion has
> permission to enter C2. A version-upgrade lifecycle and two runtime/framework
> families were rejected as nonparallel or insufficiently distinct. This
> calibrates source-only peer-role screening; it is not a frozen cluster,
> prompt, gold label, selector input or experiment result. Evidence:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_001_2026-08-29/c1_source_evidence_wave_001/C1_SOURCE_EVIDENCE_WAVE_001_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 D1 Wave 002 materialised.** The next local source-first
> batch has two cross-origin triads: provider-specific end-to-end web hosting
> and provider-specific hosted-LLM integration. Exact source rehash and span
> binding pass, but C1 is intentionally still active because provider names or
> frameworks alone may not establish a distinct first-route. No prompt, gold,
> selector, transfer, metric or retrieval result exists. Evidence:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_002_2026-08-29/`.

> **2026-08-29 RQ1b v3 D1 Wave 002 C1 complete.** Neither provider-targeted
> composition passes source-only peer-route review: one mixes direct deployment
> routes with a resource/deployment container, and the other differs only by
> hosted-provider client interface. This constrains the next discovery wave; it
> does not yet test a prompt, gold label, field effect or retrieval. Evidence:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_002_2026-08-29/c1_source_evidence_wave_002/C1_SOURCE_EVIDENCE_WAVE_002_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 local source-frame checkpoint.** The frozen bounded
> frame now contains 29,292 canonical SHA-256-unique public-original artifacts
> from 1,613 recorded origins, plus 2,476 duplicate-path aliases. A local
> structural census and two 10,000-row cross-origin triad *triage* queues are
> complete; the second removes exact copied-name triples but does not claim
> semantic validity. These are discovery inputs only. The next gate is
> source-only envelope/operational-contrast review before a 3--4-candidate
> cluster can be drafted. No V3 prompt, gold label, retrieval, embedding,
> external transfer, metric or thesis result exists. Protocol and freeze:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V3 Public Source Frame and Cluster Discovery Protocol - 2026-08-29.md` and
> `skill_benchmark/rq1b_v3_public_source_frame/source_frame_2026-08-29/`.

> **2026-08-29 RQ1b v3 C0 feasibility calibration.** The first diversified,
> source-only triage wave screened 30 three-skill drafts drawn from 90
> non-reused canonical sources. Three triads advance to C1 source-evidence
> construction; 18 fail due to component/container structure, two due to
> copy/derivative evidence, six due to insufficient operational contrast, and
> one due to no shared task envelope. This calibrates lexical discovery only,
> not strict-triad yield or routing accuracy. A deterministic title-containment
> prefilter is now permitted only to prioritise later review waves. Ledger:
> `skill_benchmark/rq1b_v3_public_source_frame/c0_source_review_wave_001_2026-08-29/C0_SOURCE_REVIEW_WAVE_001_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 C0 Wave 002r1.** A second source-only,
> model-assisted and principal-rechecked wave screened 30 further triads from
> 90 canonical sources with zero source overlap with Wave 001. Seven advance
> only to C1 source evidence; 14 fail for component/container structure, seven
> for insufficient contrast, and two for no common envelope. The title-signal
> containment filter only ordered review and is not a scientific inclusion
> rule. Across both waves, ten candidates await C1; there is still no V3
> prompt, gold label, selector, metric, embedding, transfer or thesis result.
> Checkpoint:
> `skill_benchmark/rq1b_v3_public_source_frame/c0_source_review_wave_002r1_2026-08-29/C0_SOURCE_REVIEW_WAVE_002R1_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 C0 Wave 003.** A third zero-overlap source-only
> feasibility wave screened 30 further cross-origin lexical triads from 90
> canonical originals. Principal recheck retained two C1 source-evidence
> candidates and rejected 28 (22 container/component/nonparallel, two
> insufficient contrast, four no common envelope). Across W1--W3, 12 candidates
> await C1 from 90 reviewed triads. These are local feasibility records only:
> no prompt, gold label, field annotation, selector, metric, embedding, external
> transfer or thesis result exists. Checkpoint:
> `skill_benchmark/rq1b_v3_public_source_frame/c0_source_review_wave_003_2026-08-29/C0_SOURCE_REVIEW_WAVE_003_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 C0 Wave 004.** A fourth zero-overlap source-only
> feasibility wave screened 30 further cross-origin lexical triads from 90
> canonical originals. Principal recheck retained three C1 source-evidence
> candidates and rejected 27 (17 container/component/nonparallel, four
> insufficient contrast, six no common envelope). Across W1--W4, 15 candidates
> await C1 from 120 reviewed triads. These are local feasibility records only:
> no prompt, gold label, field annotation, selector, metric, embedding, external
> transfer or thesis result exists. Checkpoint:
> `skill_benchmark/rq1b_v3_public_source_frame/c0_source_review_wave_004_2026-08-29/C0_SOURCE_REVIEW_WAVE_004_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 C0 Wave 005.** A fifth zero-overlap source-only
> feasibility wave screened 30 further cross-origin lexical triads from 90
> canonical originals. Principal recheck retained 10 C1 source-evidence
> candidates and rejected 20 (10 container/component/nonparallel, three
> insufficient contrast, one copy/derivative, six no common envelope). Across
> W1--W5, 25 candidates await C1 from 150 reviewed triads. These are local
> feasibility records only: no prompt, gold label, field annotation, selector,
> metric, embedding, external transfer or thesis result exists. Checkpoint:
> `skill_benchmark/rq1b_v3_public_source_frame/c0_source_review_wave_005_2026-08-29/C0_SOURCE_REVIEW_WAVE_005_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 C1 gate opened.** The 25 C0 advances now enter a
> local source-evidence-card gate before any prompt is written. Every member
> needs exact source-bound input/operation/output evidence and a peer-role
> rationale; containers, lifecycle steps, generic fallbacks and overlaps fail
> closed. C1 does not create a gold label or a retrieval input. SOP:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V3 C1 Source-Evidence Card SOP - 2026-08-29.md`.

> **2026-08-28 historical RQ1b primary-field amendment.** This earlier method
> is superseded as an active execution path by the field-type availability
> protocol above. RQ1b had two evidence paths:
> RQ1b-N keeps C6-frozen original public artifacts untouched for strict
> natural-artifact validation; RQ1b-S uses a separately labelled,
> source-grounded seven-slot field-card derivative for winner-only target-field
> neutralisation plus a non-target sham control. The prior raw-full-document
> P0--P5 workflow is retained as a bounded masking feasibility audit, not a
> gate for RQ1b. The validation pilot has six pre-locked families and creates
> no selector score; it must pass literal fidelity, residual-cue, sham,
> mechanical-diff, and blind-neutralised-card checks in at least four families,
> including input/precondition and output/artifact, before scaling. Detailed
> SOP: `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Natural-Artifact And Source-Grounded Field-Card Protocol - 2026-08-28.md`.

> **2026-08-28 RQ1b-S pilot stop.** Six source-grounded field-card packets
> were built locally from hash-verified originals with two independent
> literal-valid card records each. For the first three route-preservation
> checks, two blind reviewers retained the sealed strict winner for direct and
> paraphrase prompts, but each named a different primary field from the
> pre-locked raw-artifact target: use condition became input/precondition;
> input/precondition became use condition; output/artifact became use
> condition. The required input and output gates therefore fail. No target
> neutralisation, sham edit, residual-cue review, selector, embedding, API,
> retrieval, metric, or thesis result was produced. This is a
> derivative-representation attribution failure, not a field-value or
> selector result. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_card_pilot_2026-08-28/RQ1B_S_FIELD_CARD_PILOT_CHECKPOINT_2026-08-28.md`.

> **2026-08-15 RQ2 status.** RQ1a is `REVIEWED / COMPLETE`. RQ2a is `CONFIRMATORY COMPLETE / USER-REVIEWED / THESIS-INTEGRATED`: 280 clusters, 600 prompts, 22 conditions, 13,200 rows, frozen paired statistics, cost ledger, and failure analysis pass. RQ2a remains closed. RQ2b's base-v1 B0G full-pool audit mechanically completed but its acceptable-set freeze remains `BLOCKED BEFORE RETRIEVAL`: all 7,710 review units resolve, yet 14 strict-gold rows are not fully acceptable and eight scored prompts have no fully acceptable **reviewed** candidate. A user-directed, non-B0G review of exactly those 14 cases retains six gold label skills and excludes eight material workflow mismatches. It creates a prospective 381-prompt strict-gold-only v1.1 path once materialised; it does not create acceptable metrics or an RQ2b retrieval result. The v1.1 strict-only endpoint contract, local runner/analysis bindings, and synthetic B1/B2 execution-contract smoke pass. The first review was remediated, a fresh rereview found no P0/P1, and the narrow local strict-contract seal is complete. B1X remains complete and untransmitted; the next task is to construct the separate B1R transfer-authorisation packet. Older broad matrices remain historical/exploratory.

This file is the operational roadmap for the thesis experiments. It exists to prevent drift.

Historical frozen benchmark version: `benchmark-v0.4-2026-06-16`.

Freeze manifest:

- `skill_benchmark/versions/benchmark-v0.4-2026-06-16.md`
- `skill_benchmark/versions/benchmark-v0.4-2026-06-16.json`

This version remains the source of historical v0.4 results only. The RQ2b audit found 47 recorded-file hash drifts and no per-skill source hashes, so the new work is frozen separately as `rq2b-full-library-v1-2026-08-02` rather than reported as v0.4.

Latest frozen-v0.4 result report:

- `skill_benchmark/outputs/frozen_v0_4_retrieval_matrix_summary.md`
- `skill_benchmark/outputs/frozen_v0_4_retrieval_matrix_summary.json`

For the current RQ2 state, implementation queue, completion gates, and scientific support criteria, use `thesis_notes/current/RQ2 Current Status and Implementation Tracker - 2026-07-26.md`. The detailed design is `thesis_notes/current/RQ2 Comprehensive Methodology Specification - 2026-07-26.md`. For detailed RQ1 test-unit design, leakage controls, and few-shot field templates, use `thesis_notes/current/RQ1/protocols/RQ1 Field Targeted Test Plan.md`.

The thesis is not a provider leaderboard and not a search for every possible retrieval architecture. The thesis asks:

**RQ1:** Which operational information types help distinguish semantically similar but procedurally distinct agent skills?

**RQ2:** How do skill representation and retrieval-pipeline choices affect the preservation and use of the routing-relevant operational information identified in RQ1 under semantic confusability, and what accuracy, candidate-recall, and retrieval-cost trade-offs result?

The clean RQ2a mechanism study is complete. RQ1a is `REVIEWED / COMPLETE` for use condition, input/precondition, output/artifact, dependency/resource, boundary/not-for, success/verification, and workflow/procedure. RQ2a completed the matched-content development and confirmatory stages across BM25, Qwen single-vector, SkillRouter cross-encoder, and field-aware Qwen selectors. RQ2b is frozen, its native SkillRouter-embedding amendment is approved, and B1S is sealed after v17 smoke and independent pass 13, but it remains externally untransmitted and scientifically unexecuted. The frozen-v0.4 matrix and external SkillRouter/I3C rows remain exploratory motivation and portability evidence rather than part of either current confirmatory estimate.

Immediate implementation boundary:

- retain the approved B0F-A1 amendment, repaired v17 smoke, eligible independent pass 13, and verified B1S seal as the immutable local implementation boundary;
- preserve the blocked base-v1 B0G audit as an immutable checkpoint; do not selectively edit its labels;
- preserve the locally validated 381-prompt strict-gold-only v1.1 patch from the recorded 14-case remediation before proposing any strict-gold retrieval run;
- do not send I2 source text to extraction workers until a separate exact transfer authorization is granted;
- keep Qwen API work, hosted SkillRouter work, and thesis-result writing behind their own later gates;
- leave graph/tree, external 80K neural, and downstream execution outside the minimal RQ2b core.

## Framing Evolution Log

Current framing, updated 2026-06-23:

> The thesis is information-led. RQ1 asks which operational skill information improves distinction among semantically similar skills. RQ2 compares complete strategies that preserve, organize, or exploit routing-relevant information in different ways.

RQ1 closure and RQ2 hand-off, agreed 2026-07-24:

- RQ1a establishes causal individual-field discriminability only in the controlled sibling suites, where every non-target field is held fixed.
- The supporting RQ1b public-realism audit establishes field prevalence and recoverability only. Separately, frozen RQ1b Wave 001 establishes a 62-cluster natural-original selection dataset with model-assisted acceptable-set curation. It still does not provide a single-field causal accuracy result, because naturally authored artifacts combine and repeat operational facts across titles, descriptions, workflows, examples, and requirements; every Wave 001 cluster is therefore original-only rather than mask-eligible.
- This joint expression is the practical setting rather than a flaw. For example, the imported Notion knowledge-capture, meeting-intelligence and research-documentation skills share the same Notion operations but jointly differ in their intended use, produced artifact and workflow. They are qualitative realism evidence, not clean RQ1a field-isolation units.
- The RQ1 conclusion is therefore an information-preservation requirement: a practical selector should retain the operational facts shown to resolve controlled near-neighbour ambiguity. RQ2 asks which representation and retrieval strategies can preserve, organize and exploit those combined facts, and at what accuracy, recall and cost trade-off.

Previous framing:

> Flat metadata vs embedding vs structure-aware methods.

Why it changed:

- The old framing mixed two axes: what information is available and how it is used.
- Graph/tree methods naturally encode relation or hierarchy information, while embeddings consume text unless relation information is serialized or learned.
- Field-aware rerankers test explicit use of skill fields, but learned rerankers may encode similar signals implicitly.
- The thesis should therefore report information-layer effects separately from retrieval-strategy effects.
- Near-term work should prioritize RQ1 field evidence before committing to a graph/tree information schema.

Claim boundary:

- Do not claim explicit JSON-style fields are the only solution.
- Do claim that if task, input, output, workflow, dependency, boundary, or success information is retrieval-critical, it must be made available somewhere: by authoring, deterministic parsing, LLM-assisted extraction, learned encoding, or full-artifact retrieval.
- Treat relation and hierarchy information as RQ2 strategy directions whose exact carried information is TBD until I4/I5 experiments are specified.
- Do not define or report an RQ1c yet. The active RQ1 evidence lines are RQ1a controlled field discriminability, supporting public-field recoverability, RQ1b-N public-source/strict-label framing, and the pending RQ1b-A field-type availability pilot.

## Current Position

> **2026-08-28 RQ1b cross-source live-status override.** The strict-public curation campaign is now at `76 frozen candidate compositions / 408 frozen strict packets / 119 non-primary packets / no selector study`. Round 42 added four cross-source compositions and seven strict packets only after final C3 source-cue control, two blind model-assisted C4 reviews, C5 sealed-target validation, and C6 integrity freeze. Its 34 multi-adequate and seven reviewer-disagreement packets stay out of strict top-1. The user-directed 75-composition curation target is met. This remains feasibility curation rather than retrieval evidence; do not infer a selector result from these counts. The Round 42 checkpoint supersedes historical 69/72 live counts elsewhere in this roadmap.

> **Historical RQ1b primary-field gate.** The P0--P5 target-lock pipeline
> below is retained only as a raw-document masking feasibility record. It is
> superseded by the active RQ1b field-type availability pilot above. Do not
> resume P0.5/P1/P2 field locks, masked-text challenges, winner-only target or
> sham construction, or score a `MASK_ELIGIBLE` subset under that older method.

> **2026-08-28 checkpoint.** Batches 01--10 and the pilot have completed their current local curation gates; Batch 11 is in progress. Twelve post-pilot field locks fail closed at P1/P2 or P3, and no masked artifact or selector result exists. Resume details are in `skill_benchmark/rq1b_cross_source_public_benchmark/working/masked_execution/RQ1B_MASKED_EXECUTION_CHECKPOINT_2026-08-28.md`.

We are past benchmark construction, initial selector comparison, public-skill import, public field auditing, controlled/public-gold expansion, semantic-confusability repair, the historical v0.4 local/Qwen/SkillRouter I1/I3/I2 matrix, and the RQ1a field-isolation suites. RQ2b is frozen with 2,433 approved sources, 245 controlled prompts, 144 public-gold prompts, and 12 stress prompts. Its 57-chunk I3C packet has not been transmitted, and no RQ2b scientific score exists. The completed historical I1/I2/I3 matrix motivates RQ2b; it is not the new RQ2b result. The completed RQ1a suites support field-specific claims because they use controlled shared context and vary exactly one skill-side field at a time.

Current RQ1 interpretation: input/precondition, use condition, dependency/resource as capability compatibility, and output/artifact under semantic retrieval are the strongest first-pass discriminators. Boundary/not-for is useful but weaker when authority or scope is only implied. Success/verification and workflow/procedure are positive but more conditional because they often require reasoning over acceptance gates or operation order. Examples/tests are a negative-control or workflow-support field, not an eighth core operational field: generic examples do not provide independent routing value, while rare exact example matches can strongly steer selection. The separate strict cross-source public-skill curation campaign supplies RQ1b-N inputs; its active RQ1b-A field-type availability pilot has not run a selector study.

The RQ1b-A pre-scoring validation pilot has passed; the next RQ1 work is
non-pilot C6-derived card construction and validation, not an uncontrolled
expansion or selector run. Wave 001 and the separately maintained cross-source
strict-public campaign provide frozen public inputs; neither has yet produced a
selector result. Presentation and synthesis must keep the evidence layers
separate: RQ1a controlled sufficiency, public-field recoverability, RQ1b-N
natural-artifact framing, and RQ1b-A conditional field availability. The
atomic RQ1b-A design object is one prompt, one strict public near-neighbour
cluster, a full source-grounded card, and a same-candidate-set condition that
withholds one field type.

RQ2a A0-A20 are complete. No additional RQ2a scoring is required. RQ2b B0F, B0F-A1, B0G-M, B1X, and B1S remain preserved; the authorised base-v1 B0G semantic review and C adjudication are also complete. Its final acceptable-set freeze is blocked because 14 strict golds are not fully acceptable and eight prompts lack a fully acceptable reviewed candidate. The controller and independent metadata review agree that base-v1 must not be finalised. The 2026-08-15 focused remediation is not another B0G audit: it retains six existing labels, excludes eight prompts, and has been materialised and locally validated as a strict-gold-only v1.1 manifest before any B1R proposal. A SkillRouter-native field-aware extension remains outside this amendment and would be post-hoc exploratory unless evaluated on a new untouched holdout.

Important scale clarification:

> The active frozen-v0.4 benchmark has 2433 skills, 245 controlled prompts, 144 public-gold prompts, and 12 low-information stress prompts. It tests semantic/procedural scale and context pressure: compact metadata is already above a 200k-token context budget by the current chars/4 estimate, while full artifacts and extracted-field variants are much larger. Use `thesis_notes/current/Active Benchmark Snapshot.md` and `thesis_notes/current/Current Results Summary.md` for current counts.

Historical exploratory finding, not a new RQ2a result:

> Dense retrieval is useful for broad candidate generation, but final skill selection benefits from selector-visible procedural information when the candidate universe and method are held fixed. On frozen-v0.4 controlled prompts, I3 structured fields improve over I1 under BM25, TF-IDF, Qwen embedding, Qwen rerank, SkillRouter embedding, and SkillRouter rerank. Public-gold is more mixed, which is part of the thesis: public names/descriptions can carry strong provider/task cues, while full artifacts can add noise and cost. The external SkillRouter-Eval-Core track now supports a stronger I3C verification story: cleaned I3C V2 beats I2 on Easy Hit@1/MRR/Recall/FullCoverage and narrowly beats I2 on Hard Hit@1/MRR/Recall under BM25, while using far less selector-visible text. Local frozen-v0.4 I3C is still pending; the local I3M artifact is a paid DeepSeek feasibility attempt.

Important method clarification:

> The current local schema reranker is not the final thesis method. It is `M6-v0`, a transparent diagnostic that uses weighted lexical overlap over extracted fields. The first `M6-v1-local` prototype now exists: it parses user requests into fields and compares them field-to-field against extracted skill fields. Controlled results improve slightly over `M6-v0`, but public-gold still shows that a stronger semantic or LLM-assisted field matcher is needed for messy public skills.

Current RQ1a field-isolation clarification:

> Input/precondition, output/artifact, and dependency/resource are now supported as strong positive routing signals in controlled near-neighbour suites. Dependency/resource should be framed specifically as external capability compatibility: platform, tool, API, runtime, permission, version, or provenance/resource requirements. Boundary/not-for is also useful, but conditionally: it is strong under explicit exclusion or paraphrased boundary prompts and much weaker under implicit-authority prompts where the user asks for an internal review, triage packet, or evidence summary without naming the excluded action. Therefore boundary/not-for should be framed as a scope, authority, compatibility, or guardrail signal, not as a simple positive matching field.

Current information clarification:

> The thesis should use "information layer" or "selection information" rather than only "procedural information". The completed RQ1a field groups are task/use condition, input/precondition, output/artifact, workflow/procedure, dependency/resource/platform, boundary/not-for, and success/verification. Examples/tests are retained as a negative-control or support-documentation field. Relation edges and hierarchy/task role remain RQ2 strategy directions, not completed RQ1 field-isolation evidence.

Current main risk:

> The project may drift into testing more providers or architectures without improving the thesis answer about representation information. The next expansion should improve benchmark coverage and failure-mode analysis, not become a provider leaderboard.

Current crossed-design risk:

> Representation-layer effects and retriever/reranker effects are partly separated for Qwen and SkillRouter on frozen v0.4: R1/R2/full have been run with Qwen embedding-only, Qwen rerank top-20, local-schema top-20, SkillRouter embedding-only, and SkillRouter rerank top-20 on controlled and public-gold. SkillRouter prompt-level artifacts have been recovered and working failure-mode reports exist. Final claims should discuss representation-architecture interactions rather than a universal provider ranking.

Current methodology hardening update, 2026-06-05:

> A detailed methods critique found that the main risk is conflation: field usefulness, field extraction quality, lexical cue overlap, candidate budget, and authored-skill cleanliness are not always separated. Headline comparisons must remain budget-fair, strict-gold and acceptable-alternative metrics must be separated, M6-v1-local must be named as a lexical field-aware prototype, public-gold false positives need stratum-aware labels, and the first-pass top-1 confidence intervals/McNemar tests should be integrated before final claims.

Detailed note:

- `thesis_notes/methodology/Methodology Deep Critique and Improvement Plan - 2026-06-05.md`

Current validity risk:

> The controlled benchmark exposes clean procedural fields because we authored those skills. Before final claims, we must check whether similar information exists or is extractable from real public skills. If some fields are usually absent, frame them as representation-layer normalization targets rather than assuming skill authors already provide them.

Current public-gold risk:

> Public imported skills currently support field-taxonomy validity and scale pressure. A 144-case public-gold stratum now exists as a separate external-validity benchmark. It should be reported separately from controlled-authored results because it tests messy public skill artifacts, not only controlled field usefulness. Qwen and SkillRouter summary metrics have been run on the frozen-v0.4 public-gold stratum, prompt-level SkillRouter artifacts have been recovered, and working failure-mode reports exist. Public-gold still needs per-source-family failure analysis before final writing.

## Frozen Unless Broken

These should not be changed unless a validation failure is discovered:

- Main evaluated controlled prompt set: 245 prompts.
- Separate public-gold prompt set: 144 prompts.
- Separate low-information stress set: 12 prompts, not merged into headline controlled/public results.
- Frozen full-scale skill library: 2433 skills.
- Core distinction: skill artifact vs information layer vs retrieval/encoding strategy vs final main-agent skill use.
- Current RQs.
- Main benchmark purpose: semantic confusability plus procedural distinctness.

The current validated construction condition is the 2433-skill public-expanded scale with 245 controlled prompts plus a separate 144-prompt public-gold stratum. Older 2401-skill, 201-prompt, 137-prompt, 120-prompt, and 82-prompt selector results remain historical comparisons until methods are rerun against `benchmark-v0.4-2026-06-16`.

Allowed small changes:

- Add acceptable alternatives where manual adjudication shows a near-equivalent skill is genuinely acceptable.
- Fix a prompt or skill only if gold-label stability fails.
- Add a note explaining a limitation instead of endlessly rebuilding the benchmark.
- Add more public/generated scale only if manual adjudication shows the current 2433-skill condition is not enough. Current priority is adjudication, failure-mode analysis, local I3C extraction if needed, fixed-candidate external I3C reranking if needed, and cost/latency reporting rather than more background-only expansion.

## Phase 1: Benchmark Validation

Status: Complete, with watch items.

Purpose:

Confirm that the benchmark is testing the intended problem rather than random noise, prompt leakage, or invalid gold labels.

Required evidence:

- Step 1 integrity passes.
- Step 2 procedural alignment passes.
- Step 3 semantic confusability passes.
- Step 4 prompt leakage passes.
- Step 5 scale regime passes.
- Non-core competitors have been checked enough to show they are mostly distractors, not better gold labels.

Definition of done:

- Benchmark validation reports exist.
- Any ambiguous gold labels are either fixed or recorded as acceptable alternatives.
- The thesis can defend why the benchmark targets semantic confusion under scale.

Do not reopen unless:

- A background skill is clearly more procedurally correct than the gold skill.
- A prompt directly leaks the gold skill name.
- All final methods become near-perfect, making the benchmark too easy.

## Phase 2: Final Method Set

Status: Mostly complete for I1/I2/I3, but requires methodology hardening and relation/hierarchy decisions. Method taxonomy was cleaned on 2026-06-01, `M6-v1-local` was implemented on 2026-06-03, frozen-v0.4 SkillRouter R1/R2/full embedding and reranking runs were completed on 2026-06-17, and the information-layer reframing was adopted on 2026-06-18. Final claims still need budget-fair reporting, uncertainty estimates, request-parser/field-ablation validity checks, and a decision on I4/M5 graph and I5/M4 tree/DAG tests.

Purpose:

Choose a small final set of methods that represent different information layers and retrieval strategies. This is the experimental backbone of the thesis.

Required final methods:

| Role | Method | Why keep it |
|---|---|---|
| Normal-agent baseline | M0 progressive disclosure, core only | Represents current practical main-agent selection behavior. |
| Flat lexical control | M1 BM25 or TF-IDF over flat metadata | Tests compressed metadata and lexical cueing; control only, not thesis architecture. |
| Dense card retrieval | M2 Qwen/MiniLM over R1 flat cards | Tests modern semantic retrieval over the same information as flat metadata. |
| Dense full-artifact retrieval | M2 Qwen/MiniLM over full `SKILL.md` | Tests whether full artifact embeddings already encode procedural suitability. |
| Structured-card retrieval | M3 retrieval over R2 procedural cards | Tests whether extracted procedural fields help before reranking. |
| Generic neural reranker | Dense retrieval plus Qwen rerank | Tests whether a strong generic reranker solves the problem without explicit field scoring. |
| Diagnostic schema reranker | M6-v0 current local schema rerank | Retained for transparency and historical comparison, but too crude for the final structure-aware claim. |
| Proposed procedural reranker | M6-v1 dense shortlist plus field-aware procedural rerank | Directly tests the thesis claim that extracted procedural information improves selection when used as fields. |
| Strong skill-specific baseline | SkillRouter embedding plus SkillRouter rerank | Tests against a prior-work-aligned skill retrieval and reranking system. |
| Optional tree/DAG router | M4 route by I5 hierarchy/grouping | Tests whether hierarchical narrowing gives scale efficiency or causes early branch-exclusion failures. |
| Optional graph retriever | M5 retrieval/reranking over I4 relation edges | Tests whether explicit similarity, dependency, composition, alternative, belong-to, and workflow/prerequisite relations help beyond serialized structured cards. |

Optional methods:

- M4 tree routing.
- M5 graph retrieval.
- Additional providers.

Decision rule:

Optional methods are only worth adding if they test a new representation claim. They are not worth adding just because they might improve top-1.

Architecture rule:

- Use `I1/I2/I3` ablations to answer which information is useful.
- Use `M6-v1` to test whether request-side field matching can exploit that information.
- Use `M5` graph retrieval if we need to test whether I4 relation edges improve over serialized procedural cards.
- Use `M4` tree/DAG routing mainly for I5 scalability and branch-exclusion analysis.
- Do not use tree/graph methods as decorations; each must report the additional failure mode it reveals.

Detailed M4/M5 edge methodology:

- `thesis_notes/methodology/M4 M5 Structure-Aware Architecture Plan.md`

Definition of done:

- Final method table is frozen.
- Each method has a one-sentence thesis role.
- Each method reports top-1, top-5, MRR, non-core top-1, candidate budget, and cost/latency if available.
- Headline reranker comparisons use the same candidate budget.
- Strict-gold and gold-or-acceptable results are reported separately.
- Final controlled comparisons include uncertainty estimates or paired tests.
- The method table records model settings, candidate budget, prompt stratum, and scoring rule.
- Information-layer comparisons explicitly state how the layer was encoded for each strategy, especially for I4 relation and I5 hierarchy information.

Current 2349 Qwen note:

- Qwen R1 embedding: 35.3% top-1, 50.6% non-main top-1.
- Qwen R2 embedding: 50.6% top-1, 36.5% non-main top-1.
- Qwen full-skill embedding: 50.6% top-1, 30.6% non-main top-1.
- Qwen full-skill plus Qwen rerank top-20: 61.2% top-1.
- Qwen full-skill plus local schema rerank top-100: 84.7% top-1.

Current 2401 Qwen note:

- Qwen full-skill embedding: 52.5% top-1, 73.7% top-5.
- Qwen full-skill plus local schema rerank top-100: 77.4% top-1, 91.2% top-5.
- Qwen full-skill plus `M6-v1-local` task/output/workflow rerank top-100: 78.8% top-1, 92.0% top-5, 0.851 MRR, with 93.4% candidate R@100.
- Qwen full-skill plus `M6-v1-local` all-fields rerank drops to 73.0% top-1, which confirms that all structure should not be treated as positive text.
- Integrated implicit-field cases make the task harder, but the structure-aware method still improves top-1 and reduces non-main false positives after conservative field extraction.

Current 2401 SkillRouter note:

- SkillRouter full-skill embedding: 73.0% top-1, 94.2% top-5, 0.827 MRR.
- SkillRouter full-skill plus SkillRouter rerank top-20: 83.2% top-1, 97.8% top-5, 0.898 MRR.
- SkillRouter first stage plus M6-v1-local task/output/workflow top-20: 83.2% top-1, 95.6% top-5, 0.895 MRR.
- SkillRouter first stage plus M6-v1-local task/output/workflow top-100: 86.9% top-1, 98.5% top-5, 0.927 MRR.
- Interpretation rule: top-20 is the budget-fair reranker comparison; top-100 is a larger-candidate-budget condition.

Method design note:

- `thesis_notes/methodology/Final Method Set and Information-Use Plan.md`
- `thesis_notes/checkpoints/methods/M6-v1 Field-Aware Reranker Checkpoint - 2026-06-03.md`
- `thesis_notes/methodology/Methodology Deep Critique and Improvement Plan - 2026-06-05.md`

## Phase 2b: Real-World Skill Audit and Public-Expanded Scale Condition

Status: Mostly complete. The 2349-scale condition, 460 public imports, heuristic public-skill audit, and DeepSeek model-assisted public-skill audit are done. Remaining work is selective manual adjudication of disagreement cases and non-core/public winners.

Purpose:

Use public skills to check whether our proposed representation fields correspond to information found in real skill artifacts, then create a larger scale-sensitivity condition.

Required evidence:

- Public imported skills are stored separately from generated background and controlled core skills.
- Source URL and import status are recorded.
- A field audit reports which public skills contain descriptions, inputs, outputs, workflow steps, dependencies, resources, examples, limitations, and negative boundaries.
- The audit classifies each field as `observed`, `extractable`, or `proposed normalization`.
- Controlled core expansion was kept modest historically, and old 67/85-case results remain useful for development comparison.
- Historical 2089-skill, 2349-skill, and 2401-skill results remain useful for development comparison, but the active frozen-v0.4 condition is 2433 skills, 245 controlled prompts, 144 public-gold prompts, and 12 low-information stress prompts.
- Non-core public winners are manually inspected for whether they are better, acceptable, or only plausible distractors.

Definition of done:

- The thesis can say the representation fields are not only invented from our generated benchmark, but are motivated by literature and checked against public skill artifacts.
- The thesis can separately report results on the original 67-case core and the expanded 85-case core.
- 1006 vs 2089 results are compared as scale sensitivity where historical results are available.
- Gold-label stability remains defensible after public imports.

See `thesis_notes/benchmark/Real World Skill Expansion Plan.md`.

## Phase 2d: Public-Skill Gold Validation

Status: Active frozen-v0.4 public-gold stratum exists and validation gates pass. Cleanup is still needed before final reporting only in the sense of per-source-family failure analysis and thesis prose.

Purpose:

Test whether externally authored public skills can become stable gold-label retrieval targets, rather than serving only as background distractors or evidence for the field taxonomy.

Required evidence:

- At least 100 stable public-gold prompts for external-validity validation. Current frozen-v0.4 stratum: 144 prompts, with 138 acceptable top-1 cases under prompt-specific alignment.
- At least 6 public-skill clusters or source families represented.
- Each prompt has one imported public `gold_skill`.
- Each prompt has 2-4 semantically plausible alternatives.
- Each prompt records a concrete `gold_rationale`, per-alternative rejection rationale, and field-axis annotation.
- Broad or hierarchical public skills are either atomized into a single stable procedure or rejected as gold candidates.
- Prompt text does not name the skill, source repository, or copied distinctive phrases.
- Acceptable alternatives are explicitly recorded instead of being counted as ordinary failures.

Pass criteria:

- 100% prompt references resolve.
- At least 85% of candidate public-gold prompts survive manual gold-label adjudication.
- At least 80% pass prompt-specific procedural alignment.
- At least 70-80% pass semantic-confusability checks under a modern embedding model, with documented exceptions for high-precision cases.
- 0 critical or high-risk prompt leaks.
- Selector results show useful method spread and interpretable failure modes.
- Public-gold results are reported as their own stratum: controlled-authored, public-gold, and combined.

Current checkpoint:

- Active validation reports: `skill_benchmark/outputs/public_gold_step*.md`.
- Historical checkpoint: `thesis_notes/checkpoints/public_gold/Public Gold 120 Expansion Checkpoint - 2026-06-06.md`.
- Step 1 integrity: PASS, 144/144 references resolve.
- Step 2 procedural distinctness: PASS, 144/144 prompts.
- Step 2 prompt-specific alignment: PASS with caveats, 131/144 prompts; acceptable top-1 138/144.
- Step 3 semantic confusability: PASS, 144/144 prompts.
- Step 4 prompt leakage: PASS, 0 critical and 0 high-risk.
- Local selector result: frozen-v0.4 reports exist for the 144-prompt public-gold stratum.
- Provider result: Qwen and SkillRouter have been rerun on the frozen-v0.4 144-prompt public-gold stratum. The strongest strict top-1 values are Qwen R1 + Qwen rerank top-20 at 74.3%, SkillRouter R2 embedding-only at 75.0%, and SkillRouter full embedding-only at 75.0%; reranking effects differ by representation.
- Manual/acceptable-alternative cleanup is encoded in `skill_benchmark/annotations/public_gold_acceptable_alternatives.json`.
- Method interpretation: current schema rerank underperformance on public-gold is evidence that naive field overlap is not enough. The final structure-aware method should parse request-side requirements and compare fields explicitly.

Fail criteria:

- The public skill is too broad, hierarchical, or conditional to be an atomic target.
- The prompt tests a behavior that is not clearly present in the public skill.
- Multiple alternatives are equally correct and no acceptable-alternative label is recorded.
- The result mostly tests source/name matching rather than procedural fit.
- Structure-aware methods win only because our extractor hallucinated fields without evidence spans.

Recommended sequence:

1. Select candidate public skills from the imported corpus.
2. Screen for atomicity and reject broad/hierarchical candidates.
3. Extract fields with the current information-layer extraction pipeline, then verify difficult cases with model-assisted evidence spans.
4. Draft public-gold prompts and alternatives.
5. Manually adjudicate gold stability.
6. Run the existing Steps 1-4 validation scripts on the public-gold subset.
7. Run final method selectors on public-gold-only and combined strata.
8. Analyse failures as candidate-recall, extraction, reranking, ambiguity, hierarchy, or acceptable-alternative failures.

Detailed plan: `thesis_notes/benchmark/public_skills/Public Skill Gold Validation Plan.md`.

## Phase 2c: RQ1 Field-Targeted Ablation

Status: Executed for the seven current operational fields; remaining work is synthesis, presentation, and claim discipline.

Purpose:

Test the thesis claim about which operational information matters. This is different from showing that one architecture performs well. It asks which fields contribute to distinguishing semantically similar skills.

Important interpretation update, 2026-06-23:

- The I1/I3/I2 retrieval matrix mostly answers RQ2 because it compares complete representation and retrieval strategies.
- The current global field ablation is partial RQ1 evidence because it varies field visibility, but it still aggregates across prompts whose decisive field may differ.
- Strong RQ1 claims require prompts or prompt clusters labelled by the field that should resolve the confusion.

Detailed design source: `thesis_notes/current/RQ1/protocols/RQ1 Field Targeted Test Plan.md`.

Active RQ1 split:

- RQ1a: individual field discriminability under controlled shared context.
- Supporting RQ1b audit: field prevalence and recoverability in controlled, public-gold, and external skill corpora. RQ1b naturalistic replication: frozen original-artifact acceptable-set selection, not causal masking unless an explicitly mask-eligible future wave is found.
- No RQ1c is currently defined.

Required ablations:

- Description only.
- Description + use conditions.
- + input/precondition fields.
- + output artifact fields.
- + workflow/procedure fields.
- + constraints/not-for boundaries.
- + dependencies/resources.
- + success/verification criteria where available.

Required RQ1 test-case conditions:

- The gold skill and alternatives must be semantically similar enough that a short description can plausibly confuse them.
- The prompt must contain a concrete operational requirement that maps to a `primary_distinguishing_field`. The prompt should be explicit enough for a stable gold label; it should not be made vague to avoid leakage.
- The gold skill must satisfy that field better than the alternatives.
- The field should be recoverable from the skill artifact without using the gold label or benchmark-only alternative list.
- The prompt must avoid exact skill-name leakage and unique copied phrases.
- Leakage control is applied on the skill side: the controlled baseline skill description keeps the shared cluster/task context but masks the primary distinguishing field.
- The controlled baseline must not be too vague. For example, "Extracts structured information from PDF documents" is better than "Handles PDF document processing tasks" for a PDF extraction cluster.
- The shared context may name broad task families such as PDF extraction, dataset quality, API work, browser evaluation, experiment execution, or compliance review.
- The shared context must not name target values such as scanned/native, JSON/prose, validate/repair, legal-advice/no-legal-advice, HF Jobs/local, or visual-evidence/data-scrape.
- Each field should have enough examples across domains to avoid a one-domain artifact.
- The canonical headline comparison for each field is `shared_context_only` versus `shared_context_plus_field`. The latter means the same shared non-target context plus exactly one target field line.
- `full_skill_doc` is a diagnostic whole-document condition, not the main RQ1a exposed-field condition.

Candidate field-labelled case families:

| Primary field | Example confusion | Why it tests RQ1 |
|---|---|---|
| use condition / task trigger | API contract review vs API integration planning. | Same domain and vocabulary, different user intent. |
| input / precondition | Native PDF extraction vs scanned PDF OCR. | Same object, different input state. |
| output / artifact | PDF table extraction vs PDF summarisation. | Same input, different expected artifact. |
| workflow / procedure | Data validation vs data repair vs anomaly explanation. | Same dataset domain, different operation sequence. |
| boundary / not-for | General legal/policy summary vs non-advice compliance triage. | Correct skill depends on exclusion/guardrail. |
| dependency / resource | Local experiment runner vs Hugging Face Jobs runner. | Same task, different required execution environment. |
| success / verification | UI visual QA vs browser data extraction. | Same web/browser domain, different success criterion. |

Construction sequence:

1. Derive candidate labels from existing validation artifacts where possible:
   - controlled `procedural_distinctness_report.json`;
   - controlled `procedural_requirement_alignment_report.json`;
   - public-gold prompt `field_axes`;
   - R2/R3 representation evidence.
2. For each prompt, assign one `primary_distinguishing_field` only when the decisive requirement is clear.
3. Mark prompts with multiple equally decisive fields as `multi_field` and keep them for RQ2/failure analysis rather than clean RQ1 field ranking.
4. Create or derive controlled skill-side baseline descriptions that preserve shared cluster context while masking the primary field.
5. Mark original descriptions that already expose the primary field as realistic but leaky for causal RQ1.
6. Check each field has enough cross-domain cases. If not, author a small additional controlled case set under a new benchmark version rather than editing frozen-v0.4 prompts.
7. Run the field ablation by primary field label and report field-specific deltas.
8. Only after this step, decide whether graph/tree/DAG methods should be added as RQ2 strategy comparisons.

Approval gate:

- The approved RQ1a condition set has now been applied to use condition, input/precondition, output/artifact, dependency/resource, boundary/not-for, success/verification, and workflow/procedure.
- Do not create additional RQ1 cluster prompt files unless they answer a specific unresolved claim, such as field interaction or a deliberately chosen negative-control field.
- Optional isolated corruption diagnostics must keep all non-target fields controlled and non-discriminative. Multi-field conflict corruption belongs to RQ2 robustness, not the main RQ1 field-value test.

Definition of done:

- A compact synthesis table reports hidden-field versus exposed-field top-1/MRR by field and prompt subset.
- The analysis identifies which fields give strong first-pass gains, which are conditional, which require reasoning/context, and which are workflow-support rather than routing fields.
- The thesis can answer RQ1 with evidence rather than only intuition.
- Qualitative examples show why each claim tier is justified.
- Claim boundaries are written beside each field result before any broad conclusion.

Current report:

- `skill_benchmark/outputs/field_ablation_results.md`
- `thesis_notes/results/Field Ablation Results - 2089 Scale.md`
- Refreshed frozen-v0.4 field ablation reports:
  - `skill_benchmark/outputs/frozen_v0_4_controlled_field_ablation.md`
  - `skill_benchmark/outputs/frozen_v0_4_public_gold_field_ablation.md`

Main RQ1a result:

- Strong first-pass routing fields: input/precondition, use condition, dependency/resource when framed as capability compatibility, and output/artifact under semantic retrieval.
- Conditional routing fields: boundary/not-for, success/verification, and workflow/procedure. These improve over hidden-field ties, but their value depends more on prompt wording, implied authority/context, acceptance-gate clarity, or operation-order reasoning.
- Negative-control/support field: examples/tests. Generic examples do not create a stable operational gold label; rare exact example matches can strongly attract retrievers, so examples are useful execution/support context but weak independent routing evidence.
- Earlier global field-ablation reports remain useful historical/RQ2-adjacent evidence, but final RQ1 field claims should come from the field-isolation suites.

Pass condition:

- At least one non-description field improves retrieval or reduces non-core false positives.
- If a field does not help, it is reported honestly as context-dependent or mainly useful for downstream execution rather than retrieval.
- No field is claimed as generally useful unless it improves the field-labelled subset or explains a reduction in hard-negative errors.

## Phase 3: Candidate Budget, Cost, and Latency

Status: Still required, but now follows the methodology-hardening checks.

Purpose:

Decide whether the strongest hybrid method is practical, especially at top-100 candidate budget.

Required comparisons:

- Qwen full embedding plus M6-v1-local or schema rerank at top-20, top-50, top-100.
- SkillRouter first stage plus SkillRouter rerank and M6-v1-local at matching budgets where feasible.
- Record top-1, top-5, MRR.
- Record local rerank time.
- Record whether embeddings are cached or require API calls.
- Estimate exposed candidate text length or token cost.
- Include a context-scale statement distinguishing compact metadata scale from full-artifact/structured-representation scale.

Definition of done:

- A table shows accuracy-efficiency trade-off for top-20, top-50, and top-100.
- A written decision states whether top-100 is acceptable, or whether top-50 is a better thesis recommendation.
- The thesis can say whether the best accuracy gain is worth the extra candidate budget.

Pass condition:

- One candidate budget is selected for downstream validation.
- The selection is justified by both accuracy and efficiency.

## Phase 4: Failure Mode Analysis

Status: Partially complete.

Purpose:

Turn result tables into thesis insight about what information retrieval methods preserve or lose.

Required methods to analyze:

- One flat baseline.
- One dense retrieval baseline.
- One generic neural reranker.
- The strongest hybrid method.

Required failure categories:

- First-stage exclusion.
- Semantic similarity collapse.
- Procedural field missing or underweighted.
- Negative boundary failure.
- Object/task confusion.
- Meta-skill confusion.
- Underspecified prompt.
- Acceptable alternative or annotation ambiguity.

Definition of done:

- Each final method has failure counts by category.
- At least 5 representative examples are written as thesis-ready case studies.
- The analysis explicitly connects each failure type to missing or misused representation information.

## Phase 5: Downstream Validation

Status: Planned, not executed.

Purpose:

Show whether retrieval improvements matter for actual task completion, not only ranking metrics.

Minimum viable design:

- Use 12 representative prompts.
- Include easy-success, known-confusion, and failure-prone cases.
- Compare 3 conditions:
  - flat baseline;
  - dense full-skill baseline;
  - strongest hybrid method.
- Add oracle-gold skill condition if feasible.

Pass condition:

- Oracle-gold downstream success should be at least 80%. If not, the task or skill artifact is unstable.
- Retrieval methods should only be judged downstream when the gold or acceptable skill is in the candidate set.
- Failures should be labelled as retrieval failure, skill-use failure, or task ambiguity.

Definition of done:

- Downstream artifacts exist.
- A grading rubric exists.
- Results connect retrieval quality to task success.

## Phase 6: Thesis Writing Integration

Status: Scaffold created.

Purpose:

Make sure experiments feed directly into the thesis rather than becoming disconnected reports.

Required updates:

- Update Chapter 1 with final RQs and contribution wording.
- Update Chapter 2 literature review so the final synthesis matches the current RQs.
- Fill Chapter 4 with benchmark cluster examples and validation table.
- Fill Chapter 5 with final method table and schema reranker formula.
- Fill Chapter 6 with final result tables.
- Fill Chapter 7 with failure mode analysis and design implications.
- Update conclusion only after downstream validation is complete or explicitly scoped out.

Definition of done:

- Every final result table has a matching interpretation paragraph.
- Every major claim has evidence from either literature, benchmark validation, retrieval metrics, efficiency metrics, or failure analysis.
- The thesis answers RQ1 and RQ2 directly.

## Stop Rules

Stop adding new experiments when:

- The experiment only changes provider/model but not representation information.
- The experiment cannot be compared on the same prompts, library size, and metrics.
- The experiment delays Phase 3 cost/latency or Phase 5 downstream validation.
- The expected thesis contribution would still be the same without it.

Run a new experiment only if it answers one of these:

- Does this representation preserve different information?
- Does this retrieval strategy exploit preserved information differently?
- Does this explain a failure mode in the current best method?
- Does this improve the final thesis argument, not just the score table?

## Immediate Next Steps

1. Keep the reviewed RQ1a cluster content frozen except for proven errors. `COMPLETE / ONGOING CONTROL`.
2. RQ2a protocol, representations, selectors, development split, inference rules, field-aware choice, analysis, cost ledger, and immutable confirmatory hashes are `COMPLETE / FROZEN`.
3. The separately authorised 280-cluster confirmatory run is `COMPLETE / PASS`: 600 prompts, 22 conditions, and 13,200 primary rows.
4. Frozen paired statistics, field/variant slices, cost/latency ledger, and failure examples are `COMPLETE / PASS`.
5. User results review and thesis integration are `COMPLETE`; the approved bounded interpretation is recorded in the canonical RQ2a analysis note.
6. RQ2b B0 source/provenance/token-limit audit and independent review are `COMPLETE`; review amendments are incorporated.
7. RQ2b B0F, B0F-A1, and B1X are `COMPLETE`; native SkillRouter embedding is prospectively approved, and the earlier B1S v17 smoke/seal verifies the pre-v1.1/pre-A2 implementation. The v1.1 strict-only overlay and B0F-A2 require a refreshed local smoke/seal before any science. The intended B2 comparison is dual-reranker: SkillRouter-Reranker-0.6B and Qwen `qwen3-rerank` must independently score the identical persisted Top-20 candidate list for every B1 condition. Qwen remains behind B0F-A2 review, a new seal, and a separate provider authorization. Do not extract I3C or launch a scientific selector until the relevant separate gate is approved. Keep I3C text transfer, Qwen API work, native encoder model download or compute/hosted transfer, reranking, and thesis writing behind separate gates. Graph/tree, external neural, and downstream extensions remain outside the minimal core.
