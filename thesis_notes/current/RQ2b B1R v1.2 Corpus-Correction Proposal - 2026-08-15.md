# RQ2b B1R v1.2 Corpus-Correction Proposal

Date: 2026-08-16  
Status: `V1.2 I3C AUTOMATIC GATES COMPLETE / CALIBRATED BLINDED QA FAILED / RETRIEVAL BLOCKED`  
Parent: `rq2b-full-library-v1.1-2026-08-15` is immutable and rejected before retrieval.

> Historical record only. Its proposed fresh calibrated-QA gate was superseded
> for the current V3 corpus by the explicit automatic-integrity-freeze decision
> recorded in `RQ2b V3 I3C Root-Coverage Checkpoint - 2026-08-18.md`. The V3
> evidence supports deterministic integrity, not independent semantic QA.

## Why a New Version Is Required

The completed v1.1 role-stratified blind QA rejected the I3C corpus before retrieval: 16 critical errors and seven major-error rows. The failure is not a retrieval result. Its dominant root cause is a generator-template defect in the 1,800 locally generated `background_scale` skills.

The current template in `skill_benchmark/scripts/generate_background_scale_skills.py` writes benchmark-specific language and generic routing boilerplate into every background skill. The local source scan found all 1,800 rows contain each of the following patterns:

- `Background scale skill used to create realistic retrieval pressure in the benchmark.`
- references to a `neighboring confusable skill` and an `expected artifact below`;
- a boundary against replacing a `gold-label core benchmark skill`;
- the same five generic routing workflow steps.

That text is source content, so the I3C extractor legitimately preserved some of it. It is nevertheless invalid selector-visible content because it describes the benchmark rather than a user-facing skill. The v1.1 automatic exact-evidence gate therefore does not make the resulting corpus valid for scientific retrieval.

Two other skills contain phrases such as `gold labels` because evaluating retrieval benchmarks is their actual user-facing task. They are not part of the 1,800-row template defect and must not be removed merely by a global keyword filter.

## Proposed v1.2 Source Correction

Create a new, separately versioned corpus from the same 2,433-skill library and the same 381 strict-gold prompt endpoints. Preserve every `skill_id`, prompt, and source family. Regenerate **all and only** the 1,800 `skill_benchmark/skills/background_scale/*/SKILL.md` artifacts from a corrected deterministic generator; do not modify the v1.1 artifacts.

For each background skill, retain only genuine task information already supplied by its domain/procedure definition:

- source-native name and description;
- a task-specific `Use when` statement and input/precondition;
- domain-specific dependencies/resources;
- a concrete output artifact;
- a procedure-specific workflow whose steps are determined by the procedure type, not by generic selection/routing boilerplate.

The corrected generator must remove, from both source documents and selector-visible content:

- the scale/benchmark explanation;
- `gold-label`, `core benchmark`, `retrieval pressure`, `confusable skill`, and `neighboring skill` language used as benchmark scaffolding;
- `expected artifact below` and the benchmark-specific switch/selection boundary;
- the shared five-step routing workflow and any other generic selector text that does not describe the actual procedure.

The correction must not use a blind keyword-delete pass over non-background source families. It must leave legitimate evaluation skills intact and use source-family provenance to limit the transformation.

## 2026-08-16 Local Execution Record

### I3C Extraction, Automatic Gates, And Pending Blinded QA Update

The source-assignment packet above was subsequently approved by the user in its exact hash-bound form (`472fd3ad20e11722c4ac77a2f83a0026b78c80a970bbd01c5f51dbd824354bfe`). Under that receipt, the project materialised and extracted all 57 source-only input chunks for the assembled 2,433-row v1.2 corpus with at most six low-reasoning local Codex workers active at a time. No internet, external API, provider model, hosted compute, retrieval, reranking, or thesis writing was used.

The accepted output for every chunk was revalidated against its bound input. The corpus-level automatic gate passed: all 2,433 JSONL rows parse; every `skill_id` and `source_row_index` aligns; every retained evidence item is an exact source substring; and heading-only evidence, duplicate item IDs, and missing IDs are absent. Four invalid first attempts were quarantined and replaced locally: a field-schema error (chunk 5), duplicate field item ID (chunk 26), heading-only evidence (chunk 36), and source-identity mismatch (chunk 40). The accepted merge is `i3c_merged/manifest.json`, SHA-256 `af630fe730c5fac7745c288f3b6986499f5296aa962e1b6ac388a70ff48b8f13`; it contains canonical I3C, I3C-fielded, and I3-flat evidence artifacts, each with 2,433 rows.

