# RQ1b V2+V3 BM25 and Qwen Preflight Checkpoint

Date: 2026-08-30

Status: `LOCAL BM25 COMPLETE / QWEN PAYLOAD SEALED LOCALLY / EXTERNAL RUN NOT AUTHORISED`

## Completed Local Work

The V2+V3 execution runner revalidated the immutable four-triad extension,
then verified the completed V2 BM25 result manifest and artifact hashes before
reusing its 1,392 rows. It newly scored only the V3 extension's 12 strict
routing families, 24 prompts and eight conditions (192 rows) with local BM25.

| Output | Count | Result |
| --- | ---: | --- |
| Reused native V2 BM25 rows | 1,392 | Original manifest and rows/summary SHA-256 values verify exactly. |
| New imported V3 BM25 rows | 192 | 12 families x 2 prompts x 8 conditions; complete unique-key coverage. |
| Harmonised stratified BM25 rows | 1,584 | 1,392 `native_v2_reused` + 192 `imported_v3_new`; never treated as an undifferentiated primary denominator. |

The imported V3 `FULL` condition has Top-1 `0.750`, MRR `0.8681`, mean gold
rank `1.2917` and mean BM25 gold-minus-best-wrong margin `3.8464`. Its largest
all-complete-triad single-mask Top-1 changes are input/precondition `+0.2083`
and workflow/procedure `+0.1250` for `FULL - MASK`; they are descriptive
supplemental perturbation evidence over 24 prompt pairs, not a V2-style
field-eligibility-filtered claim.

## Qwen Preflight

No network call was made. The sealed Qwen payload contains only the new V3
rendered candidate-card texts and V3 query prompts; it does not resend any V2
text or reuse/recompute V2 rows.

| Payload item | New texts | Local lexical-token proxy | UTF-8 bytes |
| --- | ---: | ---: | ---: |
| Rendered V3 candidate cards | 96 | 13,081 | 92,643 |
| V3 prompts | 24 | 1,089 | 7,144 |
| Total | 120 | 14,170 | 99,787 |

The preflight has zero cache hits in its dedicated V3 cache and permits at
most 13 serial requests / 13 successful calls, batch size at most 10,
automatic retries `0`, to DashScope international
`text-embedding-v4`, 1024 dimensions. A fresh scope-specific authorisation is
required before execution. On execution the first provider error must stop the
run and request receipts plus exact-text embeddings persist locally.

## Files

- Runner: `skill_benchmark/scripts/run_rq1b_v2_v3_complete_triad_extension.py`
- BM25 result: `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_v3_extension_2026-08-30/bm25/`
- Qwen preflight: `skill_benchmark/rq1b_cross_source_public_benchmark/outputs/field_type_ablation_confirmatory_v2_v3_extension_2026-08-30/qwen_preflight/`
- Execution amendment: `thesis_notes/archive/RQ1/superseded-public-card/RQ1b V2 Plus V3 Selector Execution Amendment - 2026-08-30.md`
