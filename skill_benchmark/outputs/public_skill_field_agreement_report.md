# Public Skill Field Audit Agreement Report

This report compares the deterministic heuristic field audit with model-assisted semantic extraction.

- Skills compared: 460

Interpretation:

- `both_present`: stronger evidence that the field exists in the public skill.
- `heuristic_only`: likely keyword/heading false positive, or model false negative.
- `model_only`: likely semantic false negative in the heuristic audit.
- `both_missing`: likely missing/proposed field.

## Field Agreement

| Field | Agreement | Both Present | Both Missing | Heuristic Only | Model Only | Avg Model Confidence |
|---|---:|---:|---:|---:|---:|---:|
| `routing_trigger` | 85.7% | 394 | 0 | 66 | 0 | 0.953 |
| `input_precondition` | 70.2% | 276 | 47 | 99 | 38 | 0.901 |
| `output_artifact` | 75.4% | 324 | 23 | 68 | 45 | 0.935 |
| `workflow_procedure` | 83.9% | 365 | 21 | 23 | 51 | 0.959 |
| `constraints_boundaries` | 81.5% | 309 | 66 | 48 | 37 | 0.950 |
| `dependencies_tools` | 85.9% | 369 | 26 | 22 | 43 | 0.958 |
| `resources_references` | 80.4% | 321 | 49 | 56 | 34 | 0.962 |
| `examples_tests` | 91.1% | 397 | 22 | 35 | 6 | 0.959 |
| `safety_side_effects` | 66.7% | 77 | 230 | 93 | 60 | 0.841 |
| `portability_environment` | 80.9% | 312 | 60 | 59 | 29 | 0.903 |
| `hierarchy_links` | 69.8% | 121 | 200 | 22 | 117 | 0.961 |

## Model Evidence Check

| Field | Evidence Found For Model-Present Labels |
|---|---|
| `routing_trigger` | all_evidence_found: 248, some_evidence_found: 62, no_evidence_found: 84 |
| `input_precondition` | all_evidence_found: 200, some_evidence_found: 62, no_evidence_found: 52 |
| `output_artifact` | all_evidence_found: 243, some_evidence_found: 68, no_evidence_found: 58 |
| `workflow_procedure` | no_evidence_found: 71, all_evidence_found: 305, some_evidence_found: 40 |
| `constraints_boundaries` | some_evidence_found: 101, all_evidence_found: 178, no_evidence_found: 67 |
| `dependencies_tools` | all_evidence_found: 308, no_evidence_found: 34, some_evidence_found: 70 |
| `resources_references` | all_evidence_found: 274, some_evidence_found: 38, no_evidence_found: 43 |
| `examples_tests` | no_evidence_found: 72, all_evidence_found: 272, some_evidence_found: 59 |
| `safety_side_effects` | some_evidence_found: 28, all_evidence_found: 91, no_evidence_found: 18 |
| `portability_environment` | all_evidence_found: 227, no_evidence_found: 37, some_evidence_found: 77 |
| `hierarchy_links` | all_evidence_found: 147, no_evidence_found: 49, some_evidence_found: 42 |

## Disagreement Cases For Manual Review

| Skill | Field | Type | Heuristic | Model | Model Evidence | Model Reason |
|---|---|---|---|---|---|---|
| `public-addy-agent-api-and-interface-design` | `input_precondition` | `heuristic_only` | `explicit` | `missing` |  | No verbatim evidence of required input artifacts or prerequisites. |
| `public-addy-agent-api-and-interface-design` | `output_artifact` | `heuristic_only` | `explicit` | `missing` |  | No explicit mention of a deliverable or expected output artifact. |
| `public-addy-agent-api-and-interface-design` | `dependencies_tools` | `heuristic_only` | `extractable` | `missing` |  | No explicitly required tools, APIs, or binaries listed. |
| `public-addy-agent-api-and-interface-design` | `portability_environment` | `heuristic_only` | `extractable` | `missing` |  | No mention of OS, language version, or environment assumptions. |
| `public-addy-agent-api-and-interface-design` | `hierarchy_links` | `model_only` | `missing` | `implicit` | See `deprecation-and-migration` for how to safely remove things users depend on. | Reference to another skill implies a hierarchical or related link. |
| `public-addy-agent-browser-testing-with-devtools` | `resources_references` | `model_only` | `missing` | `implicit` | ## Writing Test Plans for Complex UI Bugs

