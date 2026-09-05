# Real-World Skill Expansion Plan

Date: 2026-05-28

This note records how to expand the benchmark toward 2000 skills without losing the thesis focus.

## Decision

Expanding to about 2000 skills is useful, but only if it is framed correctly.

The 2000-skill expansion should not replace the controlled benchmark. Instead, it should add an **ecological-validity layer**:

1. Controlled core skills test semantic confusability and procedural distinctness under known gold labels.
2. Real-world imported skills test whether our representation fields match how public skills are actually written.
3. Generated background skills provide scalable retrieval pressure where public coverage is uneven.

This avoids the biggest risk: making the benchmark larger but less interpretable.

## Why Real-World Skills Help

Real-world skills help the thesis in three ways.

First, they reduce benchmark-construction bias. If all skills are generated from our own schema, then structure-aware methods may look strong partly because the benchmark was written in the same language as the method.

Second, they help justify the representation fields. Instead of saying "we decided inputs, outputs, preconditions, dependencies, resources, workflow, and negative boundaries matter," we can say:

> These fields were treated as hypothesized representation features, motivated by the literature and then checked against public SKILL.md-style skills.

Third, they make scale more realistic. Real skills contain uneven formatting, missing fields, optional resources, tool assumptions, examples, dependency declarations, limitations, and broad descriptions. This creates a better test of whether representation extraction and retrieval are robust outside our generated skill style.

## Target 2000-Skill Composition

Recommended composition:

| Layer | Target count | Role |
|---|---:|---|
| Controlled core skills | 100-120 if time permits | Gold-label evaluation and confusable clusters. Current count is 67. |
| Public imported skills | 200-500 if feasible | Ecological validity and real-world background distractors. |
| Generated background skills | Remainder to 2000 | Scale pressure and controlled near-domain distractors. |

The final thesis should report all three counts separately. Do not hide generated skills inside a single "real-world" count.

## Controlled Core Expansion

Current controlled core:

- 67 evaluated prompts.
- 67 unique gold skills.
- 11 evaluated families.
- Current family distribution:
  - browser/web automation: 6
  - code/GitHub workflow: 6
  - data/spreadsheet: 7
  - documents/files: 7
  - metrics/observability: 6
  - news monitoring: 5
  - planning/meetings: 5
  - reading/research: 8
  - reply/messaging: 5
  - security/appsec: 6
  - skill lifecycle: 6

Recommendation:

> Expand the controlled core modestly, not aggressively. A good target is 100-120 evaluated prompts/skills. This gives stronger evidence than 67 cases without making manual gold-label validation unmanageable.

Do not expand the controlled core just by generating more generic skills. Add new controlled cases only when they introduce a new procedural distinction or a public-skill-derived distinction.

Good expansion sources:

- Public office/file skills: PDF, DOCX, PPTX, XLSX, MarkItDown, OCR, layout conversion, form extraction.
- Public coding/deployment skills: Playwright, Netlify deploy, API design, architecture review, debugging, CI/CD, release packaging.
- Public dataset/research skills: Hugging Face datasets, paper reading, evidence extraction, method comparison, literature synthesis.
- Skill ecosystem skills: skill creation, installation, packaging, evaluation, migration, dependency/resource analysis.
- Communication/workflow skills: brainstorming, planning, implementation plans, handoff summaries, project risk reviews.

Suggested controlled-core additions:

| New cluster | Approx skills/prompts | Why it helps |
|---|---:|---|
| Office artifact operations | 6-8 | Public skills show file-type-specific procedures and resources. |
| Deployment/browser QA | 5-6 | Separates testing, debugging, deployment, and verification. |
| API/backend design | 5-6 | Separates API design, architecture review, dependency analysis, and implementation planning. |
| Dataset/research operations | 5-6 | Adds external data/API/resource dependencies. |
| Skill ecosystem operations v2 | 5-6 | Strengthens meta-skill confusion cases. |
| Planning/creative workflow | 4-5 | Tests vague user-intent and planning-before-execution boundaries. |

This would add about 30-40 new controlled cases, bringing the total to roughly 100-110.

Controlled expansion pass condition:

- Each new prompt has a stable gold label.
- Each new gold skill has at least two plausible alternatives.
- Each gold/alternative distinction differs on at least two procedural axes where possible.
- At least half of the new clusters should be motivated by real public skill artifacts or public skill patterns.
- The original 67-prompt benchmark remains runnable as the v1 baseline.

