# RQ2b B1R I3C Extraction Completion Checkpoint

Date: 2026-08-15  
Version: `rq2b-full-library-v1.1-2026-08-15`

## Boundary

This checkpoint records the user-approved B1R local I3C source-text extraction, automatic validation, representation derivation, and the subsequent user-authorised local completion of the blinded QA workflow. It is **not** a retrieval, embedding, reranking, downstream-task, or thesis-result artifact.

The B1R approval receipt binds the exact packet `fedb297afda625784225761b77c949d46c49d5df113f3e7f1df3b04b2648871f` and scope `b9a3dfc3ff95479403f6a21564aee62322e9296e0e950659d5955a8e42544cfc`. It permits source text only to low-reasoning inherited Codex workers, prohibits internet/external APIs and scientific selector execution, and does not itself authorise manual-QA completion. The later manual-QA completion receipt binds the corrected v2 packet and six local blind-review batches only; it still prohibits retrieval, provider calls, and thesis-result writing.

## Completed Local Work

- 57/57 bound chunks completed and independently revalidated.
- 2,433/2,433 accepted canonical rows, with contiguous `source_row_index` values and unique `skill_id` values.
- All per-chunk JSONL parsing, row-count, identity-alignment, literal-evidence-substring, heading-only-evidence, duplicate-ID, and missing-ID gates passed.
- 63 explicit assignments were recorded: 57 final completed chunk assignments and six failed/replacement assignments. Peak active workers: six. The six failures are retained in the worker ledger; canonical outputs come only from the final completed attempt for each affected chunk.
- Actual source-text transfer was 9,175,369 UTF-8 bytes and 1,974,188 local proxy tokens across assignments, below the approved ceilings of 10,032,775 bytes and 2,141,036 tokens. The larger 10,842,844-byte JSONL artifact total includes wrapper metadata and is not the authorised source-text count.
- Network calls and external API calls: zero.

## Automatic Merge Outcome

The I3C merger re-ran source-grounded canonicalisation across all accepted rows and derived two matched selector representations from the same retained evidence spans:

- canonical rows: `i3c_merged/canonical_extractions.jsonl`, SHA-256 `54a4167951a90edeb8f27c296b5b9233731f0bd9ae53c177aa72187800b9aaab`;
- I3C-fielded rows: `i3c_merged/i3c-fielded-evidence.jsonl`, SHA-256 `27d263be53e4af3e69cf3a404f05964ae7365f06d6530d378f24dfb4c0264b56`;
- I3-flat rows: `i3c_merged/i3-flat-evidence.jsonl`, SHA-256 `3c4905f010a8342d66fd9e468710ac876e276328ec1cb7921914a44e4f47f873`.

Full-corpus automatic summary: zero parse, identity, and evidence-substring failures; zero heading-only spans retained; 2,433 matching I3C/I3-flat evidence rows; two duplicate I3C selector-text rows beyond the first are reported descriptively, not treated as duplicate IDs. Field coverage/item counts are retained in the merge manifest rather than interpreted as performance evidence.

The binding artifacts are:

- merge manifest: `skill_benchmark/rq2b_full_library/rq2b-full-library-v1.1-2026-08-15/i3c_merged/manifest.json`, SHA-256 `8f577d9026cf1f7451161b269ffe8abd41e6aae695cf5707ead82ecbd73b3bc4`;
- execution ledger: `skill_benchmark/rq2b_full_library/rq2b-full-library-v1.1-2026-08-15/i3c_extraction_execution_ledger.json`, SHA-256 `822953471796d53703f6f2cf6ed28cbbef012e65c6494ad70b3f2086c59bbaee`.

## Blind QA Gate

The first deterministic packet at `i3c_manual_qa/` is retained but **superseded and unreviewed**: its deterministic sampler did not satisfy the protocol's required role-stratified coverage. No reviewer received that packet. It is not valid evidence for the QA gate.

The corrected deterministic v2 packet at `i3c_manual_qa_v2/` is built and verified:

- packet manifest: SHA-256 `0609956dd63343dd0f5574a0f804f28ee2912e7c0e044febe725da6b35ffb92e`;
- reviewer packet: SHA-256 `5606ca3f155eef1ab37b3765904a01b962e00d56b9a6ef643539403ee1ca0e9a`;
- sampling key, withheld from reviewers: SHA-256 `4f1572fb417357676afb36bbd41b9775b07ba8c07488982fd98203de9026bb82`;
- uncompleted review form: SHA-256 `d580b02701e66c6797876b18234ffbaf8d2b52788cf3ca86d8488a774dec3c7d`.

The reviewer packet excludes prompt, gold label, stratum, and routing-role metadata. Its sampling key covers all seven operational fields, 26 corpus families, and all required roles: 68 eventual-gold skills, 15 hard neighbours, and 37 background skills. It is split into six immutable 20-row inputs by batch manifest SHA-256 `aa0f5d4e431ab41734a3bdfa9f599c8cf5a10c9e9beca77cfef41dd5a9e4f658`. The completion receipt binds these exact artifacts and permits only six medium-reasoning local blind reviewers, one per batch. A failed critical/major-error decision requires the protocol's corpus-wide correction path; it cannot be selectively repaired only within the sample.

## QA Decision

All six independent blind reviews completed with complete identity-aligned forms. The final decision is `manual_qa_rejected_corpus_wide_correction_required`, recorded in `i3c_manual_qa_v2/manual_qa_decision.json` (SHA-256 `b9b2b39494cc9a098491bdb2d3c567c7d48473df429d290cbf2d542c266ab89b`): 16 critical errors and seven major-error rows (5.83%), exceeding both the zero-critical rule and the 5% row threshold. Several field-stratum major-error rates also exceed 5%.

The descriptive local failure analysis establishes a corpus-wide cause: all 1,800 `background_scale` source skills contain shared generic routing scaffold, expected-artifact boilerplate, and `gold-label/core benchmark` language. Fifteen critical leakage annotations come from this source-family contamination; the remaining critical annotation identifies an ambiguity between raw exact evidence and whitespace-normalised selector serialization. The completed v1.1 corpus must not be selectively patched or used for any retrieval stage.

## Next Approval Gate

A new corpus-version correction specification and explicit user approval are required before any revised source is assigned to a subagent. It must remove benchmark scaffolding across every affected background-scale source, define the handling of generic routing boilerplate, clarify the raw-evidence/whitespace-normalisation rule, create new source hashes, and require a fresh role-stratified 120-row blind QA sample. Local BM25, Qwen/SkillRouter embedding, either reranker, and thesis result integration remain prohibited.
