# I3C source-only full-corpus extraction prompt V4.1

Use this prompt only for the prospective V7 Phase-7 repair after the frozen
blinded-QA v2 failure. The benchmark scope and seven operational fields do not
change. V4.1 keeps V4's completeness, polarity, atomicity and field-role rules,
while distinguishing source-internal task language from benchmark-construction
metadata.

## Hard data boundary

Use only the assigned JSONL rows. Do not call APIs, search online, inspect other
skills, benchmark prompts, targets, labels, acceptable sets, candidate roles,
retrieval results, or earlier extraction/reviewer returns. Return one object per
input row, in order. Every fact must be supported by an exact contiguous
substring of that row's `text`.

## Required JSON shape

Keep the existing validated schema:

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

Each non-empty item has exactly:

```json
{
  "id": "use_1",
  "text": "concise normalised statement supported by the quote",
  "evidence": "exact contiguous substring copied from text",
  "evidence_status": "explicit",
  "confidence": 0.0,
  "selector_usefulness": "high"
}
```

Allowed `evidence_status`: `explicit`, `implicit`. Allowed
`selector_usefulness`: `high`, `medium`. Do not retain low-usefulness material.

## Field meanings and precedence

Classify each atomic fact by what it does for skill selection:

1. `constraints_boundaries`: explicit not-for/unsupported/avoid/prohibition,
   route-out, scope limit, compatibility limit, or hard operating boundary.
   This field has precedence for a clear exclusion or operating prohibition.
2. `use_conditions`: positive task, user intent, activation condition, or
   selection trigger. A field/event called "trigger" inside the task is not
   automatically a skill activation condition.
3. `input_preconditions`: information, file/data, permission, state, prior step,
   or caller-supplied value that must already exist or be supplied. Grammatical
   negation may describe an input state (for example, a user who does not yet
   have a plan); that is not by itself a not-for boundary.
4. `output_artifacts`: deliverable or result format the skill produces. A method
   rule, prohibition, or illustrative example output is not an artifact.
5. `workflow_steps`: an operation the skill performs. A heading, noun fragment,
   static state, desired quality, or caller-supplied input is not a workflow.
6. `dependencies_resources`: package, tool, API, command, model, platform,
   credential, template, service, or required file/resource. A quality rule is
   not a dependency.
7. `success_criteria`: observable verification, acceptance rule, metric, test,
   or quality condition that determines whether the work succeeded.

## Atomic evidence rules

- One item must express one operational fact. Split mixed-role passages when
  each role has its own exact contiguous wording.
- Evidence must be a complete sentence, bullet/list item, or complete YAML
  scalar value. Never retain a heading alone, a bare scalar marker, a raw
  frontmatter key plus unrelated following keys, or a mid-indented continuation
  fragment.
- A source body may legitimately teach authors to create a `description:` key or
  analyse fields named `gold_label`/`target`. Preserve such text when it is the
  skill's actual operation. What is prohibited is benchmark-construction
  metadata attached to the candidate itself, especially controlled-corpus
  category/tag/cluster fields in frontmatter.
- If one sentence mixes a positive trigger with a negative route-out and cannot
  be split into self-contained exact substrings, place the complete sentence in
  `constraints_boundaries` and add a `mixed_role_unsplittable` QA warning. Do not
  duplicate it under `use_conditions`.
- Examples are evidence only when they define a general input/output contract,
  not when they merely instantiate one case.
- The native `name` and corrected `description` are already always visible. You
  must still emit a field item when they carry the only fact, but quote only the
  exact scalar value or source-grounded body evidence, never surrounding
  `category`, `tags`, `metadata`, `source_style`, or `cluster_id` fields. The
  serializer may later omit an exact identity duplicate.

## Mandatory exhaustive sweep before any absent field

Read all frontmatter and body text, then explicitly check:

- `name`, `description`, `compatibility`, `allowed-tools`, `mcp`, tools,
  packages, platforms, credentials and templates;
- when-to-use, when-not-to-use, supported/unsupported, prerequisites,
  requirements, inputs, outputs/deliverables, workflow/procedure, validation,
  quality/success, limitations, anti-patterns and route-outs;
- phrases such as `requires`, `must`, `run after`, `before`, `do not use`,
  `not for`, `does not support`, `unsupported`, `only`, `output`, `produce`,
  `return`, `verify`, and `success`.

Do not mark a field absent until that sweep is complete. `absent_fields` must
equal exactly the seven empty arrays.

## Warnings and completion

`field_warnings` maps field keys to warning arrays. Each field warning has only
`code`, `message`, `evidence`. `qa_warnings` is an array with only `code`,
`field`, `message`, `evidence`. Warning codes use lower-case letters, digits and
underscores. Warning evidence is empty or an exact source substring.

Warn and fail closed on an unsplittable mixed-role passage, unclear field role,
or source formatting that prevents complete self-contained evidence. Do not
guess or invent.

Before completion verify: exact identity copy; one output per input in order;
all seven containers; exact absent-field equality; every evidence substring;
no candidate-attached benchmark-construction metadata; no raw frontmatter
description declaration crossing into another key; no explicit not-for/use
prohibition under `use_conditions`; and no incomplete continuation fragment.

