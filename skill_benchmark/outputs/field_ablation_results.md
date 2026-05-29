# Representation Field Ablation Results

This report tests which representation fields help retrieve the gold skill.

- Prompts: 85
- Ablations: 56

## Cumulative Field Ablations

| Scorer | Scale | Field Set | Top-1 | Accept Top-1 | Top-5 | MRR | Non-Core Top-1 | Visible Tokens |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `tfidf` | `core` | Description only | 75.3% | 75.3% | 95.3% | 0.841 | 0.0% | 4026 |
| `bm25` | `core` | Description only | 75.3% | 75.3% | 96.5% | 0.845 | 0.0% | 4026 |
| `tfidf` | `core` | Description + use conditions | 87.1% | 87.1% | 97.7% | 0.925 | 0.0% | 9822 |
| `bm25` | `core` | Description + use conditions | 84.7% | 84.7% | 98.8% | 0.901 | 0.0% | 9822 |
| `tfidf` | `core` | + input / preconditions | 85.9% | 85.9% | 97.7% | 0.916 | 0.0% | 14317 |
| `bm25` | `core` | + input / preconditions | 85.9% | 85.9% | 98.8% | 0.912 | 0.0% | 14317 |
| `tfidf` | `core` | + output artifacts | 88.2% | 88.2% | 100.0% | 0.937 | 0.0% | 17073 |
| `bm25` | `core` | + output artifacts | 88.2% | 88.2% | 98.8% | 0.926 | 0.0% | 17073 |
| `tfidf` | `core` | + workflow / procedure | 91.8% | 91.8% | 100.0% | 0.955 | 0.0% | 23801 |
| `bm25` | `core` | + workflow / procedure | 90.6% | 90.6% | 98.8% | 0.941 | 0.0% | 23801 |
| `tfidf` | `core` | + constraints / not-for | 83.5% | 83.5% | 100.0% | 0.907 | 0.0% | 27973 |
| `bm25` | `core` | + constraints / not-for | 81.2% | 81.2% | 98.8% | 0.890 | 0.0% | 27973 |
| `tfidf` | `core` | + dependencies / resources | 83.5% | 83.5% | 100.0% | 0.907 | 0.0% | 28213 |
| `bm25` | `core` | + dependencies / resources | 81.2% | 81.2% | 98.8% | 0.890 | 0.0% | 28213 |
| `tfidf` | `current_full` | Description only | 60.0% | 60.0% | 78.8% | 0.694 | 25.9% | 96502 |
| `bm25` | `current_full` | Description only | 69.4% | 69.4% | 89.4% | 0.772 | 11.8% | 96502 |
| `tfidf` | `current_full` | Description + use conditions | 74.1% | 74.1% | 89.4% | 0.813 | 15.3% | 269525 |
| `bm25` | `current_full` | Description + use conditions | 84.7% | 84.7% | 95.3% | 0.885 | 4.7% | 269525 |
| `tfidf` | `current_full` | + input / preconditions | 76.5% | 76.5% | 89.4% | 0.825 | 12.9% | 274020 |
| `bm25` | `current_full` | + input / preconditions | 84.7% | 84.7% | 95.3% | 0.890 | 7.1% | 274020 |
| `tfidf` | `current_full` | + output artifacts | 82.3% | 82.3% | 91.8% | 0.871 | 11.8% | 311442 |
| `bm25` | `current_full` | + output artifacts | 88.2% | 88.2% | 96.5% | 0.916 | 3.5% | 311442 |
| `tfidf` | `current_full` | + workflow / procedure | 84.7% | 84.7% | 95.3% | 0.891 | 8.2% | 466123 |
| `bm25` | `current_full` | + workflow / procedure | 89.4% | 89.4% | 97.7% | 0.927 | 2.4% | 466123 |
| `tfidf` | `current_full` | + constraints / not-for | 77.6% | 77.6% | 94.1% | 0.851 | 8.2% | 505636 |
| `bm25` | `current_full` | + constraints / not-for | 78.8% | 78.8% | 97.7% | 0.872 | 3.5% | 505636 |
| `tfidf` | `current_full` | + dependencies / resources | 75.3% | 75.3% | 94.1% | 0.833 | 11.8% | 685009 |
| `bm25` | `current_full` | + dependencies / resources | 78.8% | 78.8% | 97.7% | 0.871 | 2.4% | 685009 |

