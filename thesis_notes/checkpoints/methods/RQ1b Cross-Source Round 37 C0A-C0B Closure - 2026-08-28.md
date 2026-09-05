# RQ1b Cross-Source Round 37 C0A-C0B Closure

Date: 2026-08-28

## Boundary

This checkpoint records navigation-only composition screening and exact-original
source review. It is not human annotation, retrieval, embedding, reranking, an
API result, a metric, or a downstream-task result.

## C0A Navigation Gate

- The Round 37 M0--M2 source pool supplied six disjoint navigation lanes. C0A
  returned two tentative three-candidate directions.
- One scientific-computing direction was mechanically rejected before source
  review because two of its three candidates came from the same origin. It is
  retained as `C0A_PROPOSAL_NOT_A_CLUSTER_OR_RESULT`; it was not repaired or
  advanced.
- One commerce/analytics direction used three distinct sources and advanced
  solely to C0B source review.

## C0B Exact-Original Gate

- The three candidate originals were copied into a read-only packet after
  SHA-256 verification. The source-only reviewer received the C0B protocol,
  roster provenance, and those originals only: no C0A envelope/risk, prompt,
  label, acceptable set, retrieval input, model result, or metric.
- C0B structurally rejected the commerce/analytics proposal. The HubSpot sales
  reporting and Google Ads budget sources are bounded domain workflows, while
  the GA4 source is a broad connector covering reporting, navigation,
  configuration, and event sending. This is a source-supported
  generic-plus-specialised/interface-container asymmetry, not three comparable
  independent first routes.
- Local validation confirmed all five stored evidence substrings are exact
  substrings of their matching byte-preserved originals. No schema alias or
  evidence repair was needed.

## Outcome and Running State

Round 37 adds zero C1 drafts, C2 prompts, C4 reviews, C6 compositions, strict
packets, or non-primary packets. The strict state remains **62 frozen candidate
compositions / 352 frozen strict prompt packets / 57 non-primary packets / no
retrieval results**. Thirteen more compositions are required for the current
75-composition curation target.

This is a strict feasibility curation outcome. It does not establish selector
accuracy, representation quality, natural conflict frequency, or end-to-end
routing success. Fresh Round 38 public-source discovery runs separately under
the discovery-first cadence.

## Evidence

- Protocol: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/rq1b_cross_source_main_benchmark_protocol_2026-08-26.md`
- C0A merge: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c0a_round37_merge_summary_2026-08-28.json`
- Exact source packet: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c0b_round37_exact_source_packet_summary_2026-08-28.json`
- C0B ledger validation: `skill_benchmark/rq1b_cross_source_public_benchmark/manifest/c0b_round37_ledger_validation_2026-08-28.json`
