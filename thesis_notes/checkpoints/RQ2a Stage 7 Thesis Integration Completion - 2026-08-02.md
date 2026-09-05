# RQ2a Stage 7 Thesis Integration Completion

Date: 2026-08-02

State: **PASS / COMPLETE / USER-REVIEWED**

## Scope

This checkpoint records the documentation-only closure of RQ2a after the user approved integration of the completed confirmatory evidence. It did not rerun a selector, call an external API, alter an embedding, change the frozen protocol, or recompute a scientific result.

## Scientific evidence retained unchanged

- Confirmatory design: 280 clusters, 600 prompts, 22 conditions, and 13,200 aligned fixed-candidate decisions.
- Analysis SHA-256: `189d6b20b091e2f2d3bd30f168355ccf2a73efa3eef3b082075725040fec0ce7`.
- Cost-ledger SHA-256: `980af3ff9c9106d7f43d029b69aa5a1bb07515faf2e15b0b96e70bca5332cdec`.
- Failure-report SHA-256: `a0e96747f544904d424bf6fe83a656bd3b27533b4e2b2c9b8166fb91a8c6d155`.
- Thesis-facing analysis source: `thesis_notes/current/RQ2a Confirmatory Results and Analysis - 2026-08-02.md`.

## Documentation synchronised

The current result summary, active snapshot, experiment roadmap, methodology tracker, risk register, nine-step status, thesis progress tracker, English and Chinese RQ2 methodology specifications, current RQ2 tracker, execution ledger, and prior Stage 5 audit now identify RQ2a as complete and user-reviewed. Historical smoke/development checkpoints remain historical rather than being rewritten as current state.

The thesis now records:

1. the fixed three-sibling experimental unit and matched-content representations;
2. the correct local three-candidate BM25 corpus rather than a global BM25 index;
3. Qwen `text-embedding-v4` as an independently encoded bi-encoder condition;
4. `pipizhao/SkillRouter-Reranker-0.6B` as direct joint query-candidate cross-encoder scoring;
5. the frozen Qwen `uniform-top-two` seven-field selector;
6. the full 22-condition matrix, nine preregistered contrasts, field slices, costs, and bounded interpretation;
7. the explicit statement that no SkillRouter-native field-aware condition was tested; and
8. the exclusion of full-library recall, graph/tree retrieval, downstream execution, and public-library generalisation from the completed RQ2a claim.

## Thesis verification

- Build command: `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` from `thesis_latex/`.
- Build state: PASS; bibliography and cross-references resolved.
- PDF: `thesis_latex/main.pdf`, 82 A4 pages.
- PDF SHA-256: `2a4a30715d59b38862d451efd708e317c1ed4a7540a99f70d64c7f30be51fd02`.
- Visual QA: abstract, methodology model-definition pages, complete RQ2a matrix/contrast/field/cost pages, discussion, limitations, and conclusion were rendered with Poppler and inspected. No clipping, overlap, unreadable table, or orphaned abstract continuation remains.
- Existing non-fatal overfull/underfull warnings occur in older RQ1/conceptual-framework text and are outside this RQ2a integration; no new RQ2a table overflow was reported.

## Final RQ2a claim

In fixed-candidate near-neighbour routing, candidate-specific operational facts are essential, but explicit field headings are not an independent or universal source of accuracy. Pooled Qwen embeddings favour matched flat propositions over fielded text. Frozen Qwen field-wise scoring recovers the fielded pooling penalty but does not beat flat Qwen overall. SkillRouter cross-encoder scoring is strongest in accuracy and much more expensive for novel query-candidate pairs. Representation and retrieval architecture must therefore be evaluated together.

## Remaining boundary

RQ2a is closed. RQ2b remains an unreviewed separate design and must not be inferred as authorised or complete from this checkpoint.
