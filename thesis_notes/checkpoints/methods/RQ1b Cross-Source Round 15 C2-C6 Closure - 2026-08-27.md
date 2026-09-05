# RQ1b Cross-Source Round 15 C2-C6 Closure

Status: `C6_FREEZE_PASS_NOT_A_RETRIEVAL_OR_RESULT`

## What Closed

Seven C1-passed, cross-source 3--4-candidate compositions entered Round 15
prompt curation. C2 drafted 46 direct/paraphrase requests. C3 first applied a
literal cue audit, then a separate manual semantic-risk review; the final
combined manual ledger marks all 46 requests as cue-safe operational-context
prompts, with residual cue risk retained rather than hidden.

C4 used two independent model-assisted blinded reviewers per packet. The
packet set was split into two disjoint halves so reviewer pairs were
independent by packet range. The first materialisation was invalidated before
acceptance because it exposed source provenance; its outputs were not used.
The replacement C4R03 materialisation redacted provenance before review. Exact
evidence-substring auditing required citation-only repairs for 20 truncated or
format-shifted citations. The original reviews remain preserved; the repair
ledgers replace only those failed evidence strings with exact text from the
same anonymous card and do not change reviewer identity, adequacy judgment,
rationale, or coverage.

## C4--C6 Outcome

| Gate | Outcome |
|---|---:|
| C4 packets reviewed | 46 |
| Exact two-reviewer singleton agreements | 43 |
| Multi-adequate agreements | 0 |
| Reviewer disagreements | 3 |
| C5 strict singleton packets | 43 |
| C5 unresolved packets | 3 |
| C6-frozen candidate compositions | 7 |
| C6-frozen strict prompt packets | 43 |

The three C4 disagreements are `C4R03-037`, `C4R03-040`, and `C4R03-044`.
They remain unresolved/excluded from the strict primary stratum; no
post-review relabelling was performed.

## Evidence

- C3 final manual ledger:
  `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c3_manual_semantic_round15_v2_2026-08-27.jsonl`
- C4 combined consensus:
  `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c4_round15_v3_combined_consensus_2026-08-27.json`
- Citation-only repair ledgers:
  `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c4_round15_v3_half_a_A1_citation_repair_2026-08-27.json` and
  `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c4_round15_v3_half_b_A2_citation_repair_2026-08-27.json`,
  `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c4_round15_v3_half_b_B2_citation_repair_2026-08-27.json`
- C5 stratum summary:
  `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c5_round15_v3_summary_2026-08-27.json`
- C6 freeze summary:
  `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c6_round15_v3_summary_2026-08-27.json`

## Boundary and Next Gate

This is public-skill curation and blinded-review evidence only. It establishes
that the 43 frozen prompt/candidate units meet this protocol's source,
cue-audit, singleton, and reuse checks. It does not run or report retrieval,
embedding, reranking, API, metric, or downstream-task performance.

Round 16 has already completed a discovery-first M0 pass over 37 additional,
non-overlapping public repository leads. The next action is M1 commit pinning,
exact-byte staging, and provenance verification for selected leads before a
new C0A cohort is formed. A missing declared repository licence is recorded as
reference-only provenance and does not exclude a public original from
curation.
