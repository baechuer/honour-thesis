# V7 I1 source-grounded identity overlay review V1

## Boundary

Review only the assigned source-only rows. Do not inspect benchmark prompts,
targets, labels, acceptable sets, candidate roles, retrieval outputs, or other
reviewer returns. Do not use the network.

Each row has a malformed source-native `description` scalar. The source bytes
remain authoritative and immutable. Your task is to propose one concise
source-grounded description that identifies when or why the skill is selected.
This is an identity repair, not a skill rewrite.

## Decision rule

- `RECOVER_FRONTMATTER_CONTINUATION`: use only when the malformed declaration is
  `description: Use this skill when >` and its immediately indented continuation
  contains a usable description. Preserve the leading `Use this skill when` and
  normalise the continuation as folded YAML text.
- `SOURCE_GROUNDED_BODY_OVERLAY`: use when the literal description is `>` (or no
  usable continuation exists). Select the narrowest complete sentence(s) from
  the source body that state the skill purpose or activation condition.
- `UNRESOLVED`: use if the source has no adequate identity statement.

The proposed description may normalise whitespace but may not add facts. Record
an exact contiguous `source_evidence` substring from the supplied `source_text`
that fully supports it. The evidence must not be a heading alone, example prompt,
generic workflow step, benchmark metadata, or a neighbour-routing annotation.

## Return schema

Return exactly one JSON object per input row, in input order:

```json
{
  "review_id": "<copy>",
  "skill_id": "<copy>",
  "reviewer_lane": "A or B",
  "status": "COMPLETE",
  "decision": "RECOVER_FRONTMATTER_CONTINUATION | SOURCE_GROUNDED_BODY_OVERLAY | UNRESOLVED",
  "proposed_description": "<nonempty unless unresolved>",
  "source_evidence": "<exact contiguous source substring, nonempty unless unresolved>",
  "notes": "<brief source-only rationale>"
}
```

Do not copy `source_text` into `notes`. Do not edit sources or prior artifacts.

