# RQ2a Stage 5 Confirmatory Completion Audit

Date: 2026-08-02

State: `COMPLETE / PASS / PENDING USER RESULTS REVIEW`

Thesis write: `NOT PERFORMED`

> **Post-audit addendum, 2026-08-02.** The state above records the controller's terminal state at the end of Stage 5. The user subsequently reviewed the bounded interpretation and instructed that the final RQ2a analysis be recorded in current Markdown and the thesis. A20 is now complete; see `thesis_notes/current/RQ2a Confirmatory Results and Analysis - 2026-08-02.md` and the Stage 7 thesis-integration checkpoint. The frozen analysis, cost, failure, and execution hashes below are unchanged.

## 1. Authorised execution identity

- Confirmatory packet SHA-256: `8766a9e3e2c6e682a1d795a7ae3ec3614d53bc30e1da42227e6e4f18b0f4828b`
- Execution seal SHA-256: `839367521039a41b422a6a3ee9bd69d0c62b2515f187c280d40a187c1674d924`
- Independent review SHA-256: `c1fc7e5413db7fb3f801d0679afafe49f63f92da1242503a5c005ced5d446095`
- Structured authorisation SHA-256: `d2b96498cf41bcba028220e5987e71064d2e492b2bfd793c2b5ca7bedef21769`
- Frozen protocol SHA-256: `70d29cd1c2fa74b73e875daafa7d973508c181f5f7a1da43c7eef6561a68bf0c`

The controller completed with `PASS` and `complete_pending_user_results_review`. It did not write to the thesis LaTeX or PDF.

## 2. Completion and quality gates

| Gate | Result |
|---|---|
| Confirmatory scope | 280 clusters, 600 prompts, three candidates |
| Primary condition matrix | 22/22 conditions |
| Primary rows | 13,200/13,200 unique aligned rows |
| Primary run rows | BM25 4,800; SkillRouter 3,000; Qwen 4,800; field-aware 600 |
| Warm verification | SkillRouter, Qwen, and field-aware scientific rows reproduce exactly |
| Run and analysis hashes | Pass |
| Paired prompt/cluster identities | Pass |
| Complete primary condition set | Pass |
| Statistical protocol | 10,000 cluster bootstraps; 10,000 paired sign-flips; full secondary-family Holm correction |
| Failure analysis | Complete, deterministic descriptive evidence only |
| Thesis write | Not performed; blocked pending user review |

## 3. Full condition matrix

Top-1 is cluster-weighted and tie-adjusted. MRR is prompt-weighted and tie-adjusted.

| Selector | Representation | Top-1 | MRR | Margin | Strict confusion | Tie rate |
|---|---|---:|---:|---:|---:|---:|
| BM25 | diluted 1x | 0.864 | 0.920 | 1.9058 | 0.127 | 0.023 |
| BM25 | diluted 2x | 0.863 | 0.919 | 1.9109 | 0.128 | 0.023 |
| BM25 | diluted 4x | 0.864 | 0.920 | 1.8888 | 0.127 | 0.023 |
| BM25 | fielded | 0.864 | 0.921 | 1.9082 | 0.127 | 0.023 |
| BM25 | flat | 0.843 | 0.911 | 1.8985 | 0.147 | 0.023 |
| BM25 | order-controlled | 0.864 | 0.921 | 1.9082 | 0.127 | 0.023 |
| BM25 | prose | 0.840 | 0.908 | 1.8944 | 0.152 | 0.023 |
| BM25 | shared-only | 0.333 | 0.611 | 0.0000 | 0.000 | 1.000 |
| Qwen field-aware uniform top two | fielded | 0.823 | 0.901 | 0.0436 | 0.145 | 0.057 |
| Qwen single-vector | diluted 1x | 0.778 | 0.876 | 0.0378 | 0.228 | 0.000 |
| Qwen single-vector | diluted 2x | 0.778 | 0.872 | 0.0369 | 0.232 | 0.000 |
| Qwen single-vector | diluted 4x | 0.763 | 0.867 | 0.0363 | 0.247 | 0.000 |
| Qwen single-vector | fielded | 0.757 | 0.863 | 0.0347 | 0.252 | 0.000 |
| Qwen single-vector | flat | 0.824 | 0.902 | 0.0427 | 0.185 | 0.000 |
| Qwen single-vector | order-controlled | 0.790 | 0.880 | 0.0410 | 0.223 | 0.000 |
| Qwen single-vector | prose | 0.782 | 0.873 | 0.0396 | 0.233 | 0.000 |
| Qwen single-vector | shared-only | 0.333 | 0.611 | 0.0000 | 0.000 | 1.000 |
| SkillRouter cross-encoder | diluted 2x | 0.942 | 0.967 | 3.6345 | 0.063 | 0.000 |
| SkillRouter cross-encoder | fielded | 0.951 | 0.973 | 3.7486 | 0.053 | 0.000 |
| SkillRouter cross-encoder | flat | 0.955 | 0.975 | 4.2650 | 0.048 | 0.000 |
| SkillRouter cross-encoder | prose | 0.946 | 0.969 | 4.0002 | 0.058 | 0.000 |
| SkillRouter cross-encoder | shared-only | 0.333 | 0.611 | 0.0000 | 0.000 | 1.000 |

