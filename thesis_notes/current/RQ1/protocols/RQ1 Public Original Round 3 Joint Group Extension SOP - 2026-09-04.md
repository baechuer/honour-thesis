# RQ1 Public Original Round 3 Joint Group Extension SOP

<!-- RQ1-RECORD-STATUS:START -->
> **RQ1 record status (2026-09-04): `CURRENT_CANONICAL`.** Current supporting joint-group public-original experiment protocol. Canonical index: `thesis_notes/current/RQ1/README.md`.
<!-- RQ1-RECORD-STATUS:END -->



Date: 2026-09-04  
Status: `GROUP BM25 + QWEN TWIN COMPLETE / VALIDATED / USER RESULT REVIEW REQUIRED / NOT IN THESIS PDF`

## Purpose

This is a separately labelled supporting extension to the completed Round-3
single-field original-document test. It asks whether removing a coherent set of
operational information from otherwise identical public source documents causes
a larger or clearer routing loss than removing a single field. It does not
replace the single-field primary result and cannot attribute an observed change
to one member of a group.

The extension must not be confused with the completed August field-card group
study. That earlier study replaced values in extracted cards with a common
marker. This one starts with the exact public original `SKILL.md` documents and
removes the exact verified source lines already removed by the component
Round-3 masks.

## Predeclared Groups

| Group condition | Component fields |
| --- | --- |
| `REMOVE_TASK_SPECIFICATION_R3` | use condition; input/precondition; output/artifact |
| `REMOVE_EXECUTION_VERIFICATION_R3` | workflow/procedure; success/verification |
| `REMOVE_APPLICABILITY_CAPABILITY_R3` | boundary/not-for; dependency/resource |

Each group is one separate `FULL_ORIGINAL` versus its own group-removal
comparison. There is no pooled three-group effect and no comparison of the raw
scores of different retrievers.

## Derived-Clear Eligibility Rule

A group case is eligible only if the same composition, routing family and
singleton gold occur in the frozen Round-3 clean-only case list for **every**
component field. This ensures that every candidate in every component mask has
already received a canonical Round-3 `CLEAR` decision and that the same frozen
direct/paraphrase prompt pair and gold label apply to the group.

The group document is deterministically created as the union of line deletions
in its component Round-3 masks, measured against the same original source
document. A candidate passes the derived-clear group gate only when all of the
following hold:

1. every component field mask is hash-verified and `CLEAR` for that candidate;
2. each component differs from the original only by blanking source lines;
3. each group line is blank exactly when at least one component mask blanked
   that original non-empty line; and
4. the group document makes no other byte or line change.

No third semantic review is needed after this exact-union proof: an operation
that only deletes additional source lines cannot reintroduce a candidate-
specific value absent from every component mask. This is a derived-clearance
claim, not a new judgement that the masked document remains executable or
well-written.

## Planned Denominators

The current frozen single-field case intersections yield:

| Group | Composition-family cases | Distinct compositions | Planned ranking rows |
| --- | ---: | ---: | ---: |
| Task specification | 99 | 37 | 396 |
| Execution/verification | 138 | 51 | 552 |
| Applicability/capability | 132 | 50 | 528 |
| Total, separate group comparisons | 369 | group denominators overlap | 1,476 |

The composition is the inferential unit within a group. Direct/paraphrase are
averaged within routing family, then families are equally averaged within
composition. A composition appearing in more than one group is intentionally
reused within its respective group comparison; it must not be treated as an
independent observation across groups.

## Execution and Metrics

1. Materialise group documents and build a hash-bound group freeze.
2. Independently validate source identity, component mask identity, exact union
   semantics, candidate membership, prompt/gold binding and row counts.
3. Run local BM25 over the frozen group cases.
4. Analyse paired Top-1, MRR, gold rank, native margin, winner transitions and
   direct/paraphrase slices with a 10,000-resample composition-clustered paired
   bootstrap.
5. Construct a local-only Qwen preflight from the group freeze. Qwen execution
   requires a new exact text-transfer authorisation because group documents are
   new texts; the prior single-field authorisation does not cover them.

