# RQ1b Cross-Source Round 17 C2-C6 Closure

Date: 2026-08-27

## Boundary

This checkpoint closes the Round 17 curation sequence after the earlier M1-C1
closure. It records prompt cue control, source-deidentified model-assisted
adequacy review, strict-singleton stratum assignment, and packet freezing. It
does not record human annotation, retrieval, representation scoring, embedding,
reranking, API use, a metric, or downstream-task success.

## C2 and C3

- The ten C1-passed cross-source candidate compositions yielded 70 final C2
  prompt packets: one direct and one paraphrase prompt per intended candidate.
- Final C3 literal audit v2 passed 70/70 prompts with no remaining title or
  copied-source phrase failure.
- The manual C3 ledger preserves 34
  `C3_ALLOWED_EXPLICIT_OPERATIONAL_CONTEXT_NOT_A_LABEL_OR_RESULT` records and
  36 `C3_REWORDED_FOR_LITERAL_CUE_NOT_A_LABEL_OR_RESULT` records. Both denote
  prompts that passed final C3; the second retains the fact of an earlier
  cue-only rewrite. Residual cue risk is still recorded per packet.

## C4 to C6

- Two independent source-deidentified model-assisted reviewers assessed all 70
  anonymous packets and all 250 displayed candidate cards. These are not human
  annotations.
- Initial C4 validation failed closed: 26 Reviewer-A evidence citations were
  not literal card substrings. A citation-only repair replaced those spans with
  exact snippets from the same anonymous cards; adequacy values and rationales
  did not change. The subsequent audit validated card coverage and every cited
  substring.
- Final C4 produced 70 exact two-reviewer singleton agreements, zero
  multi-adequate agreements, and zero disagreements. C4 alone does not see the
  card-to-skill key and is not a gold-label result.
- C5 unsealed the mapping and verified that all 70 singleton cards match the
  pre-sealed C2 intended candidate. There were no unresolved packets.
- C6 revalidated C1 source hashes, candidate compositions, two-origin minimum,
  candidate reuse, and final C3 status before freezing ten candidate
  compositions and 70 strict packets.

## Running Strict Curation State

The historical C6 files now total 27 frozen cross-source candidate compositions
and 176 strict direct/paraphrase prompt packets:

- 17 initial packets;
- 22 Round 13 packets;
- 43 Round 15 packets;
- 24 Round 16 packets; and
- 70 Round 17 packets.

This is a strict natural-artifact curation count, not a retrieval corpus size,
accuracy score, selector result, or claim that operational constraints are
implicitly expressed by users. Each Round 17 C6 record retains residual cue
risk and must be reported as a natural-artifact case with explicit operational
context where applicable.

## Artefacts

- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c2_prompt_drafts_round17_v2_2026-08-27.jsonl`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c3_round17_literal_cue_audit_v2_2026-08-27.json`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c3_round17_manual_semantic_disposition_2026-08-27.jsonl`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c4_round17_model_assisted_consensus_2026-08-27.json`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c5_round17_strata_summary_2026-08-27.json`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c6_round17_primary_freeze_2026-08-27.jsonl`
- `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c6_round17_primary_freeze_summary_2026-08-27.json`