## 4. Preregistered contrasts

| Family | Contrast | Top-1 difference | 95% cluster-bootstrap CI | Raw p | Holm p | At least 3pp practical support |
|---|---|---:|---:|---:|---:|---|
| Primary | Qwen fielded minus flat | -0.067 | [-0.099, -0.036] | 0.0002 | Not applicable | No |
| Secondary | BM25 fielded minus flat | +0.021 | [+0.010, +0.033] | 0.0008 | 0.0040 | No |
| Secondary | SkillRouter fielded minus flat | -0.004 | [-0.014, +0.006] | 0.5240 | 0.5240 | No |
| Secondary | Qwen fielded minus prose | -0.025 | [-0.060, +0.010] | 0.1594 | 0.3188 | No |
| Secondary | Field-aware minus Qwen fielded | +0.066 | [+0.021, +0.111] | 0.0051 | 0.0204 | Yes |
| Secondary | Qwen fielded minus diluted 2x | -0.021 | [-0.036, -0.006] | 0.0101 | 0.0303 | No |
| Secondary | Qwen fielded minus shared-only | +0.424 | [+0.380, +0.467] | 0.0001 | 0.0008 | Yes |
| Secondary | BM25 fielded minus shared-only | +0.531 | [+0.506, +0.555] | 0.0001 | 0.0008 | Yes |
| Secondary | SkillRouter fielded minus shared-only | +0.618 | [+0.599, +0.635] | 0.0001 | 0.0008 | Yes |

The primary positive organisation hypothesis is not supported. Field labels inside one Qwen vector reduce Top-1 relative to matched flat text. The frozen field-aware strategy recovers 6.6 percentage points relative to that fielded single-vector condition, but its descriptive Top-1 of 0.823 is nearly identical to flat Qwen at 0.824. It therefore demonstrates better use of field boundaries, not superiority over the strongest single-vector serialisation in this matrix.

## 5. Field-level descriptive slices

| Field | Qwen flat | Qwen fielded | Field-aware | Field-aware minus fielded |
|---|---:|---:|---:|---:|
| Use condition | 0.925 | 0.888 | 0.938 | +0.050 |
| Input/precondition | 0.913 | 0.888 | 0.900 | +0.013 |
| Output artifact | 0.963 | 0.950 | 0.917 | -0.033 |
| Workflow/procedure | 0.638 | 0.600 | 0.658 | +0.058 |
| Dependency/resource | 0.963 | 0.963 | 0.771 | -0.192 |
| Boundary/not-for | 0.683 | 0.625 | 0.739 | +0.114 |
| Success/verification | 0.688 | 0.388 | 0.838 | +0.450 |

These slices are descriptive and not separately multiplicity-tested. They suggest that uniform top-two is especially useful for success/verification and boundary information, while it can suppress strong dependency and output signals. This heterogeneity is important for interpretation and later RQ2b design.

## 6. Cost, latency, and persistence

| Primary run | New API calls | Provider tokens | Construction wall | Online time per prompt | Total wall |
|---|---:|---:|---:|---:|---:|
| BM25 | 0 | 0 | 0.000s | 0.001100s | 0.945s |
| Qwen single-vector | 590 | 1,175,784 | 1,085.293s | 0.002869s | 1,087.359s |
| Qwen field-aware | 77 | 13,583 | 203.259s | 0.002398s | 204.760s |
| SkillRouter cross-encoder | 0 | 0 | 0.000s | 11.099921s | 6,666.917s |

