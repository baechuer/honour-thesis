# Representation Field Ablation Results

This report tests which representation fields help retrieve the gold skill.

- Prompts: 137
- Ablations: 28

## Cumulative Field Ablations

| Scorer | Scale | Field Set | Top-1 | Accept Top-1 | Top-5 | MRR | Non-Core Top-1 | Visible Tokens |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `tfidf` | `core` | Description only | 72.3% | 72.3% | 95.6% | 0.824 | 0.0% | 5957 |
| `bm25` | `core` | Description only | 70.8% | 70.8% | 96.4% | 0.818 | 0.0% | 5957 |
| `tfidf` | `core` | Description + use conditions | 78.8% | 78.8% | 97.1% | 0.877 | 0.0% | 13126 |
| `bm25` | `core` | Description + use conditions | 81.8% | 81.8% | 97.1% | 0.888 | 0.0% | 13126 |
| `tfidf` | `core` | + input / preconditions | 76.6% | 76.6% | 97.1% | 0.861 | 0.0% | 18792 |
| `bm25` | `core` | + input / preconditions | 80.3% | 80.3% | 97.1% | 0.883 | 0.0% | 18792 |
| `tfidf` | `core` | + output artifacts | 77.4% | 77.4% | 98.5% | 0.872 | 0.0% | 22234 |
| `bm25` | `core` | + output artifacts | 83.2% | 83.2% | 98.5% | 0.901 | 0.0% | 22234 |
| `tfidf` | `core` | + workflow / procedure | 80.3% | 80.3% | 100.0% | 0.893 | 0.0% | 30931 |
| `bm25` | `core` | + workflow / procedure | 83.2% | 83.2% | 99.3% | 0.904 | 0.0% | 30931 |
| `tfidf` | `core` | + constraints / not-for | 77.4% | 77.4% | 99.3% | 0.875 | 0.0% | 36129 |
| `bm25` | `core` | + constraints / not-for | 78.8% | 78.8% | 99.3% | 0.882 | 0.0% | 36129 |
| `tfidf` | `core` | + dependencies / resources | 76.6% | 76.6% | 99.3% | 0.871 | 0.0% | 36369 |
| `bm25` | `core` | + dependencies / resources | 78.1% | 78.1% | 99.3% | 0.878 | 0.0% | 36369 |
| `tfidf` | `current_full` | Description only | 61.3% | 61.3% | 83.9% | 0.721 | 19.0% | 98433 |
| `bm25` | `current_full` | Description only | 66.4% | 66.4% | 91.2% | 0.771 | 8.8% | 98433 |
| `tfidf` | `current_full` | Description + use conditions | 70.1% | 70.1% | 91.2% | 0.802 | 8.8% | 272829 |
| `bm25` | `current_full` | Description + use conditions | 79.6% | 79.6% | 94.9% | 0.866 | 2.9% | 272829 |
| `tfidf` | `current_full` | + input / preconditions | 67.2% | 67.2% | 89.0% | 0.766 | 13.9% | 468875 |
| `bm25` | `current_full` | + input / preconditions | 80.3% | 80.3% | 95.6% | 0.869 | 1.5% | 468875 |
| `tfidf` | `current_full` | + output artifacts | 69.3% | 69.3% | 91.2% | 0.794 | 12.4% | 507087 |
| `bm25` | `current_full` | + output artifacts | 81.0% | 81.0% | 97.8% | 0.880 | 1.5% | 507087 |
| `tfidf` | `current_full` | + workflow / procedure | 73.7% | 73.7% | 94.2% | 0.831 | 7.3% | 665434 |
| `bm25` | `current_full` | + workflow / procedure | 80.3% | 80.3% | 98.5% | 0.886 | 1.5% | 665434 |
| `tfidf` | `current_full` | + constraints / not-for | 73.7% | 73.7% | 94.2% | 0.831 | 7.3% | 706385 |
| `bm25` | `current_full` | + constraints / not-for | 75.2% | 75.2% | 98.5% | 0.860 | 2.2% | 706385 |
| `tfidf` | `current_full` | + dependencies / resources | 73.7% | 73.7% | 94.9% | 0.829 | 8.0% | 885767 |
| `bm25` | `current_full` | + dependencies / resources | 75.9% | 75.9% | 98.5% | 0.864 | 1.5% | 885767 |

## Single-Field Checks

| Scorer | Scale | Field | Top-1 | Top-5 | MRR | Non-Core Top-1 | Visible Tokens |
|---|---|---|---:|---:|---:|---:|---:|

## Initial Interpretation

- On full scale with TF-IDF, `a4_workflow` is strongest at 73.7% top-1, compared with 61.3% for description-only.
- Treat these as local lexical ablations; they test representation content, not provider model strength.
- If a field adds little in this report, it may still matter for execution, downstream validation, or neural reranking.
