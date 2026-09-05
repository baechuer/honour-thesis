# RQ1b V2 Plus V3 Complete-Triad Integration Checkpoint

Date: 2026-08-30

Status: `LOCAL MATERIALISATION AND REBUILD CHECK PASS / NO SELECTOR RUN`

## Decision

Clean direct V3 C6 accounting before any merge. Only the four V3 parent triads
with 6/6 strict target-by-direct/paraphrase cases are admitted to a new
V2-compatible extension. The two four-case parents are quarantined rather than
repaired or made asymmetric.

## Evidence

- Builder: `skill_benchmark/scripts/build_rq1b_v2_v3_complete_triad_extension.py`
- Output: `skill_benchmark/rq1b_final_public_corpus_v1/v2_v3_complete_triad_extension_2026-08-30/`
- Verification: `python3 skill_benchmark/scripts/build_rq1b_v2_v3_complete_triad_extension.py --check`
- Result: 4 imported triads, 12 strict routing families, 24 prompts, 32 V3
  condition files, and 2 quarantined partial parents.

The local validator verifies V3 C6 card/audit/consensus hashes against source
artifacts; resolves every C6 prompt SHA-256 to its final C2 prompt text;
checks C5 label-to-source mappings; checks selected-card/gold binding; checks
three target-by-direct/paraphrase pairs; and validates the exact seven-field
schema used by V2.

## Future Matrix

| Stratum | Compositions | Strict families | Prompts |
| --- | ---: | ---: | ---: |
| Native V2 completed result | 48 | 87 | 174 |
| Imported V3 extension, unscored | 4 | 12 | 24 |
| Harmonised future run | 52 | 99 | 198 |

The eight conditions yield 1,584 rows per retriever. This checkpoint creates
no external transfer, embedding, selector score, metric or thesis finding.
Native V2 must remain separately reportable in any later run.
