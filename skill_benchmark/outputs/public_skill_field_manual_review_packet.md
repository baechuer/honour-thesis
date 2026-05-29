# Public Skill Field Manual Review Packet

Purpose: manually check whether the automated public-skill field audit is overcounting or undercounting field evidence.

Source audit file: `/Users/jackyzhang/Work/Honour Thesis/skill_benchmark/outputs/public_skill_field_audit.jsonl`

Review labels to fill in:

- `correct`: automatic status is reasonable.
- `overcount`: automatic status claims evidence that is too weak.
- `undercount`: automatic status missed evidence visible to a human.
- `ambiguous`: the skill is too broad or underspecified to label confidently.

Pass target before final thesis claims: at least 80% of reviewed field labels should be `correct`, and any systematic overcount should be fixed or disclosed.

## public-anthropic-algorithmic-art

- Origin: `anthropics/skills`
- Source name: `algorithmic-art`
- Source URL: https://github.com/anthropics/skills/tree/main/skills/algorithmic-art
- Audit file: `/Users/jackyzhang/Work/Honour Thesis/skill_benchmark/skills/public_imported_background/public-anthropic-algorithmic-art/source/SKILL.original.md`
- Word count: 2759
- Headings: algorithmic philosophy creation, the critical understanding, how to generate an algorithmic philosophy, philosophy examples, essential principles, deducing the conceptual seed, p5.js implementation, ⚠️ step 0: read the template first ⚠️, technical requirements, craftsmanship requirements, output format, interactive artifact creation, critical: what's fixed vs variable, required features, using the artifact, variations & exploration, the creative process, resources

Manual decision:

- Overall: 
- Broad/hierarchical/atomic? 
- Does this skill support our representation-field taxonomy? 

| Field | Auto Status | Evidence To Check | Human Status | Notes |
|---|---|---|---|---|
| `routing_trigger` | `explicit` | description: Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. / Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems. |  |  |
| `input_precondition` | `explicit` | - What is received: Some subtle input or instructions by the user to take into account, but use as a foundation; it should not constrain creative freedom. / - **ARTISTIC FREEDOM**: The next Claude interprets the philosophy algorithmically - provide creative... |  |  |
| `output_artifact` | `explicit` | Output .md files (philosophy), .html files (interactive viewer), and .js files (generative algorithms). / The result of painstaking frequency calibration where every ratio was carefully chosen to produce resonant beauty. / Every seed produces unique crystal... |  |  |
| `workflow_procedure` | `explicit` | Beauty lives in the process, not the final frame. / - **PROCESS OVER PRODUCT**: Always emphasize that beauty emerges from the algorithm's execution - each run is unique / ## THE CREATIVE PROCESS |  |  |
| `constraints_boundaries` | `extractable` | Create original algorithmic art rather than copying existing artists' work to avoid copyright violations. / - **Avoid redundancy**: Each algorithmic aspect should be mentioned once. / Avoid repeating concepts about noise theory, particle dynamics, or mathem... |  |  |
| `dependencies_tools` | `missing` |  |  |  |
| `resources_references` | `explicit` | ### ⚠️ STEP 0: READ THE TEMPLATE FIRST ⚠️ / - ✅ Copy the template's exact HTML structure / The template is the foundation. |  |  |
| `examples_tests` | `explicit` | ### PHILOSOPHY EXAMPLES / ```javascript / ```javascript |  |  |
| `safety_side_effects` | `extractable` | When particles are near, their phases interfere - constructive interference creates bright nodes, destructive creates voids. |  |  |
| `portability_environment` | `extractable` | - What happens next: The same version receives the philosophy and EXPRESSES IT IN CODE - creating p5.js sketches that are 90% algorithmic generation, 10% essential parameters. / The philosophy must guide the next version to express ideas ALGORITHMICALLY, no... |  |  |
| `hierarchy_links` | `missing` |  |  |  |

## public-architecture-patterns

- Origin: `wshobson/agents via SkillRet preview`
- Source name: `architecture-patterns`
- Source URL: https://github.com/wshobson/agents/tree/main/plugins/backend-development/skills/architecture-patterns
- Audit file: `/Users/jackyzhang/Work/Honour Thesis/skill_benchmark/skills/public_imported_background/public-architecture-patterns/source/SKILL.original.md`
- Word count: 998
- Headings: architecture patterns, when to use this skill, core concepts, 1. clean architecture (uncle bob), 2. hexagonal architecture (ports and adapters), 3. domain-driven design (ddd), detailed patterns and worked examples, testing — in-memory adapters, tests/unit/testcreateuser.py, troubleshooting, use case tests require a running database, circular imports between layers, framework decorators appearing in domain entities, all logic ending up in controllers, value objects raising errors too late, contex

Manual decision:

