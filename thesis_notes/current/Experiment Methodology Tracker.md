# Experiment Methodology Tracker

Last updated: 2026-09-04

> **2026-09-04 unified RQ1 thesis integration (`SCIENTIFICALLY COMPLETE / THESIS-INTEGRATED / RESEARCHER REVIEW COMPLETE`).** RQ1 is now reported as one research question with two complementary interventions, rather than as separately named RQ1a/RQ1b results. Experiment 1 is the researcher-confirmed controlled near-neighbour field-isolation study; its examples/tests suite remains a negative control, not an eighth routing field. Experiment 2 is the source-grounded and mechanically validated public original-document removal study: the same source document is scored intact and after every cited line for one field, or one exact-union field group, is removed from every candidate. The 2026-08-30 derivative field-card ablation is retained only as historical sensitivity because it tests a materially different representation and cannot be pooled with source-document removal. The current public RQ1 conclusion is cross-retriever stable evidence for use condition and success/verification; task specification and execution/verification are also stable joint groups. Other individual fields are retriever-conditional, and boundary/not-for has no stable positive strict Top-1 result. The unblinded researcher confirmation at `skill_benchmark/rq1_human_review/2026-09-04/` is complete: all 350 controlled, 194 public-gold, and 402 public-removal rows were approved. Exact instructions are preserved in packet receipts. Frozen gold was visible in the first two streams and intact/removed documents in the third; this supports researcher confirmation, not blinded or independent annotation. No further RQ1 experiment is required under the current scope. The remaining RQ1 work is final submission editing, dated RQ1 entries below are historical, and the active research focus moves to RQ2. The writing packet is `thesis_notes/current/Results Writing Packet - 2026-09-04.md`; the status index is `thesis_notes/current/RQ1/README.md`.

> **2026-09-04 results-writing packet (`SUPERSEDED BY UNIFIED RQ1 INTEGRATION`).**
> A consolidated table/metric inventory for the completed controlled RQ1, latest
> source-original RQ1 removal, RQ2a and RQ2b V3 packages is now at
> `thesis_notes/current/Results Writing Packet - 2026-09-04.md`. It expressly
> distinguishes the current original-source RQ1 results from the older
> field-card ablation, which must not be pooled. It also records that RQ2b
> B3-v2's old local `not thesis text` label was superseded by the already
> verified B5 integration in the thesis chapters.

> **2026-09-04 RQ1 public-original joint group extension (`HISTORICAL PRE-CLOSURE CHECKPOINT / SUPERSEDED BY TOP BLOCK`).** The completed Round-3 source-original single-field twin intentionally excluded joint masks. This supporting extension treats task specification (use/input/output), execution/verification (workflow/success), and applicability/capability (boundary/dependency) as three separately analysed source-document deletion groups. It uses only intersections of the existing clean `CLEAR` single-field cases: respectively 99/37, 138/51 and 132/50 routing-family cases/compositions, totalling 369 cases and 1,476 ranking rows per retriever. Group documents are exact line-deletion unions of their verified component Round-3 masks; the derived-clear audit passed and confirms that no group mask can reintroduce a component-removed line. Both retrievers and their independent row/paired-analysis validators passed. BM25 Full-minus-Removed Hit@1 is +0.266 [+0.196, +0.336], +0.176 [+0.094, +0.262] and +0.136 [+0.087, +0.186]. Qwen `text-embedding-v4` (1024) is +0.088 [+0.005, +0.162], +0.074 [+0.007, +0.141] and +0.014 [-0.043, +0.062], respectively. Thus task specification and execution/verification are stable positive groups in both first-stage retrievers; applicability/capability is BM25-positive but Qwen-indeterminate. Qwen used the explicitly authorised payload `8d9d87e791a0f34807f4a2ae8f85ec43798a7df356bffd8a38a4db22520bb2ea`: 342 new document texts, zero query texts, 35 successful no-retry calls and 283,526 provider-reported input tokens. At this checkpoint these results had not yet entered the thesis; the closure block above records their later review and integration. They remain group-specific combined-information results, not component attribution or cross-retriever score pooling. SOP: `thesis_notes/current/RQ1/protocols/RQ1 Public Original Round 3 Joint Group Extension SOP - 2026-09-04.md`; checkpoints: `thesis_notes/checkpoints/methods/RQ1 Public Original Round 3 Joint Group BM25 Result - 2026-09-04.md`, `thesis_notes/checkpoints/methods/RQ1 Public Original Round 3 Joint Group Qwen Result - 2026-09-04.md`.

> **2026-09-04 RQ1 public-original clean-only twin (`HISTORICAL PRE-CLOSURE CHECKPOINT / SUPERSEDED BY TOP BLOCK`).** The frozen Round-3 source-original field-removal comparison completed for both first-stage retrievers: deterministic local BM25 and DashScope international Qwen `text-embedding-v4` at 1024 dimensions. Each ran the identical 1,078 composition-family cases, direct/paraphrase prompt pairs and full-versus-single-field-removed candidates, producing and independently validating 4,312 ranking rows per retriever. Qwen used the explicitly authorised payload `38a8bab9938f884390caae6c0c062aac7ff7d08510b7e380156cf7fa6dba16d2`: 1,898 cache-miss texts, 190 successful no-retry requests and 2,394,292 provider-reported input tokens; embeddings persist locally. A composition-clustered paired bootstrap finds stable positive Full-minus-Removed Hit@1 changes for use condition and success/verification under both retrievers. BM25 additionally has stable positive changes for input/precondition, output/artifact, workflow/procedure and dependency/resource; Qwen's intervals for those four fields cross zero. Boundary/not-for is not a stable positive Top-1 effect for either retriever. At this checkpoint the result still awaited user review and thesis integration; the closure block above records their completion. The result remains field-specific and retriever-conditional: it does not pool raw BM25 and cosine scores or claim all fields are equally important. Canonical outputs: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_{bm25_results,qwen_results,twin_synthesis}/`; checkpoint: `thesis_notes/checkpoints/methods/RQ1 Public Original Round 3 Twin Result and Failure Analysis - 2026-09-04.md`.

> **2026-09-04 RQ1 public-original Qwen preflight (`F2 COMPLETE / HISTORICAL PRE-EXECUTION STATE`).** A local-only, hash-validated preflight was built from the same 1,078-case Round-3 clean-only freeze as BM25. It identifies 1,510 unique document texts and 388 unique prompt texts, all cache misses under the dedicated text-embedding-v4/1024 cache schema: 1,898 potential outbound texts, 10,109,779 UTF-8 bytes, 1,341,769 local lexical token proxy and at most 190 request attempts/successes with no retry. Its payload SHA-256 is `38a8bab9938f884390caae6c0c062aac7ff7d08510b7e380156cf7fa6dba16d2`; independent validation confirmed zero network calls and zero transmitted texts at preflight time. This record is superseded for current run state by the F1--F3 completion entry above. Checkpoint: `thesis_notes/checkpoints/methods/RQ1 Public Original Round 3 Qwen Preflight - 2026-09-04.md`.

> **2026-09-04 RQ1 public-original clean-only BM25 (`F1 COMPLETE / QWEN PENDING`).** The local deterministic BM25 twin completed from the F0 freeze: 1,078 composition-family cases x direct/paraphrase x full/removed condition = 4,312 ranking rows. Independent row and composition-level analysis validators passed; result hash is `010fee2f8f548bcd22c08f2eb8b65bdece0850c2cce231fdad58f178967ee1d3`. At the equal-weight composition level, removing use, input, output, workflow, success or dependency information lowers Hit@1 by 0.091--0.151, with each field's 95% composition-clustered paired bootstrap interval above zero. Boundary/not-for changes Hit@1 by +0.024 with interval [-0.014, 0.064], so it is not a stable BM25 Top-1 effect despite a positive margin diagnostic. This is a BM25-only source-based RQ1 result, not a cross-retriever conclusion; no Qwen/API/hosted run or thesis/PDF write has happened. Full result and limits: `thesis_notes/checkpoints/methods/RQ1 Public Original Round 3 BM25 Result - 2026-09-04.md`.

> **2026-09-04 RQ1 public-original clean-only test freeze (`F0 COMPLETE / SELECTORS NOT RUN`).** The project selected the Round-3 clean-only denominator rather than a fourth deletion round. The frozen primary comparison is exact full public originals versus exact Round-3 single-field removal masks, with a field-specific unit admitted only when every candidate is Round-3 `CLEAR`, all source/mask hashes verify, and a pre-existing strict singleton-gold family supplies exactly one direct and one paraphrase prompt. The freeze contains 1,078 composition-family cases / 2,156 prompt rows across 82 source compositions, but prompt rows are repeated measures: primary estimates first average prompt variants and routing families within each composition, then use a composition-clustered paired bootstrap. Eligible composition counts are use 57, input 53, output 49, workflow 63, success 59, boundary 69, dependency 52; all pass the predeclared 30-composition minimum. The local BM25 runner has passed only a synthetic self-test and no-scoring 4,312-row dry run; no real BM25, Qwen, API, hosted run, metric or thesis/PDF result exists yet. SOP: `thesis_notes/current/RQ1/protocols/RQ1 Public Original Round 3 Clean-Only Scoring Freeze and Test SOP - 2026-09-04.md`; checkpoint: `thesis_notes/checkpoints/methods/RQ1 Public Original Round 3 Clean-Only Scoring Freeze - 2026-09-04.md`; machine freeze: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/round3_clean_only_scoring_freeze/`.

> **2026-09-04 RQ1 exhaustive public-original ablation (`FORCED-REMOVAL ROUND 3 COMPLETE / NO SCORING`).** Fresh anonymous clearance is complete and parent-validated for all 574/574 units and 1,855/1,855 candidate cards. All 574 canonical records passed the Round-3 schema, identity and exact current-card evidence validator. Candidate decisions are 1,609 `CLEAR`, 232 `RESIDUAL`, and 14 `UNCERTAIN`; 439 units are `CLEAR` across every candidate. The field-level fully-clear unit counts are boundary/not-for 77/82, dependency/resource 55/82, input/precondition 58/82, output/artifact 55/82, success/verification 65/82, use-condition 62/82, and workflow/procedure 67/82. Compared with Round 2, cited deletion improves clearance but does not establish total absence of the target field in every public document. This is a full-document redaction/clearance result, not routing evidence, a selector denominator, or an authorisation to score. The next step requires an explicit method decision between another evidence-cited removal round and a separately frozen clean-only complete-case scoring protocol. Completion checkpoint: `thesis_notes/checkpoints/methods/RQ1 Public Original Exhaustive Ablation Forced Removal Round 3 Completion - 2026-09-04.md`.

> **2026-09-04 RQ1 exhaustive public-original ablation (`FORCED-REMOVAL ROUND 3 TECHNICAL MATERIALISATION COMPLETE / FRESH BLIND CLEARANCE ACTIVE / NO SCORING`).** Round 3 deterministically removed only the 573 exact current-card lines cited by the 383 canonical Round-2 `RESIDUAL` decisions. It covers all 574 units / 1,855 candidate cards: 1,464 Round-2 `CLEAR` and 8 `UNCERTAIN` cards were copied byte-for-byte, while only the evidence-cited residual cards changed. The local exact-diff audit passed with zero failures. This is a routing-only representation transformation, not proof that target information is absent and not a routing result. New prompt/gold/source-map/selector-blind clearance is active; no selector, API, hosted, scoring or thesis/PDF action is authorised. SOP: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/FORCED_REMOVAL_ROUND3_SOP.md`; technical checkpoint: `thesis_notes/checkpoints/methods/RQ1 Public Original Exhaustive Ablation Forced Removal Round 3 Technical Materialisation - 2026-09-04.md`.

> **2026-09-04 RQ1 exhaustive public-original ablation (`FORCED-REMOVAL ROUND 2 COMPLETE / NO SCORING`).** The fresh source/prompt/gold/map/selector-blind clearance ledger is complete and parent-validated: 574/574 units, 82/82 compositions and 1,855/1,855 candidate cards. Decisions are 1,464 `CLEAR`, 383 `RESIDUAL`, and 8 `UNCERTAIN`; 377 units are clear across every candidate. This demonstrates that deleting all known Round-1 leakage reduces but does not eliminate field overlap. It is a clearance finding, not routing evidence or a frozen scoring denominator. Round 3 may delete only exact spans cited by the 383 Round-2 residual records; the eight uncertain cards have no such evidence and remain non-clean. No selector/API/scoring/PDF action is authorised. Completion checkpoint: `thesis_notes/checkpoints/methods/RQ1 Public Original Exhaustive Ablation Forced Removal Round 2 Completion - 2026-09-04.md`.

> **2026-09-04 RQ1 exhaustive public-original ablation (`FORCED-REMOVAL ROUND 2 SERVICE-BLOCKED PARTIAL CLEARANCE / NO SCORING`).** Fresh source/prompt/gold/map/selector-blind clearance has been canonicalised for `OR82-001--070`: 490/574 field units, 70/82 compositions, and 1,589/1,855 candidate cards. The verified decisions are 1,229 `CLEAR`, 358 `RESIDUAL`, and 2 `UNCERTAIN`; 312 units are clear for every candidate. Each canonical record passed parent JSON, identity, exact-evidence and current-card quote validation. The remaining 84 units / 266 cards (`OR82-071--082`) remain unreviewed, not inferred clear or residual. On 2026-09-04, fresh-reviewer startup repeatedly failed before packet access with the same Codex backend `404`; all failed agents were closed without outputs. This is a service block on the remaining blind-clearance work, not a scientific result, and no selector/API/scoring/PDF action is authorised. Resume only with fresh clearance for the 12 missing compositions, then construct Round 3 from all canonical Round-2 residual spans. Checkpoint: `thesis_notes/checkpoints/methods/RQ1 Public Original Exhaustive Ablation Forced Removal Round 2 Service-Blocked Checkpoint - 2026-09-04.md`.

> **2026-09-03 RQ1 exhaustive public-original ablation (`FULL BLIND CLEARANCE ROUND 1 COMPLETE / NO SCORING`).** The active unified primary frame is frozen at 82 compositions / 265 original public documents / 574 composition-field units. Its canonical ledger retains 265 source paths and 264 distinct byte hashes because two paths have byte-identical content. Exact local materialisation produced 574 single-field and 246 joint conditions (2,650 masks); all 2,650 passed exact-diff audit with zero unlogged edits. The 44 no-op masks and 515 `NEAR_EMPTY` masks remain reported density properties, not exclusions. All 574/574 single-field units and 1,855 candidate masks independently underwent prompt/gold/source-map-blind clearance: 710 candidate reviews are `CLEAR`, 1,145 are `RESIDUAL`, and none is `UNCERTAIN`. Every canonical record passed the exact-span validator before ingest, and canonical file count is 574. W015-B01 remains a delayed duplicate explicitly non-adopted beside the frozen assignment. This completes clearance only: it is neither a routing result nor a selector denominator. No prompt, gold label, source identity, candidate role, selector, API, hosted job or thesis/PDF result entered this stage. SOP: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/FULL_CLEARANCE_SOP.md`; canonical ledger: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/canonical_field_map_ledger/CANONICAL_FIELD_MAP_LEDGER.json`; mask audit: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/full_target_masks/audit/exact_diff_audit.json`; completion checkpoint: `thesis_notes/checkpoints/methods/RQ1 Public Original Exhaustive Ablation Full Clearance Round 1 Completion - 2026-09-03.md`.

> **2026-09-03 RQ1 exhaustive public-original ablation (`FORCED-REMOVAL ROUND 2 PREPARED / NO SCORING`).** Round 1 showed that natural public skill documents often repeat target-field information outside their mapped field spans. The follow-on condition therefore preserves all immutable originals and Round-1 evidence while deterministically deleting every exact residual span cited by the Round-1 canonical ledger. This is explicitly a routing-only representation: it may leave a damaged or non-executable skill document, which is admissible because the question is whether the removed information changes routing rather than whether the modified skill can still run. The materialiser records round-one hashes, evidence, deleted line numbers, post-deletion hashes and token loss for all 574 single-field units / 1,855 candidate cards. It is not itself a scientific clearance result: a second fresh prompt/gold/source-map/selector-blind clearance is mandatory before any selector scoring. SOP: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/FORCED_REMOVAL_ROUND2_SOP.md`.

> **2026-09-03 RQ1 exhaustive public-original ablation (`FORCED-REMOVAL ROUND 2 FRESH-CLEARANCE PARTIAL CHECKPOINT / NO SCORING`).** The deterministic Round-2 transformation deleted 6,480 Round-1-cited residual lines across all 574 units / 1,855 cards and passed a zero-failure local exact-diff audit. Fresh source/prompt/gold/map/selector-blind review has now canonicalised 98/574 units (14 complete compositions, OR82-006--OR82-019) and 322 candidate cards: 245 `CLEAR`, 77 `RESIDUAL`, 0 `UNCERTAIN`; 58 units have every candidate `CLEAR`. These are progress counts only, not a frozen denominator or routing result. The 476 unreviewed units remain neither clear nor residual by inference. Initial independent reviews show that removal of all known Round-1 spans substantially reduces but does not always eliminate target information; newly cited exact spans must feed a later Round-3 forced deletion only after full Round-2 coverage. All agents used for this completed batch were closed. Resume with fresh reviewers for OR82-001--OR82-005 under the shared-output procedure, then OR82-020 onward; revalidate and canonicalise every returned JSON before use. Evidence: `skill_benchmark/rq1_public_original_exhaustive_ablation_v1/forced_round2_masks/`, `forced_round2_clearance/canonical_round2/`, and `FORCED_REMOVAL_ROUND2_SOP.md`.

> **Historical pilot only (`SUPERSEDED AS THE PRIMARY STATUS`).** The earlier 14-unit / 49-candidate target-clear pilot remains an auditable development artifact. It is not the current public-original denominator and must not be reported as completion of the 574-unit experiment. The current primary status is the full blind-clearance round recorded above.

> **2026-08-31 RQ1 public-corpus consolidation.** The sole source-composition
> intake frame is now the 82-entry deduplicated registry: 76 historical C6
> compositions plus six direct-V3 C6 additions. The completed selector result
> remains 46 scored compositions / 99 strict routing families / 198 prompts;
> 87 V2 families are historical subset accounting, not a second corpus. All
> later public RQ1 methods must run eligibility on the 82-entry frame and
> freeze one complete-case subset before scoring. See
> `thesis_notes/current/RQ1/supporting/RQ1 Public Corpus Consolidation Policy - 2026-08-31.md`.

> **2026-08-31 RQ1 82-registry source-only parse (`S0 COMPLETE / NO MASK OR SELECTOR`).** The complete, merged source registry has been parsed before any new intervention: 82 compositions / 265 original skill documents. Seventy-six historical compositions were reused only after exact original-byte hash, candidate identity/order and seven-field-schema verification; six direct-V3 compositions (18 original documents, including two prompt-coverage-partial compositions) received independent source-only parsing. The final ledger contains 1,860 exact evidence spans and passes hash, three/four-candidate coverage, seven-field-schema, line-range and quote-substring verification with zero failures. Field presence is structural inventory only, not routing evidence. No prompt, gold label, selector, embedding, mask or metric entered S0. Output root: `skill_benchmark/rq1_public_original_removal_v3_82_registry/`; audit: `skill_benchmark/rq1_public_original_removal_v3_82_registry/audit/parse_audit.json`; checkpoint: `thesis_notes/checkpoints/methods/RQ1 82 Registry Source Parse Closure - 2026-08-31.md`.

> **2026-08-31 RQ1 public-original 82-registry removal (`S1 SOURCE-ONLY ELIGIBILITY COMPLETE / NO SELECTOR OR EXTERNAL EXECUTION`).** The fresh, non-overwriting candidate-field removal-map audit completed across all 82 compositions / 265 hash-verified original documents. Twenty-eight canonical batches passed structural, evidence-coverage, line-range, non-broadening and unsafe-blocker validation. `MAP_READY` counts are 21 use-condition, 19 input/precondition, 25 output-artifact, 22 workflow/procedure, 32 success/verification, 37 boundary/not-for and 27 dependency/resource; 0--1 composition per field has no editable value and the remainder is conservatively `ORIGINAL_ONLY` because a candidate has an unsafe or uncertain removal. This is neither a residual-clearance nor a routing effect. Only exact-diff materialisation, independent prompt/gold-blind residual review, strict-family linkage and a frozen complete-case denominator may make a selector stage eligible. No prompt, gold label, selector, embedding/API, hosted compute, or thesis/PDF result entered S1. Protocol: `thesis_notes/archive/RQ1/original-document-lineage/RQ1 Public Original-Document 82 Registry Removal Amendment - 2026-08-31.md`; ledger: `skill_benchmark/rq1_public_original_removal_v3_82_registry/eligibility_ledger/`; checkpoint: `thesis_notes/checkpoints/methods/RQ1 82 Registry S1 Eligibility Closure - 2026-08-31.md`.

> **2026-08-31 RQ1 public-original 82-registry materialisation (`S2 COMPLETE / LOCAL TECHNICAL ONLY / PENDING BLIND RESIDUAL REVIEW`).** Frozen S1 maps produced 750 candidate-mask rows: single-field conditions cover 19--37 compositions each; the map-ready group conditions cover 5 task-specification, 18 execution/verification and 22 applicability/capability compositions. Independent reconstruction found zero source-hash, masked-hash or unregistered-diff failures. The 1,144 ledgered no-op blank lines are permitted because they were already empty and did not alter text. One task-specification group is excluded for conflicting canonical replacements; no other condition was repaired. This technical closure is not a residual or routing result. Next is S3, a fresh prompt/gold-blind single-field residual review; group clearance can only be derived when every component single-field condition survives. Evidence: `thesis_notes/checkpoints/methods/RQ1 82 Registry S2 Technical Materialisation Closure - 2026-08-31.md`; S3 SOP: `thesis_notes/archive/RQ1/original-document-lineage/RQ1 Public Original-Document S3 Blind Residual Review SOP - 2026-08-31.md`.

> **2026-08-31 RQ1 public-original 82-registry residual closure (`S3 COMPLETE / FEASIBILITY CLOSED / NO SCORING`).** The prompt/gold/source-map-blind residual audit reviewed all 183 technically materialised single-field composition conditions in 61 canonical batches. Thirty-three conditions are `CLEAR`: use-condition 2/21, input/precondition 2/19, output-artifact 3/25, workflow/procedure 0/22, success/verification 11/32, boundary/not-for 15/37 and dependency/resource 0/27. All three pre-specified groups have zero surviving compositions because every group includes at least one non-clear component field. This is too sparse for the intended seven-field/three-group public RQ1 comparison; strict-family linkage, denominator freezing and selectors stop here. The outcome is a conservative full-document deletion feasibility result, not a retrieval effect or a statement that the fields lack routing value. Evidence: `skill_benchmark/rq1_public_original_removal_v3_82_registry/blind_residual_ledger/`; checkpoint: `thesis_notes/checkpoints/methods/RQ1 82 Registry S3 Blind Residual Closure - 2026-08-31.md`.

> **2026-08-31 S1 first-wave mapper quality gate (`REMAP REQUIRED / NOT A FIELD-ELIGIBILITY RESULT`).** The first six anonymous mapping batches covered 18 compositions, but all six were rejected before canonical ledger ingestion: their `UNSAFE_MIXED_CARRIER` decisions lacked line-addressable blocking evidence naming the non-target content that an edit would remove. The strengthened validator now fails these files, including one preliminary copy made before the rule existed. This is a mapping-quality correction, not evidence that the fields are unremovable. The same source-only packets are being remapped under `ELIGIBILITY_QUALITY_AMENDMENT.md`; no selector, residual review, score, external transfer, or thesis/PDF result is authorised. Audit: `skill_benchmark/rq1_public_original_removal_v3_82_registry/eligibility_submissions/review/FIRST_WAVE_QUALITY_REJECTION.md`.