The now-built `i3c_manual_qa/` packet contains a deterministic, 120-row blinded source/extraction sample. It stratifies only local source properties available inside the source-only boundary: main-evaluated/background/other cohort, source policy, family, source length, selector density, field presence, and existing warning coverage. The reviewer packet deliberately excludes prompts, gold labels, alternatives, roles, strata, clusters, and retrieval outcomes. Its manifest SHA-256 is `56e4cd3484faa50d630de01f178ba29b0c8ef61331238df636fba2ec412fc298`; its sampling key remains local and was not given to reviewers.

Under a separate one-time local QA receipt, six independent reviewers completed one disjoint 20-row batch each. The 120-row form is structurally complete, identity-aligned, and preserves zero reported critical errors with 75 reported major rows. These raw counts are **not** a valid corpus rejection or a retrieval result: the v1.2 packet did not freeze a material-coverage rule or acceptance threshold, and reviewer batches range from zero to sixteen major rows. Most raw major labels are `missing_material_field`; batch 003 and batch 004 have the same cohort and source-policy composition but report zero versus fifteen major rows. The integrity audit (`i3c_manual_qa/manual_qa_integrity_audit.json`, SHA-256 `7705212f773d97bfa1ad0fc4dcc7770047e78ead1d556e3f954751e60abf3014`) therefore supersedes the raw finalizer's pass/fail interpretation while preserving its form and output unchanged.

This section supersedes the older pre-approval statements below. The raw-QA attempt was retained as provenance only; it was followed by a separately frozen calibrated blinded extraction-fidelity re-review. A valid QA pass would have established only eligibility to seek a later retrieval/scoring approval; it would not itself have established a representation or retrieval result.

### 2026-08-18 Calibrated Blinded Re-review And Retrieval Block

The calibrated re-review contract froze a 120-row source-only packet, eight local calibration fixtures, one permitted calibration replacement per reviewer, and acceptance at zero critical-error rows and at most six major-error rows. Six independent local reviewers passed all calibration fixtures and completed disjoint 20-row review batches. The completed form is structurally valid and identity-aligned (`review_form_completed.jsonl`, 120 rows, SHA-256 `53a15637c19c53714613b7f483e6f029d28eec956b5c6cbc064de94cafc7cffb`). The frozen finalizer decision is `manual_qa_failed_retrieval_blocked`.

The frozen decision reports four critical rows and eleven major rows (9.17%). A post-decision, source-grounded failure audit confirms that every evidence string in the four critical reports remains an exact source substring. Those reports arose because the reviewer packet exposed the non-selector-visible normalised parser `text` next to the selector-visible exact `evidence`; the reviewers tested the former as though it were the latter. This is a reviewer-packet/rubric visibility defect, not a literal-evidence automatic-gate failure. It does **not** convert the decision into a pass: eleven major rows alone exceed the frozen limit of six.

The actionable major pattern is corpus-wide rather than a sampled-row repair. Ten of the eleven majors concern missing `use_conditions`; the audit finds 149 `public_original` skills with all seven I3C fields empty despite a non-empty source-native description, including 74 descriptions that explicitly contain `use when`. The remaining major is a generic output span that retained a negative statement but omitted the distinctive output evidence. The failure audit is `i3c_manual_qa_calibrated_v6/failure_audit.json`; it binds the 2,433-row canonical extraction, source manifest, review packet, completed form, and decision. It records zero external API calls and zero retrieval, embedding, reranking, or thesis-result runs.

Therefore B1L local BM25 is not eligible to start. The next corrective action is a new, versioned source-grounded I3C extraction policy that captures selector-useful source-native metadata in the canonical fields while retaining evidence-only selector serialisation, followed by automatic validation and a fresh calibrated blinded review. It requires a new explicit source-assignment approval; neither the consumed v1.2 extraction approval nor this re-review approval authorises it.

