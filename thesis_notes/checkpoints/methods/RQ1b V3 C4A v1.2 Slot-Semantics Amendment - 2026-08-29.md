# RQ1b V3 C4A v1.2 Slot-Semantics Amendment

Date: 2026-08-29  
Status: `PROSPECTIVE LOCAL-ONLY REPAIR / NO REBUILD OR REVIEW YET / NO CARD, LABEL, SELECTOR, OR RESULT`

## Why v1.2 Is Needed

The v1.1 non-exclusive quotation rule correctly allowed one exact source span
to support more than one slot, but it did not sufficiently separate three
semantic roles that often co-occur in natural prose:

1. a supplied material from an external dependency/resource;
2. an ordinary workflow step from an explicit acceptance/verification test; and
3. a delivered artifact from a sentence that merely mentions reading it after
   production.

This is a schema-calibration repair. It is not evidence that any information
field does or does not aid routing.

## Invariant Rules

- Every quote remains an exact contiguous source substring.
- Slots are non-exclusive: repeat a qualifying quote in each applicable slot.
- Do not paraphrase, infer a missing fact, merge separated text, consult a
  prompt/target, use a title/heading/frontmatter/URL/path, or use a selector.
- `NOT_STATED` means that no literal source span satisfies the slot's rule.
- Slot labels classify *source evidence*, not an intended route or a user
  request. The same source can legitimately have sparse or empty slots.

## Binding Slot Rules

| Slot | Include only literal evidence of | Explicit exclusion |
|---|---|---|
| `use_condition` | applicability, user goal, or situation in which the skill should be used | a bare product/topic mention without applicability |
| `input_precondition` | an artifact, data, state, access condition, or pre-existing environment that the work consumes or requires before its central operation; an uploaded agreement is an input | a software package/service merely used to perform work; a produced result |
| `output_artifact` | an artifact, structured result, state change, or delivered format that the skill creates, returns, exports, or writes | a line that only says to read/inspect a result without stating that the skill creates or returns it |
| `workflow_procedure` | an action, ordered step, transformation, or method the skill performs; a post-production inspection can be workflow if it is stated as an action | an acceptance claim with no action; a deliverable declaration by itself |
| `success_verification` | an explicit pass/fail check, threshold, comparison, test, validation, measurement, or acceptance condition | ordinary completion, a statement that an artifact exists, reading an output, reporting a result, or a generic recommendation to be careful |
| `boundary_not_for` | an explicit exclusion, route-out, unsupported scope, prohibition, or limitation | an unstated limitation inferred from the source or a missing capability |
| `dependency_resource` | a named external package, API, service, runtime, credential, tool, account, hardware, or data resource whose availability is explicitly required to execute the skill | a user-supplied input artifact, an output location/artifact, or a generic action verb; optional named tools unless the source makes their availability required |

## Calibration Examples

- “Upload the agreement, extract obligations, then return a risk memo” may be
  quoted in `input_precondition`, `workflow_procedure`, and `output_artifact`.
  It is **not** success/verification without a literal acceptance check.
- “After conversion, read the resulting `.md`” may be a workflow inspection;
  it is not success/verification unless the source gives a criterion such as
  “verify all headings and links pass.” The `.md` may be output evidence only
  if another exact source span says it is created, returned, or exported.
- “Requires the Anthropic API key” is `dependency_resource`; “the user uploads
  a contract” is `input_precondition`, not a dependency.

## Required Rebuild Gate

Before C4B, the next C4A builder wave must use these rules, persist every raw
builder return, literal-audit every quote, run a source-only slot-conformance
review, and reject any disagreement that cannot be resolved by the rules
without reference to prompt or target. The older v1.1 packets and their
unpersisted delivery gap remain historical; they are not rewritten.