> **2026-08-31 RQ1 public-original information-removal feasibility audit (`CLOSED / NO SELECTOR OR EXTERNAL EMBEDDING EXECUTION`).** This local audit compared complete frozen public originals with source-line masks that removed one documented field or group without broadening the skill's capability. It is a routing-only intervention, so the edited document was permitted to become incomplete or non-executable. The source-only first-pass mapping, exact-diff audit, and a 42-item stratified residual review found `35 residual / 7 clear`. Thirty-two affected items received a supplemental source-only map; three were unsafe mixed carriers and one had an edit conflict. The 31 rebuilt masks passed a fresh technical audit, then a new prompt/label-blind reviewer found `28 residual / 3 clear`. This leaves no credible denominator for single-field or group BM25/Qwen metrics. It is a **document-redaction feasibility finding**, not a field-effect result: no query, label, selector, embedding/API transfer, hosted run, human review packet, or thesis/PDF result was created. It does not alter the already completed derivative public-card RQ1b experiment. Evidence: `thesis_notes/checkpoints/methods/RQ1 Public Original-Document Redaction Feasibility Closure - 2026-08-31.md`; protocol: `thesis_notes/archive/RQ1/original-document-lineage/RQ1 Public Original-Document Information-Removal Execution SOP - 2026-08-31.md`.

> **2026-08-31 RQ1 public-original information-removal execution (`FIRST-PASS REDACTION MAP INCOMPLETE / NO SELECTOR OR EXTERNAL EMBEDDING EXECUTION`).** RQ1 will compare each complete frozen original document with the same document after the explicit, candidate-distinguishing values of one field have been removed. Input examples include format, schema, source state, path, prior-artifact name, and credential. The edited text may become incomplete or non-executable; that is acceptable because this is a routing-only RQ1 comparison, not a downstream execution test. Task/method identity remains, and a removal must never broaden the original capability (for example, it must not turn `PDF` into “any file”). Source-only parsing, conservative first-pass maps, materialisation, and exact reconstruction have completed. A stratified prompt-blind residual review over 42 composition-condition items spanning all seven fields and three groups found explicit field-value residue in 35 items and cleared 7. This is a map-completeness gate, not a selector result: the affected items require source-only expansion plus fresh residual review; leaked masks will not be scored. CFTC-001/002 remain historical feasibility records under the older semantic-erasure rule; any reuse needs fresh residual and human review. Rule and SOP: `thesis_notes/archive/RQ1/original-document-lineage/RQ1 Public Original-Document Redaction Amendment - 2026-08-31.md` and `thesis_notes/archive/RQ1/original-document-lineage/RQ1 Public Original-Document Information-Removal Execution SOP - 2026-08-31.md`.

> **2026-08-31 CFTC-001 original-document feasibility gate (`FIELD_MASK_REJECT / NO SCORING`).** A fresh prompt-blind source-only mapper and a separate prompt-blind feasibility reviewer examined three complete original documents for an `input_precondition` intervention. Although one general document-parsing skill was maskable in isolation, two candidate skills defined their task identity through PDF-only input, title, trigger, and core workflow. CFTC-001 is therefore rejected before mask construction: no selector, score, API transfer, or result denominator exists. This is a validity safeguard, not a negative retrieval finding. The next intake must select compositions in which the target requirement is documented separately from the skill's identity. Evidence: `skill_benchmark/rq1_public_original_mask_v1/formal_queue/CFTC-001_input_precondition/INDEPENDENT_FEASIBILITY_REVIEW.md`.

> **2026-08-31 CFTC-002 original-document feasibility gate (`FIELD_MASK_REJECT / NO SCORING`).** A second, method-distinct public triad was mapped using only anonymised raw originals. It also failed before mask construction: ranked gene lists, identifier rules, expression matrices, group files, and prior result objects are the documented operating contracts of the corresponding analysis modes. This demonstrates that CFTC-001 was not merely a PDF-domain accident. The strict requirement to remove every semantic input cue from a full natural document while preserving the same skill is presently infeasible for both examined triads. Do not sweep further compositions under this protocol until the intervention scope is deliberately revised. Evidence: `skill_benchmark/rq1_public_original_mask_v1/formal_queue/CFTC-002_input_precondition/MAPPER_RUN_RECORD.md`.

> **2026-08-30 RQ1 public-original masking pilot approved (`NO SCORING`).**
> The user approved the CFTC-064 full-original `input_precondition` masking
> convention after reviewing each original, mask, source-span ledger, and local
> residual scan. CFTC-064 remains a technical demonstration only because its
> mapper had seen historical prompts while the compact pilot was selected. The
> next authorised work is a fresh source-only, prompt-blind mapping packet,
> followed by a separate residual review and another user-facing composition
> review before any condition is frozen. No retrieval, embedding, external
> transfer, hosted run, or thesis/PDF write is authorised. Protocol and
> approved pilot: `thesis_notes/archive/RQ1/original-document-lineage/RQ1 Public Original-Document
> Field-Masking Pilot Protocol - 2026-08-30.md` and
> `skill_benchmark/rq1_public_original_mask_v1/pilot/CFTC-064_input_precondition/`.

> **2026-08-30 RQ1 public-original masking amendment (`PILOT PREPARATION / NO SCORING`).** The user approved a new public RQ1 method that uses complete frozen `SKILL.original.md` documents rather than seven-slot derivative cards. For each verified field condition, the intervention will remove or minimally neutralise all mapped occurrences of that field from every candidate original document in a composition, with source-span, residual-cue, and non-target-preservation gates. The first authorised step is one local `input_precondition` pilot review packet; no selector, embedding, external transfer, hosted compute, or thesis/PDF write is authorised. This is a prospective replacement of the public RQ1 primary method only if the pilot and later full protocol pass; historical card-mask results remain preserved but non-primary. Authoritative protocol: `thesis_notes/archive/RQ1/original-document-lineage/RQ1 Public Original-Document Field-Masking Pilot Protocol - 2026-08-30.md`.

> **2026-08-30 RQ1 final evidence integration and provenance correction.**
> RQ1a now has a deterministic local cluster-level re-analysis over the seven
> frozen row-level suites: prompt variants are averaged within each 50-cluster
> suite before 10,000 cluster bootstrap resamples. All fourteen
> field/retriever hidden-to-exposed Top-1 intervals are positive. A
> gold-minus-retrieval-leading-negative margin is also retained for every row;
> it is explicitly not a human semantic-nearest-negative annotation. The
> source units are researcher-authored and mechanically rubric-checked. The
> 350-row ledger retrospectively records iterative author review: all 350 core
> clusters are `AUTHOR_REVIEWED_RETAINED` by Jacky Zhang, with none excluded.
> This is author review, not independent or blinded annotation. Protocol and
> receipt: `thesis_notes/archive/RQ1/original-document-lineage/RQ1a Human Review Protocol - 2026-08-30.md`
> and `skill_benchmark/rq1a_field_discriminability/human_review_2026-08-30/author_review_confirmation_receipt.json`; results:
> `skill_benchmark/outputs/rq1a_cluster_uncertainty_2026-08-30/`.

> **2026-08-30 final RQ1b thesis-facing boundary.** The final public-card
> experiment begins with a 1,099-artifact public source-discovery frame and is
> separate from original-only naturalistic feasibility curation. It contains 46 scored
> candidate compositions drawn from 52 frozen artifacts, 99 strict routing
> families, 198 prompts, and `FULL + seven candidate-synchronous masks` per
> retriever. Strict families passed two source-deidentified model-assisted
> singleton reviews, not human annotation. Direct/paraphrase and families are
> averaged within composition before a 5,000-replicate paired composition
> bootstrap. BM25 FULL is 0.6919 Top-1 / 0.8321 MRR and Qwen FULL is 0.8485 /
> 0.9184. Every primary single-field Top-1 and MRR interval includes zero.
> The legitimate conclusion is that no statistically reliable single-field
> effect was detected in this corpus, consistent with distributed/redundant
> public-card routing evidence rather than a universal independent gain from
> one field. Joint masks are
> separately denominated supporting evidence only. Final package:
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_v3_final_2026-08-30/`; failure synthesis:
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_v2_v3_result_failure_analysis_2026-08-30/`.

> **2026-08-30 RQ1b V2+V3 result synthesis and failure-analysis SOP --
> user-approved and complete.** The researcher approved the frozen,
> local-only procedure before any case inspection. It separates
> the 99-family single-field primary matrix from the three separately
> denominated joint-field supporting comparisons; retains all `FULL -> MASK`
> transitions, recoveries, rank/margin changes, source hashes and V2/V3
> provenance; and prohibits changing prompts, cards, gold, eligibility or
> scored rows. Only `1 -> 0` is a routing regression, while `0 -> 1` is a
> required counterexample and stable-correct margin loss is an ordering
> fragility signal. SOP: `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V2 Plus V3 Result Synthesis
> and Failure Analysis SOP - 2026-08-30.md`. The local package validates 3,796
> pair records and all 16 predeclared cross-retriever-concordant cases (13
> regressions, 3 recoveries). Eleven regressions contain a directly
> intent-matching withheld field/group; two gene-list workflow/verification
> cases are retained as retrieval-sensitivity counterexamples; three recoveries
> show residual-field redundancy. The review cannot alter the scientific matrix
> or write thesis LaTeX/PDF. Closure checkpoint:
> `thesis_notes/checkpoints/methods/RQ1b V2 Plus V3 Result Synthesis And
> Descriptive Failure Analysis Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V2+V3 joint-group local result.** A supporting
> joint-field availability extension materialised three candidate-synchronous
> V3 masks and verified its exact V2 eligibility binding. Local BM25 reused
> 696 V2 rows, added 96 V3 rows and analysed 1,024 rows across three separate
> group-specific `FULL` versus mask comparisons: task specification (85
> families), execution/verification (89), and applicability/capability (82).
> Task specification has a positive composition-bootstrap Top-1 interval
> (`+0.0965`, 95% `[+0.0081,+0.1911]`); execution/verification and
> applicability/capability retain positive margin intervals. This is supporting
> joint-set evidence, not a causal result for individual fields and not a
> replacement for the single-field primary analysis. Qwen is not run: a local
> preflight isolates 36 new group-mask cards, no new queries, and four maximum
> no-retry requests pending separate external-text approval. Evidence:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V2 Plus V3 Joint Group Extension Amendment -
> 2026-08-30.md` and `thesis_notes/checkpoints/methods/RQ1b V2 Plus V3 Joint
> Group BM25 and Qwen Preflight - 2026-08-30.md`.

> **2026-08-30 RQ1b V2+V3 joint-group Qwen twin complete.** The exact
> cache-aware payload sent 36 new V3 group-mask cards only; 24 queries and 12
> `FULL` cards were cache hits. All four no-retry calls succeeded (6,428
> provider tokens), producing 96 new V3 rows and 1,024 separately denominated
> V2+V3 group-analysis rows. Under Qwen, execution/verification has positive
> composition-bootstrap intervals for Top-1 (`+0.0634`), MRR (`+0.0341`) and
> margin (`+0.0061`); task specification has positive MRR/margin but an
> inconclusive Top-1 interval, while applicability/capability is inconclusive.
> This corroborates a partial joint-set effect only; it does not identify any
> individual field as causal or alter the primary single-field result. Outputs:
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_v3_extension_2026-08-30/qwen/`.

> **2026-08-30 RQ1b final public-corpus consolidation and accounting
> correction.** The current source of truth is
> `skill_benchmark/rq1b_final_public_corpus_v1/`, generated and verified by
> `skill_benchmark/scripts/build_rq1b_final_public_registry.py`. It preserves
> three non-pooled strata: historical cross-source C6 provenance (76
> compositions / 408 cases), the scored V2 field-card ablation (48 active
> compositions / 87 strict-preserved routing families / 174 prompts), and
> direct V3 C6 curation (six parent compositions / 32 cases; four complete and
> two partial). The 82-composition source-hash union is an inventory only. All
> earlier `V3 37 / 231` statements are superseded rather than silently edited:
> they carried over a historical cross-source running count and are not
> reproducible from V3 C6 freeze ledgers. No V2/V3 score pooling is permitted.

> **2026-08-30 RQ1b V2+V3 complete-triad integration amendment.** Four direct
> V3 parent triads are now eligible for a prospective V2-compatible extension:
> each has three candidates, six strict target-by-direct/paraphrase cases, a
> complete source-grounded seven-field card, C4A audit, C4B singleton consensus
> and C5/C6 hash bindings. The two four-case V3 parents are quarantined. The
> future matrix has 52 candidate compositions, 99 strict routing families, 198
> prompts and eight conditions; it is not yet a selector result and does not
> revise the completed native V2 score. SOP:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V2 Plus V3 Complete-Triad Integration Amendment - 2026-08-30.md`.

> **2026-08-30 RQ1b V2+V3 selector execution amendment.** The next execution
> scores only imported V3 cards/prompts and reuses completed V2 selector rows
> by verified artifact reference. BM25 is local; the Qwen `text-embedding-v4`
> twin needs a new exact-payload approval after its local cache-aware preflight.
> Any field effect from the 12 imported V3 families is supplemental
> all-complete-triad perturbation evidence, because it does not inherit V2's
> per-field eligibility ledger. Native V2, imported V3 and the 99-family
> harmonised view must stay distinct. SOP:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V2 Plus V3 Selector Execution Amendment - 2026-08-30.md`.

> **2026-08-30 RQ1b V2+V3 local selector checkpoint.** V2 BM25 is reused by
> exact original-result manifest/artifact verification; only imported V3's 192
> rows are newly calculated. The resulting 1,584-row package is tagged by
> native-V2 reuse versus imported-V3 computation. Qwen preflight is local only:
> it seals 96 rendered V3 cards and 24 V3 prompts (14,170 local lexical-token
> proxy, 99,787 bytes) for at most 13 no-retry calls. It has no provider call,
> cost, Qwen result or thesis/PDF write. Checkpoint:
> `thesis_notes/checkpoints/methods/RQ1b V2 Plus V3 BM25 And Qwen Preflight - 2026-08-30.md`.

> **2026-08-30 RQ1b V2+V3 Qwen extension complete.** After the exact-payload
> authorisation, Qwen `text-embedding-v4` (1024 dimensions) embedded only the
> preflighted 96 rendered V3 cards and 24 V3 prompts. All 13 no-retry calls
> succeeded, used 20,843 provider tokens and persisted exact-text embeddings
> locally. The runner computed 192 V3 rows and reference-reused 1,392 frozen V2
> rows into a verified 1,584-row package. Imported V3 `FULL` is 0.7917 Top-1
> and 0.8889 MRR; the 99-family harmonised view is 0.8485 Top-1 and 0.9184 MRR.
> V3 per-field deltas remain supplemental all-complete-triad perturbation
> estimates; they neither pool into nor replace V2's primary eligibility-filtered
> result. No thesis LaTeX/PDF result was written. Checkpoint:
> `thesis_notes/checkpoints/methods/RQ1b V2 Plus V3 Qwen Extension Result - 2026-08-30.md`.

> **2026-08-30 RQ1b final V2+V3 unification decision and analysis.** V2 and
> V3 now constitute one final public-artifact field-removal experiment, not
> separate scientific estimators. The frozen corpus has 52 composition
> artifacts, of which 46 actually contribute a strict routing family; the final
> denominator is therefore 46 scored compositions, 99 families, 198 prompts,
> eight candidate-synchronous conditions and 1,584 rows per retriever. The
> main field effect averages direct/paraphrase and all family pairs within each
> composition, then uses a 5,000-replicate paired composition bootstrap. V2/V3
> tags remain for provenance only. Qwen `FULL` is 0.8485 Top-1 / 0.9184 MRR;
> BM25 `FULL` is 0.6919 / 0.8321. All unified single-field Top-1 and MRR 95%
> intervals cross zero. This bounds the public-artifact claim to directional
> field-availability evidence, not a universal isolated-field gain. Final
> analysis: `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_v3_final_2026-08-30/`.

> **2026-08-30 RQ1b final metric ledger.** The complete local-only ledger is
> calculated and independently recomputed from frozen selector rows. It reports
> absolute FULL/masked Top-1, MRR, gold rank and native margin; raw prompt-pair
> effects; 5,000-replicate composition-bootstrap effects; and Top-1 transition
> counts. In the primary unified single-field experiment every Top-1/MRR CI
> includes zero, but BM25 margin intervals are positive for input, workflow,
> success and boundary; Qwen has a positive success-margin interval. The V2-only
> three-field group study correctly retains its frozen eligibility intersections
> (73 task-specification, 77 execution/verification, 70 applicability/capability
> families): all three groups have raw accuracy degradation, while margin loss
> is stable for BM25 task/execution/applicability and Qwen task specification.
> Ledger: `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_final_result_ledger_2026-08-30/`.

> **2026-08-30 RQ1b V2+V3 joint-group extension.** The next local-only step
> extends V2's three grouped candidate-synchronous masks to the four complete
> V3 triads. It adds all 12 V3 strict families to each frozen V2 group-specific
> eligibility set, producing 85 task-specification, 89 execution/verification
> and 82 applicability/capability families. BM25 will score only the 72 newly
> materialised V3 mask rows; V3 FULL rows are reused after exact manifest/hash
> validation. Qwen requires a new preflight and exact payload authorisation for
> 36 new V3 group-mask card texts; queries and V3 FULL cards must remain cache
> reuse only. Protocol:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V2 Plus V3 Joint Group Extension Amendment - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 039 provenance and high-recall source-only
> amendment.** Five metadata-only M0 lanes returned 118 leads; 87 survived
> source-frame origin comparison and 84 remained after excluding all 47
> historically successful M1 roots. Nineteen of the balanced 20 M1 roots passed
> pin/filter/tree verification, yielding 191 path-only rows; deterministic M2
> froze 153 and M3 captured 153/153. Seven were historical byte aliases and 146
> became additive provenance-only originals. Exact three-way header title terms
> produce only four source-disjoint T0 triads, so that low-recall queue is kept
> but supplemented with T0S: five source-disjoint batches over all 146 originals
> may propose evidence-backed 3–4 candidate peer-route drafts. T0S has no
> prompt, label or target and each proposal must pass a mechanical literal/hash/
> origin audit followed by a separate independent T0 review. Record:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_039_2026-08-30/`.

> **2026-08-30 RQ1b V3 Wave 039 public-navigation amendment.** Because Wave
> 038's 243 new originals produced no source-grounded T0 permission, Wave 039
> first broadens discovery rather than weakening the strict parallel/singleton
> criterion. Five independent M0 lanes may record only public repository and
> path metadata; they prioritise concrete domain-bounded collections and do not
> fetch source text, construct clusters, or access prompts, labels, selectors,
> metrics or prior results. Fresh-origin deduplication, commit pinning, capture,
> byte-level source-frame amendment and source-only T0 remain separate required
> gates. Record: `skill_benchmark/rq1b_v3_public_source_frame/
> d1_source_intake_wave_039_2026-08-30/`.

