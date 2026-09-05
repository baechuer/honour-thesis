# Public Original Skill Source Correction - 2026-06-23

## Decision

For final public-gold benchmark reporting, imported public skills must use the upstream public `SKILL.md` artifact stored at `skill_benchmark/skills/public_imported_background/<skill>/source/SKILL.original.md` as the public skill source of truth.

The top-level normalized wrapper at `skill_benchmark/skills/public_imported_background/<skill>/SKILL.md` is retained for import provenance, source URLs, license notes, and background-scale bookkeeping. It should not be treated as the final full public skill body for public-gold comparisons.

## Reason

The wrapper was introduced when public skills were first imported as background scale distractors. It normalizes provenance and dependency/resource signals and prevents broad public skills from silently becoming clean controlled-core skills.

Public-gold later changed the role of selected public imports: those skills became gold-label targets. In that role, the benchmark should compare against the publicly available skill artifact itself, not the normalized wrapper.

## Current Implementation Status

The local source pipeline was corrected on 2026-06-23.

- `run_offline_selectors.load_full_skill_texts()` now calls `full_skill_source_path()`.
- For public imports, `full_skill_source_path()` resolves to `source/SKILL.original.md` when that file exists.
- For non-public controlled/generated skills, full text remains the authored top-level `SKILL.md`.
- `export_skill_representations.py` now keeps stable wrapper skill ids for label alignment, but uses the public original description and public original sections/body for R1/R2/R3 text when `source/SKILL.original.md` exists.
- `generate_public_style_controlled_expansion.py` was also updated after this source correction so the 32 public-style controlled skills are longer and messier public-document-style artifacts while preserving the intended use/input/output/procedure/dependency information.
- The local representation manifest was rebuilt after this correction.
- The local crossed lexical BM25/TF-IDF matrix was rerun after this correction.

Controlled-skill rows are not affected by the public-original override, because controlled skills' top-level `SKILL.md` files are the authored source artifacts.

## Refreshed Local Outputs

- Rebuilt representations: `skill_benchmark/representations/manifest.json`.
- Integrity check: `skill_benchmark/outputs/benchmark_integrity_report.md` and `.json`.
- Refreshed crossed lexical matrix: `skill_benchmark/outputs/frozen_v0_4_crossed_lexical_matrix.md` and `.json`.

Refreshed strict top-1 rows:

| Stratum | Retriever | R1 | R2/I3H | Full/I2 |
|---|---|---:|---:|---:|
| Controlled | BM25 | 55.1% | 58.0% | 66.5% |
| Controlled | TF-IDF | 52.6% | 59.6% | 69.4% |
| Public-gold | BM25 | 55.6% | 54.9% | 59.0% |
| Public-gold | TF-IDF | 56.9% | 50.7% | 48.6% |

## Remaining Caveat

Existing provider/Qwen and SkillRouter rows that were generated before this correction should still be treated as wrapper-era or pre-regeneration historical rows until rerun under the corrected source policy. Do not spend on those reruns until the corpus/source policy is intentionally frozen.

Keep wrapper files on disk for provenance unless a new benchmark version explicitly removes them.
