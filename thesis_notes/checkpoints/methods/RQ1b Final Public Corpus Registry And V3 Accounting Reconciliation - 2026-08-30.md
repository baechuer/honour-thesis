# RQ1b Final Public Corpus Registry And V3 Accounting Reconciliation

Date: 2026-08-30

Status: `PASS / FINAL STRATIFIED REGISTRY / V3 COUNT CORRECTED / NO SCORE POOLING`

## Decision

`skill_benchmark/rq1b_final_public_corpus_v1/` is the canonical final
provenance and eligibility registry for the RQ1b public-skill work. It is a
registry, not a new benchmark run. Its generated artifacts are:

- `composition_registry.jsonl`: one record per candidate-set source-hash
  signature, with all applicable stratum membership;
- `summary.json`: machine-readable counts, source hashes and claim boundary;
- `README.md` and `INTEGRITY_REPORT.md`: reporting and non-pooling rules.

The deterministic builder is
`skill_benchmark/scripts/build_rq1b_final_public_registry.py`. It passed both
`--write` and `--check` on 2026-08-30.

## Final Accounting

| Stratum | Recomputed unit count | Permitted use |
| --- | ---: | --- |
| Historical cross-source C6 | 76 candidate compositions / 408 strict prompt cases | Historical public-source and curation provenance. |
| V2 field-card availability ablation | 48 active compositions / 128 routing families | V2 scored subset: 87 strict-preserved families and 174 prompts. |
| Direct V3 C6 records | 6 parent compositions / 32 strict prompt cases | Fresh source-frame curation only. Four compositions are complete; two are partial. |
| Unified source-hash registry | 82 unique candidate compositions | Provenance inventory only. |

V2 active compositions are wholly contained in the historical cross-source
source set. The six direct V3 C6 candidate sets are distinct by their sorted
source SHA-256 signatures, yielding the 82-composition union.

## V3 Correction

Earlier V3 prose stated `37 compositions / 231 strict prompt cases`. The
direct V3 C6 files are the relevant reproducible records and contain 32 cases
across six parent compositions. The earlier count reused the historical
cross-source `34 / 213` curation state and incremented it with later V3 waves.
It is therefore not a valid V3 source-frame cohort total. Historical files are
preserved unchanged; the current trackers link to this correction rather than
silently overwriting their audit history.

## Interpretation Guardrails

- No V2 selector result may be pooled with V3 C6 curation-only cases.
- The V2.1 joint-mask amendment is a V2 subset and is not an additional public
  corpus.
- The 82-composition provenance union is not 82 independent scored routing
  tasks and must not be presented as that.
- The two partial V3 compositions cannot enter a complete-composition selector
  denominator unless a later frozen amendment explicitly authorises a
  case-level analysis.
- Wave 039 discovery material has no C1 permission and is outside this final
  registry.

## Verification

```zsh
python3 skill_benchmark/scripts/build_rq1b_final_public_registry.py --check
```