> **2026-08-30 RQ1b V3 Wave 038 M3/provenance/T0 preparation.** The 377
> bounded M2 paths completed a one-shot pinned raw-body capture with 377/377
> local rehash checks. Byte-level comparison against the base frame plus 23
> amendments (30,989 frozen hashes) retained 132 historical aliases and two
> within-wave aliases, and froze 243 byte-distinct originals as a provenance
> amendment only. A local, zero-network T0 ordering step then uses only each
> amendment source's `name`/`title` front matter and heading, never the generic
> description text: it forms 58 lexical drafts and selects eight
> source-disjoint, three-origin triads. The superseded description-token roster
> is preserved explicitly because it admitted generic `when/review` signals.
> The eight final T0 assignments expose reviewers only to source originals and
> the source-only protocol. They have no prompt, label, intended winner,
> representation, selector, metric, retrieval or field-effect status. Record:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_038_2026-08-30/`.

> **2026-08-30 RQ1b V3 Wave 038 T0 closure.** The eight triads were partitioned
> into three source-disjoint batches (3/3/2) and independently assessed using
> only a local source-only protocol plus their 24 bound originals. Each return
> supplied one exact substring per original; all three return audits passed
> source hash, assignment and literal evidence checks. The final ledger records
> one `LIKELY_NONPARALLEL` composition and seven `NO_PLAUSIBLE_TRIAD`
> compositions: the apparent shared title terms were too broad to establish a
> bounded common operational envelope. No triad received `READY_FOR_C1`, so
> Wave 038 stops before C1, prompt construction, labels, selectors or metrics.
> This is a strict public-source feasibility observation only; V3 remains 37
> compositions / 231 cases. Record: `skill_benchmark/rq1b_v3_public_source_frame/
> d1_source_intake_wave_038_2026-08-30/source_only_triage/T0_PRINCIPAL_LEDGER.json`.

> **2026-08-30 RQ1b V3 Wave 038 public-navigation restart.** With Wave 037
> closed and the strict V3 cohort unchanged at 37/231, Wave 038 begins with
> six disjoint M0 discovery lanes. Workers may record only public repository
> metadata and `SKILL.md` path hints; they cannot inspect a body, form a
> cluster, or see prompts, labels, representations, selector outputs, metrics
> or previous decisions. This creates a new provenance queue only. Principal
> deduplication and a separately logged M1--M3 pass remain necessary before
> source triage. Record: `skill_benchmark/rq1b_v3_public_source_frame/
> d1_source_intake_wave_038_2026-08-30/`.

> **2026-08-30 RQ1b V3 Wave 038 M1 metadata closure.** M0 retained 66 unique
> navigation leads, including 32 not matching existing origin-name metadata.
> A predeclared 20-root balanced subset then performed one native-Git HEAD pin
> and one verified `blob:none`, no-checkout tree enumeration each; all 20
> passed and exposed 2,090 `SKILL.md` paths. This remains metadata only: the
> script checks the tree SHA against the pin and fails closed if the blob filter
> cannot be verified, but captures no source body. M2 will make a deterministic
> bounded path roster prior to one-shot M3 raw capture. No source-frame
> admission, triage, cluster, prompt, label, retrieval, selector, metric or
> field effect exists. Record: `skill_benchmark/rq1b_v3_public_source_frame/
> d1_source_intake_wave_038_2026-08-30/m1_network_enabled/`.

> **2026-08-30 RQ1b V3 Wave 038 M2 roster freeze.** The 2,090 M1 path-only
> records were deterministically reduced to a 377-path capture roster across
> the 19 roots that exposed at least one `SKILL.md`. Selection caps each root at
> 30 and round-robins first-two-segment path buckets; it reads path strings only
> and is deliberately not a semantic ranking. The frozen roster is the sole
> input for the next one-shot M3 public raw capture. No source body, admission,
> triage, cluster, prompt, label, retrieval, selector, metric or field effect
> exists. Record: `skill_benchmark/rq1b_v3_public_source_frame/
> d1_source_intake_wave_038_2026-08-30/m2_capture_roster/`.

> **2026-08-30 RQ1b V3 Wave 037 local T0 and C1 closure.** After Wave 036's
> predeclared GitHub metadata batch stopped at HTTP 403 rate limiting, a
> zero-network contingency scanned the frozen 10,000-row distinct-title lexical
> queue. It excluded 1,971 historical C0/C6-touching drafts, retained 8,029
> eligible drafts, and prepared 18 source-disjoint triads over 54 rehashed
> originals. Six evidence-every-member T0 reviews classified 13 as likely
> nonparallel, two as no plausible triad, and three as C1 candidates. Every
> one of the six independent C1 returns and all nine bound originals passed
> literal-span/source-hash audit. No packet obtained the two-reviewer C2
> advance: pgvector and PMax were nonparallel/component mixtures; caching had
> no C2-advance consensus. This is curation feasibility only, not a cluster,
> prompt, label, selector, metric, retrieval or field result. Strict V3
> remains **37 frozen compositions / 231 strict cases**. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 037 Local T0 and C1 Closure -
> 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Waves 034--036 discovery accounting amendment.** Wave
> 034 completed its source-only T0/C1 sequence after 456 exact-once captures
> and 114 byte-distinct additions; its two C1 packets made zero C2 advances.
> Wave 035 then captured 238 more originals, admitted 116 byte-distinct
> additions, and independently rejected both of its four-skill C1 packets as
> nonparallel/component sets. Wave 036 has 39 distinct navigation leads (32
> new after prior-wave deduplication), but all 20 one-shot M1 metadata requests
> encountered GitHub HTTP 403 rate limiting, so it has no source body or
> source-frame addition. These are provenance and strict-curation feasibility
> records only; no prompt, label, selector, retrieval, metric or field effect
> has been produced. The strict V3 cohort remains **37 frozen compositions /
> 231 strict cases**. Records: `thesis_notes/checkpoints/methods/RQ1b V3 Wave
> 034 Public Source Intake - 2026-08-30.md`, `thesis_notes/checkpoints/methods/
> RQ1b V3 Wave 035 Intake and C1 Closure - 2026-08-30.md`, and
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 036 Public Discovery Stop -
> 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 033 C4A--C6 strict closure.** Five pinned roots
> supplied 322 one-shot public captures, yielding 199 byte-distinct additions;
> this provenance pool was screened separately from cluster validity. Of eight
> source-only T0 groups, two entered C1; the immune triad stopped on peer-route
> disagreement, while the pathway-input triad completed six cue-safe cases.
> Two exact-span C4A cards passed literal audit and 19/21 field statuses agreed.
> A malformed builder response and an original canonical quote-space failure
> remain retained; an r1 mechanical substitution used only an existing
> literal-valid builder excerpt. C4B produced 6/6 exact singleton agreements,
> C5 6/6 sealed-target matches, and C6 froze six low-risk cases. The V3 cohort
> is now **37 frozen compositions / 231 strict cases**. This is curation
> feasibility only, not human annotation, field effect, selector, metric or
> retrieval evidence. Record: `thesis_notes/checkpoints/methods/RQ1b V3 Wave
> 033 C4A-C6 Strict Freeze - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 032 C4A--C6 strict closure.** One source-bound
> public survey triad completed all gates. Two original C4A drafts remain
> retained failures because their quotations were nonliteral; fresh,
> independent exact-span cards both passed literal audit and agreed on 21/21
> field-status decisions. After source-only canonicalisation, two key-blind
> C4B reviewers reached six singleton consensuses. The first audit is retained
> with one trailing-space evidence defect; a mechanical one-character
> amendment produced an exact-evidence r1 pass. C5 gives 6/6 sealed-target
> matches; C6 freezes six low-risk cases with zero exclusions. The V3 cohort is
> now **36 frozen compositions / 225 strict cases**. This is curation
> feasibility only, not a human annotation, field effect, selector, metric or
> retrieval result. Record: `thesis_notes/checkpoints/methods/RQ1b V3 Wave 032
> C4A-C6 Strict Freeze - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 032 multi-root public-source intake.** Five
> commit-pinned public roots yielded 171 raw artifact captures. Clean-frame
> SHA-256 deduplication admitted 85 byte-distinct public originals, retained 80
> frozen aliases and 6 within-wave aliases, and froze the additions as source
> provenance only. Five non-overlapping, prompt-free source-only T0 groups now
> cover 19 artifacts in independent structural review. No prompt, label,
> selector, metric, or result exists; at its intake closure V3 remained **35
> frozen compositions / 219 strict cases**. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 032 Public Source Intake - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 031 C1--C3 curation closure.** Two framework
> groups passed source-only T0/C1 evidence but did not become strict clusters:
> orchestration rejected all 6/6 C2 task positions for multi-adequacy risk;
> RAG retained only 2/6 cue-safe positions and therefore failed complete
> candidate symmetry required for C4. This is a negative curation-feasibility
> observation, not an RQ1b field effect, selector result, or label. The V3
> strict cohort remains **35 compositions / 219 cases**. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 031 C1-C3 Curation Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 031 pinned public-source intake.** Four public
> roots completed commit-pinned, body-free path census (482 paths) and a
> deterministic 313-path roster. One-shot capture succeeded for all 313
> artifacts; full clean-frame SHA-256 deduplication retained 100 byte-distinct
> public originals and 213 historical byte aliases, then froze all 100 solely
> as provenance additions. All 100 novel bodies originate from one root; the
> other three roots deduplicated to historical aliases, so source-family
> diversity remains a later discovery requirement. Ten non-overlapping,
> prompt-free T0 source-only triads are in bounded review packets. No D1/C1--C6
> decision, cluster, prompt, label, selector, metric or result exists; the
> current V3 strict total remains **35 compositions / 219 cases**. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 031 Public Source Intake Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 029 C4A--C6 closure.** The W27/W29 UI-design
> triad completed source-deidentified seven-slot card preservation, two
> key-blind model-assisted C4B adequacy reviews, sealed-target reconciliation
> and C6 source/ledger hash verification. A one-packet reviewer-2 exact-quote
> defect was corrected by a fresh key-blind review while preserving the
> original response; the amended audit records six exact singleton agreements,
> six sealed-target matches, six low-risk frozen prompt cases and zero
> exclusions. The **V3 source-frame cohort is now 35 C1--C6-frozen
> compositions / 219 strict prompt cases**. This is curation feasibility only,
> not human annotation, selector, metric or retrieval evidence, and remains
> separate from historical cross-source campaign counts. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 029 C4A-C6 Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 030 broad multidomain intake.** M0 retained 285
> public navigation leads across 16 lanes, while six 403 lanes remain retained
> failures. Twenty-one predeclared roots then completed one-shot pinned
> path-only census (453 paths). The 108-path deterministic capture completed
> cleanly; full clean-frame SHA-256 deduplication retained 53 byte-distinct
> originals and 55 aliases, all frozen as provenance-only additions. Local
> lexical pretriage is a reading aid. No D1/C1--C6 composition, prompt, label,
> selector, metric or result exists; strict total remains 34/213. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 030 Broad Multidomain Public Source Intake - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 029 targeted supplemental intake.** Five
> predeclared public `SKILL.md` bodies were captured once, rehashed and
> deduplicated only against the clean immutable frame plus Waves 009--027:
> all five are byte-distinct source-frame additions, with zero aliases and zero
> failures. This provenance operation excludes quarantined Wave 028. The
> UI-trio D1 source-only reviews reached audited `READY_FOR_C1` consensus, then
> materialised one prompt-free C1 packet whose three-source binding audit and
> principal trigger/operation/output/boundary finaliser pass. The frozen C1
> outcome is `ADVANCE_C2_PROMPT_CONSTRUCTION`; shared-template and mixed-domain
> risk constrained C2 to domain-specific, cue-controlled prompts. C2 binding
> then passed six records; both blind C3 reviewers required a cue-only rewrite
> of over-bundled source constraints, and both fresh C3R1 reviewers allowed all
> six shorter prompts at low residual risk. C4A field-card construction is the
> next gate. The cross-wave auditor binds repeated frozen source manifests and
> fails closed on duplicate IDs. No strict label, selector, metric or retrieval
> result exists; the strict total remains 34 compositions / 213 packets. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 029 Targeted Supplemental Public Source Intake - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 028 capture quarantine.** A new M0/M1 route
> discovered 200 public repository leads, pinned 16 trees and formed a
> 243-URL raw roster. A detached local capture process overlapped its resume:
> the retained manifest has 362 records, 119 duplicate URLs and a completion
> report inconsistent with the manifest count. The entire capture stream is
> retained but quarantined as zero source-frame additions. No D1/C1--C6,
> prompt, label, selector, metric or retrieval result exists; the strict total
> remains 34 compositions / 213 packets. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 028 Capture Quarantine - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 027 targeted public-source intake.** Sixteen
> pinned public trees produced a 289-body one-shot capture. Exact SHA-256
> deduplication against the immutable frame and prior amendments retained 235
> byte-distinct provenance additions and 54 frozen aliases; all are pre-C1.
> A canonical-path/literal-heading inventory and local lexical neighbour list
> support reading order only. No D1 proposal, C1--C6 advance, prompt, label,
> selector, metric or retrieval result exists; the strict total remains 34
> compositions / 213 packets. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 027 Targeted Public Source Intake - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 026 broad public-source intake.** Sixteen pinned
> public trees produced a 197-body one-shot capture. Exact SHA-256
> deduplication against the immutable frame and prior amendments retained 172
> byte-distinct provenance additions and 25 frozen aliases; all are pre-C1.
> A canonical-path/literal-heading inventory and local lexical neighbour list
> support reading order only. No D1 proposal, C1--C6 advance, prompt, label,
> selector, metric or retrieval result exists; the strict total remains 34
> compositions / 213 packets. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 026 Broad Public Source Intake - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 025 broad public-source intake.** Twelve pinned
> public repositories yielded a 230-body successful raw capture. Exact
> SHA-256 deduplication against the immutable frame plus all prior amendments
> retained 198 byte-distinct source additions, 31 frozen aliases and one
> within-wave byte alias; the 198 originals are frozen as provenance only.
> Local literal-heading inventory and lexical neighbour ranking are a reading
> aid, not D1/C1 evidence. The health-digest candidate is now closed before
> D1: all targeted reviews were mechanically invalid under the strengthened
> audit and later readings disagreed on peer parallelism. Short-form product
> ads are `LIKELY_NONPARALLEL`; video frame extraction/analysis/transcription
> is a component/different-granularity family. No C1--C6 advance, prompt,
> label, selector, metric or retrieval result exists; the official strict total
> remains 34 compositions / 213 packets. Records:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 025 Broad Public Source Intake - 2026-08-30.md`
> and `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_025_2026-08-30/source_only_triage/HEALTH_DIGEST_TRIAD_CLOSURE_2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 024 source-intake and C4A closure.** A corrected,
> predeclared public `SKILL.md` roster yielded a clean 232-row capture stream
> after a concurrent-append incident quarantined 251 duplicate-attempt URLs.
> Exact SHA-256 deduplication retained 87 byte-distinct provenance additions
> and 145 aliases. One CaseMark derivative-analysis triad passed source-only
> C1 and six low-residual-risk C3 packets, but failed C4A: both literal-valid
> anonymous builders omitted the same qualifying workflow excerpt and two
> independent conformance reviewers rejected canonicalisation. No C4B--C6
> advance, label, selector, metric or retrieval result exists; the official
> strict total remains 34 compositions / 213 packets. Records:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_024_2026-08-30/README.md`
> and `thesis_notes/checkpoints/methods/RQ1b V3 Wave 024 Source Intake And C4A Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 023 source-intake closure.** A pinned-clone,
> no-code-execution discovery route captured 145 public `SKILL.md` originals
> once. Exact SHA-256 deduplication found 144 already-frozen aliases and one
> byte-distinct healthcare library router, which was frozen solely as an
> additive provenance record. It had no three- or four-member source-only
> peer set and therefore did not enter D1. No C1--C6 advance, prompt, label,
> selector, metric or retrieval result exists; the official strict total
> remains 34 compositions / 213 packets. Record:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_023_2026-08-30/README.md`.

> **2026-08-30 RQ1b V3 Wave 021 D1--C1 closure.** Eighty-seven one-shot
> public captures yielded 71 byte-distinct additions and 16 aliases. Eight
> source-only groups screened 69 additions; most were containers, workflow
> components, broadly substitutable sources or nonparallel deliverables. The
> only D1 finance triad entered two independent C1 reviews, which agreed on
> literal evidence but disagreed over the Controller--FP&A peer-role boundary.
> The C1 gate therefore failed closed as `REJECT_NONPARALLEL_OR_COMPONENT`.
> No C2--C6 advance, label, selector, metric or retrieval result exists; the
> official strict total remains 34 compositions / 213 packets. Checkpoint:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 021 D1-C1 Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 022 M0--M1 navigation stop.** Eight targeted
> GitHub metadata lanes produced 644 M0 repository leads. The predeclared 40
> public tree-metadata attempts all failed once and are retained without retry;
> no tree or skill body was admitted or downloaded. This is a discovery
> infrastructure outcome, not a source, cluster or retrieval result. Record:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_022_2026-08-30/README.md`.

> **2026-08-30 RQ1b V3 Wave 019 C1--C4A closure.** One hundred public
> captures produced 84 byte-distinct additive originals and 16 frozen aliases.
> Two source-only parallel-route compositions advanced through C1, C2 and C3:
> a four-accounting-reconciliation quartet and a three-native-Office-editing
> triad. Fourteen prompt packets passed the C3 cue gate after six cue-only
> revisions. Both compositions then failed C4A because independent source-only
> conformance reviewers found qualifying original-source evidence omitted or
> misallocated in the literal-valid anonymous cards; no principal repair,
> union or card substitution is allowed. Thus 0 C4B--C6 advances, no strict
> label, selector, metric or retrieval result, and the official strict total
> remains 34 compositions / 213 packets. Checkpoint:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 019 C1-C4A Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 020 initial source-only triage.** Eighty-six
> fresh source paths yielded 78 byte-distinct additive originals and eight
> aliases. The first five source groups were conservatively screened as
> non-parallel before C1: test methodologies, code-change lifecycle roles,
> repository maintenance stages, memory-workspace stages and scholarly
> publication deliverables. This is ongoing source triage, not a Wave 020
> closure or a cluster/selector result. Log:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_020_2026-08-30/source_only_triage/W20_INITIAL_TRIAGE_LOG.md`.

> **2026-08-30 RQ1b V3 Wave 018 duplicate-only source-intake closure.** Thirty
> public platform-operation leads were captured once across nine lanes, with no
> failed capture. Exact SHA-256 deduplication against the immutable frame plus
> Waves 009--017 found all 30 bodies already frozen. Therefore no source-frame
> amendment, D1 composition, C1 screen, prompt, gold label, representation,
> selector, metric or retrieval result exists. The strict total remains 34
> compositions / 213 packets. Checkpoint:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 018 Duplicate-Only Source Intake Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 017 source intake and triage closure.** Nineteen
> public leads yielded 19 one-shot readable captures; byte deduplication
> against the immutable frame plus Waves 009--016 retained seven additions and
> 12 already-frozen aliases. Five conservative source-only compositions were
> rejected before C1: data-operation routes were nonparallel/multi-adequate,
> database migration had only a plausible pair, semantic asset work mixed
> authoring with downstream use, and repository/cloud-security families had no
> narrow common envelope. No C2--C6 advance exists. The strict total remains
> 34 compositions / 213 packets. Checkpoint:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 017 Source Intake and Triage Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 016 C1--C4A closure.** One GitHub Actions
> triad passed source-only C1 and its six C2 direct/paraphrase packets passed
> C3 after two cue-only wording revisions. The final C3 ledger retains two
> low and four medium residual-risk operational-signal annotations. At C4A,
> two literal-valid anonymous field-card builders both omitted qualifying
> source spans; two independent source-only conformance reviewers therefore
> rejected canonicalisation under v1.2 rather than allowing a principal repair.
> This stops the composition before C4B/C5/C6: no strict label, selector,
> field effect, metric or retrieval result exists, and the official strict
> total remains 34 compositions / 213 packets. Checkpoint:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 016 C1-C4A Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 013 strict-screen closure.** Fifty-six public
> cross-origin leads were retrieved once with 56 readable captures; 37 were
> already-frozen byte aliases and 19 were frozen only as a new additive source
> amendment. Independent source-only triage rejected broad data/API, research,
> incident, accessibility and UI families as non-parallel before D1. Three
> conservative D1 compositions (security review, compliance, presentation
> authoring) passed literal/hash materialisation, then all failed C1: each
> contained either a broad parent container, an operational component, or two
> complete adequate routes. No case reaches C2; the strict total remains 34
> frozen compositions and 213 strict packets. This is feasibility evidence,
> not a prompt, label, field, selector, metric or retrieval result. Checkpoint:
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 013 Cross-Origin Source Discovery and C1 Checkpoint - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 012 interim closure.** A 30-lead, eight-lane
> cross-origin intake produced 29 single-attempt raw captures, 18 previously
> frozen byte aliases, 11 byte-distinct additions, and one retained 404 record
> (not retried). Source-only triage nominated one generic code-review quartet
> and one data-visualisation triad for D1. Both passed literal/hash
> materialisation but independently failed C1 as non-parallel or
> component/container compositions; neither proceeds to C2. This is an
> informative strict-feasibility screen, not a benchmark failure repaired by
> relabelling or an experiment result. Records:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_012_2026-08-30/`
> and `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_012_2026-08-30/`.

> **2026-08-30 RQ1b V3 Waves 009--011 source-only closure.** Wave 009's
> video-editing D1 draft and Wave 010's contract-review D1 draft each passed
> byte/source binding, then independently failed C1 because the proposed peers
> were non-parallel containers, specialised implementations, or preparation
> workflows. Wave 011 added a full public catalog intake: 127 sources were
> fetched, of which only six were byte-distinct after deduplication and all six
> share one origin. Across Waves 009--011 there are now 100 byte-distinct
> additions to the immutable source frame (88 + 6 + 6), **not** 100 clusters;
> no new parent composition reached C2--C6. These are source discovery and
> feasibility findings only, with no prompt, label, field-ablation, selector,
> metric or retrieval result. Closure records:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_009_2026-08-30/`,
> `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_010_2026-08-30/`,
> and `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_011_2026-08-30/`.

> **2026-08-30 RQ1b V3 execution priority.** Pause additional D1/public-skill
> discovery. C4A--C6 Wave 001 is complete: four canonical cards passed
> literal/provenance and source-only conformance audits, five were strictly
> rejected for shared omitted source evidence, and C6 froze 14 strict prompt
> cases across three parent compositions. Only one parent has all candidates'
> direct/paraphrase variants frozen; all 14 cases have high/medium cue risk.
> This is strict curation, not selector evidence; D1 discovery can resume.
> Execution record:
> `thesis_notes/checkpoints/methods/RQ1b V3 C4A v1.2 Priority Execution - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 Wave 009 public-source amendment.** A new public
> source intake retrieved 199 raw Markdown artifacts once and deduplicated them
> by rehashed local bytes against the immutable 2026-08-29 source frame. There
> are 88 byte-distinct additions and 111 already-frozen byte duplicates. The 88
> additions are frozen in a separate Wave 009 amendment; this changes neither
> the old frame nor the count of C1--C6-valid parent clusters. The next step is
> source-only D1 triage under the unchanged common-envelope and parallel-first-
> route rules. It is not prompt construction, strict-label validation, a field
> ablation, selector input, metric or retrieval result. Records:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_009_2026-08-30/`.

> **2026-08-28 active RQ1b field-ablation method.** The current public RQ1b
> intervention is not winner-only deletion and does not use a primary-field
> classification. After source-grounded field cards preserve the strict gold
> under selection-only blinded review, `FULL` is compared with seven conditions
> that replace one field value in **every** candidate with the same absence
> marker. BM25 and, only after separate text-transfer approval, Qwen dense
> embedding are compared within selector by Top-1, rank/MRR, conditional loss,
> and native paired gold-versus-best-wrong margin. Cross-slot residual facts are
> audited as redundancy, not treated as hidden failures. Protocol:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Public Field-Type Ablation Protocol - 2026-08-28.md`.
> The validation pilot passed on 2026-08-28 (5/6 applicable families); its
> exact construction, audit and residual-ledger record is checkpointed at
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_pilot_2026-08-28/RQ1B_FIELD_TYPE_ABLATION_PILOT_CHECKPOINT_2026-08-28.md`.
> No score or API operation is authorised by that pilot pass.

> **2026-08-29 RQ1b-A active input.** The non-pilot public field-card corpus is
> now frozen after literal construction, surface-cue remediation, exact-source
> same-slot audit, packet-binding audit, and byte-level input freeze. It has 48
> compositions, 128 routing families, and 256 prompt variants. The experiment
> has not yet passed its two-reviewer FULL-card preservation gate; therefore no
> selector, embedding, retrieval, metric, API or effect result exists.

> **2026-08-29 RQ1b-A preservation Wave 001.** Two blinded, schema/evidence
> audited FULL-card reviews have been adjudicated for 18 ordered routing
> families. Six preserve the sealed singleton gold for both prompt variants;
> 12 are ineligible for field-type ablation scoring (nine `NONE_ADEQUATE`, two
> reviewer disagreements, one multi-adequate). This gate validates strict-label
> usability, not field causality or selector performance. The sequence must
> continue over the remaining unadjudicated families before defining any scoring
> subset. Checkpoint: `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_001_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A preservation Wave 002.** Eighteen more opaque packets
> completed dual independent reviews and audit: 13 pass, five exclusion. The
> cumulative state is 19 strict-preserved and 17 excluded among 36 adjudicated
> families, with 92 still pending. This selects a defensible future scoring
> population; it does not estimate model accuracy or the availability effect of
> any field. Checkpoint: `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_002_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A preservation Wave 003.** The next 18 packets yielded 12
> strict-preserved families and six exclusion, giving 31 pass / 23 exclusion /
> 74 pending across 54 adjudicated. Replacement reviewers were used only after
> four original responses failed mechanical exact-evidence validation; invalid
> payloads remain retained as audit history. The state is not an accuracy,
> selector or field-effect finding. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_003_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A preservation Wave 004.** 17 validly reviewed packets
> added 14 pass and three exclusion. The cumulative strict-gold gate is 45
> pass / 26 exclusion across 71 adjudicated families, with 56 undispatched and
> one `UNADJUDICATED_FORMAT_HOLD` (`CFTF-099`). The hold reflects repeated
> mechanical evidence-audit failure, not a route or label judgement. No
> selector, retrieval or field-effect claim exists. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_004_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A preservation Wave 005.** Eighteen more packets yielded
> 15 pass and three exclusion. The gate has now adjudicated 89 families: 60
> strict-preserved, 29 excluded, 38 undispatched, plus the separate
> `CFTF-099` format hold. It remains pre-scoring validity control only.
> Checkpoint: `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_005_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A preservation Wave 006.** 13 pass and five exclusion
> from 18 further packets yields 73 strict-preserved and 34 exclusion across
> 107 adjudicated families. Twenty remain undispatched; `CFTF-099` remains a
> separate format hold. No scoring or field-effect result exists. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_006_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A preservation Wave 007.** The next 18 packets produced
> 12 strict-preserved and six excluded families. Cumulatively 125 are
> adjudicated: 85 strict-preserved, 40 excluded, two undispatched, plus the
> separate `CFTF-099` format hold. Ten A-side and four B-side initial payloads
> failed exact-evidence mechanics only and were independently replaced before
> use. This keeps the strict-label population auditable; it is not a selector
> score or a field-effect estimate. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_WAVE_007_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A FULL-card preservation complete.** The 128 active
> packets resolve to 87 strict-preserved, 40 excluded and one separate format
> hold. The final local integrity, packet-binding and ledger-join checks pass;
> post-preservation per-field eligibility is 77--86 families. The only next
> pre-scoring gate is dual independent residual-redundancy review of the 48
> frozen source-card-only packets. This is still no selector score, field
> effect, embedding, retrieval, external API or thesis result. Completion
> checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_FULL_CARD_PRESERVATION_COMPLETION_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual Wave 001.** The first six source-card-only
> residual packets are double-reviewed and consensus-bound across 124
> candidate-field targets. Exact agreement is 96; `none`/`partial`/
> `substantial` consensus counts are 58/35/3, with 28 disagreements retained.
> This is a redundancy stratification gate, not an effect or retrieval result;
> 42 packets remain. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_001_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual Wave 002.** Six more packets add 142 targets
> and 111 exact agreements (43 `none`, 54 `partial`, 14 `substantial`, 31
> disagreements). The cumulative source-card-only ledger is 12/48 packets and
> 266/994 targets. This remains pre-scoring redundancy stratification. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_002_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual Wave 003.** Six packets add 117 targets with
> 91 exact agreements; cumulative residual coverage is 18/48 packets and
> 383/994 targets. This remains pre-scoring redundancy stratification.

> **2026-08-29 RQ1b-A residual Wave 004.** Six packets add 123 targets and
> 87 exact agreements (26 `none`, 48 `partial`, 13 `substantial`, 36
> disagreements). The cumulative source-card-only ledger is 24/48 packets and
> 506/994 targets. Initial response-schema or literal-quote failures were
> preserved as mechanical audit history and independently replaced before
> consensus. This remains pre-scoring redundancy stratification, not retrieval
> or field-effect evidence. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_004_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual Wave 005.** Six packets add 113 targets and
> 82 exact agreements (47 `none`, 26 `partial`, nine `substantial`, 31
> disagreements). The cumulative source-card-only ledger is 30/48 packets and
> 619/994 targets. Any independently replaced payloads are mechanical audit
> history only. This is still pre-scoring redundancy stratification. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_005_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual Wave 006.** Six source-card-only packets add
> 120 targets (54 `none`, 25 `partial`, 12 `substantial`, 29 disagreements)
> and 91 exact independent-review agreements. Cumulative coverage is 36/48
> packets and 739/994 targets. This remains pre-scoring redundancy
> stratification only, not strict-gold, selector, retrieval, embedding, or
> field-effect evidence. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_006_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A residual Wave 007.** Six source-card-only packets add
> 128 targets (83 `none`, 24 `partial`, eight `substantial`, 13 disagreements)
> and 115 exact independent-review agreements. Cumulative coverage is 42/48
> packets and 867/994 targets. This remains pre-scoring redundancy
> stratification only, not strict-gold, selector, retrieval, embedding, or
> field-effect evidence. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_RESIDUAL_REDUNDANCY_WAVE_007_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A local pre-BM25 gate.** Residual review is complete at
> 48/48 packets and 994/994 candidate-field targets (391 `none`, 287
> `partial`, 97 `substantial`, 219 disagreements; 775 exact agreements).
> Original opaque-core bindings remain frozen at 128 selection and 48 residual
> packets. A separate condition-materialisation freeze amendment locks the
> conditions generated only from 48 in-corpus immutable canonical cards; all 48
> candidate-synchronous masks pass mechanical audit. Strict primary readiness
> is 87 preserved families and field denominators of 77--86. No BM25,
> retrieval, embedding, external API, metric, or thesis result exists; BM25
> awaits user approval. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_type_ablation_confirmatory_v2_2026-08-28/CFTC_V2_LOCAL_PRE_BM25_READINESS_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A authorised execution sequence.** Local BM25 is now
> authorised for the immutable v2 ledger-defined strict subset only. It is
> followed by a local Qwen payload/cost preflight; no prompt or card text may
> leave the workspace until a separate exact-scope Qwen approval. A future v3
> expansion toward 100+ strict public candidate compositions and a separate
> source-stratified field-prevalence census are deferred until v2 results and
> failure analysis are reviewed. They are separate evidence lines, not a way
> to increase v2 denominators or revise frozen labels. See
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Public Extension and Field Prevalence Decision Note - 2026-08-29.md`.

