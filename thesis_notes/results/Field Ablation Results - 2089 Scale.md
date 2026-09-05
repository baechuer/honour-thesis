# Field Ablation Results - 2089 Scale

Date: 2026-05-29

Purpose: Step 7 field ablation over representation content. This asks which information fields help retrieval, rather than only asking which architecture performs best.

## Run

Command:

```bash
python3 skill_benchmark/scripts/run_field_ablation_selectors.py --include-single
```

Outputs:

- `skill_benchmark/outputs/field_ablation_results.json`
- `skill_benchmark/outputs/field_ablation_results.md`

Scope:

- 85 prompts
- core scale and 2089-skill full scale
- local TF-IDF and BM25 selectors
- cumulative field sets and single-field checks

## Full-Scale Cumulative Results

TF-IDF:

| Field Set | Top-1 | Top-5 | MRR | Non-Core Top-1 | Visible Tokens |
|---|---:|---:|---:|---:|---:|
| Description only | 58.8% | 80.0% | 0.692 | 28.2% | 84,870 |
| Description + use conditions | 76.5% | 89.4% | 0.828 | 12.9% | 244,432 |
| + input/preconditions | 77.6% | 90.6% | 0.834 | 10.6% | 248,927 |
| + output artifacts | 85.9% | 92.9% | 0.890 | 7.1% | 286,349 |
| + workflow/procedure | 85.9% | 96.5% | 0.899 | 7.1% | 441,030 |
| + constraints/not-for | 78.8% | 95.3% | 0.861 | 7.1% | 480,543 |
| + dependencies/resources | 75.3% | 94.1% | 0.839 | 8.2% | 642,607 |

BM25:

| Field Set | Top-1 | Top-5 | MRR | Non-Core Top-1 | Visible Tokens |
|---|---:|---:|---:|---:|---:|
| Description only | 69.4% | 89.4% | 0.774 | 10.6% | 84,870 |
| Description + use conditions | 84.7% | 94.1% | 0.886 | 4.7% | 244,432 |
| + input/preconditions | 84.7% | 95.3% | 0.888 | 5.9% | 248,927 |
| + output artifacts | 88.2% | 96.5% | 0.916 | 2.4% | 286,349 |
| + workflow/procedure | 89.4% | 96.5% | 0.926 | 1.2% | 441,030 |
| + constraints/not-for | 78.8% | 97.7% | 0.870 | 2.4% | 480,543 |
| + dependencies/resources | 78.8% | 97.7% | 0.870 | 2.4% | 642,607 |

## Main Interpretation

The ablation strongly supports the representation-information claim:

- Description-only retrieval is much weaker at scale.
- Use conditions provide the largest early gain.
- Output artifacts provide the clearest additional top-1 gain.
- Workflow/procedure improves rank quality and top-5 recall, especially under BM25.
- Preconditions help modestly, mostly by reducing non-core false positives.
- Naively adding `not_for` text can hurt top-1 because lexical retrieval treats negative boundaries as positive matching text.
- Naively adding dependency/resource text can add noise and token cost. This supports treating dependency/resource information as targeted reranker evidence or a separate feature, not simply more text to concatenate.

## Single-Field Signal

Single-field full-scale results show that no individual field is sufficient:

- `use_when` is strongest as a single field: 77.6% TF-IDF top-1 and 80.0% BM25 top-1.
- `workflow` is also useful: 62.4% TF-IDF and 71.8% BM25.
- `preconditions`, `output`, `not_for`, and dependency/resource fields are weaker alone.
- Dependency/resource fields alone perform poorly and attract many non-core background/public matches.

## Thesis Implication

This is stronger than simply saying "structure-aware retrieval is better."

The result suggests:

> The most retrieval-critical fields are use conditions, outputs, and workflow/procedure. Preconditions provide smaller but useful disambiguation. Negative boundaries and dependency/resource information should be handled carefully because naive text concatenation can introduce retrieval noise.

This supports a design claim:

> Structure-aware representation should not merely expose more text. It should expose the right procedural fields and use field-aware scoring or reranking so that negative boundaries, dependencies, and resources do not swamp the core routing signal.

## Caveat

These are local lexical ablations, not provider model ablations. They test representation content under BM25/TF-IDF. The result should be interpreted alongside Qwen/provider runs and downstream validation.
