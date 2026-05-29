# Public Skill Field Audit Agreement Report

This report compares the deterministic heuristic field audit with model-assisted semantic extraction.

- Skills compared: 200

Interpretation:

- `both_present`: stronger evidence that the field exists in the public skill.
- `heuristic_only`: likely keyword/heading false positive, or model false negative.
- `model_only`: likely semantic false negative in the heuristic audit.
- `both_missing`: likely missing/proposed field.

## Field Agreement

| Field | Agreement | Both Present | Both Missing | Heuristic Only | Model Only | Avg Model Confidence |
|---|---:|---:|---:|---:|---:|---:|
| `routing_trigger` | 68.0% | 136 | 0 | 64 | 0 | 0.903 |
| `input_precondition` | 83.0% | 153 | 13 | 22 | 12 | 0.909 |
| `output_artifact` | 85.5% | 168 | 3 | 14 | 15 | 0.944 |
| `workflow_procedure` | 85.5% | 168 | 3 | 13 | 16 | 0.950 |
| `constraints_boundaries` | 81.0% | 116 | 46 | 27 | 11 | 0.943 |
| `dependencies_tools` | 92.0% | 177 | 7 | 3 | 13 | 0.970 |
| `resources_references` | 74.5% | 131 | 18 | 42 | 9 | 0.947 |
| `examples_tests` | 91.5% | 173 | 10 | 14 | 3 | 0.951 |
| `safety_side_effects` | 72.0% | 24 | 120 | 29 | 27 | 0.842 |
| `portability_environment` | 87.5% | 157 | 18 | 14 | 11 | 0.917 |
| `hierarchy_links` | 88.5% | 86 | 91 | 7 | 16 | 0.971 |

## Model Evidence Check

| Field | Evidence Found For Model-Present Labels |
|---|---|
| `routing_trigger` | all_evidence_found: 118, some_evidence_found: 14, no_evidence_found: 4 |
| `input_precondition` | some_evidence_found: 22, all_evidence_found: 117, no_evidence_found: 26 |
| `output_artifact` | some_evidence_found: 21, all_evidence_found: 137, no_evidence_found: 25 |
| `workflow_procedure` | no_evidence_found: 41, all_evidence_found: 125, some_evidence_found: 18 |
| `constraints_boundaries` | some_evidence_found: 23, all_evidence_found: 79, no_evidence_found: 25 |
| `dependencies_tools` | some_evidence_found: 32, all_evidence_found: 138, no_evidence_found: 20 |
| `resources_references` | all_evidence_found: 105, some_evidence_found: 17, no_evidence_found: 18 |
| `examples_tests` | no_evidence_found: 36, all_evidence_found: 108, some_evidence_found: 32 |
| `safety_side_effects` | all_evidence_found: 35, no_evidence_found: 7, some_evidence_found: 9 |
| `portability_environment` | all_evidence_found: 125, no_evidence_found: 24, some_evidence_found: 19 |
| `hierarchy_links` | no_evidence_found: 17, all_evidence_found: 82, some_evidence_found: 3 |

## Disagreement Cases For Manual Review