> **2026-08-29 RQ1b-A BM25 result.** Local per-composition BM25 over the
> frozen strict v2 scope is complete and independently audited: 87 strict
> families, 174 direct/paraphrase prompts and 1,392 condition rows, with zero
> network calls. Under all-eligible composition-aware analysis, use condition
> has the largest directional full-minus-mask Top-1 contrast (0.068; 95% CI
> `[-0.018, 0.165]`), while every field-level Top-1 and MRR bootstrap interval
> crosses zero. This is a conditional natural-card finding, not an isolated
> field-causality or universal ranking claim. The residual `none`/`partial`
> stratum and all mask transitions are stored with the run. Qwen dense
> retrieval is still unexecuted and requires an exact external-text payload
> approval. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_bm25_2026-08-29/BM25_RESULT_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b-A Qwen payload gate.** The exact local preflight for the
> Qwen single-vector comparator is complete: 1,246 cache-miss texts (1,072
> candidate-condition cards and 174 prompts), 1,414,939 bytes, 197,099 local
> lexical-token proxy and at most 126 no-retry calls. The local runner's
> cache/cosine test and source-length check pass. An attempted execution was
> rejected before process start because this exact DashScope payload had not
> been specifically authorised. At that payload gate, no transfer, call, cache
> write, charge or Qwen result existed. This is a payload gate, not a Qwen
> experiment result.

> **2026-08-29 RQ1b-A Qwen result.** The separately authorised Qwen
> `text-embedding-v4` single-vector twin is complete and locally audited on
> the same frozen strict v2 input as BM25: 87 families, 174 prompts, eight
> conditions and 1,392 rows. The one-time external execution sent exactly the
> preflighted 1,246 texts; 126/126 serial calls succeeded without automatic
> retry and embeddings persist locally. All-eligible composition-bootstrap
> intervals for every field's `FULL-MASK` Top-1 and MRR cross zero. This is a
> conditional natural-card availability/redundancy result, not isolated field
> causality, a universal ranking, or an RQ2 pipeline result. The audited
> checkpoint and residual analysis are at
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_qwen_2026-08-29/QWEN_RESULT_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b v2.1 joint-mask method.** The next RQ1b operation is a
> prospective-before-joint-results field-set availability extension, not a
> revision of v2. It freezes three candidate-synchronous masks over the v2
> cards: `MASK_TASK_SPECIFICATION` (use/input/output),
> `MASK_EXECUTION_VERIFICATION` (workflow/success), and
> `MASK_APPLICABILITY_CAPABILITY` (boundary/dependency). Each group uses only
> the intersection of its constituent-field eligibility sets. BM25 is local;
> Qwen requires a new cache-aware exact payload preflight and separate external
> authorisation. The result can support a joint-set contribution claim only;
> it cannot identify decisive individual fields. Protocol:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Joint Field-Set Availability Amendment - 2026-08-29.md`.

> **2026-08-29 RQ1b v2.1 local BM25 result and Qwen payload gate.** Joint-card
> mechanics and v2 source bindings pass locally. BM25 is complete at 696 rows,
> zero network calls, and a passed independent audit; all group-level Top-1 and
> MRR composition-bootstrap intervals cross zero. The cache-aware Qwen payload
> contains 710 total local texts but only 402 new document texts: 174 queries
> and 134 unchanged FULL cards are already validated cache hits. No new query
> text will be transmitted. The payload permits at most 41 serial no-retry
> calls and needs its own exact approval. This gate is not a Qwen result.

> **2026-08-29 RQ1b v2.1 Qwen twin completed.** After exact user approval,
> DashScope `text-embedding-v4` received only the preflighted 402 new
> candidate-card texts; no query text was transmitted. All 41 serial calls
> succeeded with zero automatic retries and recorded 95,694 provider tokens.
> The completed external receipts and the exact cache were then bound to a
> local cache-only finaliser when the original runner did not write score
> files; it made no credential/API/network/cache-write action and generated
> the audited 696-row result. Qwen's three primary group-level Top-1 and MRR
> bootstrap intervals all span zero. This is a completed selector twin with a
> bounded null/uncertainty finding, not an isolated-field result or thesis
> integration. Checkpoint:
> `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_joint_mask_v21_qwen_2026-08-29/QWEN_RESULT_CHECKPOINT_2026-08-29.md`.

> **2026-08-29 RQ1b v3 source-frame and cluster discovery.** The next public
> RQ1b cohort is deliberately split into a large canonical public source frame
> and a strict 3--4-candidate routing cohort. The frame accepts only
> provenance-recorded original artifacts after exact hash deduplication and
> excludes packet copies, quarantine, outputs and synthetic overlays. It may
> support source-stratified operational-field recoverability/co-occurrence
> audit, not a claim that the field taxonomy was learned from all skills. The
> cluster cohort will be frozen separately to at least 100 candidate
> compositions under strict preservation and cue-control gates. No selector,
> embedding, API, score or thesis result has begun. Protocol:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V3 Public Source Frame and Cluster Discovery Protocol - 2026-08-29.md`.

> **2026-08-29 RQ1b v3 structural marker summary.** A new local-only summary
> over all 29,292 frozen canonical public originals records the coverage and
> co-occurrence of *explicit heading markers*, not semantic field prevalence.
> Workflow/procedure markers appear in 45.514% of artifacts, output/artifact
> in 31.684%, and use-condition in 30.418%; 24.952% expose none of the seven
> markers and only seven artifacts expose all seven. This supports a careful
> public-artifact heterogeneity observation, not a claim that the taxonomy was
> induced from the corpus or that a missing heading means missing information.
> The summary distinguishes 1,564 canonical-content origin identities from
> 1,613 raw source-path origin identities retained through duplicate aliases.
> Evidence: `skill_benchmark/rq1b_v3_public_source_frame/structural_marker_summary_v3_2026-08-29/STRUCTURAL_MARKER_SUMMARY.md`.

> **2026-08-29 RQ1b v3 provenance and new discovery queue.** The declared
> 29,292-record source frame now has a local SHA mapping of the older
> cross-source campaign: all 76 legacy three/four-candidate compositions
> represented by 408 frozen-primary rows occur byte-for-byte in the V3 frame.
> This is deliberately marked `MAPPED_NOT_MERGED`: it does not inherit legacy
> model-assisted review, make a V3 label, or authorise any retrieval. In
> parallel, C0 Waves 007 and 008 materialised two further disjoint source-only
> queues, each with 30 triads / 90 originals. Wave 007 has now completed
> source-only review and finalisation: two entries advance only to C1 and 28
> are rejected before prompt construction. Wave 008 is now also complete: 29
> triads reject before C1 and one Figma composition advances only to C1, where
> it rejects as a component-parent-downstream lifecycle chain. Wave 009 is now
> complete: all 30 source-disjoint triads reject before C1 (22
> component/container/nonparallel, two insufficient contrast, six no common
> envelope). Wave 010 now repeats this result across 30 new source-disjoint
> triads: 21 component/container/nonparallel, two insufficient contrast and
> seven no-common-envelope rejections. Across W1--W10, this C0 path has
> screened 300 lexical triads and remains a discovery calibration, not a
> strict-cluster, prompt, field-effect or retrieval result.
> Records:
> `thesis_notes/checkpoints/methods/RQ1b V3 Legacy Mapping And Wave 007 Discovery Checkpoint - 2026-08-29.md`.
> `thesis_notes/checkpoints/methods/RQ1b V3 Wave 008 Source-Only Materialisation Checkpoint - 2026-08-29.md`.
> `thesis_notes/checkpoints/methods/RQ1b V3 C0 Wave 008 and C1 Wave 003 Closure - 2026-08-29.md`.
> `thesis_notes/checkpoints/methods/RQ1b V3 C0 Wave 009 Closure - 2026-08-29.md`.
> `thesis_notes/checkpoints/methods/RQ1b V3 C0 Wave 010 Closure - 2026-08-29.md`.

> **2026-08-29 RQ1b V3 D1 Wave 006r2 source-semantic recruitment closed.**
> Ten completed lexical C0 waves are retained as feasibility calibration, not
> a claim that peer public routes do not exist. Five disjoint local source-only
> lanes recruited three cross-source triads using literal trigger/input,
> operation, output and constraint/route-out evidence. W6 and W6r1 remain
> fail-closed quotation audits; W6r2 changed only literal spans and rehashed
> all nine originals. Prompt-free C1 then rejected two provider/runtime trios
> for insufficient operational contrast and the SAST trio because Horusec is a
> broad multi-tool container. It generated zero C2 permissions, prompts,
> labels, field effects or retrieval results. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 D1 Wave 006r2 And C1 Closure - 2026-08-29.md`.

> **2026-08-30 RQ1b V3 D1 Wave 007r1 source-semantic recruitment and C1 closed.**
> Five local-only source-grounded triads were repaired from a preserved
> fail-closed literal-evidence attempt using only exact excerpts, then rehashed
> and materialised with zero source reuse. Prompt-free C1 grants C2 construction
> permission to database-distribution migration and workflow-orchestration
> migration; it rejects proposal writing and compliance for no bounded common
> envelope, and video derivatives as adjacent components. This creates neither
> a valid cluster, prompt, gold label, field effect, selector input nor retrieval
> result. The next local step is a 12-slot C2 roster under the frozen cue-control
> SOP. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 D1 Wave 007r1 And C1 Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 D1 Wave 007r1 C2-C3 closed.** The two C1 permissions
> produced a source-bound 12-slot C2 roster and 12 local direct/paraphrase
> drafts. Mechanical inventory finds zero title, short-name or exact three/four
> token source-phrase hits. C3 allows eight low-risk operational packets. Four
> workflow-migration packets remain `REJECT_UNSAFE_CUE` after a separately
> retained cue-only r1 rewording and independent recheck: the necessary rule
> bundles are still highly identifying. This is neither cue-safety proof,
> strict-label validation, field effect nor retrieval result. The eight allowed
> packets cannot enter C4 while the separate C4A source-card schema remains on
> hold. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 D1 Wave 007r1 C2-C3 Closure - 2026-08-30.md`.

> **2026-08-30 RQ1b V3 D1 Wave 008 source-first expansion registered.** The
> frozen 29,292-artifact frame remains a provenance-bounded discovery pool and
> heading-marker census, not a semantic field-prevalence study. Five local,
> source-only recruitment lanes search previously unused originals for natural
> cross-origin peer-route triads or quartets. Every later C1--C6 and global
> C4A hold remains unchanged; a recruited candidate is not a prompt, label,
> field result, selector input, metric or retrieval result.

> **2026-08-30 RQ1b V3 D1 Wave 008 C1 closed.** Five isolated local
> recruitment lanes yield one `NO_CANDIDATE`, two source-level broad/nonparallel
> rejections, and two mechanically valid source triads. The latter both fail
> independent prompt-free C1: database migration is a broad-container plus
> specialist routes; WCAG auditing is static-code, page/component and
> comprehensive-site scope rather than three peers. The r2 materialisation
> passes all six source hashes, literal spans and reuse checks, but C1 grants
> zero C2 permissions. This remains no cluster, label, field effect, selector,
> metric or retrieval result. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 D1 Wave 008 And C1 Closure - 2026-08-30.md`.

> **2026-08-29 RQ1b v3 C4A v1.2 schema repair drafted.** The repair retains
> non-exclusive literal quotations but binds the two remaining calibration
> ambiguities: user-supplied artifacts are inputs rather than resources, and
> only literal pass/fail tests, thresholds, comparisons, validations,
> measurements or acceptance conditions count as success/verification. The
> packet materialiser now carries these rules for a fresh future builder wave.
> No C4A v1.2 builder result, canonical card, strict label, selector or metric
> has been created. The v1.2 packet materialisation is recorded separately
> below. Record:
> `thesis_notes/checkpoints/methods/RQ1b V3 C4A v1.2 Slot-Semantics Amendment - 2026-08-29.md`.

> **2026-08-29 RQ1b v3 C4A v1.2 Wave 001 packets materialised.** Four
> anonymous compositions / 12 original-source copies rehash against the frozen
> source manifest and carry the new v1.2 rules. This is preparation only: no
> builder has responded, no card is canonical, and C4B remains prohibited.
> Evidence:
> `thesis_notes/checkpoints/methods/RQ1b V3 C4A v1.2 Wave 001 Packet Materialisation - 2026-08-29.md`.

> **2026-08-29 RQ1b v3 C2-C3 Wave 002 complete.** Five D1 Wave 005
> C1-approved, source-only compositions produced 30 direct/paraphrase C2
> drafts. Binding audit passed, C3 mechanically inventoried prompt/source
> overlap, and independent source-deidentified review requested nine cue-only
> r1 changes. A fresh packet-level recheck yields 25 `low`, one `medium`, and
> four `high` residual-cue-risk annotations. All 30 may later enter C4 only
> with those annotations; this is not cue-safety proof, a strict label,
> selector input, score or result. C4A remains separately held for source-card
> schema calibration. Evidence:
> `thesis_notes/checkpoints/methods/RQ1b V3 C2-C3 Wave 002 Cue Gate Checkpoint - 2026-08-29.md`.

> **2026-08-29 RQ1b v3 D1 Wave 003r1 completed C1.**
> Three source-only triads were re-materialised after a fail-closed W3 literal
> span check: Spark migration by source dialect; PDF conversion by output
> artifact; and privacy-rights work by jurisdiction. W3r1 binds nine canonical
> originals with zero source reuse, network calls or transmitted text, and its
> three prompt-free C1 packets pass source-binding audit. C1 advances none:
> Spark language variants retain one migration chain; the PDF set contains a
> broad parser container; and the privacy set mixes broad programmes with a
> specialist request workflow. This is not a strict cluster, prompt, gold
> label, representation, selector input, metric or retrieval result. The
> original failed audit, final ledger and revised packet lineage are retained at
> `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_003_2026-08-29/`
> and `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_003r1_2026-08-29/`.

> **2026-08-29 RQ1b v3 C0 Wave 001.** A source-only, model-assisted and
> principal-rechecked feasibility calibration over 30 diversified triads has
> completed after a source-binding audit of 90 non-reused originals. Final
> dispositions are 3 C1 advances, 18 component/container rejections, 2
> copy/derivative rejections, 6 insufficient-contrast rejections and 1
> no-envelope rejection. No prompt or label was made and this does not estimate
> strict cluster yield. The main lesson is operational: lexical same-topic
> triage frequently returns broad containers plus specialised components, so
> later C0 review may prioritise records whose post-shared-title signal tokens
> are non-empty and non-contained. Full ledger and claim boundary:
> `skill_benchmark/rq1b_v3_public_source_frame/c0_source_review_wave_001_2026-08-29/C0_SOURCE_REVIEW_WAVE_001_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 C0 Wave 002r1.** The second zero-overlap
> source-only feasibility wave has completed its provenance audit and final
> ledger: 7 C1 source-evidence advances, 14 nonparallel/component rejections,
> 7 insufficient-contrast rejections, and 2 no-envelope rejections over 30
> triads / 90 sources. The title-containment heuristic prioritised review only;
> it does not validate a candidate. A principal recheck rejected one proposed
> geospatial advance because a broad source covered the specialised role.
> Combined C0 status is ten C1 candidates from 60 reviewed triads, with no
> prompt, gold, field annotation, selector input, metric, API, or thesis
> result. Checkpoint:
> `skill_benchmark/rq1b_v3_public_source_frame/c0_source_review_wave_002r1_2026-08-29/C0_SOURCE_REVIEW_WAVE_002R1_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 C0 Wave 003.** Thirty further zero-overlap
> source-only triads passed local provenance audit. Independent reviewers
> proposed nine C1 advances; principal source recheck retained two and rejected
> seven as container/component/interface or broad-overlap cases. Final outcomes:
> 2 C1 advances, 22 nonparallel/component rejections, 2 insufficient-contrast
> rejections and 4 no-common-envelope rejections. Combined C0 status is 12 C1
> candidates from 90 triads, with no prompt, gold, field annotation, selector,
> metric, API, or thesis result. Checkpoint:
> `skill_benchmark/rq1b_v3_public_source_frame/c0_source_review_wave_003_2026-08-29/C0_SOURCE_REVIEW_WAVE_003_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 C0 Wave 004.** Thirty further zero-overlap
> source-only triads passed local provenance audit. Independent reviewers
> proposed 12 C1 advances; principal source recheck retained three and rejected
> nine as lifecycle, generic-fallback, container or broad-overlap cases. Final
> outcomes: 3 C1 advances, 17 nonparallel/component rejections, 4
> insufficient-contrast rejections and 6 no-common-envelope rejections.
> Combined C0 status is 15 C1 candidates from 120 triads, with no prompt, gold,
> field annotation, selector, metric, API, or thesis result. Checkpoint:
> `skill_benchmark/rq1b_v3_public_source_frame/c0_source_review_wave_004_2026-08-29/C0_SOURCE_REVIEW_WAVE_004_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 C0 Wave 005.** Thirty further zero-overlap
> source-only triads passed local provenance audit. Independent reviewers
> proposed 18 C1 advances; principal source recheck retained 10 and rejected
> eight as broad containers, overlapping variants, or non-peer task envelopes.
> Final outcomes: 10 C1 advances, 10 nonparallel/component rejections, 3
> insufficient-contrast rejections, 1 copy/derivative rejection and 6
> no-common-envelope rejections. Combined C0 status is 25 C1 candidates from
> 150 triads, with no prompt, gold, field annotation, selector, metric, API, or
> thesis result. Checkpoint:
> `skill_benchmark/rq1b_v3_public_source_frame/c0_source_review_wave_005_2026-08-29/C0_SOURCE_REVIEW_WAVE_005_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 C0 Wave 006.** A sixth, zero-overlap lexical triage
> wave passed source-binding and roster-disjointness audit over 30 triads / 90
> originals, but advanced none to C1: 24 reject as nonparallel/component or
> container, five for no common envelope, and one for insufficient operational
> contrast. This is a completed calibration of title/local-FTS discovery, not
> a public-skill prevalence, strict-cluster yield, gold-label, prompt, selector
> or retrieval result. Lexical C0 remains separately reported at 25 C1
> candidates from 180 screened triads. D1 is next and keeps C1--C6 unchanged.
> Checkpoint:
> `skill_benchmark/rq1b_v3_public_source_frame/c0_source_review_wave_006_2026-08-29/C0_SOURCE_REVIEW_WAVE_006_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 C0 Wave 007.** A seventh zero-overlap source-only
> lexical wave completed its binding audit and final ledger over 30 triads / 90
> new originals. It retains only two `ADVANCE_C1_SOURCE_EVIDENCE` entries:
> performance-decay diagnosis and threat-intelligence workflows. Both remain
> subject to C1 overlap/lifecycle checks. The other 28 triads reject before C1:
> 18 nonparallel/component/container, two insufficient operational contrast,
> and eight no-common-envelope. This updates the lexical calibration to 27 C1
> candidates from 210 screened triads; it is neither a valid cluster count nor
> a prompt, gold, field annotation, selector, metric, API or thesis result.
> Evidence:
> `skill_benchmark/rq1b_v3_public_source_frame/c0_source_review_wave_007_2026-08-29/C0_SOURCE_REVIEW_WAVE_007_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 C1 Wave 002.** Both Wave 007 C0 permissions fail
> source-only C1 after binding audit and independent review. The
> traffic/content/ad-decay group has only a broad performance-decline frame,
> while the threat-intelligence group is an explicit enrichment-to-product-to-
>hunt lifecycle. Thus zero C2 prompt-construction permissions arise. This is a
> source-screening negative result only: it does not test field effects,
> representations or retrieval. Evidence:
> `skill_benchmark/rq1b_v3_public_source_frame/c1_source_evidence_wave_002_2026-08-29/C1_SOURCE_EVIDENCE_WAVE_002_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 C1 source-evidence SOP.** The first 25 C0 advances
> now enter a separate, local, prompt-free gate. C1 requires literal source
> spans for every candidate's input/trigger, operation, output and available
> boundary under one source-grounded envelope, and rejects any lifecycle,
> container, wrapper, duplicate or insufficiently distinct composition. A C1
> pass permits only later prompt construction; it is not a gold label, valid
> cluster, selector input or retrieval result. SOP:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V3 C1 Source-Evidence Card SOP - 2026-08-29.md`.

> **2026-08-29 RQ1b v3 D1 directed-discovery amendment.** D1 is a
> prospective local-only, source-first discovery path kept separate from C0
> lexical feasibility calibration. It gives priority to natural artifacts with
> source-visible source-to-target transformations, provider/interface choices,
> or prerequisite/boundary contrasts. It does not create prompts, labels,
> representations, selector inputs or results, and it cannot bypass C1 exact
> evidence, C3 cue control, C4 double-blind singleton review or C5/C6 freeze.
> See `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V3 D1 Directed Public-Source Discovery Amendment - 2026-08-29.md`.

> **2026-08-29 RQ1b v3 D1 Wave 001 materialised.** Four source-only triad
> drafts passed local source rehash and exact-substring validation for every
> trigger, operation, output and available constraint excerpt (12 members;
> zero external calls or transfers). The drafts cover typed document-to-
> Markdown conversion, bounded Browser SDK upgrades, runtime-specific Sentry
> setup, and static documentation-site generators. They enter independent C1
> source-evidence review only; all four are same-origin and retain source-family
> and cue-risk flags. This is not a prompt, gold, valid-cluster, selector or
> retrieval result. Evidence:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_001_2026-08-29/D1_DIRECTED_DRAFT_MATERIALISATION_AUDIT.json`.

> **2026-08-29 RQ1b v3 D1 Wave 001 C1 complete.** Exact-span source-only
> review retained one conversion triad for C2 prompt construction and rejected
> three compositions before prompt construction: one was a serial upgrade
> lifecycle, while two varied only runtime/framework rather than a first-route
> operational role. This remains neither a valid cluster nor a gold, field
> effect, selector, embedding, metric, or routing result. Ledger and literal
> validation: `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_001_2026-08-29/c1_source_evidence_wave_001/C1_SOURCE_EVIDENCE_WAVE_001_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 D1 Wave 002 materialised.** Two source-only,
> cross-origin triads passed mechanical source binding: end-to-end provider
> hosting (Vercel/Render/Netlify) and hosted-LLM application integration
> (OpenAI/Claude/Gemini). C1 independently checks whether the former has
> multiple adequate routes and the latter hides a broad generic fallback or
> container. No prompt, gold, selector, embedding, transfer, metric or routing
> result has been created. Evidence:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_002_2026-08-29/`.

> **2026-08-29 RQ1b v3 D1 Wave 002 C1 complete.** Both cross-origin
> provider-targeted triads were rejected before prompt construction. Render is
> a resource/deployment container alongside Vercel/Netlify's direct deploy-to-
> URL routes; OpenAI/Claude/Gemini retain one text-generation operation with
> provider/client substitution only. This is a source-only peer-role finding,
> not evidence that provider/dependency information has no routing value. Exact
> ledger and validation:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_002_2026-08-29/c1_source_evidence_wave_002/C1_SOURCE_EVIDENCE_WAVE_002_CHECKPOINT.md`.