- Guard totals: 667 attempts, 667 successes, 6,661 unique new texts.
- Attempt audit: all 667 records are `complete`, use the DashScope international embeddings endpoint, `text-embedding-v4`, and 1,024 dimensions; 590 are document batches and 77 are field-component batches. Every record has `plaintext_persisted=false`.
- Token totals: 1,130,034 local audit tokens and 1,189,367 provider tokens.
- Query transfer: zero; all 600 query embeddings were cache hits.
- Standard-list-price estimate: USD 0.08325569 at the frozen USD 0.07 per million token snapshot, below USD 0.11.
- Persistent Qwen embedding cache: 251,568,857 bytes across 9,211 files.
- Persistent SkillRouter score cache: 5,732,097 bytes across 9,750 files.
- Warm verification made zero provider calls and zero new SkillRouter forward passes.

The Qwen construction cost is paid once and reused; cached online scoring is milliseconds per prompt. The uncached SkillRouter run is much more accurate but took about 11.10 seconds per prompt locally. Cached SkillRouter lookup is fast, but that warm lookup is not the cost of scoring a novel query-candidate pair.

## 7. Descriptive failure decomposition

| Category | Prompt count |
|---|---:|
| Qwen fielded helps over flat | 21 |
| Qwen fielded harms versus flat | 61 |
| Qwen fielded and flat both fail | 90 |
| Field-aware recovers a Qwen fielded failure | 84 |
| Field-aware harms a Qwen fielded success | 54 |

This is descriptive supporting evidence. It must not be presented as a separately preregistered inferential family.

## 8. Completed metadata correction

`controller_state.json` correctly recorded the final state, completed steps, matrix, guard totals, warm digests, output hashes, and completion time, but retained stale `failed_step` and `failure` values from the superseded first attempt. This inconsistency has now been corrected without rerunning or changing scientific evidence:

- the original state is preserved unchanged as `metadata_corrections/controller_state_before_terminal_cleanup.json`, SHA-256 `19e3c6daeef1ac627c1604943d8783bcff74e932c69a1df0ddb50a647ce69706`;
- the corrected terminal state removes only `failed_step` and `failure`, SHA-256 `7719d9aa1a383b443f1864a2dca126b8c56e13dae7178c2008a87f6160840560`;
- `metadata_corrections/terminal_state_cleanup.json`, SHA-256 `461d31b8d61e2b446dbad3837660b34241957f3be34fb03b90092e830873890c`, records the reason, before/after hashes, removed values, implementation hashes, test results, zero external requests, and no thesis write;
- the controller now clears failure-only fields before a fresh run and before a successful terminal transition;
- controller, stage-gate, and selector-adapter regression suites all pass;
- the exact controller used during the authorised execution is archived as `metadata_corrections/run_rq2a_confirmatory_sequence.executed_sealed.py` and matches the execution seal SHA-256 `ba60ff5efe55a76dde110ec394ea52b97cca9be5e7a8a1f4de8ec8f6724b9f77`.

The current hygiene-fixed controller has a different source hash and therefore cannot be used under the completed run's old seal. Any future rerun requires a new freeze, seal, review, and authorisation. The analysis, cost, and failure-report hashes remain unchanged.

## 9. Claim boundary and next gate

The confirmatory evidence supports three narrow statements for review:

1. The routing-relevant operational facts strongly improve selection over shared context without those facts.
2. Explicit field headings alone do not reliably improve retrieval and can harm a pooled dense representation.
3. A retrieval strategy that explicitly uses field boundaries can recover that penalty for some fields, but the frozen uniform top-two rule does not outperform the best flat Qwen representation overall.

These statements are not yet thesis claims. The user must review the evidence and approve the interpretation before A20 or any thesis LaTeX/PDF result update begins.

## 10. Evidence locations

- Analysis: `skill_benchmark/outputs/rq2a_matched_content/analysis/confirmatory-complete-v1/analysis.json`, SHA-256 `189d6b20b091e2f2d3bd30f168355ccf2a73efa3eef3b082075725040fec0ce7`.
- Cost ledger: `skill_benchmark/outputs/rq2a_matched_content/analysis/confirmatory-complete-cost-v1/cost_ledger.json`, SHA-256 `980af3ff9c9106d7f43d029b69aa5a1bb07515faf2e15b0b96e70bca5332cdec`.
- Failure report: `skill_benchmark/outputs/rq2a_matched_content/analysis/confirmatory-failures-v1/failure_report.json`, SHA-256 `a0e96747f544904d424bf6fe83a656bd3b27533b4e2b2c9b8166fb91a8c6d155`.
- Controller state: `skill_benchmark/outputs/rq2a_matched_content/analysis/confirmatory-controller-v1/controller_state.json`.
- Primary and warm rows: `skill_benchmark/outputs/rq2a_matched_content/confirmatory/`.
