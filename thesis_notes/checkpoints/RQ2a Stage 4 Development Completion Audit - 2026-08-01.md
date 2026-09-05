# RQ2a Stage 4 Development Completion Audit

Date: 2026-08-01

Status: **IMPLEMENTATION AND DEVELOPMENT GOAL COMPLETE; CONFIRMATORY STUDY NOT STARTED**

## Scope Of This Audit

This audit checks the active user goal: specify RQ2a before implementation; build and approve the representations; prepare the selectors; begin and complete a development experiment; provide an initial result review with justified metrics; record every stage in the trackers; stay within RQ2a; and do not write unreviewed results into the thesis.

It does **not** claim that RQ2a has a confirmatory scientific answer. The confirmatory split remains untouched and requires separate explicit authorisation.

## Requirement-By-Requirement Evidence

| User requirement | Authoritative evidence | Audit result |
|---|---|---|
| Start from a tracker/spec with explicit requirements and completion criteria | `thesis_notes/current/RQ2a Execution Protocol and Run Ledger - 2026-07-26.md`; `skill_benchmark/rq2a_matched_content/protocol.json`; frozen `analysis_spec.json` | **PROVED** |
| Build the RQ2a representations before selector experiments | Eight artifacts under `skill_benchmark/rq2a_matched_content/representations/`; serializer `rq2a-serialiser-v1.4`; manifest source counts 350 clusters, 750 prompts, and 1,050 candidates | **PROVED** |
| Approve that representations satisfy the experimental requirements | `validation_report.json` is `PASS` with zero errors and zero warnings across 8,400 candidate-representation rows; 14-cluster manual sample review passes | **PROVED** |
| Prepare appropriate selectors/retrievers | Common fixed-candidate runner plus BM25, Qwen single-vector, pinned SkillRouter cross-encoder, and leakage-free seven-field Qwen field-aware adapters | **PROVED** |
| Validate selectors before the main experiment | Real cold/warm smokes, exact cache reproduction, all-artifact length audit, no-truncation checks, adapter tests, and stage-gate tests pass | **PROVED** |
| Run the RQ2a development experiment | Four canonical primary runs cover BM25 8 conditions, Qwen 8, SkillRouter 5, and both field-aware aggregation candidates over 70 clusters/150 prompts; 3,450 unique primary rows | **PROVED** |
| Reuse and locally persist authorised embeddings | Development Qwen runs persist 1,474 candidate and 243 field-component vectors; warm Qwen verification has 2,100 cache hits, zero misses, and zero API calls | **PROVED** |
| Give an initial review using justified metrics | `development-complete-v1` reports cluster-weighted tie-adjusted Top-1, MRR, margin, strict confusion, tie rate, paired bootstrap intervals, sign-flip tests, and Holm correction | **PROVED** |
| Record cost rather than accuracy alone | `development-complete-cost-v1` separates primary/smoke/verification roles, construction and online work, provider tokens/calls, model compute, cache behaviour, storage, and representation size | **PROVED** |
| Report each stage and keep tracker states current | Stage 0--4 reports are appended to the canonical run ledger; canonical tracker, roadmap, progress, methodology, risk, snapshot, and results-summary files now state Stage 4 development complete/A16 frozen | **PROVED** |
| Stay within RQ2a | No RQ2b, graph/tree, downstream, or additional external benchmark run was launched in this stage | **PROVED** |
| Do not write results into the thesis before user review | Development manifests and ledgers record `thesis_write=not_performed`; no Stage 4 run ID, freeze hash, or reported development effect appears in `thesis_latex/` | **PROVED** |

## Development Evidence Boundary

The primary development contrast, Qwen fielded minus flat, is `-5.48pp` cluster-weighted tie-adjusted Top-1 with 95% cluster-bootstrap interval `[-12.62pp,+1.19pp]` and paired sign-flip `p=0.144`. It does not support a field-heading advantage in development.

The positive controls do pass: fielded operational content beats shared-only by `+49.76pp` for Qwen, `+53.21pp` for BM25, and `+60.48pp` for SkillRouter. This supports the usability of the reviewed facts, not the superiority of one literal format.

The development rule for field-aware scoring is frozen as `qwen-field-aware-uniform-top-two`. Its `+4.21pp` difference over Qwen single-vector fielded has an interval crossing zero and does not constitute confirmatory support.

## Reproducibility And Freeze Evidence

- Complete analysis: `skill_benchmark/outputs/rq2a_matched_content/analysis/development-complete-v1/analysis.json` and `.md`.
- Complete cost ledger: `skill_benchmark/outputs/rq2a_matched_content/analysis/development-complete-cost-v1/cost_ledger.json` and `.md`.
- Immutable pre-confirmatory manifest: `skill_benchmark/rq2a_matched_content/confirmatory_freeze_manifest.json`.
- Freeze SHA-256: `273b61172628eaf6fe6cb172cebe7dfe9235fce49f694501e45aff72dbaa7181`.
- Freeze state: `frozen_before_confirmatory`; expected/complete conditions `22/22`; errors `0`.
- Regression status: Python compilation, selector adapter tests, stage-gate tests, manifest revalidation, and `git diff --check` pass.
- Confirmatory output state: no confirmatory output directory or result file exists.

## Completion Decision

The active implementation/development objective is **complete and verified**. The next scientific stage is a separately authorised confirmatory run over the frozen 280-cluster split. Until that happens, the thesis must describe RQ2a as development-complete but not scientifically answered, and no Stage 4 effect estimate should enter the thesis results chapter.