> **2026-08-29 RQ1b v3 local discovery checkpoint.** The bounded source frame
> is now frozen at 29,292 SHA-unique canonical artifacts from 1,613 origins;
> 2,476 exact duplicate paths are retained only as aliases. The all-record
> structural census reports explicit heading-marker counts, not semantic-field
> prevalence. Two local cross-origin triad queues of 10,000 drafts each are
> available: a broad queue and a three-distinct-normalised-title queue. The
> latter is merely an obvious-copy filter. Neither queue contains prompt,
> label, selector, metric, embedding, model-call or field-effect evidence.
> Next: source-only semantic-envelope and operational-contrast review to form
> V3-C0b cluster drafts. Exact locations and claim boundaries are in
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V3 Public Source Frame and Cluster Discovery Protocol - 2026-08-29.md`.

> **2026-08-29 RQ1b v3 D1 Wave 004r1 completed C1.** The initial W4
> materialisation failure is retained; W4r1 changes only Markdown-formatting
> evidence spans and passes rehash/literal validation for nine cross-origin
> originals. Prompt-free C1 source review grants three C2 permissions only:
> agreement review, structured-data visualisation, and presentation authoring.
> The C1 ledger has three advances, zero source reuse, zero network calls and
> zero transmitted texts. None is a valid cluster, gold label, selector input,
> field effect, or retrieval result. C2 must follow the frozen cue-control
> handoff SOP before any blinded singleton review:
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V3 C2 Prompt Construction and Cue-Control Handoff SOP - 2026-08-29.md`.

> **2026-08-29 RQ1b v3 C2-C3 Wave 001 complete.** Four C1-approved D1
> compositions produced 24 direct/paraphrase C2 packets. A single cue-only r1
> rewrite removed a copied Seaborn source phrase without changing the sealed
> construction target or operational intent. C3 then allowed all 24 only to
> C4, with 20 `high` and four `medium` residual-cue-risk annotations. This is
> not cue-safety proof, a gold label, field-card preservation, selector input,
> metric or retrieval result. C4 still requires source-deidentified seven-slot
> cards and two independent key-blind singleton reviews. Frozen evidence:
> `thesis_notes/checkpoints/methods/RQ1b V3 C3 Wave 001 Cue Gate Checkpoint - 2026-08-29.md`.

> **2026-08-29 RQ1b v3 C4A builder packets materialised.** Four anonymous
> builder packets now bind 12 source-hash-verified originals to the C2/C3
> lineage, but contain no prompt, source ID, title map or sealed target. They
> require two independent seven-slot exact-evidence transcriptions and literal
> identity-line audits before C4B can judge adequacy. This materialisation has
> zero network calls and does not create a card, label, selector input, metric
> or result. Evidence:
> `thesis_notes/checkpoints/methods/RQ1b V3 C4A Builder Packet Materialisation - 2026-08-29.md`.

> **2026-08-29 RQ1b v3 C4A calibration hold.** Two independent source-only
> seven-slot builders returned draft cards for the four anonymous packets, but
> their treatment of natural statements that jointly encode a trigger, action
> and artifact diverged across input, workflow and output slots. No card was
> made canonical and no literal-audit pass, C4B adequacy review, strict label,
> selector input or result was created. The required repair is a source-only
> slot-placement rule, followed by fresh independent builders; it may not use a
> prompt or target to choose a preferred assignment. Evidence:
> `thesis_notes/checkpoints/methods/RQ1b V3 C4A Dual-Builder Calibration Hold - 2026-08-29.md`.

> **2026-08-29 RQ1b v3 D1 Wave 005 source triage.** Twenty further local,
> cross-origin source-only drafts were screened against the frozen 29,292-item
> frame. Seven are merely queued for C1 exact-source review: accessibility,
> content-corpus audit, pre-release security, transaction control,
> agreement-form review, resource forecasting and data-model representation.
> The remaining thirteen are explicitly held or rejected for reuse, no plausible
> third, nonparallel/component, or parent-review risk. This is neither seven C1
> passes nor seven clusters, and contains no prompt, gold, selector, embedding
> or retrieval result. Evidence:
> `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_005_2026-08-29/D1_W5_SOURCE_TRIAGE.md`.

> **2026-08-29 RQ1b v3 D1 W5 C1 closed.** The seven queued
> source-only drafts now bind to 21 unique immutable originals. Local
> input-binding and source-binding audits pass with zero path/hash errors,
> zero candidate reuse, zero network calls and zero transmitted texts. Three
> independent source-only reviews and the literal finaliser yield five C2
> permissions; security is rejected as complementary and forecasting as too
> abstract. These are not valid clusters, prompts, gold labels, selector inputs
> or results. Evidence: `thesis_notes/checkpoints/methods/RQ1b V3 D1 W5 C1 Source-Evidence Closure - 2026-08-29.md`.

> **2026-08-28 RQ1b method amendment.** Do not infer a single-field causal
> effect by deleting spans from naturally authored public full documents. RQ1b
> now separates RQ1b-N untouched original-artifact strict routing validation
> from RQ1b-S source-grounded field-card winner ablation. Field cards contain
> only exact source excerpts in fixed operational slots; the winner-only target
> neutralisation is paired with an identical non-target sham neutralisation.
> This is a derivative-representation sensitivity experiment, not a claim about
> field deletion from the raw artifact. The old P0--P5 workflow remains a
> feasibility audit. See
> `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Natural-Artifact And Source-Grounded Field-Card Protocol - 2026-08-28.md`.

> **2026-08-28 RQ1b-S pilot stop.** The field-card pilot does not advance to
> target/sham comparison. In its first three pre-scoring route-preservation
> checks, field cards preserved the sealed strict winner but blind reviewers
> consistently attributed the route to a different primary field than the
> raw-artifact P0.5 lock. The pre-registered requirement that input and output
> pass locked-field reaffirmation is therefore unmet. Do not relabel the
> target after this observation; any new card-ablation study needs a primary
> field frozen on the card representation before route review. See the pilot
> checkpoint at
> `skill_benchmark/rq1b_cross_source_public_benchmark/working/field_card_pilot_2026-08-28/RQ1B_S_FIELD_CARD_PILOT_CHECKPOINT_2026-08-28.md`.

> **2026-08-15 RQ2 status.** RQ2a development, freeze, confirmatory scoring, paired analysis, cost ledger, failure decomposition, user review, and thesis integration are complete. RQ2b's base-v1 B0G review also completed mechanically: 15,420 validated initial decisions, 250 validated C adjudications, and 7,710 resolved reviewed units. Its final acceptable-set freeze remains `BLOCKED BEFORE RETRIEVAL`: 14 strict-gold rows are not fully acceptable and eight scored prompts have no fully acceptable reviewed candidate. A separate user-directed review of exactly those 14 original gold labels retains six and excludes eight material workflow mismatches. It does not rerun B0G or build acceptable alternatives; its 381-prompt strict-gold-only v1.1 manifest is materialised and locally validated. This produces no RQ2b retrieval result and leaves B1R, all selector work, external transfer, and thesis-result writing unauthorised.

This file records experiment methods and execution venues. For new RQ2 work, the higher-authority source is `thesis_notes/current/RQ2 Current Status and Implementation Tracker - 2026-07-26.md`; lower historical sections here remain provenance records. Every reported result should identify the prompt stratum, skill library scale, representation, selector or first-stage retriever, reranker, candidate budget, scoring rule, cache policy, and execution venue.

For the current canonical thesis framing, use `thesis_notes/current/Information Layer Framework.md`. The older `Representation Layer Horizontal Comparison.md` file remains a result table, but thesis prose should now use "information layer" rather than "representation layer" unless referring to implementation artifacts such as `R1_flat_metadata.jsonl`.

Canonical I3 model-extraction protocol: `thesis_notes/current/I3 Model Extraction Protocol.md`.

Historical frozen benchmark version: `benchmark-v0.4-2026-06-16`.

Freeze manifest:

- `skill_benchmark/versions/benchmark-v0.4-2026-06-16.md`
- `skill_benchmark/versions/benchmark-v0.4-2026-06-16.json`

Do not use v0.4 for RQ2b: its recorded files now include 47 hash drifts and it lacks per-skill source hashes. RQ2b uses the new frozen version `rq2b-full-library-v1-2026-08-02`. Existing v0.4 result files remain historical and should retain their original version ID.

## Current RQ2a Method Contract

Status: `CONFIRMATORY COMPLETE / USER-REVIEWED / THESIS-INTEGRATED`. Development rows remain calibration history; final scientific estimates come from the untouched 280-cluster confirmatory split. Detailed analysis: `thesis_notes/current/RQ2a Confirmatory Results and Analysis - 2026-08-02.md`.

RQ2a reuses the 350 reviewed RQ1a clusters and 750 prompts, split by cluster into:

- 70 development clusters, approximately 150 prompts;
- 280 confirmatory clusters, approximately 600 prompts.

The core matched-content representations are:

| Representation | Selector-visible change | State |
|---|---|---|
| `shared-only` | Shared neutral context; sibling-specific operational values omitted. | Implemented and validated in serializer v1.4. |
| `same-facts-fielded` | All seven reviewed values with explicit labels and boundaries. | Implemented and validated in serializer v1.4. |
| `same-facts-flat` | Identical values and order with labels removed. | Implemented and proposition-matched. |
| `same-facts-prose` | Identical propositions in one frozen prose template. | Implemented and proposition-matched. |
| `same-facts-diluted-2x` | Fielded values plus sibling-identical support text. | Implemented; padding/leakage QA passes. |

Required fixed-candidate selectors:

| Selector | RQ2a role | Execution venue | State |
|---|---|---|---|
| BM25 | Lexical core baseline; BM25 statistics computed within each fixed three-sibling decision corpus. | Local CPU. | Confirmatory complete for eight representations; 4,800 rows. |
| Qwen `text-embedding-v4` single-vector | Primary bi-encoder semantic selector; one reusable vector per complete candidate. | Provider API orchestration with persistent cache. | Confirmatory complete for eight representations; 4,800 rows and exact zero-call warm reproduction. |
| `pipizhao/SkillRouter-Reranker-0.6B` | Direct query-candidate cross-encoder scoring over all three candidates; not SkillRouter embedding. | Local CPU for the fixed-candidate study. | Confirmatory complete for five core representations; 3,000 rows, zero truncation, and exact zero-forward-pass warm reproduction. |
| Qwen semantic field-aware | Required secondary mechanism test on `same-facts-fielded`. | Provider API orchestration with persistent query/field caches. | Confirmatory complete for frozen `uniform-top-two`; 600 rows and exact zero-call warm reproduction. |
| One fixed LLM A/B/C/ABSTAIN selector | Reasoning diagnostic only. | Frozen provider or Codex method with model/prompt/version recorded. | RQ1 tooling exists; RQ2a prompt not frozen. |

The RQ2a field-aware adapter separately embeds all seven fields, uses only the raw query, directly scores all three candidates, and exposes no target-field, gold, role, or alternative metadata. It does not blend a first-stage score. Maximum field similarity and uniform top-two average were compared on development clusters only; `uniform-top-two` was frozen and applied unchanged to all 600 confirmatory prompts. No SkillRouter-native field-aware selector was run; historical SkillRouter-first-stage plus M6 rows use a different second-stage matcher.

RQ2b is `BASE-V1 B0G BLOCKED / V1.1 STRICT-GOLD MANIFEST READY`. Its canonical protocol is `thesis_notes/current/RQ2b Full-Library Retrieval Execution Protocol and Run Ledger - 2026-08-02.md`. The frozen base corpus has 2,433 skills and 401 prompts; the untransmitted I3C packet has 2,433 rows, 57 chunks, and 1,782,352 local proxy tokens. The base-v1 B0G audit resolved 7,710 review units for 389 scored prompts, but strict-gold coverage fails for 14 rows and fully-acceptable coverage fails for eight prompts within the reviewed candidate pool. The focused remediation retains six original labels and excludes eight prompts; its 381-prompt strict-gold-only v1.1 manifest is locally validated. It does not create an acceptable set. The v17 smoke binds 26 implementation scripts and the verified seal rejects stale prompt/representation/configuration/candidate artifacts, including native encoder truncation or model-contract drift. Source-text review, I3C source transfer, Qwen API work, native SkillRouter encoder model download or compute/hosted transfer, hosted SkillRouter reranking, and thesis-result integration remain separate gates. Graph/tree retrieval, external neural reruns, and downstream execution remain outside the minimal core.

RQ2b terminology: Qwen `text-embedding-v4` is the generic-provider first-stage bi-encoder and produces reusable query/document-chunk vectors with the frozen max-chunk policy. The prospective B0F-A1 amendment adds `SkillRouter-Embedding-0.6B`, a separate skill-tuned first-stage bi-encoder, using one complete representation up to 32,768 tokens with no truncation or chunking. Its tokenizer also remains the pinned local proxy tokenizer for Qwen chunk auditing, but its weights are used only in its own separately authorised replication condition. B2 uses `SkillRouter-Reranker-0.6B`, which jointly scores each query-candidate window and cannot reuse either first-stage vector as a reranker score.

## RQ1 Field-Targeted Test Design

The current I1/I3/I2 representation matrix is mainly RQ2 evidence: it compares complete strategy conditions. RQ1 needs a stricter field-targeted design that asks which operational information actually distinguishes semantically similar skills.

Detailed source of truth: `thesis_notes/current/RQ1/protocols/RQ1 Field Targeted Test Plan.md`.

Current RQ1 evidence split:

> **2026-08-28 RQ1b cross-source live-status override.** Round 42 passed C6 under the unchanged strict 3--4-candidate, cross-source public-original protocol. The live curation state is `76 FROZEN CANDIDATE COMPOSITIONS / 408 FROZEN STRICT PROMPT PACKETS / 119 NON-PRIMARY EXPLORATORY-OR-DISAGREEMENT-OR-MISMATCH PACKETS / NO RETRIEVAL RESULTS`. Round 42 added four source-backed compositions and seven strict packets. Its final C3 lineage ended at 36 low / 12 medium / 0 high cue-risk records; two anonymous model-assisted C4 reviewer pairs produced seven exact singletons, 34 multi-adequate agreements, and seven disagreements. Only C5 sealed-target-matched singletons froze. The 75-composition curation target is met. This remains curation/feasibility bookkeeping, not human annotation, retrieval, API use, model performance, or a metric. Evidence: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 42 M0-C6 Closure - 2026-08-28.md`.

> **2026-08-28 RQ1b cross-source masked-execution protocol.** The current corpus contains 76 candidate compositions, 209 strict routing-test families (candidate composition plus strict-gold target), and 408 prompt variants. It has a separately recorded pre-retrieval pipeline: P0 hash-roster reconstruction; P0.5 independent blind field-contrast coding because C6 does not consistently encode a machine-readable primary field and one composition may have multiple strict targets; P1/P2 target-evidence mapping; P3 mask construction/fidelity control; P4 masked-text residual-cue challenge; and P5 execution freeze before any selector is run. It is `P0 MASTER-ROSTER PRECHECK PASS / P0.5 IN PROGRESS / P1-P7 NOT STARTED`: the local P0 roster reconstructs all 408 C6-to-C2 prompt lineages across 26 locked C2 files, 209 families, and 76 compositions, with every canonical source byte rehashed. A four-family P0.5 pilot first locked one output-artifact field but its two validated evidence maps found inseparable structural carriers, so all four pilot families are now `ORIGINAL_ONLY`. No source evidence has been masked, no family is mask-eligible, and no BM25/Qwen result exists. The protocol keeps `MASK_ELIGIBLE`, `ORIGINAL_ONLY`, and `EXCLUDE` distinct, uses original public artifacts only, and preserves RQ1a/RQ2 boundaries. Protocol: `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Cross-Source Masked Field-Evidence Execution Protocol - 2026-08-28.md`; P0 roster: `skill_benchmark/rq1b_cross_source_public_benchmark/working/masked_execution/p0_master_roster_2026-08-28.json`; pilot audits: `skill_benchmark/rq1b_cross_source_public_benchmark/working/masked_execution/p05_field_coding_round01_2026-08-28/P05_ROUND01_AUDIT.md` and `skill_benchmark/rq1b_cross_source_public_benchmark/working/masked_execution/p1_evidence_mapping_round01_2026-08-28/P1_P2_UNION_DECISION.md`.

> **2026-08-28 masked-execution checkpoint.** P0.5 batches 01--10 plus the four-family pilot have passed through their available curation gates; Batch 11 remains in progress. Twelve post-pilot locks have already failed closed to `ORIGINAL_ONLY` during P1/P2 or P3. The one P1/P2 union with no inseparable cue still failed P3 because evidence spans were non-unique/overlapping, so no masked copy exists. This is still no-retrieval, no-metric work; see `skill_benchmark/rq1b_cross_source_public_benchmark/working/masked_execution/RQ1B_MASKED_EXECUTION_CHECKPOINT_2026-08-28.md`.

- **RQ1a controlled individual-field sufficiency (`REVIEWED / COMPLETE`):** field-targeted test units check whether a specific skill-side field value improves selection among near-neighbour siblings under controlled shared context. Its hidden condition intentionally ties siblings; it therefore establishes field sufficiency under controlled ambiguity, not natural prevalence or necessity.
- **Supporting public-skill field-realism audit (`COMPLETE / CONTEXT ONLY`):** the 460-file public-original corpus audit and extraction QA show whether source artifacts contain recoverable evidence for the seven fields. This is grounding evidence, not an RQ1b routing-accuracy experiment.
- **RQ1b naturalistic public-skill replication (`WAVE 001 FROZEN / NATURAL_ORIGINAL_ONLY / NOT EXECUTED`):** a separate 1,099-artifact source corpus (460 historical originals, 168 staged MIT-licensed Emmraan originals, 471 staged MIT-licensed Skill Me originals) yielded a frozen local-only Wave 001 of 62 valid source-disjoint natural-original clusters over 129 unique candidate skills. Each freezes source hashes, two task prompts, a literal-overlap disposition, exact residual evidence spans, and two model-assisted blinded reviewer tables; all 62 have an agreed singleton acceptable first skill for both prompts. All are `ORIGINAL_ONLY`, because the operational contrast is distributed through natural titles, workflows, examples, and resources, so no causal masked delta is permitted. The field mix is `use_condition` 17, `output_artifact` 20, `dependency_resource` 6, `input_precondition` 7, `workflow_procedure` 6, `boundary_not_for` 4, and `success_verification` 2; fields below five are exploratory. This meets the 50-cluster feasibility threshold, but it is not a retrieval result, human annotation, or external transmission. No BM25, embedding, selector, API, or external transfer has occurred. Protocol and freeze certificate: `thesis_notes/archive/RQ1/superseded-public-card/RQ1b Naturalistic Public Skill Replication Protocol - 2026-08-24.md` and `skill_benchmark/rq1b_naturalistic_public_replication/manifest/wave_001_freeze_certificate.json`.
- **RQ1b cross-source strict-public expansion (`TARGET MET / ROUND 42 C6 FROZEN / 76 COMPOSITIONS / 408 STRICT PROMPTS / 119 NON-PRIMARY / NOT EXECUTED`):** this is a separate, stricter cross-source campaign over original public artefacts. Round 35 C6 adds five compositions and 22 strict singleton packets; Round 36 adds three compositions and 18 packets. Round 37's fresh cohort produced no addition: C0A rejected one origin-duplicated triad and exact-source C0B rejected one generic connector plus specialised-workflow triad, with five literal evidence spans independently verified. Round 38 discovery added 173 historic-root-new public sources after a self-inclusion correction, staged 708 SHA-verified originals from 52 origins, and advanced three source-backed compositions. Round 39 began with new six-lane public discovery: 65 net-new pinned roots, 698 canonical SHA-verified originals from 34 origins, 14 C0A directions, and one source-backed C0B/C1 quartet. Round 40 corrected an M1 historic-prefix defect without changing source bytes, then staged 816 canonical originals from 46 origins and advanced three source-backed triads. Its C2 prompts were source-informed reworded before the final C3 pass; C3 allowed all 18 with residual cue risk retained. Two source-deidentified model-assisted C4 reviews yielded 16 exact singleton agreements and two disagreements. Citation normalisation repaired 27 evidence spans only, not adequacy judgments or rationales. C5/C6 froze the three compositions and 16 strict packets only. By the Round 40 closure, the cumulative 72 non-primary packets remained exploratory/disagreement/mismatch records rather than forced labels. C3 records keep literal cue control distinct from conservative source-informed construction-sensitivity review; they are residual-risk metadata, not human judgment or semantic-fidelity proof. This is not human annotation, an RQ1a causal masking study, retrieval evidence, or an externally transmitted/model-provider result. The 75-composition target is met; any future cohort must begin with fresh public-source discovery and preserve C0--C6 gates. Checkpoints: `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 35 C0A-C6 Closure - 2026-08-28.md`, `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 36 C0A-C6 Closure - 2026-08-28.md`, `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 37 C0A-C0B Closure - 2026-08-28.md`, `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 38 M0-C6 Closure - 2026-08-28.md`, `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 39 M0-C6 Closure - 2026-08-28.md`, and `thesis_notes/checkpoints/methods/RQ1b Cross-Source Round 40 M0-C6 Closure - 2026-08-28.md`.
- **RQ1c joint-field interaction (`DEFERRED`):** do not build or score it before reviewing RQ1b results. Combined all-field representations, graph/tree grouping, and retriever robustness remain later RQ2 concerns unless the thesis framing is explicitly changed.

RQ1 test unit:

| Component | Requirement |
|---|---|
| Fixed prompt requirement | Explicit enough for a stable gold label. |
| Near-neighbour skill pair/cluster | Same domain and broad task family, with plausible sibling confusion. |
| Shared neutral skill context | Keeps broad task context but removes the target field value. |
| Target field values | Skill-side values that differ, such as scanned/native input, JSON/prose output, validate/repair workflow, or HF Jobs/local dependency. |
| Fixed retriever/metric | Same method, candidate budget, and metric while field visibility changes. |

RQ1 test-case schema:

| Field | Required value |
|---|---|
| `prompt_id` | Stable prompt identifier. |
| `gold_skill` | One gold skill that should be selected. |
| `confusing_alternatives` | 2-4 semantically plausible but procedurally wrong alternatives. |
| `primary_distinguishing_field` | One of `use_condition`, `input_precondition`, `output_artifact`, `workflow_procedure`, `boundary_not_for`, `dependency_resource`, or `success_verification`. |
| `secondary_distinguishing_fields` | Optional extra fields that also support the gold. |
| `field_evidence_gold` | Exact skill-artifact evidence showing the gold has the required field. |
| `field_evidence_alternatives` | Evidence or rationale showing why alternatives lack, conflict with, or are weaker on the field. |
| `prompt_requirement` | The user-request phrase that requires this field. |
| `controlled_baseline_description` | Shared neutral skill-side context with the primary field removed. |
| `baseline_leakage_status` | `clean`, `leaky_original_description`, `too_vague`, or `multi_field`. |

RQ1 evaluation outputs:

- global field ablation table;
- field-labelled ablation table grouped by `primary_distinguishing_field`;
- hard-negative sibling error rate by field;
- within-cluster top-1/MRR;
- field delta against description-only, reported as `top1(description + field) - top1(description only)`;
- length-control or field-dropout check before making causal claims about a field.

Use these tests to answer RQ1. Use I1/I3/I2 with Qwen, SkillRouter, lexical retrieval, rerankers, graph, or tree methods later for RQ2 only after their carried information and leakage controls are specified.

Canonical RQ1a condition names:

| Condition | Selector-visible text | Interpretation |
|---|---|---|
| `shared_context_only` | Shared neutral skill-side context with the tested field omitted. | Hidden-field baseline; should intentionally tie siblings. |
| `shared_context_plus_field` | Same shared context plus exactly one target field line. | Main exposed-field condition for RQ1a. |
| `field_only` | The target field value alone. | Diagnostic only. |
| `full_skill_doc` | Whole generated skill artifact. | Diagnostic only; tests whether the field signal survives document noise and added cost. |

All thesis-facing RQ1a field tables should use `shared_context_only` versus `shared_context_plus_field` as the causal field-isolation contrast. Do not use `full_skill_doc` as the main RQ1a exposed-field condition.

Critical RQ1 control condition:

- The prompt should be explicit enough to support a stable gold label. It should state the object and operational requirement, such as scanned PDF, JSON table output, HF Jobs execution, no legal advice, or visual verification.
- The prompt is not the experimental variable and should not be made vague to avoid leakage.
- Leakage control is applied to the skill-side baseline representation. The baseline should keep the shared cluster/task context but remove the primary distinguishing field.
- Example: for scanned-vs-native PDF extraction, "Extracts structured information from PDF documents" is a better baseline than "Handles PDF document processing tasks" because it preserves the shared task while hiding the scanned/native distinction.
- If the original description already contains the tested field, keep it as a realistic RQ2 baseline and create a controlled masked baseline for RQ1. If masking makes the case too vague, mark it `too_vague` and exclude it from clean RQ1 field ranking.
- Input/precondition and output/artifact authoring/design were approved and run on 2026-06-24. Boundary/not-for was promoted to a thesis-facing RQ1a run on 2026-06-25 with explicit, paraphrase, and implicit-authority prompt variants. Use condition was run on 2026-06-27 with direct and paraphrase prompt variants. Its result supports use condition as a strong task-intent signal, but the paraphrase drop, especially under BM25, means it should be described as wording-sensitive and sometimes requiring semantic intent interpretation. Dependency/resource was narrowed and rerun on 2026-06-28 as a required platform/tool/API/runtime/permission/version/provenance field, not as a generic input-resource field. It should be reported through the same canonical RQ1a field-isolation contrast as the other suites: `shared_context_only` versus `shared_context_plus_field`. Its prompt variants are `direct` and `contextual`; contextual rows use the user prompt plus positive routing context as the query text, because real public-skill dependency evidence is often expressed through tool/MCP availability, auth, runtime, API, package version, package metadata, or resource context. Generic setup/download commands such as `npm install`, `pip install`, `npm ci`, build/test/lint commands, or dependency-hygiene advice are not counted as strong dependency/resource routing evidence unless they encode a named capability or compatibility conflict. The suite now includes 9 version-compatibility clusters, making version a covered subtype rather than only a theoretical dependency/resource category. Extra no-I/O or identical-I/O runner conditions are exploratory diagnostics only, not separate thesis claims. A dependency interaction test may be designed later, where input/output partially narrow candidates and dependency/resource resolves the remaining ambiguity. Success/verification was refined and run on 2026-06-30 as a concrete acceptance-gate suite: threshold checks, validation checks, evidence/source anchoring, unresolved finding state, rollback proof, reproducible failure, and runtime smoke checks are valid; polished writing, broad style, persuasive wording, and generic output quality are excluded. Its result is positive but weaker and more paraphrase-sensitive than the strongest fields. Workflow/procedure has now also been authored, rubric-checked, run, and analysed as a heterogeneous procedure-order/operation-path suite.

Shared-context non-leakage rule:

- The shared context may contain broad domain/task-family words such as PDF extraction, dataset quality, API work, browser evaluation, experiment execution, or compliance document review.
- It must not contain the target field value or close synonyms, such as scanned/native, JSON/prose, validate/repair, legal-advice/no-legal-advice, Hugging Face Jobs/local, or visual evidence/data scrape.
- If a human can pick the gold using the shared context alone, the shared context leaks and must be rewritten or the unit marked `leaky_original_description`.
- If a human cannot understand the broad task family, the unit is too vague and should be marked `too_vague`.

Optional RQ1 diagnostic: isolated corruption:

- Isolated corruption can be used to test whether the retriever actually attends to the target field.
- It must use the same controls as the main RQ1 field test: fixed prompt, same skill pair/cluster, same retriever, same candidate budget, and non-target fields held controlled/non-discriminative.
- Corrupt or swap only the `primary_distinguishing_field`.
- If ranking flips or degrades, report this as field sensitivity.
- Do not use multi-field conflict corruption as RQ1 evidence. Cases where one corrupted field conflicts with several correct fields belong to RQ2 robustness/conflict-resolution and may require `no valid skill` or clarification outcomes.

Completed RQ1a suites, 2026-06-24:

| Property | Value |
|---|---|
| Field | `input_precondition` |
| Suite | `skill_benchmark/rq1a_field_discriminability/input_precondition/` |
| Clusters | 50 near-neighbour clusters |
| Prompts | 100 prompt variants: direct + paraphrase-safe for each cluster |
| Candidates per prompt | 3 sibling skills, one gold and two hard negatives |
| Controlled variable | Skill-side exposure of input/precondition |
| Hidden-field condition | `shared_context_only`, intentionally tied across siblings |
| Exposed-field condition | `shared_context_plus_field` |
| Full-doc diagnostic | `full_skill_doc` |
| Retrievers run | BM25 and Qwen `text-embedding-v4` |
| Metrics | Tie-aware top-1, MRR, lift over hidden-field baseline |
| Result file | `skill_benchmark/outputs/rq1a_input_precondition_bm25_qwen_embedding.md` |

Main result:

Prompt subset `Combined` pools the direct and paraphrase-safe prompt rows.

| Retriever | Prompt subset | Hidden field top-1 | + input/precondition top-1 | Lift | MRR + field |
|---|---:|---:|---:|---:|---:|
| BM25 | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| BM25 | Paraphrase | 33.3% | 91.0% | +57.7pp | 0.953 |
| BM25 | Combined | 33.3% | 95.5% | +62.2pp | 0.977 |
| Qwen embedding | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| Qwen embedding | Paraphrase | 33.3% | 94.0% | +60.7pp | 0.970 |
| Qwen embedding | Combined | 33.3% | 97.0% | +63.7pp | 0.985 |

Interpretation boundary: this is clean RQ1a evidence for one operational field under controlled near-neighbour conditions. It should not be merged with the frozen-v0.4 full representation matrix as if it were an I1/I2/I3 strategy result.

Second completed RQ1a suite, 2026-06-24:

| Property | Value |
|---|---|
| Field | `output_artifact` |
| Suite | `skill_benchmark/rq1a_field_discriminability/output_artifact/` |
| Clusters | 50 near-neighbour clusters |
| Prompts | 100 prompt variants: direct + paraphrase-safe for each cluster |
| Candidates per prompt | 3 sibling skills, one gold and two hard negatives |
| Controlled variable | Skill-side exposure of output/artifact |
| Hidden-field condition | `shared_context_only`, intentionally tied across siblings |
| Exposed-field condition | `shared_context_plus_field` = same shared context plus `Output Artifact: ...` |
| Full-doc diagnostic | `full_skill_doc`, diagnostic only |
| Retrievers run | BM25 and Qwen `text-embedding-v4` |
| Metrics | Tie-aware top-1, MRR, lift over hidden-field baseline |
| Result file | `skill_benchmark/outputs/rq1a_output_artifact_bm25_qwen_embedding.md` |

Main result:

Prompt subset `Combined` pools the direct and paraphrase-safe prompt rows.

| Retriever | Prompt subset | Hidden field top-1 | + output/artifact top-1 | Lift | MRR + field |
|---|---:|---:|---:|---:|---:|
| BM25 | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| BM25 | Paraphrase | 33.3% | 53.3% | +20.0pp | 0.723 |
| BM25 | Combined | 33.3% | 76.7% | +43.3pp | 0.861 |
| Qwen embedding | Direct | 33.3% | 100.0% | +66.7pp | 1.000 |
| Qwen embedding | Paraphrase | 33.3% | 92.0% | +58.7pp | 0.957 |
| Qwen embedding | Combined | 33.3% | 96.0% | +62.7pp | 0.978 |

Interpretation boundary: this is clean RQ1a evidence for the output/artifact field. It also shows that paraphrased output requests are much harder for BM25 than for Qwen embedding.

Third completed RQ1a suite, 2026-06-25:

| Property | Value |
|---|---|
| Field | `boundary_not_for` |
| Suite | `skill_benchmark/rq1a_field_discriminability/boundary_not_for/` |
| Clusters | 50 near-neighbour clusters |
| Prompts | 150 prompt variants: direct + paraphrase-safe + implicit-authority for each cluster |
| Candidates per prompt | 3 sibling skills, one gold and two hard negatives |
| Controlled variable | Skill-side exposure of boundary/not-for constraint |
| Hidden-field condition | `shared_context_only`, intentionally tied across siblings |
| Exposed-field condition | `shared_context_plus_field` = same shared context plus `Boundary / Not For: ...` |
| Mechanical rubric | `skill_benchmark/rq1a_field_discriminability/boundary_not_for/rubric_summary.md`, 50/50 `accepted_strict` |
| Main output | `skill_benchmark/outputs/rq1a_boundary_not_for_bm25_qwen_embedding_with_implicit.md` |
| Status | Complete thesis-facing RQ1a field-isolation result |

Main result:

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

Interpretation boundary: boundary/not-for is useful, but should be framed as scope, authority, compatibility, or guardrail evidence. It is much weaker when the prompt implies authority or scope rather than stating the exclusion directly.

## Current Research Frame

The thesis studies candidate subsetting for large agent skill libraries. The main question is not "which retriever wins"; it is first which operational information helps distinguish semantically similar but procedurally different skills, and then how representation/retrieval strategies preserve, organize, or exploit routing-relevant information under scale.

Current framing:

- Axis 1 is the **information layer**: what the selector can know about each skill.
- Axis 2 is the **retrieval/encoding strategy**: how routing-relevant information is encoded, searched, ranked, traversed, or reranked.
- Graph, tree, embedding, and reranker methods are retrieval/encoding strategies, not the main thesis object by themselves.
- If task, input, output, workflow, dependency, boundary, or success information is retrieval-critical, a scalable system must make it available somewhere: author-provided metadata, deterministic parsing, LLM-assisted extraction, learned encoders/rerankers, or full-artifact retrieval.
- Therefore, explicit fields are not claimed as the only possible solution. They are an inspectable and controllable way to test which operational information matters.
- Current priority is RQ1: field ablations and cluster/prompt-type analyses should be completed before making strong graph/tree claims.
- Graph/tree/DAG information assumptions remain TBD. They may organize relation, provenance, grouping, dependency, or branch-summary signals, but they should not be described as carrying the same information as I3 unless that mapping is explicitly implemented and evaluated.

## Prompt Strata

| Stratum | Prompt count | Purpose | Prompt source |
|---|---:|---|---|
| Controlled | 245 | Designed semantic-confusability clusters with gold labels and near-neighbour alternatives, including public-style controlled prompts. | `skill_benchmark/prompts/*.json` |
| Public-gold | 144 | Externally authored/public skill targets, used to test whether the representation claim generalizes beyond generated controlled skills. | `skill_benchmark/prompts_public_gold/*.json` |
| SkillRouter-Eval-Core external | 75 scored tasks, separate from local benchmark | External portability check using the public SkillRouter benchmark; not a replacement for controlled thesis evidence. | `skill_benchmark/external/skillrouter_eval_core` |
| Combined | 389 | Reporting view combining controlled and public-gold strata. Use only after reporting strata separately. | Controlled + public-gold |
| Low-information stress | 12 separate stress prompts | Tests how methods behave when prompt evidence is vague or under-specified. | `skill_benchmark/prompts_low_information/*.json` |

Broad prompt pool: 401 prompts = controlled + public-gold + low-information stress.

Default skill-library scale: `current_full`, currently the frozen 2433-skill library. Avoid using `core` for public-gold because public target skills are not present in the controlled-core candidate pool.

Public-gold clustering caveat:

- Public-gold retrieval is not cluster-restricted. The selector ranks against the full `current_full` library.
- Public-gold source-of-truth rule, added 2026-06-23: final public-gold reporting should use the upstream public skill artifact stored at `skill_benchmark/skills/public_imported_background/<skill>/source/SKILL.original.md`. The normalized top-level wrapper `SKILL.md` is retained for import provenance and background-scale bookkeeping.
- Current correction status, 2026-06-23: `run_offline_selectors.load_full_skill_texts()` now prefers public originals through `full_skill_source_path()`, and `export_skill_representations.py` now derives public-imported R1/R2/R3 text from `source/SKILL.original.md` where present while preserving stable wrapper skill ids. The crossed BM25/TF-IDF lexical matrix, local offline selectors, Qwen provider rows, and Qwen-only fixed M6-v2 diagnostics have been refreshed after this correction. SkillRouter rows generated before this correction remain historical until rerun.
- The current public-gold prompt file uses one broad `family = public_gold_validation`, so `by_family` result summaries are not informative.
- Public-gold cases include `source_family` values such as `huggingface`, `office-document`, `github-ci`, `web-quality`, `figma`, and `agent-workflow`. These should be treated as analysis clusters, not retrieval filters.
- Before final reporting, public-gold result analysis should group failures by `source_family` and by manually defined cluster type: public-public confusion, public-controlled confusion, broad public-artifact confusion, duplicate/acceptable alternative, and background false positive.
- Current controlled/public validation residuals are recorded in `thesis_notes/checkpoints/benchmark_validation/Benchmark Residual Validation Reasons - 2026-06-06.md`; do not silently treat these residuals as ordinary selector failures.

SkillRouter-Eval-Core external-validation caveat:

- Keep this track separate from the local frozen-v0.4 benchmark. It is an external benchmark built for SkillRouter-style multi-skill routing, not for isolating the thesis-controlled semantic-confusability clusters.
- The public Easy tier has 78,361 skills; the Hard tier has 79,141 skills and is exactly Easy plus 780 hard-only distractors.
- Default scored evaluation uses 75 non-`generic_only` tasks. Many tasks require multiple skills, so report Hit@1 together with MRR@10, Recall@k, and FullCoverage@k.
- Current derived artifacts live under `skill_benchmark/external/skillrouter_eval_core/derived`; current outputs live under `skill_benchmark/external/skillrouter_eval_core/outputs`.
- First external checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter Eval Core Checkpoint - 2026-06-18.md`.
- Corpus/prompt audit checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter Corpus Richness Audit - 2026-06-23.md`.
- Audit caveat: SkillRouter-Eval-Core skill bodies are often markdown-normalized public documentation. In the full corpus, 95.0% of rows have H1 headings and 78.8% show procedural signal; in the scored gold-name subset, 98.5% have H1 headings and 79.2% show procedural signal. Common section labels include `overview`, `when to use`, `workflow`, `quick start`, `dependencies`, and `best practices`.
- Prompt caveat: SkillRouter scored tasks are substantially more informative than local controlled prompts. The 75 scored tasks average 198.4 rough tokens with median 169, 97.3% file/path references, 92.0% explicit input cues, 85.3% explicit output cues, and 40.0% numbered steps. Local controlled prompts average 36.8 rough tokens with median 25 and deliberately include near-neighbour alternatives.
- Interpretation rule: use SkillRouter-Eval-Core as portability evidence and cost/scale evidence, not as a direct replacement for the local controlled semantic-confusability benchmark.

## Information Layers

Use `I*` names in thesis prose. Existing `R*` names remain implementation labels for scripts and result files.

| Information layer | Existing implementation label | Selector-visible information | Artifact |
|---|---|---|---|
| I0 progressive disclosure | R0 / M0 traces | Main agent sees skill names/descriptions/metadata and then loads full docs after selecting. | M0 traces, not a JSONL artifact |
| I1 flat skill card | R1 | Skill name, family/category, short description, tags. | `skill_benchmark/representations/R1_flat_metadata.jsonl` |
| I2 full skill artifact | RFULL | Entire source skill text, usually with name/description included by the runner. For controlled skills this is top-level `SKILL.md`; for imported public-gold targets the source of truth is upstream `source/SKILL.original.md`. | `skill_benchmark/skills/**/SKILL.md`; public original override `skill_benchmark/skills/public_imported_background/**/source/SKILL.original.md` |
| I3 structured selection fields | R2 / parts of R3 | Task/use conditions, avoid conditions, preconditions, workflow, outputs, normalized procedural summaries, dependencies/resources, and boundaries. | `skill_benchmark/representations/R2_structured_procedural.jsonl`, `skill_benchmark/representations/R3_dependency_resource_aware.jsonl` |
| I4 skill-relation information | planned R4 | Candidate relation carriers such as input-output direction, workflow order, dependency/resource links, alternatives, composition, provenance, or similarity. Exact thesis-facing edge schema is TBD. | planned `skill_benchmark/representations/R4_graph_edges.jsonl` |
| I5 hierarchy/grouping information | planned M4 tree/DAG | Candidate grouping carriers such as domain, task family, capability family, coarse-to-fine branch summaries, and atomic skill grouping. Exact thesis-facing branch schema is TBD. | planned tree/DAG index |

Important distinction:

- I3 fields are not only authoring requirements. They are also information-layer extraction targets. Public skills may imply these fields without explicitly naming them.
- Current frozen-v0.4 I3 should be called `I3H` when extraction provenance matters: it is a heuristic/section-based extraction layer, not a uniformly model-parsed layer.
- Local I3C has not been produced. No local Codex/ChatGPT subagent extraction has been run over the 2433 frozen-v0.4 skills. External SkillRouter-Eval-Core I3C exists and should not be confused with local I3C.
- Existing DeepSeek public-skill work is `I3V`: model-assisted field verification/audit, not the canonical retrieval representation.
- Model-parsed local I3 from DeepSeek/API is `I3M`. The full local 2433-skill run completed on 2026-06-18 with `deepseek-v4-flash` primary and `deepseek-chat` fallback. Treat `skill_benchmark/representations/I3M_model_parsed.jsonl` as a paid-model feasibility/pass attempt, not the thesis-facing I3C route. Do not mix I3H, I3M, and I3C results without naming extraction provenance.
- I4/I5 are not "more fields"; they encode or organize routing-relevant relations and grouping. Graph/tree methods should only be added if they test clearly specified relation/grouping assumptions without benchmark leakage.
- I2 full text is not automatically better. It may contain more information but also more noise and higher cost.

## Method Matrix

Use this table as an implementation matrix. It should be read through the information-layer frame above: a method is a combination of information layer, encoding/search strategy, optional reranker, and candidate budget.

Source-correction warning, 2026-06-23: BM25/TF-IDF crossed lexical rows, local offline selectors, Qwen provider rows, and Qwen-only fixed M6-v2 diagnostics have been refreshed after correcting public-original source loading and regenerating public-style controlled skills as messier public-document-style artifacts. SkillRouter local rows in older result files remain historical until rerun under the corrected corpus/source policy.

Public-style controlled regeneration note: the 32 public-style controlled skills now average 741.5 rough words, include varied public-style headings, tables, YAML handoff snippets, sibling-skill boundary notes, examples, and operational anchors. They are designed to contain the same routing-critical information as the controlled benchmark, but in less schema-like public documentation form.

| Method ID | Status | Information layer / artifact | First-stage retriever | Reranker | Candidate budget | Main purpose |
|---|---|---|---|---|---:|---|
| M0 | Historical/core only | I0 / R0 | Main-agent progressive disclosure | Main agent decides | n/a | Small-library baseline and context/cost stress test. |
| M1-BM25 | Done frozen v0.4 crossed lexical audit | I1/I2/I3 via R1/RFULL/R2 | BM25 lexical | none | all | Lightweight lexical control for information-layer effects. |
| M1-TFIDF | Done frozen v0.4 crossed lexical audit | I1/I2/I3 via R1/RFULL/R2 | TF-IDF lexical | none | all | Lightweight lexical control for information-layer effects. |
| M2-MiniLM-full | Historical/local | I2 / RFULL | MiniLM embedding | none | all | Cheap local reference, not final modern baseline. |
| M2-Qwen-R1 | Done frozen v0.4 | I1 / R1 | Qwen `text-embedding-v4` | none | all | Modern dense retrieval over flat cards. |
| M2-Qwen-R2 | Done frozen v0.4 | I3 / R2 | Qwen `text-embedding-v4` | none | all | Modern dense retrieval over serialized structured fields. |
| M2-Qwen-full | Done frozen v0.4 | I2 / RFULL | Qwen `text-embedding-v4` | none | all | Modern dense retrieval over full skill docs. |
| M2-SkillRouter-full | Done frozen v0.4 | I2 / RFULL | `pipizhao/SkillRouter-Embedding-0.6B` | none | all | Skill-specific dense retrieval baseline. |
| M2-SkillRouter-R1 | Done frozen v0.4 | I1 / R1 | SkillRouter embedding | none | all | Separates SkillRouter model effect from information-layer effect. |
| M2-SkillRouter-R2 | Done frozen v0.4 | I3 / R2 | SkillRouter embedding | none | all | Skill-specific dense retrieval over structured fields. |
| M3-schema-lexical | Implemented | I3 / R2/R3 | TF-IDF/BM25 over schema text | none or schema score | all/top-k | Tests serialized structured selection information. |
| M4-tree | Planned | I5 hierarchy/grouping | Tree/DAG route | optional within-branch rerank | branch/top-k | Tests hierarchical routing and branch-exclusion failures. |
| M5-graph | Planned | I4 relation information | Graph filter/expansion/diffusion | graph-aware rerank | top-k | Tests explicit skill relations rather than serialized text only. |
| M6-v0-schema | Implemented diagnostic | I1/I3 via R1/R2/R3 | BM25, TF-IDF, MiniLM, or Qwen shortlist | deterministic schema weighted overlap | 20/50/100 | Transparent diagnostic reranker over extracted fields. |
| M6-v1-local | Done frozen v0.4 for BM25/TF-IDF/Qwen and SkillRouter top-20 | I1/I3 via R1/R2/R3 | BM25, TF-IDF, Qwen full, or SkillRouter top-20 candidates | deterministic field-aware matcher | 20/100 depending first stage | Separates first-stage candidate recall from field-aware reranking. |
| M6-v2-semantic-field | Done frozen v0.4; calibration ongoing | I1/I2/I3 via R1/RFULL/R2/R3 | Qwen or SkillRouter fixed top-20 shortlist | no-rewrite semantic field matcher | 20 | Tests semantic use of explicit fields while holding query and candidates fixed. |
| M8-Qwen-rerank-R1 | Done frozen v0.4 | I1 / R1 | Qwen embedding | Qwen `qwen3-rerank` | 20 | Strong generic neural rerank over flat cards. |
| M8-Qwen-rerank-R2 | Done frozen v0.4 | I3 / R2 | Qwen embedding | Qwen `qwen3-rerank` | 20 | Strong generic neural rerank over structured cards. |
| M8-Qwen-rerank-full | Done frozen v0.4 | I2 / RFULL | Qwen embedding | Qwen `qwen3-rerank` | 20 | Strong generic neural rerank over full skill docs. |
| M8-SkillRouter-rerank-full | Done frozen v0.4 | I2 / RFULL | SkillRouter embedding | SkillRouter reranker | 20 | Skill-specific retrieve-rerank baseline. |
| M8-SkillRouter-rerank-R1 | Done frozen v0.4 | I1 / R1 | SkillRouter embedding | SkillRouter reranker | 20 | Fair I1 skill-specific reranker comparison. |
| M8-SkillRouter-rerank-R2 | Done frozen v0.4 | I3 / R2 | SkillRouter embedding | SkillRouter reranker | 20 | Fair I3 skill-specific reranker comparison. |

## Frozen v0.4 Rerun Status

Current frozen version: `benchmark-v0.4-2026-06-16`.

I3M local paid-model feasibility status, 2026-06-18:

- Local full-library model-parsed I3M is complete for all 2433 skills, but it is DeepSeek/API-derived.
- Selector-facing artifact: `skill_benchmark/representations/I3M_model_parsed.jsonl`.
- QA/report files: `skill_benchmark/outputs/i3m/local_i3m_full_model_parse.jsonl`, `skill_benchmark/outputs/i3m/local_i3m_full_model_parse_report.md`, and `skill_benchmark/outputs/i3m/local_i3m_full_model_parse_report.summary.json`.
- Accepted pilot gate: 60 rows, 95.0% valid, 0 parse-failed rows, 99.3% exact evidence.
- Full local run: 2433 rows, 2333 valid rows (95.9%), 0 parse-failed rows, 1398 fallback rows, 54,989 extracted items, 98.7% exact evidence and 99.7% case-insensitive/whitespace-insensitive evidence.
- Checkpoint: `thesis_notes/checkpoints/methods/I3M Local Full-Library Parse Checkpoint - 2026-06-18.md`.
- Current decision: do not rely on I3M for headline results unless the cost/budget decision changes. The local thesis-facing next step is to produce a true local I3C artifact before rerunning local I3C comparisons.

External validation status, 2026-06-18:

- SkillRouter-Eval-Core downloaded into `skill_benchmark/external/skillrouter_eval_core/raw`.
- Easy/Hard public skill pools converted into I1/I2/I3H derived information-layer files in `skill_benchmark/external/skillrouter_eval_core/derived`.
- I3H parsing is chunked into 16 fixed blocks of up to 5,000 skills under `derived/i3_chunks`, so it can be resumed or replaced by a model-parsed I3M pass later.
- First disk-backed lexical external ablation has been run with SQLite FTS5 BM25 over I1, I2, and I3 for Easy and Hard. Report: `skill_benchmark/external/skillrouter_eval_core/outputs/skillrouter_eval_core_fts_information_layers.md`.
- Initial external result: I2 full body was strongest against I1/I3H; heuristic I3H improved over I1 on Hard Hit@1 but not on Recall@20 or FullCoverage@20. The later I3C V2 rerun supersedes this as the main external extracted-field result.

External I3M/I3C extraction status, 2026-06-21:

- DeepSeek/API I3M rows `0-2999` are complete as an extraction-quality pilot: 3000 deduplicated latest rows, 0 latest parse-failed rows, and 2997/3000 strict selector-valid rows after documented QA residues.
- ChatGPT/Codex I3C rows `3000-5999` are complete as a candidate practical extraction route after QA: 3000 rows, 0 parse failures, 0 missing skill ids, and 98.66% exact evidence-match after merge repair.
- Future ChatGPT/Codex I3C runs should use `skill_benchmark/extraction_prompts/I3C_SUBAGENT_EXTRACTION_V2.md`. V2 adds selector-usefulness checks and non-selector-visible QA metadata (`absent_fields`, `field_warnings`, `qa_warnings`) so sparse or generic skills are recorded honestly rather than overfilled.
- I3C V2 pilot on the first 200 rows of the SkillRouter top-20 task-relevant pool is complete: 2 subagents, 100 skills each, 200/200 merged rows, 0 parse failures, 0 missing skill ids, 1184/1184 exact evidence matches, and populated QA warnings. Status: pass with minor QA caveats. Checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 Pilot First 200 - 2026-06-19.md`.
- I3C V2 top-20 task-relevant pool extraction is complete: 3284/3284 rows, 33 subagent chunks, 0 parse failures, 0 missing skill ids, 0 duplicate skill ids, and 25544/25544 exact evidence matches after removing 27 heading-only evidence items into a cleaned canonical file. Use `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_top20_pool/I3C_V2_top20_pool_cleaned.jsonl` for the next fixed-candidate external retrieval run. Checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 Top20 Pool Extraction Checkpoint - 2026-06-19.md`.
- Full SkillRouter-Eval-Core I3C V2 extraction is complete over `all_I2.jsonl`, seeded from the cleaned top-20 I3C V2 pool. The cleaned canonical file has 79141/79141 rows, 0 parse failures, 0 missing skill ids, 0 duplicate skill ids, 498836/498836 exact evidence matches, and 0 heading-only evidence after removing 438 generic heading-only evidence items. Checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 Full-All Extraction Completion - 2026-06-20.md`.
- Full-tier external I3C FTS/BM25 retrieval has now been run. Report: `skill_benchmark/external/skillrouter_eval_core/outputs/skillrouter_eval_core_fts_information_layers_i3c_v2.md`. Easy I3C: 53.3% Hit@1, 0.586 MRR@10, 60.5% Recall@20, 44.0% FullCoverage@20. Hard I3C: 45.3% Hit@1, 0.527 MRR@10, 59.2% Recall@20, 40.0% FullCoverage@20.
- Checkpoints:
  - `thesis_notes/checkpoints/skillrouter/External SkillRouter I3M Partial Extraction Checkpoint - 2026-06-19.md`
  - `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C Subagent Parse Checkpoint - 2026-06-19.md`
  - `thesis_notes/checkpoints/skillrouter/External SkillRouter Task Coverage Checkpoint - 2026-06-19.md`
  - `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 Pilot First 200 - 2026-06-19.md`
  - `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 Top20 Pool Extraction Checkpoint - 2026-06-19.md`
  - `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 Full-All Extraction Completion - 2026-06-20.md`
  - `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 FTS Rerun - 2026-06-21.md`
