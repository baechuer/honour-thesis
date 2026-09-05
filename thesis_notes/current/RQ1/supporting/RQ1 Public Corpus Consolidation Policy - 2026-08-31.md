# RQ1 Public Corpus Consolidation Policy

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `CURRENT_SUPPORTING`.** Use for source-registry provenance and counting policy only, not as the current scored result. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Status: `ACTIVE COUNTING AND FREEZE POLICY / NO NEW SELECTOR RUN`

## Decision

RQ1 public-source work has one canonical **source-composition registry**:
`skill_benchmark/rq1b_final_public_corpus_v1/composition_registry.jsonl`.
It contains **82 unique candidate compositions**: the 76 historical
cross-source C6 compositions plus six subsequently frozen direct-V3 C6
compositions, deduplicated by their sorted candidate-source hashes.

Every future public-cluster discovery, review, masking, or representation
construction must first resolve the proposed candidate set against this
registry. A source set already present is reused rather than reintroduced as a
new V2/V3 population. A genuinely new source set is appended only in a new,
explicitly frozen registry release; it is never silently added to an already
scored result.

## The Three Counts

| Count | Unit | Meaning | Permitted use |
| ---: | --- | --- | --- |
| 82 | candidate compositions | Complete deduplicated public-source registry | Intake, provenance, and future unified freeze frame; not a result denominator by itself. |
| 46 / 99 / 198 | scored compositions / strict routing families / prompts | The completed RQ1b public-card field-removal experiment | The only current public RQ1b selector-result denominator. |
| 87 / 174 | strict V2 routing families / prompts | Historical native-V2 subset before the complete V3 extension | Provenance and reuse accounting only; not a competing corpus version. |

The 52 frozen composition artifacts in the final card package are inputs to
the 99-family matrix. Only 46 composition units contribute valid paired
composition-bootstrap summaries. This is why the final scientific summary is
`46 scored compositions / 99 families / 198 prompts`, rather than 52 or 82.

## Rule For Future RQ1 Public Experiments

1. Start from all 82 registry compositions, not from a named historical wave.
2. Run one fixed, prompt/label-independent eligibility audit for the proposed
   intervention and retain its attrition ledger.
3. Freeze one named complete-case scoring subset before any selector runs.
   A composition may be in the 82-source registry but outside the scoring
   subset when it lacks strict singleton coverage, a valid mask, or complete
   paired-condition coverage.
4. Report both the source registry size and the scoring denominator, but never
   call them the same thing or pool different eligibility regimes.
5. After scoring starts, no new clusters are appended. Later discovery forms a
   new registry release and a separately frozen experiment, so results do not
   need retroactive count adjustments.

## Current Consequence

The complete-original document-removal audit begins from the 82-composition
registry conceptually, but its first residual gate did not produce a clean
scoring subset. It remains a closed feasibility audit and does not replace the
46/99/198 derivative-card result.
