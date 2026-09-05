# RQ1b V3 C4A v1.2 Priority Execution

Date: 2026-08-30  
Status: `C4A-C6 WAVE 001 COMPLETE / LOCAL-ONLY / D1 DISCOVERY MAY RESUME / STRICT CURATION ONLY / NO SELECTOR RESULT`

## Decision

The next V3 work is to exhaust the already materialised C4A v1.2 queue before
searching for more public skills. The queue contains nine independent
anonymous three-candidate packets: four from Wave 001 and five from Wave 002.
Each binds original local source copies to the frozen C1--C3 lineage while
excluding prompts, sealed construction targets, source identities, titles,
URLs, selectors and results. This is a temporary priority rather than an end
to D1 expansion: after every queued packet reaches a recorded terminal C4A
and, where admitted, C4B--C6 disposition, the next permitted work is the next
D1 public-source discovery wave.

## Required Gate Sequence

1. Two independent builders read only one assigned anonymous packet and its
   source copies. Each returns a persisted seven-slot JSON card with exact
   contiguous quotes or `NOT_STATED`.
2. `validate_rq1b_v3_c4_field_cards.py` checks JSON shape, source-hash binding,
   literal quotation and identity-line exclusion for each raw return.
3. A separate source-only conformance review applies the v1.2 slot rules to
   valid returns. It may resolve only disagreements settled by those rules; it
   may not see a prompt, target, label or model result. A disagreement that
   cannot be resolved source-only rejects that packet from C4A.
4. Only an accepted canonical card may proceed to C4B key-blind adequacy
   review. C4B--C6, field masking, selectors, external transfer and metrics
   remain out of scope until that later gate.

## Execution Boundary

- Local source files and local subagents only; no online search, external API,
  hosted compute, embedding, reranking or text transfer.
- Persist each raw builder return before its audit. Do not overwrite historic
  v1.1 material or unpersisted-return records.
- Builders receive neither prompts nor sealed targets and do not select a
  candidate. The work is transcription rather than routing.
- New D1 discovery remains paused only while this queue is active. The queue
  has reached terminal C4A--C6 dispositions, so the next permitted work is
  source discovery under the unchanged strict gates.

## C4A Conformance And Canonicalisation Rule

The mechanical comparison enters conformance only after two distinct raw
responses both pass literal audit. The conformance reviewer reads only the
anonymous packet, its original source copies, the two valid cards and the
comparison report. For each candidate-slot cell it must:

1. accept an `EVIDENCE` quote only when it literally satisfies that slot's
   v1.2 inclusion rule;
2. retain every conforming exact quote from either builder, in deterministic
   lexicographic order, because slots are non-exclusive and no prompt may be
   used to prefer a shorter or more route-helpful card;
3. set `NOT_STATED` only where the underlying anonymous source has no
   qualifying literal span. If both builders omitted a clearly qualifying
   source span, reject the packet for a fresh builder wave rather than adding
   a third reviewer's new evidence; and
4. reject the whole packet when the rule cannot settle a status or quote
   disagreement without inferring a missing fact.

The reviewer therefore constructs at most a source-evidence card. It may not
name a winner, judge adequacy, use prompt information or interpret an evidence
difference as a routing effect. The resulting canonical card is still subject
to the later C4B strict-adequacy gate.

## Operational Blocker

On 2026-08-30, five stale running subagents visible to the local agent manager
were closed. After their shutdown confirmations, the manager still rejected a
new C4A builder, including a single-worker capacity probe, with
`collab spawn failed: agent thread limit reached`. No builder response was
created and no packet was modified. This is an execution-capacity block, not a
C4A validity, card-fidelity or routing finding. Do not replace the required
two independent builders with a single main-thread transcription.

## Acceptance Boundary

This priority is a throughput decision, not a scientific amendment. It cannot
make a C2/C3 survivor a valid cluster and cannot establish field availability,
strict gold, routing value, retrieval performance or a thesis result.

## C4A Execution Disposition (2026-08-30)

All nine materialised packets have now reached a terminal C4A disposition.
Four passed both independent literal-return audits, source-only conformance,
and the coordinator's canonical-card provenance audit:

- `C4A-RQ1B-V3-D1-W4-001`
- `C4A-RQ1B-V3-D1-W4-002`
- `C4A-RQ1B-V3-D1-W4-003`
- `C4A-RQ1B-V3-D1-W5-013`

Five were rejected at C4A because the two literal-valid builders jointly
omitted source evidence required to settle a slot under the v1.2 rule:

- `W1-001` and `W5-008`: unresolved shared omission after replacement-builder
  attempts;
- `W5-007`, `W5-015`, and `W5-020`: a named dependency/resource existed in
  the source but was jointly omitted, so a reviewer could not add new evidence
  during conformance.

Raw builder returns, including literal-audit failures, remain preserved under
`skill_benchmark/rq1b_v3_public_source_frame/c4a_v1_2_execution_2026-08-30/`.
The successful canonical cards passed
`validate_rq1b_v3_c4_canonical_card.py`; this proves only that the card uses
literal-valid builder evidence. It does not prove completeness, adequacy,
strict gold, or retrieval value.

The four admitted cards were materialised into C4B v2 key-blind review
inputs at
`skill_benchmark/rq1b_v3_public_source_frame/c4b_blind_review_wave_001_v2_2026-08-30/`:
24 C3-allowed prompt-card cases for each of two independently permuted
reviewer files. The blind-packet audit passed with zero source-identity or
sealed-target leaks. The C4A-card unpermutation key is deliberately separated
from the C5 sealed-target key, so C4B consensus cannot compare itself with the
construction target. C4B reviewer responses, C5 target reconciliation and C6
freeze are now recorded below.

## C4B--C6 Wave 001 Closure (2026-08-30)

The C4B v2 blind-packet audit passed before review: two reviewer files each
contained 24 distinct, source-deidentified prompt-card packets, and the C4A
unpermutation mapping remained separate from the C5 sealed-target key. Two
independent key-blind reviewers returned all 48 required judgments. One
reviewer response contained a non-exact selected-card quote; the original was
preserved, a fresh reviewer corrected that one anonymous packet without seeing
the original response, and the mechanical one-record amendment was re-audited.

The final C4B consensus passed with 14 strict singleton agreements and 10
non-singleton/no-consensus cases. C5 then compared only the 14 anonymous
singleton choices with the sealed construction target: all 14 were target
consistent; none mismatched. C6 verified candidate-source SHA-256 values, C1
and C3 ledger bindings, canonical-card/audit lineage, C3 allow status, prompt
binding, cue-risk agreement, C4B consensus and C5 reconciliation. It froze 14
strict **prompt cases** and excluded 10 cases, all with zero integrity
failures.

The unit distinction is material: 14 frozen cases occur across three parent
candidate compositions, but only one parent composition has all three target
skills and both direct/paraphrase variants frozen. The 14 cases carry 12
`high` and two `medium` residual-cue-risk annotations. They may support a
strict source-card curation audit with a cue stratum; they cannot be described
as implicit-semantic evidence, a 14-cluster cohort, a retrieval result, or a
field-effect result. The closure artifacts are under
`skill_benchmark/rq1b_v3_public_source_frame/c4b_blind_review_wave_001_v2_2026-08-30/`.
