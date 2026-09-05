# RQ2b V3 I3C Root-Coverage Checkpoint

Date: 2026-08-18  
State: `AUTOMATIC INTEGRITY FROZEN / B1L LOCAL BM25 COMPLETE / POST-RUN INTEGRITY VERIFIED / USER RESULT REVIEW REQUIRED`

## Bound Scope

This checkpoint concerns only the user-approved V3 local source-assignment
packet `91c47b40fdd73ad30ed4591390bd5fc265b814fadf2fd4e4e16f214b184afcf1`.
It used the unchanged 2,433-row v1.2 source manifest, the V3 prompt, and at
most six low-reasoning local workers. Source construction and automatic
integrity validation made zero network calls, external API calls,
provider/hosted-model calls, retrieval/reranking runs, or thesis result writes.
The separately approved local B1L BM25 run is recorded below.

## Completed Worker Corpus

- Every one of the 57 planned chunk outputs exists and independently passes
  strict JSONL parsing, expected row count, identity/order alignment, exact
  evidence-substring, heading-only, duplicate-ID, and missing-ID checks.
- The accepted worker corpus contains 2,433 rows with 2,433 unique `skill_id`
  values.
- The first local merge was built at
  `skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/i3c_merged/manifest.json`
  (SHA-256 `340539d3a47ecf6b6642f6182dc0e1964727a97c93e1ea152035293c5eb52caf`).
  It is retained as an initial automatic-gate artifact only.

## Root-Coverage Correction

The V3-specific audit compares every `public_original` source-native
description to the current I3C output. The initial merge still had 23 of 460
non-empty public descriptions with all seven fields empty; 19 of those 23
descriptions explicitly contained `use when`. All were in bound chunk 49.

Chunk 49 was re-extracted as one whole 32-row replacement, not as a sampled
row patch. Its replacement output independently passes every generic automatic
gate. The current worker corpus now has:

- `0/460` non-empty public-native descriptions with all seven I3C fields empty;
- `0/243` descriptions containing `use when` with all seven I3C fields empty.

The first merge cannot be treated as final because it hashes the old chunk-49
output. Following the separately approved, source-free local finalisation
packet, the replacement was bound into the immutable final merge at
`skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/i3c_merged_final/manifest.json`
(SHA-256 `50220955aadafa66f4f5032763ceb5ed4e68b88c04bc2b3b5cab98f1f253b661`).
It again passes the automatic JSONL, identity, literal-evidence, heading-only,
duplicate-ID, missing-ID, and root-coverage checks.

## Duplicate Observation

The initial merge reports one duplicate selector-text row beyond the first.
It is an upstream exact-source duplicate, not an extractor collapse:
`public-swebench-xlsx` and `public-xlsx` have the same original source SHA-256
`dd316db7785a6be12966c2a2d848931fbf5f518b3cdb0a66fa62ee835ead1cfc`, the same
name/description, and the same I3C selector. A second upstream exact-source
duplicate pair is `public-anthropic-mcp-builder` and
`public-swebench-mcp-builder`, with source SHA-256
`0f4592dcb53cf2b5d6b7febee6b4152018b565551a1c29e3c612f57b218ab295`.
Both source-duplicate pairs remain present and are explicitly recorded for the
future full-library design decision; neither has
been silently removed or relabelled.

## Calibrated QA Packet

The permitted local packaging step is complete at
`skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/i3c_manual_qa_calibrated_v1/manifest.json`
(SHA-256 `1990b6a46b27e16c539ac131814ad64b63eed34fbdc89695422ee47d71fa6bcb`).
It contains 120 blinded source/extraction pairs: all 32 rows from the repaired
chunk 49 plus 88 deterministic coverage/stratified rows, six unassigned
20-row batches, and eight calibration fixtures. The reviewer view exposes only
source-native selector metadata plus literal extracted evidence; it hides the
internal normalised parser `text` field that caused the prior packet-visibility
ambiguity. The packet itself was validated as 120 rows with 32 pinned rows,
zero parser-text entries, and zero reviewer-visible prompt/gold/retrieval keys.

## Quarantined Manual-QA Attempt

The user approved completion of the frozen packet and six independent local
reviewers each completed its eight calibration fixtures and one disjoint
20-row batch (`48` calibration rows and `120` review rows in total). The
mechanical finalizer correctly refused to aggregate the batch judgements:
the frozen guidance did not define the complete critical-error codebook or the
exclusive-code rule for the generic-span fixture, while its answer key required
an exact code match. All reviewers agreed on every fixture's severity and field
attribution, but used semantically equivalent unlisted critical codes; two also
added a reasonable but undeclared secondary code to the generic-span fixture.

