# RQ1b V2+V3 Selector Execution Amendment

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `HISTORICAL_OR_SUPERSEDED`.** Retained for provenance and method history. Do not use its dated status, denominator, or result as the current RQ1 claim unless the canonical RQ1 index explicitly carries it forward. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Status: `COMPLETE / UNIFIED V2+V3 FINAL ANALYSIS / THESIS WRITE DEFERRED FOR REVIEW`

Date: 2026-08-30

## Purpose

Score only the newly admitted complete V3 triads, then reuse the completed V2
result files by verified artifact reference. The resulting rows form **one
final RQ1b field-removal experiment**, rather than two scientific estimators.
This avoids re-sending or re-scoring V2 texts while preserving source provenance
for later heterogeneity and integrity checks.

## Frozen Inputs

| Stratum | Existing state | Execution action |
| --- | --- | --- |
| Native V2 | 48 compositions, 87 strict routing families, 174 prompts and 1,392 completed rows per retriever | Reuse only after verifying the existing manifest, artifact hashes, row coverage and V2 freeze. |
| Imported V3 extension | 4 complete triads, 12 strict routing families, 24 prompts and 192 rows per retriever | Score newly, once for each retriever. |
| Partial V3 parents | 2 incomplete 4/6-case parents | Keep quarantined; never score or use in a denominator. |

The extension input is
`skill_benchmark/rq1b_final_public_corpus_v1/v2_v3_complete_triad_extension_2026-08-30/`.
It is revalidated with its source/hash compatibility builder before every run.

## Retrievers And Boundaries

1. **BM25:** local-only; runs only the 192 imported-V3 rows. It then emits a
   combined 1,584-row view containing V2 rows copied by reference and the new
   V3 rows.
2. **Qwen `text-embedding-v4`, 1024 dimensions:** local preflight first. It
   creates a text-id inventory for V3 cards and prompts, checks the dedicated
   V3 cache, and records the exact missing document/query text counts, local
   token proxy and no-retry request ceiling. It sends no text during preflight.
   The separately authorised execution then embedded only 96 rendered V3 cards
   and 24 V3 prompts. All 13 no-retry calls succeeded; embeddings and receipts
   are persisted in the dedicated V3 cache/output package.
3. **Unified estimator with provenance tags:** reporting uses all verified V2
   and V3 rows as one paired field-removal experiment. `native_v2_reused` and
   `imported_v3_new` remain row-level provenance tags only; they support audit
   and heterogeneity checks but are not separate main denominators.

## Field-Effect Interpretation

The unified matrix has exact `FULL + seven all-candidate masks` for every
strict prompt family. Its main estimator is `FULL - MASK(field)` over all 198
paired prompts, with direct/paraphrase and within-composition families averaged
before a 5,000-replicate composition-level paired bootstrap over the 46 scored
candidate compositions. This makes the experiment one field-availability test,
while avoiding pseudo-replication from several prompts in a single composition.

## Acceptance Criteria

- V2 reuse: original result manifest hashes, 1,392-row coverage, 87 families,
  174 prompt instances and V2 freeze all verify exactly.
- V3: 12 families, 24 prompts, 8 conditions, 192 unique family/prompt/condition
  rows; all candidates remain present across conditions.
- Unified experiment: 46 scored candidate compositions drawn from 52 frozen
  composition artifacts, 99 families, 198 prompts and 1,584 rows per
  retriever. The 1,392 V2 and 192 V3 rows retain provenance tags only.
- Qwen: no outgoing request without a new scope-specific authorisation;
  no automatic retry; first provider error stops execution; exact-text
  embeddings persist in a dedicated local V3 cache with receipts.

## Outputs

`skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_v3_extension_2026-08-30/`

The output directory will contain independent BM25/Qwen manifests, new V3
rows, reference-validated combined rows, stratum summaries and a local cost
ledger. It does not alter the original V2 output directories.

## Completed Execution Record

The exact authorised payload
`710406e2baddbea20546b0523a52f1dbdbe5e2049c9679096fb405d0eead9a35`
completed on 2026-08-30. The first sandbox-local DNS failure is retained at
`qwen_local_transport_failure_no_provider_contact/`; it made no provider
contact, produced no embedding and is not counted as a provider call. The
manual restricted-network execution then made 13/13 successful no-retry calls,
with 120 cache misses, zero cache hits and 20,843 provider tokens. It produced
192 new imported-V3 rows and a verified 1,584-row stratified package.

| Stratum / view | Prompt instances | Top-1 | MRR | Mean gold rank | Mean native margin |
| --- | ---: | ---: | ---: | ---: | ---: |
| Imported V3, `FULL` | 24 | 0.7917 | 0.8889 | 1.2500 | 0.0766 |
| Native V2 reused, `FULL` | 174 | 0.8563 | 0.9224 | 1.1782 | 0.1043 |
| Unified V2+V3 final experiment | 198 | 0.8485 | 0.9184 | 1.1869 | 0.1010 |

The unified paired analysis is authoritative for this final RQ1b corpus.
Across both retrievers, every composition-bootstrap 95% interval spans zero.
BM25 has its largest positive point estimates for use condition (+0.0226
Top-1) and input/precondition (+0.0163); Qwen has its largest positive point
estimate for workflow/procedure (+0.0109). These are directional, bounded
signals, not evidence that any isolated field is universally necessary.

The complete metric ledger additionally records absolute FULL/masked Top-1,
MRR, gold rank, native score margin, raw paired deltas, composition bootstrap
intervals and `1->0`/`0->1` transitions. The historical V2 joint-field groups
are reported separately using their frozen group-specific eligibility
intersections, not silently counted as all 87 families. Ledger:
`skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_final_result_ledger_2026-08-30/`.
