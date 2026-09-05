# RQ1b V2+V3 Qwen Extension Result

Date: 2026-08-30

## Scope And Boundary

This checkpoint records the completed Qwen single-vector selector extension
over four newly admitted complete V3 public-skill triads and its final unified
analysis with V2. The combined package retains `native_v2_reused` and
`imported_v3_new` as provenance tags, but the final scientific estimator uses
both as one experiment.

The authoritative output is
`skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_v3_extension_2026-08-30/qwen/`.

## Authorised External Execution

- Payload SHA-256: `710406e2baddbea20546b0523a52f1dbdbe5e2049c9679096fb405d0eead9a35`
- Endpoint/model: DashScope international `text-embedding-v4`, 1024 dimensions.
- Transferred texts: 96 rendered V3 candidate cards plus 24 V3 prompts.
- Provider execution: 13 request attempts, 13 successful calls, zero automatic retries.
- Provider usage reported: 20,843 tokens.
- Cache outcome: 120 V3 cache misses before execution; all exact-text embeddings persisted after success.
- Local-only preflight proxy: 14,170 lexical tokens and 99,787 UTF-8 bytes.

The initial sandbox-local DNS failure was archived at
`.../qwen_local_transport_failure_no_provider_contact/`. It had no provider
contact, no embedding, no result row and no charge. The subsequently executed
restricted-network run is the 13-call provider execution reported above.

## Integrity Checks

- Qwen manifest status: `RQ1B_V2_V3_EXTENSION_QWEN_EXTERNAL_RUN_MANIFEST`.
- New V3 rows: 192 unique `(routing family, prompt variant, condition)` keys.
- V2 references: 1,392 verified frozen rows.
- Harmonised package: 1,584 unique rows: 192 `imported_v3_new` and 1,392
  `native_v2_reused`.
- V3 row artifact SHA-256: `5437840109475782f336fb4714372f0840a2f9d071f8ab3ef27e0878929e1802`.
- Combined row artifact SHA-256: `5832fc2cf55f9eba92dfbe56eccb021e71ff6b7be2d0d3243c31fe833789761b`.

## Extension Results

| Stratum / view | Prompt instances | Top-1 | MRR | Mean gold rank | Mean gold-minus-best-wrong margin |
| --- | ---: | ---: | ---: | ---: | ---: |
| Imported V3 `FULL` | 24 | 0.7917 | 0.8889 | 1.2500 | 0.0766 |
| Native V2 reused `FULL` | 174 | 0.8563 | 0.9224 | 1.1782 | 0.1043 |
| Unified V2+V3 final experiment | 198 | 0.8485 | 0.9184 | 1.1869 | 0.1010 |

## Unified Final Experiment

The final experiment is 46 scored candidate compositions drawn from 52 frozen
composition artifacts, with 99 strict routing families, 198 prompts and eight
candidate-synchronous conditions. Within each composition, paired effects are
averaged across its families and direct/paraphrase prompts before a
5,000-replicate composition-level bootstrap. The complete final analysis is at
`skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_v3_final_2026-08-30/`.

All single-field Top-1 and MRR bootstrap intervals include zero for both BM25
and Qwen. BM25's largest positive Top-1 point estimate is use condition
(`+0.0226`), followed by input/precondition (`+0.0163`); Qwen's is
workflow/procedure (`+0.0109`). The result therefore supports only bounded,
directional field-availability evidence in this natural public-artifact corpus,
not a universal independent contribution of any isolated field.

## Complete Metric Ledger

The final local-only metric ledger reports absolute and paired Top-1, MRR,
gold-rank and native-margin values, composition-level bootstrap intervals, and
Top-1 transition counts for both the unified single-field experiment and the
separately scoped V2 joint-group study. The latter uses its frozen
group-eligibility intersections rather than all mechanically materialised rows.
Authoritative ledger:
`skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_final_result_ledger_2026-08-30/`.

## Thesis Boundary

The result is recorded in method/progress trackers but deliberately not written
to thesis LaTeX or PDF pending user review.