Those outputs are retained, hash-recorded, and quarantined at
`skill_benchmark/rq2b_full_library/rq2b-i3c-v3-2026-08-18/i3c_manual_qa_calibrated_v1/manual_qa_attempt_audit.json`.
They are neither an extraction-fidelity pass nor a failure, and they must not
be scored post hoc.

## Automatic Integrity Freeze And B1L Preparation

The user then explicitly directed that no further blinded/manual QA be run for
this version. This changes the admissible evidence, not the quarantined batch:
the V3 corpus may be used only on the strength of deterministic provenance and
representation-integrity checks, and it must not be described as independently
semantic- or human-QA-complete.

The fail-closed local automatic validator passed and wrote:

- automatic-integrity report:
  `automatic_integrity_freeze/automatic_integrity_freeze_report.json`, SHA-256
  `a3fe05dda00c6e7935262d8be30a69ddb45b15eeeef7426fbfc642a7071c988f`;
- automatic-freeze checkpoint:
  `automatic_integrity_freeze/automatic_integrity_freeze_checkpoint.json`,
  SHA-256 `5bcf41581fff5d89dc9331b50e10b48f01fecc156c69e4b4e722f6d293a9d937`.

It replays all 57 source/output chunks and confirms 2,433 source, canonical,
I3C-fielded, and I3-flat rows; strict JSONL/schema/identity/source hashes;
literal source evidence and heading exclusion; serialisation replay; zero
fieldless public-native descriptions; zero fieldless `use when` descriptions;
the two retained exact-source duplicate groups; and zero benchmark scaffold
matches in the corrected background sources. It performs no retrieval,
reranking, provider request, or thesis-result write.

The first two B1L preflights are retained but superseded without execution
during static implementation review: V1 lacked runtime runner self-hash
verification, and V2 did not yet require a warm replay of persisted indexes or
a fresh automatic-integrity replay at execution time. The corrected V3 B1L
preflight is frozen at `b1l_preflight_v3/b1l_preflight_report.json`, SHA-256
`992595ce3f8392c69c8ff778514ec149e51ac47d20563b8a1534626ec9d0aaed`.
It creates V3-local I1 and exact-source I2, binds final I3C/I3-flat, verifies
all four representations over 2,433 identities, isolates 381 strict scored
prompts (243 controlled and 138 public-gold) without `valid_skills` or other
alternative-label fields, and verifies that every strict gold ID exists in the
candidate library. The future local BM25 matrix is exactly four indexes and
1,524 prompt-representation rankings, with Top-100 persistence and no stress
prompt in accuracy denominators.

The text-free, local-only execution packet is
`b1l_preflight_v3/b1l_execution_approval_packet.json`, SHA-256
`caf10c1370e1610275b0eecfb6ddb0f9214c9d95cb2708ef61a80e17389ce8ec`.
The B1L runner passed synthetic and full no-scoring preflight checks and
refused `--execute` before any index construction unless an exact approval
receipt bound that packet. The user then approved the packet on 2026-08-18;
the one-time local receipt is `b1l_preflight_v3/b1l_execution_approval_receipt.json`,
SHA-256 `def03cd54d5b2e0f3d5512a481e498017e9375c68acdb6e70fd0332ae2fdf255`.

## B1L Local BM25 Execution And Post-Run Verification

The authorised V3 B1L run completed locally with four global 2,433-skill BM25
indexes and all 1,524 strict prompt-representation rankings. It persisted every
Top-100 list and then reloaded each index from disk to replay all 381 prompts;
all 1,524 replayed Top-100 lists match the persisted result rows exactly.

- Result JSONL: `b1l_preflight_v3/b1l_local_bm25_run/b1l_strict_results.jsonl`,
  SHA-256 `3ec257b5c398cccee6f7ac7e7fc8ce4b25e1ced3c2539b469accad97cad877cc`.
- Post-run integrity report: `b1l_preflight_v3/b1l_local_bm25_run/b1l_bm25_postrun_integrity_report.json`,
  SHA-256 `029b80757eb28f060022052baaf4192a35f0e359abf63846935df9b327cf3506`.
- Network calls, external API calls, provider calls, embeddings, reranking, and
  thesis-result writes: `0`.

Across all 381 strict prompts, I1 achieved Hit@1 `0.564`, MRR@10 `0.679`, and
Recall@20 `0.906`; I2 achieved `0.627`, `0.749`, and `0.966`; I3-flat achieved
`0.504`, `0.626`, and `0.887`; and I3C achieved `0.504`, `0.625`, and `0.885`.
This is a descriptive lexical B1L baseline only. It does not establish an RQ2b
representation conclusion, because dense retrieval and both rerankers have not
run, and the V3 corpus has deterministic provenance evidence rather than an
independent human-semantic-completeness claim.