- Overall: 
- Broad/hierarchical/atomic? 
- Does this skill support our representation-field taxonomy? 

| Field | Auto Status | Evidence To Check | Human Status | Notes |
|---|---|---|---|---|
| `routing_trigger` | `explicit` | description: Implement proven backend architecture patterns including Clean Architecture, Hexagonal Architecture, and Domain-Driven Design. / ## When to Use This Skill |  |  |
| `input_precondition` | `extractable` | - Use in-memory adapters in tests — no Docker required / - `saga-orchestration` — Sagas require well-defined aggregate boundaries, which DDD tactical patterns provide |  |  |
| `output_artifact` | `extractable` | **Produces:** layered structure with clear dependency rules, interface definitions, and test boundaries. / return self._store.get(user_id) / return next((u for u in self._store.values() if u.email == email), None) |  |  |
| `workflow_procedure` | `extractable` | response = await use_case.execute(CreateUserRequest(email="alice@example.com", name="Alice")) / await use_case.execute(CreateUserRequest(email="alice@example.com", name="Alice")) / response = await use_case.execute(CreateUserRequest(email="alice@example.com... |  |  |
| `constraints_boundaries` | `extractable` | - Creating testable codebases where use-case tests do not require a running database / - **Bounded Contexts**: Isolate a coherent model for one subdomain; avoid sharing a single model across the whole system / It must never import from `adapters/` or `infra... |  |  |
| `dependencies_tools` | `missing` |  |  |  |
| `resources_references` | `explicit` | Detailed pattern documentation lives in `references/details.md`. / - [`references/advanced-patterns.md`](references/advanced-patterns.md) / ## Related Skills |  |  |
| `examples_tests` | `explicit` | ## Detailed patterns and worked examples / ```python / ### Use case tests require a running database |  |  |
| `safety_side_effects` | `missing` |  |  |  |
| `portability_environment` | `extractable` | - **Bounded Contexts**: Isolate a coherent model for one subdomain; avoid sharing a single model across the whole system / Create a separate ORM model in `adapters/repositories/` and map to/from the domain entity in the repository's `_to_entity()` method. |  |  |
| `hierarchy_links` | `explicit` | ## Related Skills |  |  |

## public-writing-plans

- Origin: `obra/superpowers via SkillRet preview`
- Source name: `writing-plans`
- Source URL: https://github.com/obra/superpowers/tree/main/skills/writing-plans
- Audit file: `/Users/jackyzhang/Work/Honour Thesis/skill_benchmark/skills/public_imported_background/public-writing-plans/source/SKILL.original.md`
- Word count: 918
- Headings: writing plans, overview, scope check, file structure, bite-sized task granularity, plan document header, [feature name] implementation plan, task structure, task n: [component name], no placeholders, remember, self-review, execution handoff

Manual decision:

- Overall: 
- Broad/hierarchical/atomic? 
- Does this skill support our representation-field taxonomy? 

| Field | Auto Status | Evidence To Check | Human Status | Notes |
|---|---|---|---|---|
| `routing_trigger` | `explicit` | description: Use when you have a spec or requirements for a multi-step task, before touching code / ## Overview |  |  |
| `input_precondition` | `extractable` | > **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. / result = function(input) / def function(input): |  |  |
| `output_artifact` | `extractable` | Each plan should produce working, testable software on its own. / Each task should produce self-contained changes that make sense independently. / return expected |  |  |
| `workflow_procedure` | `extractable` | - "Run the tests and make sure they pass" - step / - [ ] **Step 1: Write the failing test** / - [ ] **Step 2: Run test to verify it fails** |  |  |
| `constraints_boundaries` | `explicit` | Assume they don't know good test design very well. / ## Scope Check / If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable. |  |  |
| `dependencies_tools` | `missing` |  |  |  |
| `resources_references` | `missing` |  |  |  |
| `examples_tests` | `extractable` | ```markdown / ````markdown / ```python |  |  |
| `safety_side_effects` | `missing` |  |  |  |
| `portability_environment` | `missing` |  |  |  |
| `hierarchy_links` | `explicit` | > **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. / This is a checklist you run yourself — not a subagent dispatch. / ## Execution Han... |  |  |

## public-huggingface-huggingface-paper-publisher

- Origin: `huggingface/skills`
- Source name: `huggingface-paper-publisher`
- Source URL: https://github.com/huggingface/skills/tree/main/skills/huggingface-paper-publisher
- Audit file: `/Users/jackyzhang/Work/Honour Thesis/skill_benchmark/skills/public_imported_background/public-huggingface-huggingface-paper-publisher/source/SKILL.original.md`
- Word count: 2111
- Headings: overview, integration with hf ecosystem, version, dependencies, core capabilities, 1. paper page management, 2. link papers to artifacts, 3. research article creation, 4. metadata management, usage instructions, prerequisites, method 1: index paper from arxiv, method 2: link paper to model/dataset, how linking works, method 3: claim authorship, method 4: manage paper visibility, method 5: create research article, paper template structure, abstract, 1. introduction, 2. related work, 3. methodolog

Manual decision:

- Overall: 
- Broad/hierarchical/atomic? 
- Does this skill support our representation-field taxonomy? 

| Field | Auto Status | Evidence To Check | Human Status | Notes |
|---|---|---|---|---|
| `routing_trigger` | `explicit` | description: Publish and manage research papers on Hugging Face Hub. / # Overview / # Core Capabilities |  |  |
| `input_precondition` | `extractable` | When linking papers to models or datasets, proper YAML frontmatter is required: |  |  |
| `output_artifact` | `extractable` | - `ml-report` - Machine learning experiment report |  |  |
| `workflow_procedure` | `explicit` | It streamlines the workflow from paper creation to publication, including integration with arXiv, model/dataset linking, and authorship management. / # Usage Instructions / **Start Claim Process:** |  |  |
| `constraints_boundaries` | `missing` |  |  |  |
| `dependencies_tools` | `explicit` | # Dependencies / The included script uses PEP 723 inline dependencies. / - Run scripts with `uv run` (dependencies are resolved from the script header) |  |  |
| `resources_references` | `explicit` | - **Research Article Template**: Generate professional, modern scientific papers / - **Citation Management**: Maintain proper attribution and references / - **Citation Tracking**: Maintain paper references across repositories |  |  |
| `examples_tests` | `explicit` | ```markdown / ```bibtex / ### Integration Examples |  |  |
| `safety_side_effects` | `extractable` | - **Permission Denied**: HF_TOKEN lacks write access to repository |  |  |
| `portability_environment` | `explicit` | It streamlines the workflow from paper creation to publication, including integration with arXiv, model/dataset linking, and authorship management. / - **Model/Dataset Linking**: Connect papers to relevant artifacts through metadata / # Version |  |  |
| `hierarchy_links` | `explicit` | # Check all paper links in a repository |  |  |

## public-markitdown

- Origin: `K-Dense-AI/scientific-agent-skills via public skill directory`
- Source name: `markitdown`
- Source URL: https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/markitdown
- Audit file: `/Users/jackyzhang/Work/Honour Thesis/skill_benchmark/skills/public_imported_background/public-markitdown/source/SKILL.original.md`
- Word count: 1524
- Headings: markitdown - file to markdown conversion, overview, visual enhancement with scientific schematics, supported formats, quick start, installation, install with all features, or from source, command-line usage, basic conversion, specify output file, pipe content, enable plugins, python api, basic usage, convert from stream, advanced features, 1. ai-enhanced image descriptions, initialize openrouter client (openai-compatible api), 2. azure document intelligence, command line, python api, 3. plugin s

Manual decision:

- Overall: 
- Broad/hierarchical/atomic? 
- Does this skill support our representation-field taxonomy? 

| Field | Auto Status | Evidence To Check | Human Status | Notes |
|---|---|---|---|---|
| `routing_trigger` | `explicit` | description: Convert files and office documents to Markdown. / ## Overview / python scripts/generate_schematic.py "your diagram description" -o figures/output.png |  |  |
| `input_precondition` | `explicit` | ## Quick Start / - **Audio transcription**: Requires additional compute resources / - **AI image descriptions**: Requires API calls (costs may apply) |  |  |
| `output_artifact` | `explicit` | python scripts/generate_schematic.py "your diagram description" -o figures/output.png / markitdown document.pdf > output.md / # Specify output file |  |  |
| `workflow_procedure` | `explicit` | - Document conversion workflow diagrams / - Integration workflow visualizations / Process Multiple Documents |  |  |
| `constraints_boundaries` | `missing` |  |  |  |
| `dependencies_tools` | `explicit` | allowed-tools: Read Write Edit Bash / ### Installation / # Install with all features |  |  |
| `resources_references` | `explicit` | python scripts/generate_schematic.py "your diagram description" -o figures/output.png / # Or from source / - **Audio transcription**: Requires additional compute resources |  |  |
| `examples_tests` | `extractable` | ```python / ```python / ```python |  |  |
| `safety_side_effects` | `missing` |  |  |  |
| `portability_environment` | `explicit` | version: "1.0" |  |  |
| `hierarchy_links` | `extractable` | For detailed guidance on creating schematics, refer to the scientific-schematics skill documentation. |  |  |

## public-openai-chatgpt-apps

- Origin: `openai/skills`
- Source name: `chatgpt-apps`
- Source URL: https://github.com/openai/skills/tree/main/skills/.curated/chatgpt-apps
- Audit file: `/Users/jackyzhang/Work/Honour Thesis/skill_benchmark/skills/public_imported_background/public-openai-chatgpt-apps/source/SKILL.original.md`
- Word count: 2704
- Headings: chatgpt apps, overview, mandatory docs-first workflow, prompt guidance, classify the app before choosing code, default starting-point order, build workflow, 0. classify the app archetype, 1. plan tools before code, 2. choose an app architecture, 2a. start from an upstream example when one fits, 2b. use the starter script when a low-dependency fallback helps, 3. scaffold the mcp server, 4. scaffold the widget ui, api surface guardrails, 5. add resource metadata and security, 5a. enforce a minimum

Manual decision:

- Overall: 
- Broad/hierarchical/atomic? 
- Does this skill support our representation-field taxonomy? 

| Field | Auto Status | Evidence To Check | Human Status | Notes |
|---|---|---|---|---|
| `routing_trigger` | `explicit` | description: Build, scaffold, refactor, and troubleshoot ChatGPT Apps SDK applications that combine an MCP server and widget UI. / Use when Codex needs to design tools, register UI resources, wire the MCP Apps bridge or ChatGPT compatibility APIs, apply App... |  |  |
| `input_precondition` | `extractable` | - Make inputs explicit and machine-friendly (enums, required fields, bounds). / - If auth is required, include review-safe demo credentials and test the login path end-to-end |  |  |
| `output_artifact` | `explicit` | Use when Codex needs to design tools, register UI resources, wire the MCP Apps bridge or ChatGPT compatibility APIs, apply Apps SDK metadata or CSP or domain settings, or produce a docs-aligned project scaffold. / Use this skill to produce: / - A validation... |  |  |
| `workflow_procedure` | `explicit` | Prefer a docs-first workflow by invoking the openai-docs skill or OpenAI developer docs MCP tools before generating code. / Scaffold ChatGPT Apps SDK implementations with a docs-first, example-first workflow, then generate code that follows current Apps SDK... |  |  |
| `constraints_boundaries` | `explicit` | If doc search times out or returns poor matches, fetch the canonical Apps SDK pages directly by URL and continue; do not let search failure block scaffolding. / Do not generate a large custom scaffold from scratch if a close upstream example already exists.... |  |  |
| `dependencies_tools` | `explicit` | description: Build, scaffold, refactor, and troubleshoot ChatGPT Apps SDK applications that combine an MCP server and widget UI. / Use when Codex needs to design tools, register UI resources, wire the MCP Apps bridge or ChatGPT compatibility APIs, apply App... |  |  |
| `resources_references` | `explicit` | Read `references/apps-sdk-docs-workflow.md` for suggested doc queries and a compact checklist. / Read `references/app-archetypes.md` to classify the request into a small number of supported app shapes before choosing examples or scaffolds. / Read `reference... |  |  |
| `examples_tests` | `explicit` |  |  |  |
| `safety_side_effects` | `explicit` | - Read-only vs mutating tools / - whether `search` and `fetch` should be the default read-only tool surface / - If the app is connector-like, data-only, sync-oriented, or intended for company knowledge or deep research, default to the standard `search` and ... |  |  |
| `portability_environment` | `extractable` | - For educational/demo apps, prefer one concept per tool so the model can pick the right example cleanly. / - Returns `structuredContent` (model + widget), `content` (model narration), and `_meta` (widget-only data) intentionally / - Use `ui/update-model-co... |  |  |
| `hierarchy_links` | `missing` |  |  |  |

## public-office-slack-workflows

- Origin: `claude-office-skills/skills`
- Source name: `slack-workflows`
- Source URL: https://github.com/claude-office-skills/skills/tree/main/slack-workflows
- Audit file: `/Users/jackyzhang/Work/Honour Thesis/skill_benchmark/skills/public_imported_background/public-office-slack-workflows/source/SKILL.original.md`
- Word count: 1087
- Headings: slack workflows, overview, core workflows, 1. daily standup bot, 2. approval workflow, 3. new hire onboarding, 4. incident response, 5. cross-platform sync, slash commands, custom commands, channel management, output example, deal win notification setup, workflow configuration, message template, n8n implementation, sample output

Manual decision:

- Overall: 
- Broad/hierarchical/atomic? 
- Does this skill support our representation-field taxonomy? 

| Field | Auto Status | Evidence To Check | Human Status | Notes |
|---|---|---|---|---|
| `routing_trigger` | `explicit` | description: "Slack automation and workflow builder - notifications, standup bots, approval flows, and cross-platform integrations" / category: productivity / capabilities: |  |  |
| `input_precondition` | `missing` |  |  |  |
| `output_artifact` | `explicit` | ## Output Example / **Output**: / ## Sample Output |  |  |
| `workflow_procedure` | `explicit` | description: "Slack automation and workflow builder - notifications, standup bots, approval flows, and cross-platform integrations" / - workflow / workflow: "Async Standup" |  |  |
| `constraints_boundaries` | `missing` |  |  |  |
| `dependencies_tools` | `explicit` | # Deal Win Notification Setup |  |  |
| `resources_references` | `explicit` | related_skills: / ## Message Template |  |  |
| `examples_tests` | `explicit` | ## Output Example / ```markdown / ```javascript |  |  |
| `safety_side_effects` | `missing` |  |  |  |
| `portability_environment` | `explicit` | version: "1.0.0" / languages: |  |  |
| `hierarchy_links` | `explicit` | related_skills: |  |  |

## public-addy-agent-git-workflow-and-versioning

- Origin: `addyosmani/agent-skills`
- Source name: `git-workflow-and-versioning`
- Source URL: https://github.com/addyosmani/agent-skills/tree/main/skills/git-workflow-and-versioning
- Audit file: `/Users/jackyzhang/Work/Honour Thesis/skill_benchmark/skills/public_imported_background/public-addy-agent-git-workflow-and-versioning/source/SKILL.original.md`
- Word count: 1539
- Headings: git workflow and versioning, overview, when to use, core principles, trunk-based development (recommended), 1. commit early, commit often, 2. atomic commits, good: each commit is self-contained, bad: everything mixed together, 3. descriptive messages, good: explains intent, bad: describes what's obvious from the diff, 4. keep concerns separate, good: separate concerns, bad: mixed concerns, 5. size your changes, branching strategy, feature branches, branch naming, working with worktrees, create a

Manual decision:

- Overall: 
- Broad/hierarchical/atomic? 
- Does this skill support our representation-field taxonomy? 

| Field | Auto Status | Evidence To Check | Human Status | Notes |
|---|---|---|---|---|
| `routing_trigger` | `explicit` | description: Structures git workflow practices. / Use when making any code change. / Use when committing, branching, resolving conflicts, or when you need to organize work across multiple parallel streams. |  |  |
| `input_precondition` | `extractable` | Use when committing, branching, resolving conflicts, or when you need to organize work across multiple parallel streams. / - **Release branches are acceptable.** When you need to stabilize a release while main moves forward. / After any modification, provid... |  |  |
| `output_artifact` | `extractable` | - **Don't commit** build output (`dist/`, `.next/`), environment files (`.env`), or IDE config (`.vscode/settings.json` unless shared) |  |  |
| `workflow_procedure` | `explicit` | description: Structures git workflow practices. / # Git Workflow and Versioning |  |  |
| `constraints_boundaries` | `extractable` | Don't accumulate large uncommitted changes. / Don't combine formatting changes with behavior changes. / Don't combine refactors with features. |  |  |
| `dependencies_tools` | `extractable` | consistent with existing validation patterns in auth.ts. / update auth.ts / - src/routes/auth.ts: Has similar validation gap but out of scope |  |  |
| `resources_references` | `missing` |  |  |  |
| `examples_tests` | `explicit` | # Git checkouts midpoints; run your test at each to narrow down |  |  |
| `safety_side_effects` | `extractable` | - **Dev branches are costs.** Every day a branch lives, it accumulates merge risk. |  |  |
| `portability_environment` | `extractable` | With AI agents generating code at high speed, disciplined version control is the mechanism that keeps changes manageable, reviewable, and reversible. / Teams using gitflow or long-lived branches can adapt the principles (atomic commits, small changes, descr... |  |  |
| `hierarchy_links` | `missing` |  |  |  |

## public-addy-web-best-practices

- Origin: `addyosmani/web-quality-skills`
- Source name: `best-practices`
- Source URL: https://github.com/addyosmani/web-quality-skills/tree/main/skills/best-practices
- Audit file: `/Users/jackyzhang/Work/Honour Thesis/skill_benchmark/skills/public_imported_background/public-addy-web-best-practices/source/SKILL.original.md`
- Word count: 2029
- Headings: best practices, security, https everywhere, content security policy (csp), trusted types (modern dom-xss defense), subresource integrity (sri) for third-party scripts, security headers, prevent clickjacking — prefer csp frame-ancestors (above); x-frame-options, is the legacy fallback for older browsers., prevent mime type sniffing, do not send x-xss-protection. the legacy browser xss auditor was deprecated, and removed (chrome 78, edge 17), and in some cases it introduced its own, vulnerabilitie

Manual decision:

- Overall: 
- Broad/hierarchical/atomic? 
- Does this skill support our representation-field taxonomy? 

| Field | Auto Status | Evidence To Check | Human Status | Notes |
|---|---|---|---|---|
| `routing_trigger` | `explicit` | description: Apply modern web development best practices for security, compatibility, and code quality. / Use when asked to "apply best practices", "security audit", "modernize code", "code quality review", or "check for vulnerabilities". |  |  |
| `input_precondition` | `explicit` | SRI requires `crossorigin` and an `Access-Control-Allow-Origin` response header from the CDN. / // ❌ Recursive merges of untrusted input can pollute Object.prototype / ### Input sanitization |  |  |
| `output_artifact` | `extractable` | Angular has built-in Trusted Types support; React 19+ produces TrustedHTML when Trusted Types are enforced; for everything else, [DOMPurify](https://github.com/cure53/DOMPurify) is the de-facto sanitizer. / return { hasError: true }; / return <FallbackUI />; |  |  |
| `workflow_procedure` | `extractable` | If the CDN is compromised — as happened to polyfill.io in 2024 — the browser refuses to execute a file whose hash doesn't match. / devtool: process.env.NODE_ENV === 'production' ? |  |  |
| `constraints_boundaries` | `explicit` | Avoid protocol-relative URLs (`//example.com/...`) — they're an HTTP-era pattern with no benefit on HTTPS-only sites and hide the actual scheme from reviewers. / Pin every `<script>` and `<link rel="stylesheet">` you load from a CDN you don't control. / `in... |  |  |
| `dependencies_tools` | `explicit` | Configure your bundler to omit `sourcesContent`, or use a Sentry/Bugsnag CLI flag that does so when uploading. / ## Tools |  |  |
| `resources_references` | `explicit` | ### Subresource Integrity (SRI) for third-party scripts / ## Source maps / // ❌ Source maps exposed in production |  |  |
| `examples_tests` | `extractable` | ```javascript / ```javascript / ```javascript |  |  |
| `safety_side_effects` | `explicit` | description: Apply modern web development best practices for security, compatibility, and code quality. / Use when asked to "apply best practices", "security audit", "modernize code", "code quality review", or "check for vulnerabilities". / Covers security,... |  |  |
| `portability_environment` | `explicit` | description: Apply modern web development best practices for security, compatibility, and code quality. / version: "1.0" / Covers security, browser compatibility, and code quality patterns. |  |  |
| `hierarchy_links` | `missing` |  |  |  |

## public-lbussell-triaging-issues

- Origin: `lbussell/agent-skills`
- Source name: `triaging-issues`
- Source URL: https://github.com/lbussell/agent-skills/tree/main/skills/triaging-issues
- Audit file: `/Users/jackyzhang/Work/Honour Thesis/skill_benchmark/skills/public_imported_background/public-lbussell-triaging-issues/source/SKILL.original.md`
- Word count: 452
- Headings: workflow, step 1: list untriaged issues, step 2: investigate each issue, step 3: correlate with recent activity, step 4: categorize and present results

Manual decision:

- Overall: 
- Broad/hierarchical/atomic? 
- Does this skill support our representation-field taxonomy? 

| Field | Auto Status | Evidence To Check | Human Status | Notes |
|---|---|---|---|---|
| `routing_trigger` | `explicit` | description: >- |  |  |
| `input_precondition` | `missing` |  |  |  |
| `output_artifact` | `missing` |  |  |  |
| `workflow_procedure` | `explicit` | ## Workflow / ### Step 1: List untriaged issues / ### Step 2: Investigate each issue |  |  |
| `constraints_boundaries` | `extractable` | Do not modify issues, apply labels, assign users, post comments, or close issues.** |  |  |
| `dependencies_tools` | `missing` |  |  |  |
| `resources_references` | `missing` |  |  |  |
| `examples_tests` | `extractable` | ```shell |  |  |
| `safety_side_effects` | `missing` |  |  |  |
| `portability_environment` | `missing` |  |  |  |
| `hierarchy_links` | `missing` |  |  |  |

## public-mattpocock-git-guardrails-claude-code

- Origin: `mattpocock/skills`
- Source name: `git-guardrails-claude-code`
- Source URL: https://github.com/mattpocock/skills/tree/main/skills/misc/git-guardrails-claude-code
- Audit file: `/Users/jackyzhang/Work/Honour Thesis/skill_benchmark/skills/public_imported_background/public-mattpocock-git-guardrails-claude-code/source/SKILL.original.md`
- Word count: 300
- Headings: setup git guardrails, what gets blocked, steps, 1. ask scope, 2. copy the hook script, 3. add hook to settings, 4. ask about customization, 5. verify

Manual decision:

- Overall: 
- Broad/hierarchical/atomic? 
- Does this skill support our representation-field taxonomy? 

| Field | Auto Status | Evidence To Check | Human Status | Notes |
|---|---|---|---|---|
| `routing_trigger` | `explicit` | description: Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. / Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code. |  |  |
| `input_precondition` | `missing` |  |  |  |
| `output_artifact` | `missing` |  |  |  |
| `workflow_procedure` | `explicit` | description: Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. / ## Steps |  |  |
| `constraints_boundaries` | `explicit` | # Setup Git Guardrails / If the settings file already exists, merge the hook into existing `hooks.PreToolUse` array — don't overwrite other settings. |  |  |
| `dependencies_tools` | `explicit` | # Setup Git Guardrails / Ask the user: install for **this project only** (`.claude/settings.json`) or **all projects** (`~/.claude/settings.json`)? |  |  |
| `resources_references` | `extractable` | The bundled script is at: [scripts/block-dangerous-git.sh](scripts/block-dangerous-git.sh) |  |  |
| `examples_tests` | `extractable` |  |  |  |
| `safety_side_effects` | `extractable` | Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code. |  |  |
| `portability_environment` | `missing` |  |  |  |
| `hierarchy_links` | `missing` |  |  |  |

## public-n-skills-dev-browser

- Origin: `numman-ali/n-skills`
- Source name: `dev-browser`
- Source URL: https://github.com/numman-ali/n-skills/tree/main/skills/automation/dev-browser/skills/dev-browser
- Audit file: `/Users/jackyzhang/Work/Honour Thesis/skill_benchmark/skills/public_imported_background/public-n-skills-dev-browser/source/SKILL.original.md`
- Word count: 87
- Headings: dev browser, installation, usage

Manual decision:

- Overall: 
- Broad/hierarchical/atomic? 
- Does this skill support our representation-field taxonomy? 

| Field | Auto Status | Evidence To Check | Human Status | Notes |
|---|---|---|---|---|
| `routing_trigger` | `explicit` | description: Browser automation with persistent page state. / Use when users ask to navigate websites, fill forms, take screenshots, extract web data, test web apps, or automate browser workflows. |  |  |
| `input_precondition` | `missing` |  |  |  |
| `output_artifact` | `missing` |  |  |  |
| `workflow_procedure` | `missing` |  |  |  |
| `constraints_boundaries` | `missing` |  |  |  |
| `dependencies_tools` | `explicit` | A CLI for controlling browsers with sandboxed JavaScript scripts. / ## Installation / npm install -g dev-browser |  |  |
| `resources_references` | `missing` |  |  |  |
| `examples_tests` | `extractable` |  |  |  |
| `safety_side_effects` | `missing` |  |  |  |
| `portability_environment` | `missing` |  |  |  |
| `hierarchy_links` | `missing` |  |  |  |

## public-obsidian-obsidian-markdown

- Origin: `kepano/obsidian-skills`
- Source name: `obsidian-markdown`
- Source URL: https://github.com/kepano/obsidian-skills/tree/main/skills/obsidian-markdown
- Audit file: `/Users/jackyzhang/Work/Honour Thesis/skill_benchmark/skills/public_imported_background/public-obsidian-obsidian-markdown/source/SKILL.original.md`
- Word count: 675
- Headings: obsidian flavored markdown skill, workflow: creating an obsidian note, internal links (wikilinks), embeds, callouts, properties (frontmatter), tags, comments, obsidian-specific formatting, math (latex), diagrams (mermaid), footnotes, complete example, project alpha, tasks, notes, references

Manual decision:

- Overall: 
- Broad/hierarchical/atomic? 
- Does this skill support our representation-field taxonomy? 

| Field | Auto Status | Evidence To Check | Human Status | Notes |
|---|---|---|---|---|
| `routing_trigger` | `explicit` | description: Create and edit Obsidian Flavored Markdown with wikilinks, embeds, callouts, properties, and other Obsidian-specific syntax. / Use when working with .md files in Obsidian, or when the user mentions wikilinks, callouts, frontmatter, tags, embeds... |  |  |
| `input_precondition` | `missing` |  |  |  |
| `output_artifact` | `missing` |  |  |  |
| `workflow_procedure` | `explicit` | ## Workflow: Creating an Obsidian Note / This project aims to [[improve workflow]] using modern techniques. |  |  |
| `constraints_boundaries` | `missing` |  |  |  |
| `dependencies_tools` | `missing` |  |  |  |
| `resources_references` | `explicit` | See [PROPERTIES.md](references/PROPERTIES.md) for all property types. / See [EMBEDS.md](references/EMBEDS.md) for all embed types. / See [CALLOUTS.md](references/CALLOUTS.md) for all callout types. |  |  |
| `examples_tests` | `explicit` | ```markdown / ```markdown / ```markdown |  |  |
| `safety_side_effects` | `missing` |  |  |  |
| `portability_environment` | `missing` |  |  |  |
| `hierarchy_links` | `explicit` | ## Internal Links (Wikilinks) |  |  |

## public-oh-my-hyperfine-benchmarking

- Origin: `akillness/oh-my-skills`
- Source name: `hyperfine-benchmarking`
- Source URL: https://github.com/akillness/oh-my-skills/tree/main/.agent-skills/hyperfine-benchmarking
- Audit file: `/Users/jackyzhang/Work/Honour Thesis/skill_benchmark/skills/public_imported_background/public-oh-my-hyperfine-benchmarking/source/SKILL.original.md`
- Word count: 227
- Headings: hyperfine-benchmarking, when to use this skill, instructions, examples, availability check, two-command comparison, parameter sweep, export artifacts, best practices, references

Manual decision:

- Overall: 
- Broad/hierarchical/atomic? 
- Does this skill support our representation-field taxonomy? 

| Field | Auto Status | Evidence To Check | Human Status | Notes |
|---|---|---|---|---|
| `routing_trigger` | `explicit` | description: Use this skill to benchmark shell commands reliably with warmup runs, statistical summaries, and exportable artifacts using hyperfine. / ## When to use this skill |  |  |
| `input_precondition` | `extractable` | Keep input/workdir/environment stable across compared commands. / 'mytool --mode {mode} input.txt' |  |  |
| `output_artifact` | `extractable` | Benchmark CLI commands with reproducible methodology instead of one-off `time` output. |  |  |
| `workflow_procedure` | `explicit` | ## Instructions |  |  |
| `constraints_boundaries` | `extractable` | - Do not compare commands with different semantics unless outputs are normalized. |  |  |
| `dependencies_tools` | `explicit` | allowed-tools: Bash Read Write / Benchmark CLI commands with reproducible methodology instead of one-off `time` output. |  |  |
| `resources_references` | `explicit` | ## References |  |  |
| `examples_tests` | `explicit` | ## Examples |  |  |
| `safety_side_effects` | `extractable` | Summarize relative speedup + risk notes. |  |  |
| `portability_environment` | `missing` |  |  |  |
| `hierarchy_links` | `missing` |  |  |  |

## public-swebench-k8s-manifest-generator

- Origin: `GeniusHTX/SWE-Skills-Bench`
- Source name: `k8s-manifest-generator`
- Source URL: https://github.com/GeniusHTX/SWE-Skills-Bench/tree/main/skills/k8s-manifest-generator
- Audit file: `/Users/jackyzhang/Work/Honour Thesis/skill_benchmark/skills/public_imported_background/public-swebench-k8s-manifest-generator/source/SKILL.original.md`
- Word count: 1483
- Headings: kubernetes manifest generator, purpose, when to use this skill, step-by-step workflow, 1. gather requirements, 2. create deployment manifest, 3. create service manifest, 4. create configmap, for config files, 5. create secret, for certificate files, 6. create persistentvolumeclaim (if needed), 7. apply security best practices, 8. add labels and annotations, 9. organize multi-resource manifests, app-name.yaml, 10. validate and test, dry-run validation, server-side validation, validate with kubeva

Manual decision:

- Overall: 
- Broad/hierarchical/atomic? 
- Does this skill support our representation-field taxonomy? 

| Field | Auto Status | Evidence To Check | Human Status | Notes |
|---|---|---|---|---|
| `routing_trigger` | `explicit` | description: Create production-ready Kubernetes manifests for Deployments, Services, ConfigMaps, and Secrets following best practices and security standards. / Use when generating Kubernetes YAML manifests, creating K8s resources, or implementing production... |  |  |
| `input_precondition` | `explicit` | Use this skill when you need to: / - [ ] All required fields are present |  |  |
| `output_artifact` | `missing` |  |  |  |
| `workflow_procedure` | `explicit` | ## Step-by-Step Workflow / ## Next Steps |  |  |
| `constraints_boundaries` | `extractable` | - Use specific image tags (never `:latest`) / - Never commit secrets to Git in plain text / **Use specific image tags** - Avoid unpredictable deployments |  |  |
| `dependencies_tools` | `extractable` | - Environment variables and configuration needs / - Secret for API keys |  |  |
| `resources_references` | `explicit` | template: / **Reference:** See `references/deployment-spec.md` for detailed deployment options / **Reference:** See `references/service-spec.md` for service types and networking |  |  |
| `examples_tests` | `explicit` |  |  |  |
| `safety_side_effects` | `explicit` | description: Create production-ready Kubernetes manifests for Deployments, Services, ConfigMaps, and Secrets following best practices and security standards. / - Implement resource limits, health checks, and security contexts / - Apply security context for ... |  |  |
| `portability_environment` | `extractable` | - Container image and version / version: <version> / version: <version> |  |  |
| `hierarchy_links` | `explicit` | ## Related Skills |  |  |