For complex UI issues, write a structured test plan the agent can follow in the browser: | The skill includes an embedded test plan template as a supporting resource, though not a separate file. |
| `public-addy-agent-ci-cd-and-automation` | `input_precondition` | `heuristic_only` | `extractable` | `missing` |  | No explicit list of required inputs or prerequisites is provided in the text. |
| `public-addy-agent-ci-cd-and-automation` | `output_artifact` | `heuristic_only` | `extractable` | `missing` |  | No specific deliverable or output artifact is described; the skill sets up pipelines, not produces a file. |
| `public-addy-agent-ci-cd-and-automation` | `resources_references` | `heuristic_only` | `extractable` | `missing` |  | No separate files, scripts, or templates are referenced as supporting resources. |
| `public-addy-agent-code-review-and-quality` | `output_artifact` | `model_only` | `missing` | `implicit` | Approve a change when it definitely improves overall code health / Request changes — Issues must be addressed | The review process produces a verdict (approve/request changes) and categorized findings, but no explicit deliverable artifact. |
| `public-addy-agent-code-review-and-quality` | `dependencies_tools` | `heuristic_only` | `extractable` | `missing` |  | No required tools, APIs, or commands explicitly listed for conducting the review itself. |
| `public-addy-agent-code-review-and-quality` | `safety_side_effects` | `heuristic_only` | `explicit` | `missing` |  | No mention of permissions, privacy, destructive actions, or security side effects of the review process. |
| `public-addy-agent-code-review-and-quality` | `portability_environment` | `heuristic_only` | `extractable` | `missing` |  | No information about OS, language, version, runtime, or environment assumptions. |
| `public-addy-agent-code-simplification` | `input_precondition` | `heuristic_only` | `extractable` | `missing` |  | No explicit mention of required input artifacts or prerequisites. |
| `public-addy-agent-code-simplification` | `output_artifact` | `heuristic_only` | `explicit` | `missing` |  | No explicit mention of expected deliverable or output format. |
| `public-addy-agent-code-simplification` | `resources_references` | `model_only` | `missing` | `explicit` | Read CLAUDE.md / project conventions / Inspired by the Claude Code Simplifier plugin | Explicitly references CLAUDE.md and an external plugin as resources. |
| `public-addy-agent-code-simplification` | `portability_environment` | `heuristic_only` | `extractable` | `missing` |  | No mention of OS, language, version, runtime, or environment assumptions. |
| `public-addy-agent-context-engineering` | `input_precondition` | `heuristic_only` | `explicit` | `missing` |  | No explicit statement of required inputs or prerequisites. |
| `public-addy-agent-context-engineering` | `output_artifact` | `heuristic_only` | `explicit` | `missing` |  | No explicit output artifact or deliverable defined. |
| `public-addy-agent-context-engineering` | `workflow_procedure` | `model_only` | `missing` | `explicit` | Pre-task context loading:
1. Read the file(s) you'll modify
2. Read related test files
3. Find one example of a similar pattern already in the codebase
4. Read any type definitions or interfaces involved | The 'Pre-task context loading' subsection provides numbered steps. |
| `public-addy-agent-context-engineering` | `safety_side_effects` | `model_only` | `missing` | `explicit` | Never commit .env files or secrets / Ask before modifying database schema / Always run tests before committing | The 'Boundaries' section explicitly states safety rules. |
| `public-addy-agent-context-engineering` | `portability_environment` | `heuristic_only` | `extractable` | `missing` |  | No mention of OS, language, model, version, or runtime requirements. |
| `public-addy-agent-debugging-and-error-recovery` | `input_precondition` | `heuristic_only` | `extractable` | `missing` |  | No explicit mention of required input artifacts or prior state. |
| `public-addy-agent-debugging-and-error-recovery` | `output_artifact` | `heuristic_only` | `explicit` | `missing` |  | No specific output artifact or deliverable is defined. |
| `public-addy-agent-deprecation-and-migration` | `input_precondition` | `heuristic_only` | `extractable` | `missing` |  | No explicit required input artifacts or prerequisites mentioned. |
| `public-addy-agent-deprecation-and-migration` | `output_artifact` | `heuristic_only` | `extractable` | `missing` |  | No expected output or deliverable specified. |
| `public-addy-agent-deprecation-and-migration` | `dependencies_tools` | `model_only` | `missing` | `implicit` | Run the migration verification script: `npx migrate-check` | A tool is suggested but no explicit list of required tools. |
| `public-addy-agent-deprecation-and-migration` | `safety_side_effects` | `heuristic_only` | `extractable` | `missing` |  | No discussion of permissions, security, or destructive side effects. |
| `public-addy-agent-documentation-and-adrs` | `input_precondition` | `heuristic_only` | `explicit` | `missing` |  | No explicit precondition or required input artifacts are mentioned. |
| `public-addy-agent-documentation-and-adrs` | `dependencies_tools` | `heuristic_only` | `extractable` | `missing` |  | No required tools, APIs, or external services are listed as dependencies for using this documentation skill. |
| `public-addy-agent-documentation-and-adrs` | `safety_side_effects` | `heuristic_only` | `extractable` | `missing` |  | No discussion of permissions, privacy, security, or side effects is present. |
| `public-addy-agent-documentation-and-adrs` | `portability_environment` | `heuristic_only` | `extractable` | `missing` |  | No OS, language, model, version, runtime, or environment assumptions are specified. |
| `public-addy-agent-doubt-driven-development` | `output_artifact` | `heuristic_only` | `extractable` | `missing` |  | No explicit 'output' section; the skill's result is a vetted decision but no concrete deliverable is specified. |
| `public-addy-agent-frontend-ui-engineering` | `input_precondition` | `heuristic_only` | `extractable` | `missing` |  | No mention of required input artifacts, user-provided data, or prerequisites. |
| `public-addy-agent-frontend-ui-engineering` | `workflow_procedure` | `model_only` | `missing` | `implicit` | After building UI: / Component renders without console errors / All interactive elements are keyboard accessible (Tab through the page) | The verification checklist provides ordered steps, and component patterns offer procedural guidance. |
| `public-addy-agent-frontend-ui-engineering` | `hierarchy_links` | `heuristic_only` | `explicit` | `missing` |  | No links to related skills, subskills, or delegated workflows. |
| `public-addy-agent-git-workflow-and-versioning` | `input_precondition` | `heuristic_only` | `extractable` | `missing` |  | No explicit or implicit mention of required input artifacts or prior state. |
| `public-addy-agent-git-workflow-and-versioning` | `resources_references` | `model_only` | `missing` | `explicit` | See the splitting strategies in `code-review-and-quality` for how to break down large changes. / DORA research consistently shows trunk-based development correlates with high-performing engineering teams. | Direct references to another document and external research. |
| `public-addy-agent-git-workflow-and-versioning` | `portability_environment` | `heuristic_only` | `extractable` | `missing` |  | No explicit or implicit mention of OS, language, version, or environment assumptions. |
| `public-addy-agent-git-workflow-and-versioning` | `hierarchy_links` | `model_only` | `missing` | `explicit` | See the splitting strategies in `code-review-and-quality` for how to break down large changes. | Direct link to another skill document. |
| `public-addy-agent-idea-refine` | `dependencies_tools` | `model_only` | `missing` | `explicit` | bash /mnt/skills/user/idea-refine/scripts/idea-refine.sh | The Usage section shows a bash script invocation, and the process mentions specific tools. |
| `public-addy-agent-idea-refine` | `safety_side_effects` | `model_only` | `missing` | `implicit` | Only save if they confirm. | The skill includes a user confirmation step before saving, implying a safety measure against unwanted mutations. |
| `public-addy-agent-incremental-implementation` | `input_precondition` | `heuristic_only` | `extractable` | `missing` |  | No explicit or implicit evidence of required input artifacts or prerequisites. |
| `public-addy-agent-incremental-implementation` | `hierarchy_links` | `model_only` | `missing` | `explicit` | see `git-workflow-and-versioning` for atomic commit guidance | Explicit link to a related skill document. |
| `public-addy-agent-interview-me` | `input_precondition` | `model_only` | `missing` | `implicit` | This skill needs a live, responsive user. Do not invoke in non-interactive contexts / The ask is missing at least one of: **who** the user is, **why** they want it, what **success** looks like, what the binding **constra | The skill requires a responsive user and an underspecified ask, which is inferred from the 'When to Use' and 'Loading Constraints' sections. |
| `public-addy-agent-interview-me` | `safety_side_effects` | `heuristic_only` | `extractable` | `missing` |  | No discussion of permissions, security, mutation risk, or side effects. |
| `public-addy-agent-interview-me` | `hierarchy_links` | `model_only` | `missing` | `explicit` | Interaction with Other Skills / - **`idea-refine`**: downstream. If the confirmed intent is "I want X but I don't know how to scope it," hand off to `idea-refine` to generate variations against the now-explicit intent. / | The 'Interaction with Other Skills' section explicitly links to related skills and their roles. |
| `public-addy-agent-performance-optimization` | `input_precondition` | `heuristic_only` | `extractable` | `missing` |  | No exact verbatim quote for required input artifacts or prerequisites. |
| `public-addy-agent-performance-optimization` | `output_artifact` | `heuristic_only` | `extractable` | `missing` |  | No exact verbatim quote for a specific deliverable or result. |
| `public-addy-agent-performance-optimization` | `hierarchy_links` | `heuristic_only` | `explicit` | `missing` |  | No exact verbatim quote linking to related skills or subskills. |
| `public-addy-agent-planning-and-task-breakdown` | `dependencies_tools` | `heuristic_only` | `extractable` | `missing` |  | No required tools, APIs, or external services are listed. |
| `public-addy-agent-planning-and-task-breakdown` | `portability_environment` | `heuristic_only` | `extractable` | `missing` |  | No OS, language, version, or runtime assumptions are specified. |
| `public-addy-agent-security-and-hardening` | `input_precondition` | `heuristic_only` | `explicit` | `missing` |  | No mention of required input artifacts, user-provided data, or prerequisites. |
| `public-addy-agent-security-and-hardening` | `output_artifact` | `heuristic_only` | `extractable` | `missing` |  | No expected deliverable, file, report, or response format specified. |
| `public-addy-agent-shipping-and-launch` | `input_precondition` | `heuristic_only` | `extractable` | `missing` |  | No explicit listing of required input artifacts or prerequisites. |
| `public-addy-agent-shipping-and-launch` | `output_artifact` | `heuristic_only` | `extractable` | `missing` |  | No explicit deliverable or output format defined. |
| `public-addy-agent-shipping-and-launch` | `hierarchy_links` | `heuristic_only` | `explicit` | `missing` |  | No links to related skills or subskills; references are to checklists not skill documents. |
| `public-addy-agent-source-driven-development` | `input_precondition` | `model_only` | `missing` | `explicit` | Read the project's dependency file to identify exact versions / If versions are missing or ambiguous, ask the user. Don't guess — the version determines which patterns are correct. | Step 1 explicitly requires reading dependency files and asking for versions. |
| `public-addy-agent-source-driven-development` | `output_artifact` | `model_only` | `missing` | `explicit` | Every framework-specific code decision must be backed by official documentation. / Code that matches what the documentation shows / Every framework-specific pattern gets a citation. | The output is code with source citations, as described in Step 3 and Step 4. |
| `public-addy-agent-source-driven-development` | `resources_references` | `model_only` | `missing` | `explicit` | package.json    → Node/React/Vue/Angular/Svelte / composer.json   → PHP/Symfony/Laravel / requirements.txt / pyproject.toml → Python/Django/Flask | Lists dependency files as reference points and includes example source URLs. |
| `public-addy-agent-spec-driven-development` | `safety_side_effects` | `model_only` | `missing` | `implicit` | Never do: Commit secrets, edit vendor directories, remove failing tests without approval | The only safety-related content is the 'Never do' boundary example addressing secrets and destructive actions. |
| `public-addy-agent-spec-driven-development` | `portability_environment` | `heuristic_only` | `extractable` | `missing` |  | No OS, language, version, or runtime requirements are specified for the skill itself. |
| `public-addy-agent-spec-driven-development` | `hierarchy_links` | `model_only` | `missing` | `explicit` | Execute tasks one at a time following skills/incremental-implementation/SKILL.md (incremental-implementation) and skills/test-driven-development/SKILL.md (test-driven-development). Use skills/context-engineering/SKILL.md | The skill explicitly links to three subskills for task execution and context management. |
| `public-addy-agent-using-agent-skills` | `output_artifact` | `heuristic_only` | `extractable` | `missing` |  | No expected deliverable or output artifact is described in the document. |
| `public-addy-agent-using-agent-skills` | `dependencies_tools` | `heuristic_only` | `extractable` | `missing` |  | No external tools, APIs, or commands are listed in the document. |
| `public-addy-agent-using-agent-skills` | `resources_references` | `model_only` | `missing` | `implicit` | \| Define \| interview-me \| Surface what the user actually wants before any plan, spec, or code exists \| / ## Lifecycle Sequence

