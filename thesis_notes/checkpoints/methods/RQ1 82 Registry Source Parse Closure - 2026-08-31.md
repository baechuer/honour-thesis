# RQ1 82-Registry Source Parse Closure

Status: `S0 COMPLETE / LOCAL SOURCE-ONLY / NO MASK OR SELECTOR`

## Scope

The canonical public-source registry contains 82 deduplicated candidate
compositions: 76 historical C6 compositions plus six direct-V3 C6 additions.
This closure parses the full original source material for all 82 compositions,
without prompts, gold labels, representations, retrieval, embeddings, masks,
or metrics.

## Result

| Item | Count |
| --- | ---: |
| Compositions | 82 |
| Original skill documents | 265 |
| Verified reused historical parses | 76 |
| Independently parsed direct-V3 compositions | 6 |
| Exact evidence spans | 1,860 |
| Hash/schema/line/quote audit failures | 0 |

The evidence parser records seven fields: use condition, input/precondition,
output artifact, workflow/procedure, success/verification, boundary/not-for,
and dependency/resource. A `PRESENT` field has contiguous, line-addressable
source evidence. This is a structural inventory, not an estimate of field
utility or routing performance.

## Artifacts

- Source packet and lineage manifest:
  `skill_benchmark/rq1_public_original_removal_v3_82_registry/source_packets/`
- Complete parsed ledger:
  `skill_benchmark/rq1_public_original_removal_v3_82_registry/parse_ledger/parse_ledger.json`
- Mechanical audit:
  `skill_benchmark/rq1_public_original_removal_v3_82_registry/audit/parse_audit.json`
- Packet builder and parser tooling:
  `skill_benchmark/scripts/materialize_rq1_original_removal_v3_82_packets.mjs`,
  `build_rq1_original_removal_v3_82_parse_ledger.mjs`,
  `validate_rq1_original_removal_v3_82_parse.mjs`,
  `canonicalize_rq1_original_removal_v3_82_parse.mjs`,
  `ingest_rq1_original_removal_v3_82_parse.mjs`, and
  `audit_rq1_original_removal_v3_82_parse.mjs`.

## Next Gate

No field-removal condition is eligible merely because a field is present. A
future S1 eligibility gate must decide whether each field value can be removed
without broadening or changing the candidate's task identity, then conduct a
fresh residual-cue audit before any scoring. The earlier 76-source audit shows
this is a real feasibility gate, not a formality.
