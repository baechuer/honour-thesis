---
name: citation-grounding-helper
description: Checks whether a claim, sentence, or note is actually supported by a provided source and clarifies what the source can safely ground.
---

# Citation Grounding Helper

Checks whether a source supports a claim or note.

## Use when

- The user already has an exact claim, sentence, wording, or note they want to justify from a source.
- The task is a support check: decide whether the wording is supported, overstated, partially supported, or unsupported.
- The task is to determine whether the source supports that wording.
- The output should clarify support, overreach, ambiguity, or safer wording.

## Not for

- Summarizing a paper from scratch.
- Extracting general citation notes.
- Comparing multiple sources.
- Writing full related-work synthesis.

## Preconditions

- The user provides one or more sources, paper excerpts, notes, claims, or research summaries.
- The user indicates the intended research use: understanding, citation, method comparison, grounding, or synthesis.

## Workflow

1. Identify the exact claim or wording being checked.
2. Read the source for directly relevant support.
3. Distinguish supported, partially supported, and unsupported parts.
4. Explain overstatement, ambiguity, or missing grounding.
5. Suggest tighter wording when useful.

## Writing rules

- Be conservative about what the source supports.
- Distinguish direct support from inference.
- Preserve uncertainty and limits of scope.
- Return only the grounding assessment unless the user asks for more.

## Default shape

Use this shape unless the user asks for something else:

- Claim
- Support status: supported / partially supported / unsupported
- Why
- Safer wording if needed

## Example patterns

### Example 1

User ask:

`Does this sentence actually follow from the paper?`

Good output style:

- State whether the wording is supported
- Explain what is and is not justified
- Tighten the sentence if needed

### Example 2

User ask:

`Can I cite this source for this claim?`

Good output style:

- Focus on defensibility
- Be strict about overstatement
- Make scope limits explicit
