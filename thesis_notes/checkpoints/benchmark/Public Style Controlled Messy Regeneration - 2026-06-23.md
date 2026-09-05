# Public Style Controlled Messy Regeneration - 2026-06-23

## Decision

The public-style controlled skills should remain controlled enough to support gold labels and near-neighbour confusability, but their skill documents should look less like repeated benchmark schemas and more like public skill documentation.

This stratum is a bridge between:

- the controlled benchmark, where information fields are intentionally explicit for causal testing; and
- imported public skills, where task/use/input/output/procedure/dependency information is present but embedded in mixed prose, examples, headings, metadata, and operational notes.

## Change

Updated `skill_benchmark/scripts/generate_public_style_controlled_expansion.py`.

The regenerated 32 public-style controlled skills now include:

- longer public-document-style bodies;
- varied public-style headings;
- frontmatter tags and category metadata;
- prose routing notes;
- loose clue/result tables;
- YAML handoff snippets;
- sibling-skill confusion notes;
- examples and less-ideal request handling;
- operational anchors such as files, pages, rows, logs, screenshots, source snippets, or model/dataset identifiers.

The generator no longer presents the information as one repeated clean schema, but each skill still preserves the intended use conditions, inputs, outputs, procedure, boundaries, and dependencies.

## Corpus Audit

After regeneration:

| Corpus | Files | Mean rough words | Median rough words | Min | Max | Procedural signal |
|---|---:|---:|---:|---:|---:|---:|
| Public-style controlled | 32 | 741.5 | 738.0 | 704 | 796 | 100.0% |
| Public originals | 460 | 1196.3 | 1143.0 | 72 | 5205 | 95.2% |

This does not make the public-style controlled stratum identical to imported public skills. It makes it closer in document shape while preserving controlled gold labels.

## Verification

- Regenerated 8 clusters, 32 skills, and 64 public-style controlled prompts.
- Rebuilt representations: 2433 R1 rows, 2433 R2 rows, 2433 R3 rows, and 62032 R4 edges.
- Integrity check passed: 245 prompts and 2433 skills resolve.
- Verified all 460 imported public full-text paths resolve to `source/SKILL.original.md`.

## Local Sanity Matrix

Refreshed BM25/TF-IDF rows after regeneration:

| Stratum | Retriever | R1 Top-1 | R2/I3H Top-1 | Full/I2 Top-1 | R1 R@20 | R2 R@20 | Full R@20 |
|---|---|---:|---:|---:|---:|---:|---:|
| Controlled | BM25 | 55.1% | 58.0% | 66.5% | 93.9% | 98.0% | 98.4% |
| Controlled | TF-IDF | 52.6% | 59.6% | 69.4% | 91.4% | 95.5% | 97.5% |
| Public-gold | BM25 | 55.6% | 54.9% | 59.0% | 87.5% | 97.2% | 99.3% |
| Public-gold | TF-IDF | 56.9% | 50.7% | 48.6% | 92.4% | 94.4% | 96.5% |

## Interpretation

The messier public-style controlled skills still preserve routing-critical information, but full-source lexical retrieval is now very strong on controlled rows. This is useful rather than bad: it makes I2/full a serious comparator and forces the thesis to discuss cost and context trade-offs instead of treating full documents as a weak baseline.

Provider/Qwen and SkillRouter rows generated before this regeneration remain historical until rerun under the corrected corpus/source policy.