- Do not use the older external I3M/I3C slices in retrieval result tables. The scored task gold skills are at rows `27018-27213`, outside the completed `0-5999` slices. The completed full-all I3C V2 artifact has now been evaluated as a full-tier FTS/BM25 condition; fixed-candidate top-20/top-50 reranking remains a separate candidate-universe experiment.
- I3C V2 is an I3 field layer only. It does not create I4 relation edges or I5 hierarchy/tree structure.

I3 extraction provenance status:

- Local controlled skills: mostly explicit author-provided sections, exported deterministically into R2/R3.
- Local public imported skills: heuristic extraction plus DeepSeek model-assisted field-presence verification, but the retrieval representation used in frozen-v0.4 is still heuristic/exported R2/R3.
- SkillRouter-Eval-Core: first pass is heuristic I3H only; no DeepSeek/Qwen/LLM call was used for external I3.
- Future paid-provider I3M runs should be optional only. The practical route is I3C using `I3C_SUBAGENT_EXTRACTION_V2`; any new I3M run must be labelled as paid-provider extraction and separated from I3C.

Completed result report:

- `skill_benchmark/outputs/frozen_v0_4_retrieval_matrix_summary.md`
- `skill_benchmark/outputs/frozen_v0_4_retrieval_matrix_summary.json`
- `skill_benchmark/outputs/frozen_v0_4_method_coverage_audit.md`
- `skill_benchmark/outputs/frozen_v0_4_information_layer_matrix.md`
- `skill_benchmark/outputs/frozen_v0_4_information_layer_matrix.json`
- `skill_benchmark/outputs/frozen_v0_4_failure_mode_comparison.md`

Completed in this rerun:

- Local offline selectors on controlled and public-gold: BM25, TF-IDF, MiniLM description/full/schema, and local schema-rerank variants.
- Qwen `text-embedding-v4` embedding-only retrieval over I1/R1, I3H/R2, and I2/full skill artifacts on controlled and public-gold after the public-original source correction.
- Qwen `qwen3-rerank` top-20 reranking over refreshed Qwen R1, R2, and full-skill candidates on controlled and public-gold.
- Local-schema top-20 reranking over refreshed Qwen R1, R2, and full-skill candidates on controlled and public-gold.
- Qwen-only M6-v2 field-specific `semantic_all` matching over refreshed Qwen top-20 first-stage candidates for I1/R1, I3H/R2, and I2/full artifacts on controlled and public-gold.
- Qwen-only fixed task-heavy and field-only M6-v2 reports regenerated from the refreshed field-specific component files.
- Crossed lexical representation controls: BM25 and TF-IDF have now been rerun over R1, R2, and full-skill text on controlled and public-gold after the 2026-06-23 public-original source correction and messier public-style controlled regeneration. Output: `skill_benchmark/outputs/frozen_v0_4_crossed_lexical_matrix.md`.
- Consolidated information-layer matrix regenerated on 2026-06-23. It groups I1/R1, I3/R2, and I2/full rows by method family, adds candidate recall@20, bootstrap top-1 confidence intervals where prompt-level rows exist, and paired McNemar tests for I1 vs I3 and I3 vs I2 under fixed methods.
- Compact refreshed matrix summary generated at `skill_benchmark/outputs/frozen_v0_4_refreshed_matrix_summary_2026_06_23.md`.
- First-pass failure-mode comparison generated on 2026-06-18 for the main R2/I3 comparisons: Qwen R2 + Qwen rerank, SkillRouter R2 + SkillRouter rerank, and SkillRouter R2 + M6-v1 on controlled and public-gold.
- M6-v2 blend calibration has been run with a finer score grid over existing candidate-level outputs. Output: `skill_benchmark/outputs/frozen_v0_4_m6v2_blend_sweep_fine.md`.
- M6-v2 explicit field-weight sweep has been run over saved field-specific component similarities. Output: `skill_benchmark/outputs/frozen_v0_4_m6v2_explicit_field_weight_sweep_narrow.md`.

SkillRouter frozen-v0.4 update, 2026-06-17:

- The first hosted SkillRouter frozen-v0.4 job completed all 12 R1/R2/full embedding and rerank conditions, but failed during final artifact upload because the job token lacked write permission.
- Summary metrics were recovered from the job logs and stored in `skill_benchmark/outputs/skillrouter_v0_4_2026_06_17_recovered_summary.md`.
- A safer retry job was submitted as `6a32a10ffb114ff24a388670`; it prints a summary after every condition and uploads compact summaries before the full archive.
- Treat SkillRouter metrics as usable for the representation matrix. Prompt-level SkillRouter artifacts have now been recovered, and working failure-mode reports are available under `skill_benchmark/outputs/failure_modes_skillrouter_v0_4_*.md`.
- Qwen `text-embedding-v4` embedding-only retrieval over I1/R1, I3/R2, and I2/full skill artifacts on controlled and public-gold.
- Qwen `qwen3-rerank` top-20 reranking over R1, R2, and full-skill candidates on controlled and public-gold.
- Local-schema top-20 reranking over Qwen R1, R2, and full-skill candidates on controlled and public-gold.
- M6-v1 lexical field-aware reranking with BM25-flat, TF-IDF-flat, TF-IDF-schema, Qwen-full, and SkillRouter top-20 first stages.
- Local field-ablation diagnostics on controlled and public-gold.

Not yet completed for frozen v0.4:

- True local frozen-v0.4 I3C extraction and reruns. The existing local `I3M_model_parsed` artifact is a paid DeepSeek attempt and should not be relabelled as I3C.
- Optional SkillRouter first-stage plus M6-v1 field-aware hybrid at top-100 budget, if a wider SkillRouter candidate artifact is generated.
- M4 tree routing and M5 graph retrieval.
- Full-scale M0 progressive disclosure and downstream task-success tests.
- Final thesis-selected statistical table integration. First-pass bootstrap top-1 confidence intervals and paired McNemar tests now exist in `frozen_v0_4_information_layer_matrix.*`.

Key frozen-v0.4 representation findings:

- Controlled Qwen embedding-only: R1 = 33.9% top-1, R2 = 40.4%, full skill = 42.4%.
- Controlled Qwen + Qwen-rerank top-20: R1 = 51.0% top-1, R2 = 58.4%, full skill = 62.9%.
- Public-gold Qwen embedding-only: R1 = 57.6% strict top-1, R2 = 61.8%, full skill = 70.8%.
- Public-gold Qwen + Qwen-rerank top-20: R1 = 73.6% strict top-1, R2 = 70.8%, full skill = 72.9%.
- Qwen-only M6-v2 fixed task-heavy top-1: controlled R1/R2/full = 35.5% / 38.4% / 40.8%; public-gold R1/R2/full = 54.9% / 56.9% / 59.7%.
- M6-v1 field-aware top-100 controlled best field set (`core_boundary`) = 64.5% top-1, 91.4% top-5, but this is a larger candidate-budget diagnostic rather than a direct top-20 reranker comparison.
- After the local first-stage audit, best controlled M6-v1 local result is TF-IDF/schema + `core_boundary` at top-20: 69.8% top-1, 97.1% top-5, 0.818 MRR. Best public-gold M6-v1 local result is TF-IDF/flat + `task` at top-20: 68.1% strict top-1, 87.5% top-5, 0.763 MRR.
- Current local schema/M6-v1 methods should be described as lexical field-aware prototypes. Their public-gold weakness motivates M6-v2 semantic field matching.
- M6-v2 is deliberately a no-rewrite method for the main thesis comparison. It embeds the raw user request, compares it against selector-visible skill fields, and uses explicit lexical cues only to gate or penalize fields. It must not infer missing workflow steps, hidden user intent, optionality, or requirements not present in the request. Any LLM query parser or rewrite variant must be reported separately as a query-understanding ablation, not as the main field-representation result.
- Initial M6-v2 results are mixed. On Qwen candidates, M6-v2 task-only gives small improvements over Qwen embedding-only in several rows but is far below Qwen learned reranking. On SkillRouter candidates, M6-v2 task is competitive on public-gold but does not beat SkillRouter learned reranking on controlled R2/full. Extra no-rewrite fields often hurt, so M6-v2 currently supports the claim that fields require selective use, not that all structured fields should be added as positive evidence.
- Current M6-v2 summary reports:
- `skill_benchmark/outputs/frozen_v0_4_qwen_m6v2_comparison.md`
- `skill_benchmark/outputs/frozen_v0_4_skillrouter_m6v2_comparison.md`
- `skill_benchmark/outputs/frozen_v0_4_m6v2_blend_sweep_fine.md`
- `skill_benchmark/outputs/frozen_v0_4_m6v2_explicit_field_weight_sweep_narrow.md`
- `skill_benchmark/outputs/frozen_v0_4_m6v2_explicit_field_weight_sweep_r2_focused.md`
- `skill_benchmark/outputs/frozen_v0_4_m6v2_fixed_global_core.md`
- `skill_benchmark/outputs/frozen_v0_4_m6v2_fixed_global_core_field_only.md`
- `skill_benchmark/outputs/frozen_v0_4_m6v2_internal_weight_ablation_fixed.md`
- `skill_benchmark/outputs/frozen_v0_4_m6v2_internal_weight_ablation_fixed_detailed.md`
- `skill_benchmark/outputs/frozen_v0_4_m6v2_fixed_task_heavy.md`
- `skill_benchmark/outputs/frozen_v0_4_m6v2_fixed_task_heavy_field_only.md`

Crossed lexical representation audit, refreshed 2026-06-23:

- Controlled BM25 top-1: R1 = 55.1%, R2 = 58.0%, full = 66.5%. Candidate recall@20 rises from 93.9% on R1 to 98.0% on R2 and 98.4% on full.
- Controlled TF-IDF top-1: R1 = 52.6%, R2 = 59.6%, full = 69.4%. Candidate recall@20 rises from 91.4% on R1 to 95.5% on R2 and 97.5% on full.
- Public-gold BM25 top-1: R1 = 55.6%, R2 = 54.9%, full = 59.0%; R2 improves candidate recall@20 to 97.2% from R1's 87.5%, while full reaches 99.3%.
- Public-gold TF-IDF top-1: R1 = 56.9%, R2 = 50.7%, full = 48.6%; R2 still improves candidate recall@20 over R1 (94.4% vs 92.4%), while full reaches 96.5%.
- Interpretation: after the public-original and messier public-style controlled corrections, full text is a strong lexical comparator rather than a weak baseline. R2/I3H still improves shortlist recall over R1 in most rows, but final top-1 depends on method and corpus. Final tables must report candidate recall, selector-visible tokens, and fixed/preprocessing cost as well as top-1.

M6-v2 fine blend calibration, 2026-06-18:

- The finer sweep varies `base_weight` in 0.05 increments and penalty scale in 0.25 increments, without new API calls.
- On Qwen candidates, field-heavy blends improve public-gold R2 to 69.4% strict top-1 in the full sweep and 66.7% held-out test top-1 under the deterministic dev-selected split.
- On SkillRouter controlled candidates, the best or dev-selected weights often stay close to first-stage-heavy. This means M6-v2 field scoring is not uniformly better than a strong skill-specific first stage.
- Treat tuned M6-v2 as a diagnostic of field signal and calibration sensitivity, not as a final learned reranker. Any headline use must rely on dev/test or cross-validation, not full-set tuned weights.

M6-v2 explicit field-use tuning, 2026-06-18:

- The field-specific variant compares request-side task/input/output/workflow/dependency spans only against the corresponding skill-side fields. It does not rewrite the query or invent missing requirements.
- The narrow explicit weight sweep recomputes field scores from saved component similarities, so it does not make new embedding API calls.
- A focused R2 sweep was added after the narrow all-representation sweep. It uses cue-gated activation, base weights from 0.00 to 1.00 around useful regions, and penalty scales 0.00/0.25/0.50. Output: `skill_benchmark/outputs/frozen_v0_4_m6v2_explicit_field_weight_sweep_r2_focused.md`.
- R2 controlled results remain modest: Qwen R2 full-set best is 41.6% top-1 and dev-selected held-out top-1 is 40.7%; SkillRouter R2 full-set best is 66.1% top-1 and dev-selected held-out top-1 is 63.6%.
- R2 public-gold results are stronger but calibration-sensitive: Qwen R2 full-set best is 68.8% strict top-1 and held-out top-1 is 66.7%; SkillRouter R2 full-set best is 76.4% strict top-1 and held-out top-1 is 71.8%.
- The main methodological lesson is not "all fields improve retrieval". Current M6-v2 still often chooses task-only or first-stage-heavy settings. This supports the next improvement target: better field activation, mismatch handling, and validation-selected weights.

M6-v2 fixed global policy, refreshed Qwen-only on 2026-06-23:

- Use this as the thesis-facing fixed M6-v2 method rather than per-row tuned weights.
- Score blend: 0.30 first-stage score + 0.70 semantic-field score + 0.25 penalty/bonus adjustment.
- Field set: `semantic_all`, with cue-gated activation.
- Internal field weights after fixed-method ablation: task/use 0.50, output/artifact 0.20, workflow/procedure 0.15, input/precondition 0.10, dependency/resource 0.05.
- Refreshed Qwen-only R2 fixed task-heavy results: controlled 38.4% top-1, public-gold 56.9% top-1.
- Refreshed Qwen-only full-document fixed task-heavy results: controlled 40.8% top-1, public-gold 59.7% top-1.
- The field-only sensitivity report with base weight 0.00 is regenerated for Qwen only and remains a diagnostic; do not mix it with older SkillRouter M6-v2 fixed rows.
- Earlier SkillRouter M6-v2 fixed task-heavy rows are historical until a corrected-source SkillRouter local rerun is performed.

## Fair Comparison Rules

1. Model-only comparison: representation, prompt stratum, skill library scale, candidate budget, and reranker type must match.
2. Information-layer comparison: model, prompt stratum, skill library scale, candidate budget, and reranker type must match. Use this for `I1` vs `I2` vs `I3` claims.
3. Reranker-only comparison: first-stage retriever, representation, prompt stratum, candidate set size, and candidate text must match.
4. Controlled and public-gold must be reported separately before any combined score.
5. Top-20 rerankers should be compared against top-20 rerankers. Top-100 results are larger-budget trade-off conditions, not direct wins over top-20 systems.
6. Report candidate recall before reranking whenever using M6/M8. A failure can be caused by the first-stage retriever or by the reranker.
7. Acceptable alternatives and strict gold labels are separate scoring rules. Report both when available.
8. Query rewriting is a separate factor. If a method rewrites or expands the request into structured requirements, it cannot be compared as a pure representation-layer or reranker-only comparison against no-rewrite methods.
9. Relation/hierarchy comparisons must state how `I4/I5` information was converted for each method. A graph can consume edges directly; an embedding model can only consume relation information if it is serialized into text or converted into learned features.
10. Cost claims must specify which costs are included: indexing/extraction, first-stage retrieval, graph/tree traversal, reranking, API calls, token/context cost, and full-doc hydration.

## M6-v2 Semantic Field Matcher Design

Purpose:

- Test whether the information exposed by structured skill fields is useful when exploited semantically rather than through lexical overlap.
- Keep the first-stage candidate set fixed so that changes in performance can be attributed to reranking behavior.
- Avoid query-rewrite bias in the main comparison.

Main method:

- The I3 information layer exposes the existing fields: task/use conditions, inputs/preconditions, outputs, workflow/procedure, dependencies/resources, and boundaries/not-for conditions.
- In thesis prose, call this the I3 structured information layer. The implementation may still use R2/R3 artifacts.
- The reranker embeds the raw user request with Qwen `text-embedding-v4`.
- Each candidate skill field is embedded separately. Multi-item fields such as workflow steps are chunked and compared by max or top-k average similarity rather than summed, so longer skills are not rewarded merely for containing more text.
- Positive fields are combined with fixed weights, normalized over active fields. Active fields are detected only from explicit lexical cues in the raw request. The method does not invent procedure steps from an underspecified prompt.
- Boundaries and negative-use cases are treated mainly as penalties. A skill whose `not_for` text semantically matches the positive request is penalized. If the request explicitly excludes something and the skill boundary also excludes it, that can reduce the penalty or add a small alignment bonus.
- Final score blends normalized first-stage score with normalized semantic field score, then subtracts explicit mismatch penalties. The implementation can sweep this blend; the old conservative default was `0.70` first-stage and `0.30` semantic-field, but frozen-v0.4 calibration shows the best weight depends on the first-stage source and representation. Use dev/test-selected or cross-validated weights for any thesis-facing tuned result. Do not choose field-heavy weights on the full evaluation set and report them as final performance.

Initial fixed weights:

| Field | Weight | Notes |
|---|---:|---|
| Task/use condition | 0.35 | Always active; captures broad intent without rewriting. |
| Output | 0.25 | Active only when the raw request explicitly cues an artifact, format, answer, summary, patch, table, etc. |
| Input/precondition | 0.15 | Active only when the raw request explicitly mentions an input/source type such as PDF, repo, screenshot, API, CSV, or URL. |
| Workflow/procedure | 0.15 | Active only when the raw request explicitly cues an operation such as audit, verify, debug, inspect, ground, compare, or validate. |
| Dependency/resource | 0.10 | Active only when the raw request names a tool, platform, provider, library, API, or resource. |

Do not claim M6-v2 is a learned reranker. It is a semantic, field-aware scoring prototype that tests whether explicit skill information can be used more robustly than M6-v1 lexical matching.

## Canonical Commands

Run from repository root:

```bash
cd "/Users/jackyzhang/Work/Honour Thesis"
```

Environment:

```bash
# Required for Qwen/DashScope-backed provider runs.
# The scripts read this automatically with --dotenv .env.
DASHSCOPE_API_KEY=...

# Required only for hosted/local Hugging Face model access or jobs.
HF_TOKEN=...
```

## Execution Venues and Run Boundaries

Use this table before starting or interpreting a run. The execution venue is part of the method record because otherwise we can accidentally mix a small local smoke test with a full hosted model run.

| Experiment family | Correct execution venue | Why | Output / audit location | Hard rule |
|---|---|---|---|---|
| Local validation, representation export, BM25/TF-IDF, SQLite FTS, aggregation, LaTeX/PDF rebuild | Local Mac / repo checkout | These are CPU/file operations and should be reproducible without paid model runtime. | `skill_benchmark/outputs`, `skill_benchmark/external/skillrouter_eval_core/outputs`, `thesis_latex/main.pdf` | OK to run locally. Record command and benchmark version. |
| Qwen embedding and Qwen rerank matrix | Local orchestration calling DashScope/Qwen APIs | The local process submits remote provider API calls and caches outputs; model compute is not local. | Provider output JSON/MD under `skill_benchmark/outputs`; cache under provider cache paths. | Requires `DASHSCOPE_API_KEY`; label as provider/API cost, not local model inference. |
| DeepSeek/API I3M extraction | Local orchestration calling paid provider API | This is a paid-provider feasibility/pass attempt for model-parsed I3, not the thesis-facing I3C route. | `skill_benchmark/outputs/i3m`, `skill_benchmark/representations/I3M_model_parsed.jsonl` | Never relabel I3M as I3C. |
| ChatGPT/Codex I3C extraction | Codex subagents using assigned artifact text only | This is the practical thesis-facing I3 extraction route; workers do not call external APIs and must validate exact evidence substrings. | `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_*`, checkpoints under `thesis_notes/checkpoints/skillrouter` | Use `I3C_SUBAGENT_EXTRACTION_V2.md`; record chunk manifests and QA. |
| SkillRouter local smoke test | Local Mac only on tiny subset | Confirms code path and model loading; not a result row. | Explicit smoke-test outputs only. | Must use `--skill-subset-from-prompts`, small `--max-prompts`, and be labelled `smoke`. Never report as full matrix evidence. |
| SkillRouter full local frozen-v0.4 matrix | Hugging Face Jobs GPU or equivalent hosted GPU | The released SkillRouter embedder/reranker are 0.6B-class models and full-scale runs should not execute on the 8 GB laptop. | Hosted-job artifacts recovered/uploaded to `skill_benchmark/outputs` or a Hub dataset. | Do not run full SkillRouter matrix locally. |
| External SkillRouter-Eval-Core SkillRouter neural matrix | Hugging Face Jobs GPU | The external matrix encodes about 78k-79k skills per tier across I1/I2/I3C and uses the released SkillRouter embedder/reranker. | Dataset repo `baechuer1/honour-thesis-skillrouter-benchmark-snapshot`; result prefix `skillrouter_eval_core_skillrouter_neural_i3c_v2` | Package a snapshot, submit via `hf_jobs`, and persist results back to Hub. |
| M4/M5 graph/tree probes | Local first, then hosted only if scale requires | Planned architecture probes; execution venue depends on implementation. | Future R4/R5 outputs and experiment reports. | Do not treat planned graph/tree methods as completed I3 results. |