For a complete feature, the typical skill sequence is:

```
1.  interview-me
2.  idea-re | The Quick Reference table and Lifecycle Sequence reference other skill documents. |
| `public-addy-agent-using-agent-skills` | `safety_side_effects` | `heuristic_only` | `extractable` | `missing` |  | No permissions, security, or destructive action warnings are mentioned. |
| `public-addy-agent-using-agent-skills` | `hierarchy_links` | `model_only` | `missing` | `explicit` | ## Lifecycle Sequence

For a complete feature, the typical skill sequence is:

```
1.  interview-me
2.  idea-refine
3.  spec-driven-development
``` / 3. **Multiple skills can apply.** A feature implementation might invol | The Lifecycle Sequence and Skill Rules explicitly list a sequence of related skills. |
| `public-addy-web-accessibility` | `input_precondition` | `heuristic_only` | `extractable` | `missing` |  | No explicit precondition or required input is stated. |
| `public-addy-web-accessibility` | `constraints_boundaries` | `heuristic_only` | `extractable` | `missing` |  | No explicit scope limits or do-not-use conditions are mentioned. |
| `public-addy-web-accessibility` | `safety_side_effects` | `heuristic_only` | `extractable` | `missing` |  | No permissions, security, or destructive actions are discussed. |
| `public-addy-web-accessibility` | `portability_environment` | `heuristic_only` | `explicit` | `missing` |  | No explicit OS, language version, or runtime environment is specified. |
| `public-addy-web-best-practices` | `input_precondition` | `heuristic_only` | `explicit` | `missing` |  | No direct evidence of required inputs, prerequisites, or prior state. |
| `public-addy-web-best-practices` | `output_artifact` | `heuristic_only` | `extractable` | `missing` |  | No explicit or implicit description of a deliverable or response format. |
| `public-addy-web-best-practices` | `workflow_procedure` | `heuristic_only` | `extractable` | `missing` |  | No ordered steps or concrete process described; only reference content. |
| `public-addy-web-best-practices` | `constraints_boundaries` | `heuristic_only` | `explicit` | `missing` |  | No scope limits, not-for conditions, or guardrails mentioned. |
| `public-addy-web-best-practices` | `examples_tests` | `heuristic_only` | `extractable` | `missing` |  | No sample prompts, expected outputs, tests, or verification checks provided. |
| `public-addy-web-best-practices` | `safety_side_effects` | `heuristic_only` | `explicit` | `missing` |  | No discussion of permissions, privacy, destructive actions, or side effects of using the skill. |
| `public-addy-web-best-practices` | `portability_environment` | `heuristic_only` | `explicit` | `missing` |  | No mention of OS, language version, runtime, or environment assumptions. |
| `public-addy-web-best-practices` | `hierarchy_links` | `model_only` | `missing` | `explicit` | - [Web Quality Audit](../web-quality-audit/SKILL.md) | References section includes a link to a related skill document. |
