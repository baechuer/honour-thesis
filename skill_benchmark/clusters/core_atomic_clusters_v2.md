# Core Atomic Cluster Design V2

This benchmark version treats skill selection as a separate candidate-subsetting layer before the main agent loads full skill artifacts.

The design intentionally decomposes broad real-world skills into atomic procedural benchmark skills. A benchmark skill should have one main trigger condition, one expected input shape, one primary workflow, and one success criterion. Optional resources may support execution, but they should not hide a second routing problem.

## Design Sources

- Claude/Anthropic skills: progressive disclosure with metadata, full `SKILL.md`, and optional resources.
- OpenAI skills catalog: skills as reusable folders of instructions, scripts, and resources.
- Anthropic document, spreadsheet, and presentation skills: broad real-world parent skills that motivate atomic decomposition.
- Public browser automation, Playwright, and security threat-modeling skills: realistic examples of task families where the same surface request can require observation, interaction, testing, debugging, or risk analysis.
- Recent skill-retrieval work: SkillRet, SkillRouter, and GoSkills motivate scale, routing, and structure-aware retrieval.

## Representation Variants

These clusters can be evaluated under several selector-visible representations:

| Variant | Selector-visible information | Purpose |
|---|---|---|
| V1 flat metadata | name and positive description | Baseline compressed representation. |
| V2 structured positive schema | input, output, workflow, success criterion | Tests whether procedural fields reduce semantic confusion. |
| V3 structured boundaries | V2 plus `not_for` / avoid conditions | Tests whether negative boundary information helps. |
| V4 full artifact | complete `SKILL.md` and referenced resources | Upper-bound selection signal. |

## Core Clusters

### Document / PDF Processing

Existing family: `documents_files`

Atomic skills:

- `document-summariser`: document to compact narrative recap.
- `document-field-extractor`: document to explicit fields, clauses, figures, names, dates, or reusable structured data.
- `document-rewriter`: document to clearer or more polished content while preserving meaning.
- `document-normaliser`: messy document to consistent readable structure without substantive rewriting.
- `document-converter`: document to another representation when layout fidelity is not the main priority.
- `layout-preserving-converter`: document to another representation while preserving headings, labels, rows, and layout cues.
- `multi-document-comparison-preparer`: multiple documents to aligned comparison-ready structure.

Main confusability pattern: all skills appear to "process documents," but differ by output artifact and success criterion.

### Spreadsheet / Data Analysis

Existing family: `data_spreadsheet`

Atomic skills:

- `data-analysis-overview`: spreadsheet to broad analytical readout.
- `data-analysis-with-validation`: spreadsheet to trustworthiness and data-quality assessment.
- `data-analysis-with-anomaly-focus`: spreadsheet to unusual pattern or outlier assessment.
- `data-analysis-for-root-cause-diagnosis`: spreadsheet to likely-cause explanation.
- `data-analysis-for-forecasting`: spreadsheet to forward-looking estimate.
- `data-analysis-for-ranking-selection`: spreadsheet to ranked recommendation.
- `data-analysis-for-reporting`: spreadsheet to communicable report.

Main confusability pattern: all skills can be triggered by "analyse this spreadsheet," but the procedural objective differs.

### Research / Literature Review

Existing family: `reading_research`

Atomic skills:

- `paper-summariser`: one paper to contribution-focused summary.
- `citation-note-extractor`: source to citation-ready notes.
- `method-note-builder`: paper to method and evaluation notes.
- `related-work-synthesiser`: multiple sources to related-work synthesis.
- `source-grounding-checker`: claim plus source to grounding assessment.
- `multi-source-comparison-builder`: multiple sources to side-by-side comparison.
- `document-extractor`: source to structured extracted facts or fields.
- `general-source-summariser`: source to general compact recap.

Main confusability pattern: all skills share paper/source/citation/summarisation vocabulary, but differ by input state and later writing use.

### Code / GitHub Workflow

New family: `code_github_workflow`

Atomic skills:

- `code-reviewer`: local code or diff to review findings.
- `pr-reviewer`: GitHub PR context to review findings.
- `review-comment-resolver`: existing review comments to implemented fixes or responses.
- `ci-failure-debugger`: failing check/log to root cause and minimal fix.
- `changelog-writer`: completed technical changes to changelog bullets.
- `release-note-writer`: completed changes to user-facing release notes.

Main confusability pattern: all skills involve software changes, but the workflow changes between reviewing, implementing, debugging, and communicating.

### Skill Lifecycle / Meta-Skills

New family: `skill_lifecycle`

Atomic skills:

- `skill-finder`: search existing skill library for candidate matches.
- `skill-installer`: install or prepare installation of an existing skill.
- `skill-creator`: create a new atomic skill artifact.
- `skill-editor`: revise an existing skill.
- `skill-evaluator`: test an existing skill's trigger and behavior.
- `skill-packager`: prepare an existing skill for sharing or distribution.

Main confusability pattern: all skills mention "skills," but the intended operation differs: find, install, create, edit, test, or package.

### Browser / Web Automation

New family: `browser_web_automation`

Atomic skills:

- `web-page-snapshotter`: web page or route to visible-state evidence.
- `web-form-filler`: form or browser flow to step-by-step interaction completion.
- `web-ui-tester`: web interaction to pass/fail behavior report.
- `web-data-extractor`: web page content to structured reusable data.
- `frontend-debugger`: broken UI symptom to likely implementation cause and fix.
- `accessibility-checker`: web interface to accessibility findings and fixes.

Main confusability pattern: all skills involve opening or inspecting web pages, but the required procedure differs between observing, interacting, testing, extracting, debugging, and checking accessibility.

### Security / AppSec

New family: `security_appsec`

Atomic skills:

- `security-threat-modeler`: feature or architecture to assets, trust boundaries, abuse cases, and mitigations.
- `security-code-reviewer`: source code or diff to concrete vulnerability findings.
- `dependency-risk-auditor`: dependency set or lockfile to package and supply-chain risk assessment.
- `secret-leak-scanner`: files, logs, or diffs to exposed-secret findings and remediation.
- `auth-flow-reviewer`: auth/session/permission flow to access-control risk assessment.
- `privacy-risk-reviewer`: data collection and handling flow to privacy risk assessment.

Main confusability pattern: all skills can be described as "security review," but the right evidence and success criterion differ sharply across architecture, code, dependencies, secrets, auth, and privacy.

### Background Scale Distractors

Generated family: `background_scale`

This family is a scale layer rather than a gold-label confusable core. It contains public-skill-inspired but locally authored skills across:

- development and API work
- database and DevOps
- productivity and file management
- finance and business
- legal and compliance
- marketing, sales, and customer success
- context engineering and agent orchestration
- presentation support

Main confusability pattern: background skills create realistic near-domain collisions around the core tasks. For example, `security-code-reviewer` can collide with `security-audit`-style background skills, document extraction can collide with receipt or invoice extraction, and code review can collide with commit, PR description, debugging, or testing skills.

### Public Imported Background

Imported family: `public_imported_background`

This family keeps selected public skills separate from the controlled core. Each imported item has:

- a normalized benchmark-facing `SKILL.md`
- a source URL and raw URL
- an explicit dependency profile
- external dependency and resource signals
- the original public `SKILL.md` under `source/SKILL.original.md` when download succeeds

This family is useful for testing whether representations preserve information that flat metadata often loses: required tools, file formats, repo context, external services, optional references, and execution resources.

## Gold Label Policy

Each prompt should make one gold skill procedurally correct without naming the skill directly. Good benchmark prompts should combine:

- high surface similarity with nearby skills
- one clear procedural differentiator
- a wrong-but-plausible alternative
- stable annotation based on input, workflow, output, or success criterion

## Hierarchy Policy

The core benchmark does not use broad parent skills that internally route to domain resources. Broad public skills such as `xlsx`, `pdf`, or `skill-creator` are treated as realism seeds, then decomposed into atomic benchmark skills.

Optional resources are allowed when they support execution after selection, for example a CI failure checklist or skill packaging checklist. They should not contain alternate domain workflows that require a second selector.