The user approved only local, deterministic regeneration of this source family in bounded batches. The corrected generator `skill_benchmark/scripts/generate_background_scale_skills_v12.py` produced all 1,800 replacement `background_scale` `SKILL.md` files as 18 sequential batches of 100. The source files, per-batch manifests, and the frozen overlay manifest are contained in `skill_benchmark/rq2b_full_library/rq2b-full-library-v1.2-2026-08-16/`.

The frozen overlay manifest is `source_overlay_manifest.json`, SHA-256 `0d81f39348eea55f1faced685821d87ae59712d4b9acc263d6e7730bf79f3924`. It verifies 1,800 ordered, unique `skill_id` values, 1,800 distinct source hashes, 1,776,439 UTF-8 bytes, and zero matches for the old benchmark-scaffold and generic-workflow patterns. All 18 batch manifests record zero network calls, zero external API calls, no source assignment to subagents, and no retrieval/reranking activity. Batch 000 deterministically recovered its 100 byte-identical files after an initial manifest-writer typo; batches 001--017 created their files once.

At the time this source-overlay record was written, the unchanged 633 source texts had not yet been joined or assigned. That historical statement is superseded by the extraction update above; it remains here only to preserve the provenance chronology.

### Assembled-Corpus Preflight Update

The subsequent local assembled-corpus preflight is complete. It froze `source_manifest.jsonl`, SHA-256 `6f7accc1274ee1c410bfeaba2f32b41b7dc5168a81ef55343b7f56e37abce0c3`, in the v1.2 workspace while preserving the parent 2,433-row order. All 1,800 `background_scale` rows point to the overlay; all 633 remaining rows were reread and matched their parent source hashes exactly. The corresponding source-free chunk-plan metadata is `i3c_chunk_plan_metadata.json`, SHA-256 `026aff1dd09cc4f0f8b2db34cd73fd0e4b9d56e3674ac9c0d8ecd34198a2a502`: 57 future chunks, at most 50 rows and 59,935 local proxy tokens per chunk, with 1,455,632 local proxy tokens and 6,491,960 source UTF-8 bytes in total.

The assembled full-corpus lint still has zero forbidden matches within `background_scale`. It reports 18 instances of the broad phrase `neighboring skill` in unchanged `public_imported_background` source files; inspection confirms these are source-native route-out statements in public skills, not benchmark scaffold. The assembled preflight report `assembled_source_preflight.json`, SHA-256 `a1aa2ee752990a9a4886d72951ea3cc3470ec831f1c0da50e0f4151c5417a309`, records those distinctions and zero network/API calls, zero external text transmission, zero workers, and zero retrieval/reranking.

An initial normalised-newline token plan was quarantined after the source-assignment packet detected CRLF raw-byte drift in a subset of unchanged public sources. The manifest had not changed, but the plan's token total differed by 18 proxy tokens. The corrected plan decodes raw bytes explicitly; no source text was transmitted or written to a worker input before this correction. The quarantine README preserves the superseded artefacts and the correction rationale.

The draft, source-free assignment packet is `i3c_source_assignment_approval_packet.json`, SHA-256 `472fd3ad20e11722c4ac77a2f83a0026b78c80a970bbd01c5f51dbd824354bfe`. It binds the source manifest, lint report, chunk plan, overlay, extraction prompt, 57 planned JSONL input hashes, low-reasoning worker contract, maximum six active workers, and maximum six replacement assignments. Its state is `draft_pending_explicit_source_assignment_approval`; it contains no source text and does not create worker input files.

This preflight update replaced the preceding statement that the 633 rows had not yet been joined. Its "no I3C worker inputs or extraction outputs" statement is now superseded by the approved extraction update above. It still does not itself constitute manual-QA, retrieval, or thesis results.

## Remaining Local Preflight Before Any Source Assignment

