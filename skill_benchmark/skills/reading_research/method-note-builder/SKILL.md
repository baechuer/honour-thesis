---
name: method-note-builder
description: Extracts and organises method-focused notes from a paper, including setup, procedure, evaluation, assumptions, and relevant constraints.
---

# Method Note Builder

Builds method-focused notes from a paper.

## Use when

- The user wants to understand how a study or system was carried out.
- The task is mainly about how the work was carried out: setup, procedure, pipeline, evaluation design, baselines, assumptions, or constraints.
- The output should isolate methodological details rather than extract all fields or summarize the whole paper.
- The output should be structured around methodological detail rather than broad recap.

## Not for

- Summarizing the whole paper broadly.
- Extracting citation notes for later prose.
- Checking claim grounding.
- Synthesizing multiple sources into narrative related work.

## Preconditions

- The user provides one or more sources, paper excerpts, notes, claims, or research summaries.
- The user indicates the intended research use: understanding, citation, method comparison, grounding, or synthesis.

## Workflow

1. Identify the task, problem setting, or experimental context.
2. Extract the method, pipeline, or procedure.
3. Capture evaluation setup, data, baselines, measures, or comparison conditions when relevant.
4. Note assumptions, constraints, and limitations tied to the method.
5. Present the result as structured method notes.

## Writing rules

- Focus on method and evaluation over background narrative.
- Preserve important design constraints and setup details.
- Keep notes compact but specific enough to be reusable later.
- Return only the notes unless the user asks for another format.

## Output pattern

Use this shape unless the user asks for something else:

- Task or problem setting
- Method or procedure
- Evaluation setup
- Important assumptions or limitations

For worked examples, see `examples.md`.