Corrected remote SkillRouter-Eval-Core neural matrix run, launched 2026-06-21 and then cancelled:

- Corrected job: `6a3773a1953ed90bfb9469b7`
- Job URL: `https://huggingface.co/jobs/baechuer1/6a3773a1953ed90bfb9469b7`
- Final status: cancelled to stop Hugging Face GPU spend.
- Venue: Hugging Face Jobs `l4x1`, timeout `24h`, CUDA required.
- Snapshot source: `baechuer1/honour-thesis-skillrouter-benchmark-snapshot/skillrouter_eval_core_i3c_v2_neural_matrix_snapshot_2026_06_21.tar.gz`
- Corrected runner artifact: `job_scripts/run_skillrouter_eval_core_skillrouter_matrix_corrected_2026_06_21.py`
- Matrix: Easy/Hard x I1/FULL/I3C x SkillRouter embedding only / SkillRouter embedding top-20 -> SkillRouter rerank.
- Representation serialization: I1 = `name | description`; FULL = `name | description | body`; I3C = `name | description | cleaned I3C fields`.
- Model caps: embedding max length `4096`, reranker max length `4096`.
- Expected result directory on Hub: `results/skillrouter_eval_core_i3c_v2_neural_matrix_corrected_4096_2026_06_21`
- Checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 Corrected Neural Matrix HF Job Launch - 2026-06-21.md`
- Partial recovery checkpoint: `thesis_notes/checkpoints/skillrouter/External SkillRouter I3C V2 Corrected Neural Matrix Cancelled Partial - 2026-06-21.md`

Previous neural job `6a373487953ed90bfb94663e` is diagnostic only. Do not use it for final thesis claims because it used the older derived `I2` serialization and 2048-token caps.

Current next-run rule: split paid external SkillRouter neural jobs by expensive representation. Do not launch paid Hugging Face neural jobs with `--quiet-progress`; the logs must show the active tier, representation, mode, and batch/checkpoint progress so the job can be stopped or continued based on observed stage rather than guesswork.

Remaining-I1/I3C neural run `6a37bdd33093dba73ce2b559` failed after completing `easy_I3C_embedding` because direct Hub upload returned `403` and requested `create_pr=1`. Recovered log row: Easy/I3C embedding Hit@1 45.3%, MRR@10 0.525, Recall@20 55.1%, FullCov@20 37.3%.

Grouped replacement job `6a37c2b63093dba73ce2b58d` (`l4x1`, timeout `8h`) completed `easy_I3C`, `hard_I1`, and `hard_I3C` as grouped embedding+rerank subprocesses. Hub uploads failed with `403`, but metrics are recoverable from logs. Recovered rows: Easy/I1 embedding 49.3% Hit@1 / 0.568 MRR@10; Easy/I1 rerank 57.3% / 0.622; Easy/I3C embedding 45.3% / 0.525; Easy/I3C rerank 57.3% / 0.630; Hard/I1 embedding 44.0% / 0.535; Hard/I1 rerank 52.0% / 0.581; Hard/I3C embedding 37.3% / 0.477; Hard/I3C rerank 48.0% / 0.563.

Cancelled I2/full-document baseline: Hugging Face job `6a37cf7f953ed90bfb946ea4` was stopped because it used a 4096-token cap and is invalid as a full-context/full-document comparator. The replacement I2 run should use the SkillRouter embedder's model-limit context (`32768`) and reranker's model-limit context (`40960`) rather than the older 4096 cap. Local exact-token checks show the current external I2 full documents fit under the embedder limit.

Cancelled I3C full-context rerun: Hugging Face job `6a37d2413093dba73ce2b60b` was stopped before any condition completed because its condition loop obscured progress and risked avoidable repeated first-stage work. Do not report rows from this job.

Completed I3C full-context shared-embedding rerun: Hugging Face job `6a37d3a23093dba73ce2b60e` (`l4x1`) reran Easy and Hard `I3C` as SkillRouter embedding and embedding+rerank with quiet progress disabled. It used model-limit context (`32768` for the embedder, `40960` for the reranker), chunked overlength serialized I3C documents, aggregated chunk scores by max so no I3C content was silently dropped, and shared the first-stage embedding retrieval per tier between the embedding-only and rerank rows. Recovered rows: Easy/I3C embedding 46.7% Hit@1 / 0.531 MRR@10 / 55.1% Recall@20 / 37.3% FullCov@20; Easy/I3C rerank 57.3% / 0.631 / 55.1% / 37.3%; Hard/I3C embedding 37.3% / 0.477 / 53.7% / 37.3%; Hard/I3C rerank 48.0% / 0.563 / 53.7% / 37.3%. Summary files: `skill_benchmark/external/skillrouter_eval_core/outputs/skillrouter_eval_core_skillrouter_neural_i3c_fullcontext_shared_2026_06_21_recovered_summary.md` and `.json`.

Re-export representation components after changing skills:

```bash
python3 skill_benchmark/scripts/export_skill_representations.py
python3 skill_benchmark/scripts/analyze_representation_coverage.py
```

Validate controlled benchmark construction:

```bash
python3 skill_benchmark/scripts/validate_benchmark_integrity.py \
  --output-md skill_benchmark/outputs/benchmark_integrity_report.md \
  --output-json skill_benchmark/outputs/benchmark_integrity_report.json

python3 skill_benchmark/scripts/analyze_procedural_distinctness.py \
  --output-md skill_benchmark/outputs/procedural_distinctness_report.md \
  --output-json skill_benchmark/outputs/procedural_distinctness_report.json

python3 skill_benchmark/scripts/analyze_semantic_confusability.py \
  --output-md skill_benchmark/outputs/semantic_confusability_report_minilm_2401.md \
  --output-json skill_benchmark/outputs/semantic_confusability_report_minilm_2401.json

python3 skill_benchmark/scripts/analyze_prompt_leakage.py \
  --output-md skill_benchmark/outputs/prompt_leakage_report.md \
  --output-json skill_benchmark/outputs/prompt_leakage_report.json
```

Run local offline selector baselines on controlled prompts:

```bash
python3 skill_benchmark/scripts/run_offline_selectors.py \
  --prompts "skill_benchmark/prompts/*.json" \
  --scales current_full \
  --methods m1_bm25_flat,m1_tfidf_flat,m3_tfidf_schema,m6_bm25_schema_rerank,m6_tfidf_schema_rerank \
  --rerank-candidates 100 \
  --output-md skill_benchmark/outputs/offline_selector_evaluation_2433_201_local.md \
  --output-json skill_benchmark/outputs/offline_selector_evaluation_2433_201_local.json
```

Run crossed lexical representation controls:

```bash
python3 skill_benchmark/scripts/run_crossed_lexical_representations.py \
  --scale current_full \
  --representations r1,r2,full \
  --retrievers bm25,tfidf \
  --ranking-limit 100 \
  --output-md skill_benchmark/outputs/frozen_v0_4_crossed_lexical_matrix.md \
  --output-json skill_benchmark/outputs/frozen_v0_4_crossed_lexical_matrix.json
```

Run Qwen embedding-only controlled RFULL:

```bash
python3 skill_benchmark/scripts/run_provider_selectors.py \
  --dotenv .env \
  --prompts "skill_benchmark/prompts/*.json" \
  --scale current_full \
  --embedding-provider qwen \
  --embedding-model text-embedding-v4 \
  --embedding-representation full \
  --reranker-provider none \
  --output-md skill_benchmark/outputs/provider_selector_qwen_2401_137_full_embedding.md \
  --output-json skill_benchmark/outputs/provider_selector_qwen_2401_137_full_embedding.json
```

Run Qwen full embedding plus Qwen reranker controlled:

```bash
python3 skill_benchmark/scripts/run_provider_selectors.py \
  --dotenv .env \
  --prompts "skill_benchmark/prompts/*.json" \
  --scale current_full \
  --embedding-provider qwen \
  --embedding-model text-embedding-v4 \
  --embedding-representation full \
  --reranker-provider qwen \
  --reranker-model qwen3-rerank \
  --rerank-candidates 20 \
  --output-md skill_benchmark/outputs/provider_selector_qwen_2401_137_full_qwen_rerank_top20.md \
  --output-json skill_benchmark/outputs/provider_selector_qwen_2401_137_full_qwen_rerank_top20.json
```

Run Qwen R1/R2 public-gold variants:

```bash
for rep in r1 r2 full; do
  python3 skill_benchmark/scripts/run_provider_selectors.py \
    --dotenv .env \
    --prompts "skill_benchmark/prompts_public_gold/*.json" \
    --scale current_full \
    --embedding-provider qwen \
    --embedding-model text-embedding-v4 \
    --embedding-representation "$rep" \
    --acceptable-alternatives skill_benchmark/annotations/public_gold_acceptable_alternatives.json \
    --reranker-provider none \
    --output-md "skill_benchmark/outputs/provider_selector_qwen_public_gold_120_${rep}_embedding.md" \
    --output-json "skill_benchmark/outputs/provider_selector_qwen_public_gold_120_${rep}_embedding.json"

  python3 skill_benchmark/scripts/run_provider_selectors.py \
    --dotenv .env \
    --prompts "skill_benchmark/prompts_public_gold/*.json" \
    --scale current_full \
    --embedding-provider qwen \
    --embedding-model text-embedding-v4 \
    --embedding-representation "$rep" \
    --acceptable-alternatives skill_benchmark/annotations/public_gold_acceptable_alternatives.json \
    --reranker-provider qwen \
    --reranker-model qwen3-rerank \
    --rerank-candidates 20 \
    --output-md "skill_benchmark/outputs/provider_selector_qwen_public_gold_120_${rep}_qwen_rerank_top20.md" \
    --output-json "skill_benchmark/outputs/provider_selector_qwen_public_gold_120_${rep}_qwen_rerank_top20.json"
done
```

Run Qwen first-stage plus M6-v1 local field-aware reranker:

```bash
python3 skill_benchmark/scripts/run_m6v1_field_aware_reranker.py \
  --dotenv .env \
  --prompts "skill_benchmark/prompts/*.json" \
  --scale current_full \
  --first-stage qwen_full \
  --rerank-candidates 100 \
  --field-sets task,task_output_workflow,core,core_boundary,all \
  --output-md skill_benchmark/outputs/m6v1_qwen_full_field_aware.md \
  --output-json skill_benchmark/outputs/m6v1_qwen_full_field_aware.json
```

Run M6-v2 blend calibration over existing candidate-level outputs:

```bash
python3 skill_benchmark/scripts/sweep_m6v2_blends.py \
  --base-weights 0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0 \
  --penalty-scales 0,0.25,0.5,0.75,1.0 \
  --output-md skill_benchmark/outputs/frozen_v0_4_m6v2_blend_sweep_fine.md \
  --output-json skill_benchmark/outputs/frozen_v0_4_m6v2_blend_sweep_fine.json
```

Run M6-v2 field-specific reranking for one fixed candidate source:

```bash
python3 skill_benchmark/scripts/run_m6v2_semantic_field_reranker.py \
  --source-json skill_benchmark/outputs/frozen_v0_4_controlled_qwen_r2_embedding.json \
  --query-field-mode field_specific \
  --rerank-candidates 20 \
  --output-md skill_benchmark/outputs/frozen_v0_4_controlled_qwen_r2_m6v2_field_specific_top20.md \
  --output-json skill_benchmark/outputs/frozen_v0_4_controlled_qwen_r2_m6v2_field_specific_top20.json
```

Run M6-v2 explicit field-weight sweep over saved field-specific component scores:

```bash
python3 skill_benchmark/scripts/sweep_m6v2_explicit_field_weights.py \
  --base-weights 0,0.25,0.5,0.75,1 \
  --penalty-scales 0,0.5 \
  --activation-policies cue_gated \
  --output-md skill_benchmark/outputs/frozen_v0_4_m6v2_explicit_field_weight_sweep_narrow.md \
  --output-json skill_benchmark/outputs/frozen_v0_4_m6v2_explicit_field_weight_sweep_narrow.json
```

Run focused R2 M6-v2 explicit field-weight calibration:

```bash
python3 skill_benchmark/scripts/sweep_m6v2_explicit_field_weights.py \
  --only-reps r2 \
  --base-weights 0,0.1,0.2,0.25,0.3,0.4,0.5,0.6,0.7,0.75,0.8,0.9,1.0 \
  --penalty-scales 0,0.25,0.5 \
  --activation-policies cue_gated \
  --output-md skill_benchmark/outputs/frozen_v0_4_m6v2_explicit_field_weight_sweep_r2_focused.md \
  --output-json skill_benchmark/outputs/frozen_v0_4_m6v2_explicit_field_weight_sweep_r2_focused.json
```

Run SkillRouter locally only for smoke tests; full-scale local runs are currently impractical on the 8 GB laptop:

```bash
python3 skill_benchmark/scripts/run_skillrouter_selectors.py \
  --prompts "skill_benchmark/prompts/*.json" \
  --scale current_full \
  --skill-subset-from-prompts \
  --embedding-representation full \
  --rerank-candidates 20 \
  --max-prompts 5 \
  --device cpu \
  --output-md skill_benchmark/outputs/skillrouter_smoke_full.md \
  --output-json skill_benchmark/outputs/skillrouter_smoke_full.json
```

Hosted SkillRouter full-scale runs should use the same script in a Hugging Face Job or another GPU environment. The frozen-v0.4 R1/R2/full embedding and rerank runs are complete; the commands below are templates for rerun/reproduction, not missing work:

```bash
# Controlled and public-gold, both R1 and R2:
python3 skill_benchmark/scripts/run_skillrouter_selectors.py \
  --prompts "skill_benchmark/prompts/*.json" \
  --scale current_full \
  --embedding-representation r2 \
  --rerank-candidates 20 \
  --device cuda \
  --output-md skill_benchmark/outputs/skillrouter_controlled_r2_rerank_top20.md \
  --output-json skill_benchmark/outputs/skillrouter_controlled_r2_rerank_top20.json

python3 skill_benchmark/scripts/run_skillrouter_selectors.py \
  --prompts "skill_benchmark/prompts_public_gold/*.json" \
  --scale current_full \
  --embedding-representation r2 \
  --acceptable-alternatives skill_benchmark/annotations/public_gold_acceptable_alternatives.json \
  --rerank-candidates 20 \
  --device cuda \
  --output-md skill_benchmark/outputs/skillrouter_public_gold_120_r2_rerank_top20.md \
  --output-json skill_benchmark/outputs/skillrouter_public_gold_120_r2_rerank_top20.json
```

## Key Results Snapshot

Use this only as a quick orientation. For final writing, regenerate tables from JSON artifacts or hosted-job summaries.

Active frozen-v0.4 results:

- Main matrix: `skill_benchmark/outputs/frozen_v0_4_information_layer_matrix.md`
- Failure companion: `skill_benchmark/outputs/frozen_v0_4_failure_mode_comparison.md`
- Active prompt counts: 245 controlled, 144 public-gold, 12 low-information stress prompts.
- Active comparable information layers: I1/R1 flat card, I3/R2 structured fields, and I2/full `SKILL.md`.

The older tables below are retained as historical development checkpoints.

### Historical controlled, 201 prompts

| Method | Representation | Top-1 | Accept top-1 | Top-5 | MRR | Caveat |
|---|---|---:|---:|---:|---:|---|
| M1 BM25 flat | R1 | 61.7% | n/a | 88.1% | 0.727 | Historical 2433/201 local rerun. |
| M1 TF-IDF flat | R1 | 55.2% | n/a | 86.1% | 0.689 | Historical 2433/201 local rerun. |
| M3 TF-IDF schema | R2/R3 serialized | 65.2% | n/a | 94.0% | 0.778 | Historical 2433/201 local rerun. |
| M6 BM25 schema rerank | R1 first stage, R2/R3 rerank | 65.7% | n/a | 93.5% | 0.781 | Historical 2433/201 local diagnostic, top-100. |
| M6 TF-IDF schema rerank | R1 first stage, R2/R3 rerank | 65.7% | n/a | 91.5% | 0.773 | Historical 2433/201 local diagnostic, top-100. |
| M6-v1 TF-IDF field-aware | R1 first stage, R2/R3 rerank | 72.6% | n/a | 94.0% | 0.824 | Historical 2433/201 local prototype, best `core`/`core_boundary`, top-100. |
| M6-v1 BM25 field-aware | R1 first stage, R2/R3 rerank | 72.1% | n/a | 95.0% | 0.825 | Historical 2433/201 local prototype, best `core_boundary`, top-100. |
| Qwen embedding | RFULL | 52.5% | 53.3% | 73.7% | 0.617 | Full-document embedding only. |
| Qwen embedding + Qwen rerank | RFULL | 62.0% | 65.0% | 75.2% | 0.684 | Top-20 neural rerank. |
| Qwen embedding + local schema rerank | RFULL first stage, R1/R2/R3 rerank | 77.4% | 77.4% | 91.2% | 0.840 | Top-100 larger-budget diagnostic. |
| SkillRouter embedding | RFULL | 73.0% | 75.9% | 94.2% | 0.827 | Hosted GPU summary. |
| SkillRouter embedding + SkillRouter rerank | RFULL | 83.2% | 83.2% | 97.8% | 0.898 | Hosted GPU summary, top-20. |
| SkillRouter embedding + M6-v1 local | RFULL first stage, R1/R2/R3 rerank | 86.9% | 86.9% | 98.5% | 0.927 | Hosted GPU summary, top-100. |

### Public-gold, historical 82 prompts

| Method | Representation | Top-1 | Accept top-1 | Top-5 | MRR | Caveat |
|---|---|---:|---:|---:|---:|---|
| Qwen embedding | R1 | 62.2% | 72.0% | 84.2% | 0.720 | Public-only current R1 run. |
| Qwen embedding + Qwen rerank | R1 | 74.4% | 85.4% | 96.3% | 0.837 | Public-only current R1 run. |
| Qwen embedding | R2 | 59.8% | 73.2% | 82.9% | 0.714 | Public-only current R2 run. |
| Qwen embedding + Qwen rerank | R2 | 76.8% | 90.2% | 100.0% | 0.861 | Best current public-gold result; not directly comparable to SkillRouter full. |
| Qwen embedding | RFULL | 31.7% | 50.0% | 58.5% | 0.448 | Full public artifacts are noisy for direct Qwen embedding. |
| Qwen embedding + Qwen rerank | RFULL | 68.3% | 79.3% | 80.5% | 0.739 | Fairer full-representation comparison to SkillRouter full. |
| SkillRouter embedding | RFULL | 68.3% | 79.3% | 95.1% | 0.790 | Hosted 82-case result recorded in notes, not local JSON artifact. |
| SkillRouter embedding + SkillRouter rerank | RFULL | 64.6% | 73.2% | 92.7% | 0.778 | Reranker did not improve public-gold top-1. |
| SkillRouter embedding + M6-v1 local | RFULL first stage, R1/R2/R3 rerank | 68.3% | 78.1% | 90.2% | 0.788 | Field matcher weak on public-gold. |

The active public-gold stratum now has 144 prompts. Treat all 82-prompt public-gold selector results above as historical; frozen-v0.4 public-gold results are reported in `thesis_latex/chapters/06_results.tex` and the frozen-v0.4 output files.

### Weighted combined, 219 prompts

Historical weighted view from the 137 controlled + 82 public-gold checkpoint. Do not use it for active claims; use the frozen-v0.4 information-layer matrix instead.

| Method | Representation | Top-1 | Accept top-1 | Top-5 | MRR |
|---|---|---:|---:|---:|---:|
| Qwen embedding | RFULL | 44.7% | 52.1% | 68.0% | 0.554 |
| Qwen embedding + Qwen rerank | RFULL | 64.4% | 70.3% | 77.2% | 0.705 |
| Qwen embedding + local schema rerank | RFULL first stage, R1/R2/R3 rerank | 58.0% | 65.8% | 84.0% | 0.695 |
| SkillRouter embedding | RFULL | 71.2% | 77.2% | 94.5% | 0.813 |
| SkillRouter embedding + SkillRouter rerank | RFULL | 76.2% | 79.5% | 95.9% | 0.853 |
| SkillRouter embedding + M6-v1 local | RFULL first stage, R1/R2/R3 rerank | 79.9% | 83.6% | 95.4% | 0.875 |

## Open Experiment Gaps

Priority gaps before final claims:

The crossed I1/I2/I3 information-layer-by-architecture matrix is now complete for the audited frozen-v0.4 method families. The remaining work is hardening and interpretation, not broad rerunning.

1. Decide how much of the information-layer matrix and SkillRouter failure-mode analysis to incorporate into the thesis body.
2. Decide whether to generate a wider SkillRouter top-100 first-stage artifact for a larger-budget M6-v1 trade-off condition.
3. Build exact combined prompt file or combined report generator; current combined values are weighted aggregates.
4. Add per-cluster and per-source-family failure analysis, especially for public-gold.
5. Add further controlled or public-gold cases only in a cluster-balanced way after validation, because the current evaluated pool already has 389 controlled + public-gold prompts. Each added public cluster must have a public gold skill and 2-4 plausible alternatives drawn from public, controlled, or background skills.
6. Harden M6-v2 semantic field matching. The initial no-rewrite implementation is done, but it needs failure analysis, weight/penalty calibration on a held-out development split, and possibly a separate query-parser ablation before it can be treated as a final method.
7. Decide whether M4 tree and M5 graph are final experiment families or thesis discussion/proposed future work.
8. Add cost/latency/token reporting for top-20, top-50, and top-100 budgets.
9. Integrate first-pass paired tests and confidence intervals into the thesis results chapter, then decide whether extra paired bootstrap tests for MRR/top-k are needed for the final selected comparisons.
10. For SkillRouter-Eval-Core external validation, do not run headline I3M/I3C retrieval from the older partial extraction slices. The completed I3M rows `0-2999` and I3C rows `3000-5999` do not overlap the scored-task gold rows (`27018-27213`). The full `all_I2.jsonl` I3C V2 artifact has now been evaluated as a full-tier FTS/BM25 condition in `skillrouter_eval_core_fts_information_layers_i3c_v2.*`. Fixed-candidate top-20/top-50 evaluation can still be reported separately from full-library evaluation.
    - Prepared candidate pools from existing full-library BM25 rankings over I1/I2/I3H plus all gold skills:
      - top-20 union + gold: 3284 skills, `skill_benchmark/external/skillrouter_eval_core/derived/representations/skillrouter_task_relevant_pool_top20_I2.jsonl`;
      - top-50 union + gold: 7113 skills, `skill_benchmark/external/skillrouter_eval_core/derived/representations/skillrouter_task_relevant_pool_top50_I2.jsonl`; I3C rows can be filtered from the full-all cleaned artifact, although no separate top-50 cleaned I3C file exists yet.
    - These pools support fixed-candidate reranking/ablation. They do not replace the completed full-library/full-tier FTS first-stage retrieval.
    - Canonical I3C V2 top-20 representation: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_top20_pool/I3C_V2_top20_pool_cleaned.jsonl`.
    - Canonical I3C V2 full-all representation: `skill_benchmark/external/skillrouter_eval_core/derived/representations/i3c_v2_full_all/I3C_V2_full_all_cleaned.jsonl`.

## Result Reporting Template

Use this template when adding any new result:

```text
Method ID:
Execution venue:
Job/API provider ID if applicable:
Prompt stratum:
Prompt count:
Skill count:
Representation:
First-stage retriever:
Reranker:
Candidate budget:
Model/provider:
Cache state:
Output artifacts:
Strict top-1:
Accept top-1:
Top-5:
Accept top-5:
MRR:
Candidate recall:
Latency/cost:
Known caveats:
```
