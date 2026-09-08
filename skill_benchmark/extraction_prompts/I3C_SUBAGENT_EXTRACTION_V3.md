# I3C Subagent Extraction Prompt V3

Use this prompt only for the separately versioned RQ2b I3C V3 correction.
It preserves the V2 JSON schema so the strict evidence merger can validate the
same seven fields, but corrects the documented source-native-description gap.

## Purpose And Data Boundary

Recover selector-useful operational facts from **one assigned skill artifact**.
Use only the assigned JSONL row. Do not call APIs, search online, inspect other
skills, prompts, gold labels, alternatives, benchmark roles, or retrieval
results. Return exactly one JSON object per input row and flush completed JSONL
every 10 rows.

Only an exact quote from `text` may be used as `evidence`. The input `name` and
`description` are source-native metadata supplied to help locate the matching
source wording; they are not permission to invent or paraphrase an evidence
quote.

## Required JSON Shape

Return the exact V2-compatible JSON shape below. `schema_version` remains
`I3C_SUBAGENT_EXTRACTION_V2` because it identifies the validated output schema,
not the extraction-policy revision.

```json
{
  "schema_version": "I3C_SUBAGENT_EXTRACTION_V2",
  "parser": "codex_subagent",
  "family": "<copy input>",
  "skill": null,
  "skill_id": "<copy input>",
  "name": "<copy input>",
  "description": "<copy input>",
  "source": "<copy input>",
  "fields": {
    "use_conditions": [],
    "input_preconditions": [],
    "output_artifacts": [],
    "workflow_steps": [],
    "constraints_boundaries": [],
    "dependencies_resources": [],
    "success_criteria": []
  },
  "absent_fields": [],
  "field_warnings": {},
  "qa_warnings": []
}
```

Each non-empty field item has exactly these keys:

```json
{
  "id": "use_1",
  "text": "concise normalised statement of the supported operational fact",
  "evidence": "an exact contiguous substring copied from text",
  "evidence_status": "explicit",
  "confidence": 0.0,
  "selector_usefulness": "high"
}
```

Allowed `evidence_status`: `explicit`, `implicit`. Allowed
`selector_usefulness`: `high`, `medium`. Do not include low-usefulness items.

## Seven Operational Fields

- `use_conditions`: task, user intent, selection trigger, or activation condition.
- `input_preconditions`: required input, file/data state, context, permission, or prerequisite.
- `output_artifacts`: expected deliverable, format, report, patch, table, plan, or response shape.
- `workflow_steps`: concrete procedure, method, transformation, check, or sequence.
- `constraints_boundaries`: limit, exclusion, not-for case, or scope boundary.
- `dependencies_resources`: required tool, API, command, model, platform, credential, template, or service.
- `success_criteria`: verification, acceptance rule, metric, or quality condition.

## Mandatory Source-Native Metadata Sweep

Before declaring a field absent or the artifact sparse, inspect all of `text`,
including YAML/frontmatter `name` and `description` declarations and the body.

1. If the source-native description explicitly says when to use the skill, what
   task it performs, a required input, a concrete output, dependency, boundary,
   procedure, or success condition, assign that fact to the appropriate field.
2. Evidence must still be an exact contiguous substring of `text`. When the
   description is YAML-folded or line-wrapped, copy the contiguous raw source
   span with its original newlines and indentation. Do **not** substitute the
   whitespace-normalised input `description` for the raw evidence.
3. If the only field evidence exactly duplicates the whole source-native name or
   description after whitespace normalisation, emit the field item anyway. The
   later serializer will omit the duplicate span from the selector-visible
   evidence list because name and description are already present as fixed I1
   metadata. Do not list that field in `absent_fields`.
4. A generic title alone is not enough. A short but concrete description such as
   “Open an issue on GitHub. Use when the user asks to file an issue.” is enough
   for `use_conditions` when the raw frontmatter source contains it.
5. Use `sparse_artifact` only after this sweep finds no explicit,
   selector-useful operational fact anywhere in `text`.

## Extraction Rules

1. Extract only facts that distinguish this skill from plausible neighbours.
2. Evidence is an exact source substring; never paraphrase it in `evidence`.
3. `text` may be concise and normalised, but it is parser metadata and is not
   selector-visible.
4. Prefer a specific operational sentence to a generic negative sentence. For
   outputs, retain the actual deliverable when stated, not merely wording such
   as “the deliverable is not prose”.
5. Do not use headings without content, generic routing boilerplate, generic
   checklists, TODOs, navigation, placeholders, or examples that do not define
   an operational distinction.
6. Keep multiple distinct inputs, outputs, steps, dependencies, boundaries, or
   criteria as separately numbered items.
7. Do not create hierarchy links, relation edges, side-effect fields, selection
   summaries, or hidden benchmark metadata.
8. `absent_fields` must contain exactly the seven fields whose arrays are empty.
9. Use `field_warnings` or `qa_warnings` for genuine sparseness, breadth, or
   skipped generic content. Warning evidence must also be an exact substring if
   non-empty.

## Before Completion

Validate locally for every row: JSONL parsing; one object per input row;
unchanged `skill_id` and source identity; contiguous `source_row_index` order;
and every evidence string as an exact substring of that row's `text`.