For a retriever `r`, prompt `q`, gold `g` and group condition `c`:

```text
margin_r(q, c) = score_r(q, g, c) - max_wrong score_r(q, wrong, c)
delta_margin_r(q, group) = margin_r(q, FULL_ORIGINAL) - margin_r(q, REMOVE_GROUP_R3)
```

Positive delta margin means that removing the group reduces the gold skill's
lead over the strongest incorrect candidate. Margins are native-selector
diagnostics only: BM25, cosine embedding and reranker values may not be
combined numerically.

## Interpretation Boundary

A positive group effect supports a limited statement that the *combined*
documented information supplied routing support in these clear public-source
compositions for the tested retriever. It does not establish an additive effect,
identify which member field was decisive, supersede the single-field result, or
generalise to broader retrieval architectures.

No group result may be written to thesis LaTeX/PDF until the user reviews the
validated BM25 and, if separately authorised, Qwen result package.

## Completed Local BM25 Stage

The group freeze was materialised and checked by a separate local validator
before scoring; this was technical validation, not independent human review.
It contains 369 eligible composition-family cases and 1,476 paired ranking
rows. The freeze SHA-256 is
`7a73a3d4026ffa32b855ae3844cf3d63046aff9535435294a2cf742f84cc9062`.

The deterministic local BM25 run completed without external transmission. Its
1,476 rows and paired analysis passed separate local validator scripts and
checksum validation. This wording does not imply human annotation. Result SHA-256:
`3eb649a71770c9e24f800b3f07479bcedecc2efa5e768cdbf66210e1e1a46e14`.
Analysis SHA-256:
`2ef74203c46bdb9ce824eb0c8f23e95a5f0f6852c70bc410eee404ea822dfcb8`.

| Group | Full Hit@1 | Removed Hit@1 | Full-minus-removed [95% CI] | MRR delta [95% CI] |
| --- | ---: | ---: | ---: | ---: |
| Task specification | 0.784 | 0.518 | +0.266 [+0.196, +0.336] | +0.156 [+0.116, +0.198] |
| Execution/verification | 0.790 | 0.614 | +0.176 [+0.094, +0.262] | +0.114 [+0.065, +0.164] |
| Applicability/capability | 0.780 | 0.644 | +0.136 [+0.087, +0.186] | +0.083 [+0.055, +0.112] |

All three BM25 group comparisons have positive composition-clustered
confidence intervals for both Hit@1 and MRR. This supports only the stated
combined-information interpretation. It does not show that group members add
linearly or that any specific member field caused the result. The Qwen
preflight passed with payload SHA-256
`8d9d87e791a0f34807f4a2ae8f85ec43798a7df356bffd8a38a4db22520bb2ea`.
All 336 unique frozen queries and 304 original-document texts are valid cache
hits. Execution would send only 342 new group-masked documents (1,222,989
UTF-8 bytes; 155,923 local lexical-token proxy), in at most 35 sequential
no-retry calls. The user subsequently authorised that exact scope and Qwen
completed with 35 successful calls, 342 document cache misses, zero query
transfers and 283,526 provider-reported input tokens.

| Group | Qwen full Hit@1 | Qwen removed Hit@1 | Qwen Full-minus-Removed Hit@1 [95% CI] | Qwen MRR delta [95% CI] |
| --- | ---: | ---: | ---: | ---: |
| Task specification | 0.872 | 0.784 | +0.088 [+0.005, +0.162] | +0.047 [-0.006, +0.092] |
| Execution/verification | 0.864 | 0.790 | +0.074 [+0.007, +0.141] | +0.039 [+0.001, +0.076] |
| Applicability/capability | 0.848 | 0.834 | +0.014 [-0.043, +0.062] | +0.010 [-0.022, +0.038] |

For task specification and execution/verification, both first-stage retrievers
have positive composition-level Hit@1 intervals. Applicability/capability has a
positive BM25 effect but no stable Qwen Top-1 effect. Qwen native-margin
diagnostics are positive for all three groups, including applicability, but are
not pooled with BM25 margins or promoted over the primary Top-1 result.