Implementation rule:

Keep old prompt files stable. Add new prompt files or mark the expanded set as `core_v2`, so we can compare old 67-case results with the expanded 100-120-case results without losing continuity.

## Public Source Candidates

Search results identified several candidate sources:

- Anthropic official skills repository: `anthropics/skills`.
- Anthropic Claude skills documentation.
- `claude-office-skills/skills`, focused on business and office workflows.
- `akillness/oh-my-skills`, a larger community skill collection.
- Other community collections and public repositories containing `SKILL.md`.

Before importing a source, record:

- repository or source URL;
- skill path;
- license if visible;
- whether the skill is copied exactly, wrapped, or summarized;
- whether it contains dependencies, scripts, references, examples, or resources.

## Import Policy

Public skills should enter the benchmark as **background or audit skills**, not as gold-label core skills unless manually converted into a controlled cluster.

Rules:

- Preserve source metadata.
- Do not assume the public skill is high-quality.
- Do not use public skills as strict gold labels without manual gold-label adjudication.
- Keep public skills in a separate family such as `public_imported_background` or `public_audit`.
- If a public skill is near-equivalent to a core gold skill, either record it as an acceptable alternative or move it out of the evaluated pool.

## Real-World Skill Field Audit

For a sampled set of public skills, extract whether each skill contains:

- name;
- description;
- overview/purpose;
- when-to-use or trigger conditions;
- inputs or required input state;
- outputs or output contract;
- workflow steps;
- preconditions;
- dependencies such as CLIs, APIs, libraries, env vars, or files;
- optional resources, references, examples, assets, or scripts;
- limitations, exclusions, or `not_for`-style boundaries;
- verification/evaluation criteria;
- side effects or write/deploy/send actions.

The output should be a table:

| Field | Public-skill prevalence | Why it matters for retrieval |
|---|---:|---|
| Description | high/medium/low | Triggering and first-stage retrieval. |
| Inputs | ... | Distinguishes source type and task state. |
| Outputs | ... | Distinguishes artifact goal. |
| Workflow steps | ... | Distinguishes procedure. |
| Dependencies/resources | ... | Distinguishes feasibility and tool assumptions. |
| Negative boundaries | ... | Prevents plausible-but-wrong matches. |

This field audit becomes evidence for RQ1.

## 2000-Scale Evaluation Policy

The 2000-skill condition should be treated as a **scale-sensitivity check**:

- Run the same 67 prompts and same gold labels.
- Compare 1006 vs 2000 skills.
- Report top-1, top-5, MRR, non-core top-1, and gold first-stage rank.
- Manually inspect non-core winners for whether they are better, acceptable, or merely semantically plausible.

Pass condition:

- Background/public additions increase difficulty or candidate competition without invalidating most gold labels.
- Controlled gold labels remain human-defensible.
- Structure-aware or hybrid methods degrade less than flat methods, or their failure modes are explainable.

Fail condition:

- Many public skills become equally or more correct than the controlled gold labels.
- Results become dominated by noisy imported skills rather than semantic/procedural confusion.
- Scale increases but does not change retrieval behavior at all.

## How This Supports the Thesis

The final framing should be:

> The controlled benchmark tests procedural confusability under known labels. The real-world skill audit checks whether the proposed representation fields correspond to information that public skills actually contain or omit. The 2000-skill condition tests whether the conclusions remain stable when the candidate pool becomes larger and less curated.

This lets us make a stronger claim than "our schema works on our own generated skills." It supports a more general claim:

> Reliable skill retrieval depends on preserving procedural information that is present unevenly across real skill artifacts and often compressed away in description-only retrieval.

## Next Implementation Steps

1. Collect public skill repositories or raw `SKILL.md` URLs.
2. Write or update an importer that can copy public skills into a separate `public_imported_background` family.
3. Add a field-audit script that extracts structural features from public `SKILL.md` files.
4. Expand generated background skills only enough to reach the 2000 target after public imports.
5. Re-export R1/R2/full representations.
6. Rerun benchmark validation Steps 1-6 on the 2000-skill condition.
7. Compare 1006 vs 2000 in the thesis as scale sensitivity, not as a replacement benchmark.
