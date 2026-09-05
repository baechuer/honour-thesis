# Failure Mode Analysis: Qwen Full + Local Schema Top-100

Date: 2026-05-27

Target method:

```text
Qwen text-embedding-v4 over full SKILL.md
-> top-100 candidate pool
-> local deterministic schema reranker over R2/R3 fields
```

Result:

- 67 prompts.
- 57 strict top-1 hits.
- 10 strict top-1 failures.
- 85.1% top-1.
- 91.0% top-5.
- MRR 0.878.

This is the current strongest method, so this is the failure analysis that should guide the next refinement loop.

## Failure Split

| Failure Type | Count | Meaning |
|---|---:|---|
| First-stage exclusion | 4 | Gold skill was not in Qwen top-100, so the schema reranker could not recover it. |
| Reranker / boundary failure | 6 | Gold skill was in the top-100 candidate pool, but schema reranking did not place it first. |

This means the remaining errors are not one single problem. Some require better first-stage retrieval; others require better procedural reranking or better prompt/gold-label treatment.

## Failure Table

| Prompt | Gold | Top-1 | Gold First-Stage Rank | Final Gold Rank | Failure Mode |
|---|---|---|---:|---:|---|
| `web_p5_frontend_debugging` | `frontend-debugger` | `api-ops-handoff-brief-writer` | 223 | - | first-stage exclusion |
| `code_p1_local_code_review` | `code-reviewer` | `email-drafter` | 426 | - | first-stage exclusion |
| `doc_p4_field_extraction` | `document-field-extractor` | `receipt-extractor` | 32 | 7 | near-acceptable domain-specific competitor |
| `doc_p7_layout_preserving_conversion` | `layout-preserving-converter` | `medical-admin-ops-field-extractor` | 618 | - | first-stage exclusion |
| `plan_p5_weekly_planner` | `weekly-planner` | `meeting-ops-acceptance-test-builder` | 2 | 3 | schema overweights secondary terms |
| `read_p1_paper_summary` | `paper-summariser` | `method-note-builder` | 1 | 2 | near-neighbor schema misweighting |
| `read_p4_document_extraction` | `document-extractor` | `web-data-extractor` | 1 | 20 | underspecified cross-family extraction |
| `reply_p5_generic_fresh_draft` | `reply-drafter` | `reply-polisher` | 5 | 3 | negation/boundary failure |
| `skill_p4_edit_existing` | `skill-editor` | `docs-ops-field-extractor` | 309 | - | first-stage exclusion, object/meta confusion |
| `skill_p5_evaluate_existing` | `skill-evaluator` | `reply-polisher` | 28 | 2 | object skill vs meta-skill confusion |

## What This Tells Us

### 1. First-Stage Retrieval Is Still A Bottleneck

Four failures happen before schema reranking can help:

- `web_p5_frontend_debugging`
- `code_p1_local_code_review`
- `doc_p7_layout_preserving_conversion`
- `skill_p4_edit_existing`

In these cases, Qwen embeddings retrieve semantically related surface material but miss the procedural role of the request. Examples:

- frontend debugging gets pulled toward API operations because the prompt mentions API response contracts;
- local code review gets pulled toward email because the patch mentions `user.email`;
- skill editing gets pulled toward field extraction because the skill being edited is about field extraction.

This supports a key thesis point: even strong embeddings can confuse the object of a task with the procedure needed to act on it.

### 2. Schema Reranking Helps, But It Still Overweights Some Surface Cues

Several gold skills entered the candidate pool but were not ranked first:

- `plan_p5_weekly_planner`
- `read_p1_paper_summary`
- `reply_p5_generic_fresh_draft`
- `skill_p5_evaluate_existing`

These are not random errors. They show specific weaknesses:

- task-list contents can overpower the main planning intent;
- method/evaluation words can overpower summary intent;
- negation such as "no existing draft to polish" is not handled strongly enough;
- meta-level requests such as "evaluate this skill" can be confused with using the named skill.

### 3. Some Failures Are Gold-Label Or Acceptable-Alternative Questions

`doc_p4_field_extraction` chooses `receipt-extractor` for invoice field extraction. This is not obviously absurd. It may be a domain-specific near-equivalent rather than a strict wrong answer.

Action:

- manually adjudicate whether `receipt-extractor` or `invoice-payment-checker` should be acceptable or borderline for this prompt.

### 4. Some Prompts Are Too Generic For Stable Procedural Selection

`read_p4_document_extraction` asks for structured extraction from "this source" without a source-type cue. The model selects `web-data-extractor`, which is plausible if "source" is interpreted as web/source material.

Action:

- either accept this as a prompt weakness or introduce a query-understanding step that extracts source type before retrieval.

## Failure Mode Counts

| Mode | Count |
|---|---:|
| First-stage exclusion | 4 |
| Schema field misweighting | 2 |
| Object/meta-skill confusion | 2 |
| Negation/boundary failure | 1 |
| Acceptable/borderline domain-specific competitor | 1 |
| Underspecified prompt / cross-family ambiguity | 1 |

Counts overlap slightly because some failures have more than one cause. The most important split remains:

```text
4 retrieval-pool failures
6 reranking / boundary / annotation failures
```

## Next Actions

1. Do not add new methods yet.
2. Decide whether `doc_p4_field_extraction` needs acceptable-alternative annotation.
3. Add an explicit analysis category for meta-skill requests: edit/evaluate/find/install/create.
4. Consider a query-understanding stage for:
   - task object vs requested procedure;
   - negation and avoid-condition cues;
   - primary intent versus secondary content inside task lists.
5. Measure whether top-100 is an acceptable candidate-subsetting budget in latency/cost terms.
6. After that, run Step 9 downstream validation. The existing downstream-plan filenames still use `step8` from the earlier numbering.

## Thesis Language

Use this result carefully:

> The strongest method combines broad semantic candidate generation with structure-aware procedural reranking. Remaining errors show two bottlenecks: first-stage retrieval sometimes excludes the correct skill, and deterministic schema reranking still struggles with negation, meta-level skill operations, and underspecified requests.

This brings the project back to the core thesis question: what information must a skill representation and query representation preserve for reliable skill retrieval?