| Skill | Field | Type | Heuristic | Model | Model Evidence | Model Reason |
|---|---|---|---|---|---|---|
| `public-anthropic-algorithmic-art` | `dependencies_tools` | `model_only` | `missing` | `explicit` | p5.js from CDN - always available / templates/viewer.html using the Read tool | The skill explicitly requires p5.js CDN and the viewer template file. |
| `public-anthropic-brand-guidelines` | `input_precondition` | `heuristic_only` | `extractable` | `missing` |  | No required input artifacts or prerequisites are mentioned. |
| `public-anthropic-brand-guidelines` | `output_artifact` | `model_only` | `missing` | `implicit` | Applies Anthropic's official brand colors and typography to any sort of artifact | The output is an artifact with applied brand styling, but no specific format is described. |
| `public-anthropic-brand-guidelines` | `dependencies_tools` | `model_only` | `missing` | `implicit` | Applied via python-pptx's RGBColor class / Uses system-installed Poppins and Lora fonts | The text mentions python-pptx and system fonts as required tools. |
| `public-anthropic-brand-guidelines` | `portability_environment` | `model_only` | `missing` | `implicit` | For best results, pre-install Poppins and Lora fonts in your environment. / Uses system fonts | The environment assumes system fonts and python-pptx, implying a Python runtime, but OS is not specified. |
| `public-anthropic-canvas-design` | `workflow_procedure` | `model_only` | `missing` | `explicit` | Complete this in two steps: 1. Design Philosophy Creation (.md file) 2. Express by creating it on a canvas (.pdf file or .png file) | The high-level steps are clearly outlined, with detailed sub-steps throughout. |
| `public-anthropic-canvas-design` | `dependencies_tools` | `model_only` | `missing` | `implicit` | Search the `./canvas-fonts` directory / Download and use whatever fonts are needed | Fonts from a specific directory are referenced, but no other tools or APIs are explicitly listed. |
| `public-anthropic-canvas-design` | `safety_side_effects` | `model_only` | `missing` | `implicit` | never copying existing artists' work to avoid copyright violations | Copyright avoidance is mentioned, but no other safety or side effect details are given. |
| `public-anthropic-canvas-design` | `portability_environment` | `heuristic_only` | `extractable` | `missing` |  | No information about OS, language, model, or runtime environment is provided. |
| `public-anthropic-claude-api` | `examples_tests` | `heuristic_only` | `extractable` | `missing` |  | No example prompts, expected outputs, tests, or verification checks are present |
| `public-anthropic-claude-api` | `safety_side_effects` | `model_only` | `missing` | `implicit` | Do not edit a non-Anthropic file with Anthropic SDK calls. / If you find any, stop and tell the user that this skill produces Claude/Anthropic SDK code; ask whether they want to switch the file to Claude or want a non-Cl | Safety guardrails about not editing non-Anthropic files are present |
| `public-anthropic-doc-coauthoring` | `input_precondition` | `heuristic_only` | `extractable` | `missing` |  | No required input artifacts, prerequisites, or prior state are specified; the skill only requires user interest in writing. |
| `public-anthropic-doc-coauthoring` | `resources_references` | `heuristic_only` | `extractable` | `missing` |  | No specific referenced files, scripts, templates, or supporting resources are provided in the skill. |
| `public-anthropic-doc-coauthoring` | `hierarchy_links` | `heuristic_only` | `extractable` | `missing` |  | No links to related skills, subskills, delegated workflows, or follow-up skill documents are present. |
| `public-anthropic-frontend-design` | `output_artifact` | `model_only` | `missing` | `explicit` | Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is: - Production-grade and functional - Visually striking and memorable - Cohesive with a clear aesthetic point-of-view - Meticulously refined in every det | The skill explicitly states the output as working code meeting specific criteria. |
| `public-anthropic-frontend-design` | `dependencies_tools` | `model_only` | `missing` | `implicit` | Then implement working code (HTML/CSS/JS, React, Vue, etc.) / Use Motion library for React when available. | The skill mentions technologies and a specific library without an explicit dependencies section. |
| `public-anthropic-frontend-design` | `resources_references` | `model_only` | `missing` | `explicit` | license: Complete terms in LICENSE.txt | The frontmatter references a license file as a resource. |
| `public-anthropic-internal-comms` | `input_precondition` | `model_only` | `missing` | `implicit` | Identify the communication type from the request / If the communication type doesn't match any existing guideline, ask for clarification | Skill expects user request to include communication type as input, but not explicitly stated as precondition. |
| `public-anthropic-internal-comms` | `output_artifact` | `model_only` | `missing` | `implicit` | To write any internal communication / Follow the specific instructions in that file for formatting, tone, and content gathering | Skill produces a written communication but does not specify a particular artifact or deliverable format. |
| `public-anthropic-internal-comms` | `resources_references` | `model_only` | `missing` | `explicit` | examples/3p-updates.md / examples/company-newsletter.md / examples/faq-answers.md | Specific guideline files in the examples/ directory are listed. |
| `public-anthropic-mcp-builder` | `input_precondition` | `heuristic_only` | `explicit` | `missing` |  | No required input artifacts or prerequisites are explicitly stated. |
| `public-anthropic-mcp-builder` | `resources_references` | `model_only` | `missing` | `explicit` | [📋 MCP Best Practices](./reference/mcp_best_practices.md) / [⚡ TypeScript Guide](./reference/node_mcp_server.md) / [🐍 Python Guide](./reference/python_mcp_server.md) | Multiple reference files are explicitly linked in the documentation. |
| `public-anthropic-mcp-builder` | `safety_side_effects` | `heuristic_only` | `extractable` | `missing` |  | No permissions, security, or side effects are mentioned. |
| `public-anthropic-skill-creator` | `portability_environment` | `heuristic_only` | `extractable` | `missing` |  | No explicit mention of OS, language version, runtime, or environment assumptions. |
| `public-anthropic-skill-creator` | `hierarchy_links` | `heuristic_only` | `extractable` | `missing` |  | No links to other skills, subskills, or follow-up skill documents are provided. |
| `public-anthropic-slack-gif-creator` | `resources_references` | `model_only` | `missing` | `implicit` | Complete terms in LICENSE.txt / from core.validators import validate_gif | References LICENSE.txt and internal utility modules. |
| `public-anthropic-slack-gif-creator` | `portability_environment` | `model_only` | `missing` | `implicit` | pip install pillow imageio numpy / from PIL import Image | Assumes Python environment with PIL and related packages, but no explicit OS or version. |
| `public-anthropic-theme-factory` | `input_precondition` | `model_only` | `missing` | `implicit` | To apply styling to a slide deck or other artifact / Based on provided inputs, generate a new theme | The skill assumes an artifact to style and user input for theme selection or custom theme creation. |
| `public-anthropic-theme-factory` | `output_artifact` | `model_only` | `missing` | `implicit` | apply the selected theme's colors and fonts to the deck/artifact / After generating the theme, show it for review and verification. Following that, apply the theme | The output is a styled artifact, but not formally defined as a deliverable. |
| `public-anthropic-web-artifacts-builder` | `input_precondition` | `heuristic_only` | `explicit` | `missing` |  | No explicit required input artifacts or user-provided data mentioned. |
| `public-anthropic-web-artifacts-builder` | `output_artifact` | `model_only` | `missing` | `explicit` | This creates `bundle.html` - a self-contained artifact with all JavaScript, CSS, and dependencies inlined. / share the bundled HTML file in conversation with the user so they can view it as an artifact. | The skill clearly describes the output as a single HTML file artifact. |
| `public-anthropic-web-artifacts-builder` | `dependencies_tools` | `model_only` | `missing` | `explicit` | **Stack**: React 18 + TypeScript + Vite + Parcel (bundling) + Tailwind CSS + shadcn/ui / bash scripts/init-artifact.sh <project-name> / bash scripts/bundle-artifact.sh | The stack and scripts are explicitly listed. |
| `public-anthropic-web-artifacts-builder` | `examples_tests` | `heuristic_only` | `extractable` | `missing` |  | No example prompts, expected outputs, or sample tests are provided. |
| `public-anthropic-webapp-testing` | `input_precondition` | `model_only` | `missing` | `implicit` | To test local web applications / Is the server already running? | Requires a local web application and possibly a running server. |
| `public-anthropic-webapp-testing` | `output_artifact` | `model_only` | `missing` | `explicit` | capturing browser screenshots, and viewing browser logs / page.screenshot(path='/tmp/inspect.png', full_page=True) | The description and code examples specify screenshots and logs as outputs. |
| `public-anthropic-webapp-testing` | `dependencies_tools` | `model_only` | `missing` | `explicit` | write native Python Playwright scripts / scripts/with_server.py / from playwright.sync_api import sync_playwright | Playwright, Python, and helper scripts are clearly mentioned as required. |
| `public-anthropic-webapp-testing` | `portability_environment` | `model_only` | `missing` | `implicit` | write native Python Playwright scripts / python scripts/with_server.py / npm run dev | Assumes Python, Node.js, and Playwright are installed; no OS specified. |
| `public-api-design-principles` | `input_precondition` | `heuristic_only` | `extractable` | `missing` |  | No mention of required inputs or prerequisites. |
| `public-api-design-principles` | `output_artifact` | `heuristic_only` | `extractable` | `missing` |  | No specific deliverable or output format described. |
| `public-api-design-principles` | `workflow_procedure` | `model_only` | `missing` | `implicit` | Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient. | Instruction to read another file implies a procedural step. |
| `public-api-design-principles` | `examples_tests` | `heuristic_only` | `explicit` | `missing` |  | No examples, sample prompts, or test cases provided. |
| `public-api-design-principles` | `portability_environment` | `heuristic_only` | `extractable` | `missing` |  | No OS, language, version, or environment assumptions stated. |
| `public-architecture-patterns` | `workflow_procedure` | `heuristic_only` | `extractable` | `missing` |  | No ordered steps or procedural method provided; only conceptual explanations and troubleshooting tips. |
| `public-architecture-patterns` | `constraints_boundaries` | `heuristic_only` | `extractable` | `missing` |  | No explicit constraints or do-not-use conditions; principles described are not framed as boundaries. |
| `public-architecture-patterns` | `portability_environment` | `heuristic_only` | `extractable` | `missing` |  | No explicit environment, OS, language version, or runtime assumptions. |
| `public-brainstorming` | `output_artifact` | `model_only` | `missing` | `explicit` | Write the validated design (spec) to docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md / Invoke the writing-plans skill to create a detailed implementation plan | The skill explicitly produces a design document and transitions to implementation planning. |
| `public-brainstorming` | `dependencies_tools` | `model_only` | `missing` | `explicit` | Use elements-of-style:writing-clearly-and-concisely skill if available / Invoke the writing-plans skill to create a detailed implementation plan | Explicitly references other skills as required tools. |
| `public-brainstorming` | `resources_references` | `model_only` | `missing` | `explicit` | Read the detailed guide before proceeding: skills/brainstorming/visual-companion.md / Write the validated design (spec) to docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md | References specific file paths for visual companion guide and design document location. |
| `public-brainstorming` | `examples_tests` | `heuristic_only` | `extractable` | `missing` |  | No examples, sample prompts, tests, or verification checks are provided in the skill. |
| `public-brainstorming` | `portability_environment` | `heuristic_only` | `extractable` | `missing` |  | No OS, language, model, version, runtime, or environment assumptions are specified. |
| `public-brainstorming` | `hierarchy_links` | `model_only` | `missing` | `explicit` | The ONLY skill you invoke after brainstorming is writing-plans. / Do NOT invoke frontend-design, mcp-builder, or any other implementation skill. | Explicitly links to other skills (writing-plans, frontend-design, mcp-builder) as part of the hierarchy. |
| `public-docx` | `examples_tests` | `heuristic_only` | `extractable` | `missing` |  | No explicit examples, sample prompts, test cases, or verification checks are provided. |
| `public-docx` | `portability_environment` | `model_only` | `missing` | `implicit` | python scripts/office/soffice.py --headless --convert-to docx document.doc / npm install -g docx | Environment assumptions are implicit through tool dependencies (Python, Node.js, LibreOffice), but not explicitly stated. |
| `public-huggingface-datasets` | `output_artifact` | `model_only` | `missing` | `implicit` | use response fields such as num_rows_total, num_rows_per_page, and partial / Retrieve parquet links via /parquet | Expected outputs are described as API responses and data fields. |
| `public-huggingface-datasets` | `constraints_boundaries` | `model_only` | `missing` | `explicit` | read-only Dataset Viewer API calls / Max 100 for row-like endpoints / offset is 0-based | Multiple explicit constraints and guardrails are stated, including read-only nature, pagination limits, and privacy recommendations. |
| `public-huggingface-datasets` | `portability_environment` | `heuristic_only` | `extractable` | `missing` |  | No explicit statement about OS, language, model, or runtime compatibility. |
| `public-huggingface-datasets` | `hierarchy_links` | `model_only` | `missing` | `implicit` | use the hf-cli skill with hf datasets parquet and hf datasets sql | A reference to another skill (hf-cli) is mentioned for CLI-based operations. |
| `public-markitdown` | `constraints_boundaries` | `model_only` | `missing` | `implicit` | Supported Formats table / Large PDFs may take time; consider page ranges if supported | The supported formats imply constraints, and performance considerations hint at limitations. |
| `public-netlify-deploy` | `constraints_boundaries` | `heuristic_only` | `extractable` | `missing` |  | No explicit scope limits or do-not-use conditions found. |
| `public-netlify-deploy` | `safety_side_effects` | `model_only` | `missing` | `explicit` | Never commit secrets to Git / Authentication uses either:
- **Browser-based OAuth** (primary): `netlify login` opens browser for authentication
- **API Key** (alternative): Set `NETLIFY_AUTH_TOKEN` environment variable | Security guidance and authentication patterns provided. |
| `public-netlify-deploy` | `hierarchy_links` | `model_only` | `missing` | `explicit` | ## Bundled References (Load As Needed)

