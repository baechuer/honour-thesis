# RQ1b V3 Wave 031 C1--C3 Curation Closure

Date: 2026-08-30

## Scope and Boundary

This checkpoint closes a **curation-feasibility** sequence over two source-only
candidate compositions from the Wave 031 public-source amendment. It is not a
selector run, human annotation, information-field result, retrieval result, or
validity finding about RQ1b. It does not change the strict V3 frozen cohort.

## Frozen Inputs

- Wave 031 source amendment: 100 byte-distinct source artifacts.
- T0 source-only batches: 10 groups, with no prompt, intended winner, gold
  label, selector output, metric, or result available to reviewers.
- Only two groups advanced from T0 to C1: an orchestration-framework triad and
  a RAG-framework triad.

## Gate Outcomes

| Gate | Orchestration frameworks | RAG frameworks | Meaning |
| --- | --- | --- | --- |
| T0 | `READY_FOR_C1` | `READY_FOR_C1` | Structural reading could justify source-evidence construction only. |
| C1 | pass | pass | Literal source evidence supports a common broad envelope; this is not a strict label. |
| C2 | 0/6 prompts safe | 2/6 prompts safe | Most natural task requests leave multiple framework artifacts plausibly adequate. |
| C3 | not applicable | 2 cue-safe positions | Cue safety alone cannot repair missing candidate symmetry. |
| C4 | not eligible | not eligible | Strict adequacy requires all candidates under direct and paraphrase variants to pass the prior gates. |

## Decision

The orchestration composition is rejected as a strict-public-cluster candidate:
all six task-prompt positions had unsafe multi-adequacy risk. The RAG
composition retains two source/cue-safe positions but is also not eligible for
C4 because four of six positions were rejected at C2. No incomplete composition
may be treated as a strict singleton benchmark cluster.

## Interpretation

This is a negative feasibility observation about broad framework artifacts:
their natural boundaries commonly describe complementary implementations or
multiple adequate choices. It does **not** estimate retriever performance or
the effect of any information field. The strict V3 total therefore remains
**35 C1--C6-frozen compositions / 219 strict prompt cases**.

## Evidence

- `skill_benchmark/rq1b_v3_public_source_frame/d1_source_intake_wave_031_2026-08-30/source_only_triage/`
- `skill_benchmark/rq1b_v3_public_source_frame/d1_directed_discovery_wave_031_2026-08-30/`
- C2 ledger: `c2_prompt_construction_wave_031_2026-08-30/c2_draft_ledger_validated.jsonl`
- C3 final ledger: `c3_cue_control_wave_031r1_2026-08-30/c3_final_ledger.jsonl`