## Single-Field Checks

| Scorer | Scale | Field | Top-1 | Top-5 | MRR | Non-Core Top-1 | Visible Tokens |
|---|---|---|---:|---:|---:|---:|---:|
| `tfidf` | `core` | Single: description | 75.3% | 95.3% | 0.841 | 0.0% | 4026 |
| `bm25` | `core` | Single: description | 75.3% | 96.5% | 0.845 | 0.0% | 4026 |
| `tfidf` | `core` | Single: use_when | 82.3% | 97.7% | 0.895 | 0.0% | 6419 |
| `bm25` | `core` | Single: use_when | 81.2% | 96.5% | 0.867 | 0.0% | 6419 |
| `tfidf` | `core` | Single: preconditions | 47.1% | 77.6% | 0.592 | 0.0% | 5116 |
| `bm25` | `core` | Single: preconditions | 45.9% | 70.6% | 0.562 | 0.0% | 5116 |
| `tfidf` | `core` | Single: output | 63.5% | 87.1% | 0.729 | 0.0% | 3375 |
| `bm25` | `core` | Single: output | 62.4% | 83.5% | 0.721 | 0.0% | 3375 |
| `tfidf` | `core` | Single: workflow | 76.5% | 95.3% | 0.857 | 0.0% | 7349 |
| `bm25` | `core` | Single: workflow | 75.3% | 90.6% | 0.829 | 0.0% | 7349 |
| `tfidf` | `core` | Single: not_for | 27.1% | 61.2% | 0.414 | 0.0% | 4796 |
| `bm25` | `core` | Single: not_for | 17.6% | 52.9% | 0.341 | 0.0% | 4796 |
| `tfidf` | `core` | Single: dependencies/resources | 40.0% | 65.9% | 0.518 | 0.0% | 864 |
| `bm25` | `core` | Single: dependencies/resources | 34.1% | 62.4% | 0.469 | 0.0% | 864 |
| `tfidf` | `current_full` | Single: description | 60.0% | 78.8% | 0.694 | 25.9% | 96502 |
| `bm25` | `current_full` | Single: description | 69.4% | 89.4% | 0.772 | 11.8% | 96502 |
| `tfidf` | `current_full` | Single: use_when | 77.6% | 87.1% | 0.819 | 11.8% | 194256 |
| `bm25` | `current_full` | Single: use_when | 80.0% | 92.9% | 0.846 | 1.2% | 194256 |
| `tfidf` | `current_full` | Single: preconditions | 30.6% | 52.9% | 0.415 | 51.8% | 25788 |
| `bm25` | `current_full` | Single: preconditions | 31.8% | 52.9% | 0.421 | 48.2% | 25788 |
| `tfidf` | `current_full` | Single: output | 44.7% | 72.9% | 0.568 | 41.2% | 58715 |
| `bm25` | `current_full` | Single: output | 48.2% | 71.8% | 0.595 | 27.1% | 58715 |
| `tfidf` | `current_full` | Single: workflow | 62.4% | 82.3% | 0.711 | 25.9% | 175975 |
| `bm25` | `current_full` | Single: workflow | 70.6% | 89.4% | 0.788 | 5.9% | 175975 |
| `tfidf` | `current_full` | Single: not_for | 18.8% | 38.8% | 0.283 | 41.2% | 60810 |
| `bm25` | `current_full` | Single: not_for | 17.6% | 44.7% | 0.305 | 20.0% | 60810 |
| `tfidf` | `current_full` | Single: dependencies/resources | 12.9% | 31.8% | 0.208 | 68.2% | 200652 |
| `bm25` | `current_full` | Single: dependencies/resources | 9.4% | 18.8% | 0.130 | 84.7% | 200652 |

## Initial Interpretation

- On full scale with TF-IDF, `a4_workflow` is strongest at 84.7% top-1, compared with 60.0% for description-only.
- Treat these as local lexical ablations; they test representation content, not provider model strength.
- If a field adds little in this report, it may still matter for execution, downstream validation, or neural reranking.