- [CLI commands](references/cli-commands.md)
- [Deployment patterns](references/deployment-patterns.md)
- [netlify.toml guide](references/netlify-toml.md) | Explicit links to related skill documents in Bundled References. |
| `public-office-academic-search` | `resources_references` | `heuristic_only` | `explicit` | `missing` |  | No external files, scripts, or supporting resources are referenced. |
| `public-office-ads-copywriter` | `routing_trigger` | `heuristic_only` | `explicit` | `missing` |  | No trigger or invocation condition is specified in the SKILL.md. |
| `public-office-ads-copywriter` | `input_precondition` | `heuristic_only` | `extractable` | `missing` |  | No explicit precondition or required input artifacts are stated; the example request is illustrative only. |
| `public-office-ads-copywriter` | `workflow_procedure` | `model_only` | `missing` | `implicit` | ## Ad Copy Frameworks

### AIDA Framework
```
Attention → Interest → Desire → Action

Example:
A: "Struggling with [problem]?"
I: "Our [product] helps [target] achieve [benefit]"
D: "[Social proof] + [Unique value]"
A: " | The frameworks and templates provide a method for generating ad copy, though no ordered steps are given. |
| `public-office-ads-copywriter` | `constraints_boundaries` | `heuristic_only` | `extractable` | `missing` |  | No scope limits, guardrails, or do-not-use conditions are mentioned. |
| `public-office-ads-copywriter` | `dependencies_tools` | `model_only` | `missing` | `implicit` | models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - gpt-4
    - gpt-4o | The models section implies required or compatible language models. |
| `public-office-ads-copywriter` | `resources_references` | `heuristic_only` | `explicit` | `missing` |  | No external files, scripts, or references beyond inline content. |
| `public-office-ai-agent-builder` | `routing_trigger` | `heuristic_only` | `explicit` | `missing` |  | No section or text describes when to select or invoke this skill. |
| `public-office-ai-agent-builder` | `input_precondition` | `heuristic_only` | `extractable` | `missing` |  | No prerequisites or required input artifacts are mentioned. |
| `public-office-ai-agent-builder` | `output_artifact` | `heuristic_only` | `explicit` | `missing` |  | No explicit output or deliverable defined; the Output Example is an example, not a specification. |
| `public-office-ai-agent-builder` | `constraints_boundaries` | `heuristic_only` | `extractable` | `missing` |  | No scope limits, guardrails, or do-not-use cases are stated. |
| `public-office-ai-agent-builder` | `resources_references` | `heuristic_only` | `explicit` | `missing` |  | No external files, scripts, or supporting resources are referenced. |
| `public-office-ai-slides` | `routing_trigger` | `heuristic_only` | `explicit` | `missing` |  | No explicit or implicit statement about when the skill should be selected or invoked. |
| `public-office-ai-slides` | `constraints_boundaries` | `heuristic_only` | `extractable` | `missing` |  | No mention of scope limits, not-for conditions, or guardrails. |
| `public-office-airtable-automation` | `routing_trigger` | `heuristic_only` | `explicit` | `missing` |  | No explicit or implicit evidence for when the skill should be selected or invoked. |
| `public-office-airtable-automation` | `input_precondition` | `heuristic_only` | `extractable` | `missing` |  | No explicit or implicit evidence of required input artifacts, prerequisites, or prior state. |
| `public-office-airtable-automation` | `output_artifact` | `heuristic_only` | `explicit` | `missing` |  | No explicit or implicit evidence of expected deliverables or response format. |
| `public-office-airtable-automation` | `resources_references` | `heuristic_only` | `explicit` | `missing` |  | No explicit or implicit evidence of referenced external files, scripts, or documentation. |
| `public-office-airtable-automation` | `safety_side_effects` | `heuristic_only` | `extractable` | `missing` |  | No explicit or implicit evidence of permissions, privacy, security, or side effects. |
