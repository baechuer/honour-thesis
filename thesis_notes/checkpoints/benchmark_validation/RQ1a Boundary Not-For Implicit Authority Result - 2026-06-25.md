# RQ1a Boundary / Not-For Implicit Authority Result - 2026-06-25

## Purpose

Record the completed RQ1a boundary/not-for field-isolation suite and the added implicit-authority prompt condition.

The key methodological change is that boundary prompts are no longer treated only as explicit "do not / avoid / not for" queries. The suite now separates:

- `direct`: explicit boundary or exclusion wording;
- `paraphrase`: same boundary with safer/reduced exact wording;
- `implicit_authority`: constrained-role prompts where scope or authority is implied by the requested artifact, such as an internal review note, triage packet, or evidence summary.

## Artifacts

- Suite: `skill_benchmark/rq1a_field_discriminability/boundary_not_for/`
- Generator: `skill_benchmark/rq1a_field_discriminability/boundary_not_for/build_strict_units.py`
- Prompt rows: `skill_benchmark/rq1a_field_discriminability/boundary_not_for/prompts.jsonl`
- Rubric summary: `skill_benchmark/rq1a_field_discriminability/boundary_not_for/rubric_summary.md`
- Analysis note: `skill_benchmark/rq1a_field_discriminability/boundary_not_for/implicit_authority_analysis.md`
- Main result: `skill_benchmark/outputs/rq1a_boundary_not_for_bm25_qwen_embedding_with_implicit.md`
- Machine result: `skill_benchmark/outputs/rq1a_boundary_not_for_bm25_qwen_embedding_with_implicit.json`
- Row-level result: `skill_benchmark/outputs/rq1a_boundary_not_for_bm25_qwen_embedding_with_implicit_rows.jsonl`

## Suite Status

| Item | Value |
|---|---:|
| Clusters | 50 |
| Skills per cluster | 3 |
| Prompt variants per cluster | 3 |
| Total prompt variants | 150 |
| Accepted strict rubric clusters | 50/50 |

## Main Result

The hidden-field baseline is `shared_context_only`; all three siblings are intentionally identical on selector-visible text, so tie-aware top-1 is `0.333`. The exposed-field condition is `shared_context_plus_field`, adding exactly one line: `Boundary / Not For: <skill-specific boundary>`.

| Retriever | Prompt subset | Hidden field top-1 | + boundary/not-for top-1 | Lift | MRR + field |
|---|---:|---:|---:|---:|---:|
| BM25 | Direct | 33.3% | 98.0% | +64.7pp | 0.990 |
| BM25 | Paraphrase | 33.3% | 90.0% | +56.7pp | 0.943 |
| BM25 | Implicit authority | 33.3% | 62.0% | +28.7pp | 0.800 |
| BM25 | Combined | 33.3% | 83.3% | +50.0pp | 0.911 |
| Qwen embedding | Direct | 33.3% | 84.0% | +50.7pp | 0.917 |
| Qwen embedding | Paraphrase | 33.3% | 82.0% | +48.7pp | 0.907 |
| Qwen embedding | Implicit authority | 33.3% | 58.0% | +24.7pp | 0.777 |
| Qwen embedding | Combined | 33.3% | 74.7% | +41.3pp | 0.867 |

Qwen embedding usage: 35 embedding API calls, approximately 57,784 embedded tokens.

## Interpretation

Boundary/not-for is supported as useful, but conditionally. It is strong when the prompt explicitly states the excluded action or guardrail, and remains positive under paraphrase. Under implicit-authority prompts, the field still improves above the hidden-field tie baseline, but the lift is much smaller.

Thesis implication:

> Boundary/not-for should be framed as a scope, authority, compatibility, or guardrail signal rather than as a simple positive matching field like input/precondition or output/artifact.

This result should be reported with the implicit-authority subset separated. The `combined` row is useful for a compact overall number, but it hides the key conclusion that implicit authority is harder than explicit negation.

## Files Updated

- `thesis_notes/current/RQ1/protocols/RQ1 Field Targeted Test Plan.md`
- `thesis_notes/current/Current Results Summary.md`
- `thesis_notes/current/Thesis Experiment Roadmap.md`
- `skill_benchmark/rq1a_field_discriminability/README.md`
- `thesis_latex/chapters/05_methodology.tex`
- `thesis_latex/chapters/06_results.tex`
- `thesis_latex/chapters/07_discussion.tex`
- `thesis_latex/chapters/08_conclusion.tex`
