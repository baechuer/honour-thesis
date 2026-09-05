# RQ2b v1.2 Local Source Overlay Completion Checkpoint

Date: 2026-08-16  
State: `SOURCE CORRECTION COMPLETE / V1.2 I3C AUTOMATIC GATES COMPLETE / CALIBRATED QA FAILED / RETRIEVAL BLOCKED`

## Superseding Extraction Update

This checkpoint preserves the source-correction provenance below. Its original "extraction unauthorised" state was true when it was first written, but is now superseded. The later exact source-assignment packet (`472fd3ad20e11722c4ac77a2f83a0026b78c80a970bbd01c5f51dbd824354bfe`) was approved and consumed locally: all 57 accepted chunks and 2,433 rows passed automatic I3C validation and merged into canonical I3C, I3C-fielded, and I3-flat evidence artifacts. The merge manifest is `skill_benchmark/rq2b_full_library/rq2b-full-library-v1.2-2026-08-16/i3c_merged/manifest.json`, SHA-256 `af630fe730c5fac7745c288f3b6986499f5296aa962e1b6ac388a70ff48b8f13`.

A fresh 120-row blinded, source-only extraction-fidelity QA packet was built at `skill_benchmark/rq2b_full_library/rq2b-full-library-v1.2-2026-08-16/i3c_manual_qa/`. It intentionally excludes prompts, gold labels, alternatives, roles, strata, clusters, and retrieval outcomes. Six local reviewers completed its raw forms under a separate receipt, but the integrity audit found the gate inconclusive: the coverage rule and acceptance threshold were not frozen, and batch major rates range from 0/20 to 16/20. The raw forms are preserved; neither a corpus rejection nor retrieval readiness follows. No scientific retrieval, embedding, reranking, external call, hosted compute, or thesis result writing is authorised by this update.

## 2026-08-18 Calibrated QA Completion Checkpoint

The raw attempt was not used as the retrieval decision. A later immutable calibrated packet (`i3c_manual_qa_calibrated_v6/`) froze an acceptance rule of zero critical-error rows and at most six major-error rows, then passed six local reviewer calibration checks and collected 120 valid blinded review forms. Its final decision is `manual_qa_failed_retrieval_blocked`: 11 major rows (9.17%) exceed the maximum of 6. The post-decision `failure_audit.json` verifies that the four reported critical rows have exact source-substring **evidence**; they reflect a packet/rubric confusion between non-selector-visible parser text and selector-visible evidence. This does not make the corpus pass, because the major failure remains.

The audit finds a corpus-wide extraction-policy defect: 149 `public_original` skills have non-empty native descriptions but all seven I3C fields empty, including 74 descriptions containing an explicit `use when` statement. Ten of the eleven major rows are missing `use_conditions`; one retains only a generic output statement. No BM25, embedding, reranking, provider call, hosted compute, or thesis-result writing followed this decision. The next gate is a separately approved, versioned source-grounded extraction correction and a fresh calibrated QA cycle, not B1L retrieval.

The correction workspace `rq2b-i3c-v3-2026-08-18/` contains the sealed source-free V3 assignment packet, SHA-256 `91c47b40fdd73ad30ed4591390bd5fc265b814fadf2fd4e4e16f214b184afcf1`, which binds the unchanged v1.2 source manifest, 57 input hashes, V3 extraction policy, and local materialiser/merger without containing skill text. The user explicitly approved the packet and its bound receipt; all 57 local outputs were materialised/extracted and independently validated. A post-merge root-coverage check found 23 `public_original` descriptions still fieldless despite non-empty native descriptions, so the first merge is retained as stale audit evidence rather than a final artifact. One authorised whole-chunk replacement (chunk 49) then removed every remaining fieldless public description, including every description containing `use when`; its output independently passes generic gates. A new local remerge must bind that replacement before fresh calibrated blinded QA. This does not alter the failed v1.2 decision and does not authorise retrieval.

## Scope Completed

Under the local-only approval receipt `skill_benchmark/rq2b_full_library/rq2b-full-library-v1.2-2026-08-16/v12_local_source_regeneration_approval_receipt.json`, the project regenerated all and only the 1,800 `background_scale` source skills into a separate v1.2 overlay. The rejected `rq2b-full-library-v1.1-2026-08-15` corpus was not changed.

The completion artefact is `skill_benchmark/rq2b_full_library/rq2b-full-library-v1.2-2026-08-16/source_overlay_manifest.json`, SHA-256 `0d81f39348eea55f1faced685821d87ae59712d4b9acc263d6e7730bf79f3924`.

## Verified Facts

- 18 sequential batch manifests, each with exactly 100 rows.
- 1,800 ordered and unique `skill_id` values; 1,800 distinct source hashes.
- 1,776,439 total UTF-8 bytes across the replacement files.
- Zero matches for benchmark-scale explanation, gold-label/core-benchmark wording, confusable-neighbour wording, expected-artifact wording, benchmark switch wording, or the old generic workflow template.
- Every skill has `Use when`, `Input and preconditions`, and `Output`; the 1,720 generated domain-procedure skills also have `Dependencies and resources` and a procedure-specific `Procedure` section.
- Every batch records zero network calls, zero external API calls, no subagent source assignment, and no scientific retrieval/reranking.

Batch 000 recovered 100 byte-identical source files after the generator's first manifest-write attempt stopped at a boolean-literal typo. No later batch recovered or overwrote files; batches 001--017 each created their sources once.

## Historical Not Completed And Not Authorised

When this source-overlay checkpoint was first written, the 633 unchanged source texts had not been joined with the overlay and no v1.2 chunk plan, source-text assignment, I3C extraction, I3-flat derivation, automatic extraction QA, or blinded manual-QA packet existed. Those extraction-preparation statements are superseded by the update above; no manual QA completion, BM25, embedding, reranking, scoring, provider call, hosted compute, or thesis result writing has occurred.

The local assembled-corpus preflight and source-free assignment packet are complete; see `thesis_notes/current/RQ2b B1R v1.2 Corpus-Correction Proposal - 2026-08-15.md` for their hashes and the raw-byte correction record. The source-assignment gate and both raw/calibrated QA receipts are consumed. The v1.2 calibrated QA gate failed, so the next gate is a new source-grounded extraction correction plus a fresh calibrated review. This checkpoint remains source-correction/extraction provenance, not retrieval evidence, and does not make the corpus scientifically ready.
