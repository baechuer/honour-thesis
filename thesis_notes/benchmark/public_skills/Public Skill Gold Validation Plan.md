# Public Skill Gold Validation Plan

Date: 2026-05-30

This plan defines how imported public skills can become evaluated gold-label benchmark cases. It is Step 6b in the benchmark methodology.

## Purpose

The current public-skill corpus is useful for two things already:

- scale pressure and realistic background distractors
- evidence that our proposed representation fields often exist or are extractable in real `SKILL.md` artifacts

It is not yet evidence that externally authored public skills can be retrieved as correct gold-label answers. Public-gold validation fills that gap.

## Research Role

This step protects the thesis from a major bias:

> If only our generated controlled skills are gold labels, structure-aware methods may look strong partly because those skills were authored with our proposed fields in mind.

Public-gold prompts test whether the same representation ideas work when the target skill was written by someone else and may encode its procedure implicitly.

## Construction Target

Initial target:

- 30-50 public-gold prompts
- at least 6 public-skill clusters or source families
- one imported public `gold_skill` per prompt
- 2-4 semantically plausible alternatives per prompt
- at least one field-axis reason why the public skill is correct

Possible cluster families:

- document and file workflows
- browser or web quality workflows
- GitHub, CI, and code-maintenance workflows
- API, MCP, or tooling workflows
- deployment and environment workflows
- data or spreadsheet workflows
- skill creation, evaluation, or documentation workflows
- research or literature workflows

## Required Annotation Per Prompt

Each public-gold prompt should include:

- `id`
- `user_request`
- `gold_skill`
- `closest_alternatives`
- `gold_rationale`
- `rejection_rationale`
- `field_axes`
- `acceptable_alternatives`
- `atomization_status`
- `source_family`

Field axes:

- input or precondition
- output artifact
- workflow or procedure
- dependency or tool
- resource or reference
- constraint or not-for boundary
- side effect or safety condition
- success criterion

## Atomization Rule

Use public skills as gold labels only when the tested behavior is atomic enough to adjudicate.

Accept:

- the public skill defines one clear procedure
- the prompt can be solved by that procedure without choosing among internal subskills
- alternatives are plausible but procedurally inferior

Reject or atomize:

- the public skill is a broad router or meta-skill
- the skill says to branch into different files, domains, or linked resources depending on context
- the prompt actually tests a hidden subskill rather than the public artifact itself
- several alternatives are equally correct

## Validation Steps

1. Select candidate public skills.
2. Screen atomicity and hierarchy.
3. Extract fields using the current representation layer.
4. Use model-assisted verification for difficult or implicit cases, requiring evidence spans.
5. Draft prompts without exact skill-name, repository-slug, or copied-phrase leakage. Keep provider/tool names when they are genuine dependencies of the public skill or user task.
6. Select semantic alternatives.
7. Manually adjudicate gold stability.
8. Run existing Step 1-4 validation checks on public-gold prompts.
9. Run selector evaluations on public-gold-only and combined benchmark strata.
10. Classify failures.

## Pass Criteria

- 100% prompt references resolve.
- At least 30 public-gold prompts survive validation.
- At least 85% of candidate public-gold prompts have stable manual gold labels.
- At least 80% pass prompt-specific procedural alignment.
- At least 70-80% pass semantic-confusability checks with a modern embedding model, or exceptions are documented.
- 0 critical or high-risk prompt leaks.
- Selector results show non-trivial method spread.
- Failures can be assigned to candidate recall, extraction, reranking, ambiguity, hierarchy, or acceptable-alternative causes.

## Failure Conditions

- public skill is too broad or hierarchical
- prompt tests behavior not clearly present in the public skill
- public skill lacks enough procedural evidence for manual or model-assisted extraction
- prompt leaks the exact skill name, repository slug, or copied skill-card wording
- alternatives are equally correct without acceptable-alternative annotation
- score gains depend only on source/name matching while input state, output artifact, workflow, dependency/tool, or success criterion do not support the gold label

## Provider/Tool Cue Rule

Provider and tool names are valid public-gold evidence when the skill is actually provider-tailored. For example, a Hugging Face dataset skill, Figma implementation skill, GitHub PR-thread skill, or Netlify deployment skill may require that provider name because it changes the inputs, APIs, workflow, and output artifact.

Do not remove these names merely to make the prompt harder. Instead:

- label each prompt as provider-explicit or provider-implicit;
- require the gold rationale to cite at least one additional procedural axis beyond the provider name;
- include near-provider alternatives where possible, such as related deployment platforms, Hugging Face dataset/model/training/deployment skills, or Figma generation/implementation/review skills;
- treat exact skill title or repository slug copying as leakage, but not ordinary provider/tool dependency language.

## Expansion Recommendation

Yes, expand the pure public-gold set, but not by simply adding more public prompts. Expand only after label cleanup.

Current cleanup status:

- The expanded 120 public-gold prompts now have explicit `label_status`, `provider_cue_status`, `prompt_information_level`, `gold_label_basis`, and cleanup-note fields.
- Label status: 80 stable strict public-gold, 37 stable with acceptable alternatives, and 3 hard public-label cases.
- Provider cue status: 64 provider/tool-explicit prompts and 56 provider-implicit or generic prompts.
- Prompt information level: 61 provider-explicit with procedural requirements, 56 provider-implicit/generic with procedural requirements, and 3 hard public cases.
- The leakage report now treats provider/tool terms as valid dependency cues when the prompt is provider-specific and still rejects exact skill-name, repository slug, or copied skill-card wording.

Current validation status:

- Step 1 integrity: PASS, 120/120 prompts resolve over the 2433-skill library.
- Step 2 procedural distinctness: PASS, 120/120 prompts.
- Step 2 prompt-specific requirement alignment: PASS, 111/120 prompts.
- Step 3 semantic confusability: PASS, 110/120 prompts.
- Step 4 leakage: PASS, 0 critical and 0 high-risk leaks.
- Broad combined audit with controlled, public-gold, and low-information prompts: PASS for integrity, procedural distinctness, and leakage over 333 prompts.

Recommended order:

1. Promote only stable strict and stable acceptable-alternative cases to headline public-gold scoring.
2. Keep the 3 hard public-label cases as stress-test examples unless manually adjudicated again.
3. Rerun local, Qwen, and SkillRouter selectors on the 120-prompt public-gold stratum before reporting public-gold performance.
4. For any further new case, store gold rationale, rejection rationale, field axes, acceptable alternatives, atomization status, provider cue status, prompt information level, and source family.
5. Report public-gold separately from controlled and public-style controlled strata.

Target after cleanup:

- at least 100 stable public-gold prompts if enough atomic public skills exist; currently achieved with 117 stable strict-or-acceptable cases plus 3 hard public cases;
- at least 8 source families;
- at least 85% stable strict-or-acceptable labels after manual adjudication;
- provider-explicit and provider-implicit subtables in final results.

## Reporting

Report three strata separately:

- controlled-authored benchmark
- public-gold benchmark
- combined full-scale benchmark

The thesis should use public-gold results to test external validity, not to replace the controlled benchmark.