1. **Complete:** implement a deterministic procedure-specific background template, with distinct workflow content for each supported procedure type.
2. **Complete:** regenerate the 1,800 background source artifacts in a new versioned workspace, never in the rejected v1.1 snapshot.
3. **Complete:** run zero-network benchmark-scaffold lint over the assembled 2,433-row v1.2 source inventory. The corrected `background_scale` family has zero forbidden matches; the report retains 18 reviewed, source-native public `neighboring skill` phrases outside that family rather than deleting them globally.
4. **Complete:** recompute hashes and exact UTF-8 byte counts for the changed 1,800-row overlay, verify exact reuse of the unchanged 633 rows, freeze one 2,433-row source manifest, and recompute proxy-token totals and chunk metadata. The former 57 chunk count happens also to result under the renewed bounds, but the new manifest, bytes, and token total are independently recomputed rather than inherited.
5. Make the manual-QA contract explicit: `evidence` must be an exact raw source substring; a serialised selector span may collapse whitespace only when it is whitespace-equivalent to its raw evidence. The reviewer should test that rule rather than requiring the normalised serialization to be byte-identical to wrapped source text.
6. **Complete and executed under explicit approval:** the source-free packet was approved, materialised into its bound local inputs, and all accepted chunk outputs passed automatic extraction gates. The raw QA attempt was later superseded by a frozen calibrated re-review. That re-review failed: eleven major rows exceed the maximum of six. A source-grounded extraction-policy correction and fresh source assignment are now required; no retrieval may start.

## Calibrated v1.2 QA Gate: Executed And Failed

The preceding proposed assignment wording is superseded by execution. Under the approved packet, all 2,433 source rows (the 1,800 regenerated overlay rows and the 633 exact-hash unchanged rows) were materialised only into their bound local chunk inputs, extracted, and merge-validated as one new identity-aligned corpus version.

Then run all automatic gates again, including source-family scaffold lint, literal evidence, identity, heading-only, duplicate-ID, and missing-ID checks. Those gates are now complete. The fresh 120-row blinded QA packet is source-only stratified rather than role-stratified, because prompts, gold labels, alternatives, roles, and clusters are intentionally outside this extraction-only boundary. Preserve the v1.1 sample, reviews, and rejection decision without alteration. Do not selectively repair only sampled rows.

The raw v1.2 QA attempt did not establish eligibility for later retrieval. Its integrity audit fixed neither source nor extraction and did not permit selective sample repairs. The subsequent calibrated re-review also does not establish eligibility: it failed on eleven major rows. The re-review failure audit establishes that the reported critical errors are a packet-visibility issue, but it also identifies the material extraction gap above. BM25, Qwen, native SkillRouter, either reranker, and thesis-result writing remain unauthorised.

## Approval Boundary

The completed B1R receipt authorised one v1.1 2,433-row extraction and its six replacement attempts; it is exhausted. The v1.2 source-assignment receipt was separately approved and is now consumed for local automatic extraction/merge/QA-packet construction. The following now need a new explicit approval:

- a new, versioned source assignment for corpus-wide I3C re-extraction under a corrected extraction policy; and
- a fresh calibrated blind-QA protocol and re-review bound to that new extraction version.

No internet, external API, embedding, retrieval, reranking, hosted compute, or thesis LaTeX/PDF work is proposed in this correction stage.

## Next Decision Requested

The V3 source-grounded correction packet at `skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/source_assignment_approval_packet_sealed.json`, SHA-256 `91c47b40fdd73ad30ed4591390bd5fc265b814fadf2fd4e4e16f214b184afcf1`, was explicitly approved and bound to a local approval receipt. It contains no source text and binds the unchanged 2,433-row source manifest, 57 hash-bound inputs, `I3C_SUBAGENT_EXTRACTION_V3.md`, and the local materialiser/merger. All 57 chunks now pass the generic automatic gates. A stricter V3 root-coverage check exposed 23 remaining fieldless source-native public descriptions, so chunk 49 was re-extracted as one complete bound replacement; the repaired worker corpus has zero fieldless non-empty public descriptions and zero fieldless `use when` descriptions. Because the first merge records the prior chunk-49 hash, it is stale audit evidence, not a retrieval artifact. A small separately sealed local remerge is the next gate; retrieval remains prohibited.

Review and either approve or amend this V3 packet. It corrects the 149 fieldless public-description cases across the corpus, preserves exact evidence-only selector serialisation, repairs the reviewer-packet visibility boundary, and prohibits selective sampled-row edits. No retrieval, embedding, reranking, or thesis result writing may occur under the consumed v1.2 approvals.
