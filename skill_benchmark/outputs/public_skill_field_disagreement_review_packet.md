# Public Skill Field Disagreement Review Packet

Purpose: targeted manual review of heuristic/model disagreements from the 200-skill public field audit.

- Skills compared in source report: 200
- Total selected disagreement cases: 50

Review labels to fill:

- `heuristic_correct`
- `model_correct`
- `both_partly_correct`
- `both_wrong_or_unclear`
- `definition_needs_refinement`

Priority fields: routing trigger, resources/references, safety/side-effects, constraints/boundaries, and input/precondition.

## Field Agreement Snapshot

| Field | Agreement | Heuristic Only | Model Only |
|---|---:|---:|---:|
| `constraints_boundaries` | 81.0% | 27 | 11 |
| `dependencies_tools` | 92.0% | 3 | 13 |
| `examples_tests` | 91.5% | 14 | 3 |
| `hierarchy_links` | 88.5% | 7 | 16 |
| `input_precondition` | 83.0% | 22 | 12 |
| `output_artifact` | 85.5% | 14 | 15 |
| `portability_environment` | 87.5% | 14 | 11 |
| `resources_references` | 74.5% | 42 | 9 |
| `routing_trigger` | 68.0% | 64 | 0 |
| `safety_side_effects` | 72.0% | 29 | 27 |
| `workflow_procedure` | 85.5% | 13 | 16 |

## Cases

| Skill | Field | Type | Heuristic | Model | Heuristic Evidence | Model Evidence | Model Reason | Manual Decision | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `public-office-ads-copywriter` | `routing_trigger` | `heuristic_only` | `explicit` | `missing` | description: "Multi-platform ad copy generation for Google Ads, Meta/Facebook, TikTok, LinkedIn with A/B testing variants" / category: marketing / capabilities: |  | No trigger or invocation condition is specified in the SKILL.md. |  |  |
| `public-office-ai-agent-builder` | `routing_trigger` | `heuristic_only` | `explicit` | `missing` | description: "Build AI agents with tools, memory, and multi-step reasoning - ChatGPT, Claude, Gemini integration patterns" / category: ai / capabilities: |  | No section or text describes when to select or invoke this skill. |  |  |
| `public-office-ai-slides` | `routing_trigger` | `heuristic_only` | `explicit` | `missing` | description: "Generate complete presentations with AI - from outline to polished slides" / category: presentation / # Skill Capabilities |  | No explicit or implicit statement about when the skill should be selected or invoked. |  |  |
| `public-office-airtable-automation` | `routing_trigger` | `heuristic_only` | `explicit` | `missing` | description: "Airtable database automation - views, automations, integrations, and workflow triggers" / category: productivity / capabilities: |  | No explicit or implicit evidence for when the skill should be selected or invoked. |  |  |
| `public-office-asana-automation` | `routing_trigger` | `heuristic_only` | `explicit` | `missing` | description: Automate Asana project management workflows, task tracking, team collaboration, and reporting / category: project-management / capabilities: |  | No explicit trigger condition or invocation context found in SKILL.md. |  |  |
| `public-office-browser-automation` | `routing_trigger` | `heuristic_only` | `explicit` | `missing` | description: Automate web browser interactions, scraping, testing, and workflow automation with Puppeteer/Playwright / category: automation / capabilities: |  | No explicit or implicit trigger condition found in the document. |  |  |
| `public-office-calendar-automation` | `routing_trigger` | `heuristic_only` | `explicit` | `missing` | description: "Google Calendar and Outlook automation - scheduling optimization, meeting workflows, time blocking, and Slack/Sheets integration" / category: productivity / capabilities: |  | No explicit trigger for invoking the skill; only workflow-specific triggers exist. |  |  |
| `public-office-clickup-automation` | `routing_trigger` | `heuristic_only` | `explicit` | `missing` | description: Automate ClickUp workspace management, task workflows, time tracking, and team productivity / category: project-management / capabilities: |  | No explicit trigger for skill invocation; only internal ClickUp automation triggers are described. |  |  |
| `public-anthropic-doc-coauthoring` | `resources_references` | `heuristic_only` | `extractable` | `missing` | Is there a template or specific format to follow? / **If user provides a template or mentions a doc type:** / - Ask if they have a template document to share |  | No specific referenced files, scripts, templates, or supporting resources are provided in the skill. |  |  |
| `public-office-academic-search` | `resources_references` | `heuristic_only` | `explicit` | `missing` | related_skills: / ## References |  | No external files, scripts, or supporting resources are referenced. |  |  |
| `public-office-ads-copywriter` | `resources_references` | `heuristic_only` | `explicit` | `missing` | related_skills: / **Template 1: Problem-Solution** / **Template 2: Story-Based** |  | No external files, scripts, or references beyond inline content. |  |  |
| `public-office-ai-agent-builder` | `resources_references` | `heuristic_only` | `explicit` | `missing` | related_skills: |  | No external files, scripts, or supporting resources are referenced. |  |  |
| `public-office-airtable-automation` | `resources_references` | `heuristic_only` | `explicit` | `missing` | related_skills: / ### Base Structure Template / template: \| |  | No explicit or implicit evidence of referenced external files, scripts, or documentation. |  |  |
| `public-office-apple-shortcuts` | `resources_references` | `heuristic_only` | `explicit` | `missing` | related_skills: |  | No external file references or supporting resources mentioned. |  |  |
| `public-office-brand-guidelines` | `resources_references` | `heuristic_only` | `extractable` | `missing` | ### Complete Guide Template |  | No external files, scripts, or templates are referenced. |  |  |
| `public-office-browser-automation` | `resources_references` | `heuristic_only` | `explicit` | `missing` | related_skills: |  | No external files, scripts, templates, or documentation are referenced. |  |  |
| `public-anthropic-mcp-builder` | `safety_side_effects` | `heuristic_only` | `extractable` | `missing` | **Content Exploration**: Use READ-ONLY operations to explore available data / - **Read-only**: Only non-destructive operations required / - Security and error handling standards |  | No permissions, security, or side effects are mentioned. |  |  |
| `public-office-airtable-automation` | `safety_side_effects` | `heuristic_only` | `extractable` | `missing` | - At Risk: COUNT(Days Remaining < 7) |  | No explicit or implicit evidence of permissions, privacy, security, or side effects. |  |  |
| `public-office-asana-automation` | `safety_side_effects` | `heuristic_only` | `extractable` | `missing` | At Risk: 3 (25%) / │ Security Audit │ 🟢 │ 65% │ |  | No mention of permissions, security, or side effects. |  |  |
| `public-office-changelog-generator` | `safety_side_effects` | `heuristic_only` | `explicit` | `missing` | ### Security / - **Better Authentication** - Upgraded to OAuth 2.0 for enhanced security / \| lodash \| 4.17.20 \| 4.17.21 \| Security patch \| |  | No mention of permissions, security, or destructive actions. |  |  |
| `public-office-company-research` | `safety_side_effects` | `heuristic_only` | `explicit` | `missing` | - Risk identification / ## Risk Assessment / \| Risk \| Likelihood \| Impact \| Mitigation \| |  | No mention of permissions, privacy, security, or side effects. |  |  |
| `public-office-crypto-report` | `safety_side_effects` | `heuristic_only` | `explicit` | `missing` | - Risk factor identification / - **Technical Review**: Protocol mechanics and security / **Risk Level**: [Low / Medium / High / Very High] |  | No discussion of permissions, privacy, security, mutation risk, destructive actions, or side effects. |  |  |
| `public-office-customer-success` | `safety_side_effects` | `heuristic_only` | `explicit` | `missing` | ### Churn Risk Playbook |  | No permissions, privacy, security, or side effect information is present. |  |  |
| `public-office-data-analysis` | `safety_side_effects` | `heuristic_only` | `extractable` | `missing` | "Which customers are at risk of churning?" |  | No mention of permissions, privacy, security, or side effects. |  |  |
| `public-architecture-patterns` | `constraints_boundaries` | `heuristic_only` | `extractable` | `missing` | - Creating testable codebases where use-case tests do not require a running database / - **Bounded Contexts**: Isolate a coherent model for one subdomain; avoid sharing a single model across the whole system / It must never import from `adapters/` or `infrastructure/`. |  | No explicit constraints or do-not-use conditions; principles described are not framed as boundaries. |  |  |
| `public-netlify-deploy` | `constraints_boundaries` | `heuristic_only` | `extractable` | `missing` | Never commit secrets to Git |  | No explicit scope limits or do-not-use conditions found. |  |  |
| `public-office-ads-copywriter` | `constraints_boundaries` | `heuristic_only` | `extractable` | `missing` | - "Don't Miss Out" / "Never Miss a Deadline Again" / ✅ Never miss another deadline |  | No scope limits, guardrails, or do-not-use conditions are mentioned. |  |  |
| `public-office-ai-agent-builder` | `constraints_boundaries` | `heuristic_only` | `extractable` | `missing` | - Never make up information |  | No scope limits, guardrails, or do-not-use cases are stated. |  |  |
| `public-office-ai-slides` | `constraints_boundaries` | `heuristic_only` | `extractable` | `missing` | - Don't run as root |  | No mention of scope limits, not-for conditions, or guardrails. |  |  |
| `public-office-amazon-seller` | `constraints_boundaries` | `heuristic_only` | `extractable` | `missing` | **Manage Inventory**: Avoid stockouts and excess |  | No explicit scope limits, not-for conditions, or guardrails are stated in the document. |  |  |
| `public-office-asana-automation` | `constraints_boundaries` | `heuristic_only` | `explicit` | `missing` |  |  | No section or statement defining scope limits or constraints. |  |  |
| `public-office-clickup-automation` | `constraints_boundaries` | `heuristic_only` | `explicit` | `missing` | - Automation rules / ## Automation Rules |  | No explicit constraints, guardrails, or do-not-use conditions. |  |  |
| `public-anthropic-brand-guidelines` | `input_precondition` | `heuristic_only` | `extractable` | `missing` | - No font installation required - works with existing system fonts |  | No required input artifacts or prerequisites are mentioned. |  |  |
| `public-anthropic-doc-coauthoring` | `input_precondition` | `heuristic_only` | `extractable` | `missing` | **Context Gathering**: User provides all relevant context while Claude asks clarifying questions / **If user provides a template or mentions a doc type:** / - If they provide a link to a shared document, use the appropriate integration to fetch it |  | No required input artifacts, prerequisites, or prior state are specified; the skill only requires user interest in writing. |  |  |
| `public-anthropic-mcp-builder` | `input_precondition` | `heuristic_only` | `explicit` | `missing` | **Input Schema:** / #### 4.3 Evaluation Requirements / - **Read-only**: Only non-destructive operations required |  | No required input artifacts or prerequisites are explicitly stated. |  |  |
| `public-anthropic-web-artifacts-builder` | `input_precondition` | `heuristic_only` | `explicit` | `missing` | ## Quick Start |  | No explicit required input artifacts or user-provided data mentioned. |  |  |
| `public-api-design-principles` | `input_precondition` | `heuristic_only` | `extractable` | `missing` | **Input Validation**: Validate at schema and resolver levels / - **Over-fetching/Under-fetching (REST)**: Fixed in GraphQL but requires DataLoaders |  | No mention of required inputs or prerequisites. |  |  |
| `public-office-ads-copywriter` | `input_precondition` | `heuristic_only` | `extractable` | `missing` | No credit card required." / No credit card required. |  | No explicit precondition or required input artifacts are stated; the example request is illustrative only. |  |  |
| `public-office-ai-agent-builder` | `input_precondition` | `heuristic_only` | `extractable` | `missing` | │ │ Input │────▶│ Agent │────▶│ Output │ │ / required: ["location"] / ## Tools Required |  | No prerequisites or required input artifacts are mentioned. |  |  |
| `public-office-airtable-automation` | `input_precondition` | `heuristic_only` | `extractable` | `missing` | input: email |  | No explicit or implicit evidence of required input artifacts, prerequisites, or prior state. |  |  |
| `public-office-etl-pipeline` | `constraints_boundaries` | `heuristic_only` | `explicit` | `missing` | ### Aggregation Rules / ### Validation Rules |  | No explicit constraints, scope limits, or do-not-use conditions mentioned. |  |  |
| `public-office-expense-tracker` | `constraints_boundaries` | `heuristic_only` | `explicit` | `missing` | ### Auto-Check Rules |  | No constraints or boundaries explicitly stated. |  |  |
| `public-office-facebook-ads` | `constraints_boundaries` | `heuristic_only` | `explicit` | `missing` | ### Automated Rules |  | No section or statement defining scope limits, guardrails, or do-not-use cases. |  |  |
| `public-office-gmail-workflows` | `constraints_boundaries` | `heuristic_only` | `extractable` | `missing` | - Use specific sender filters to avoid processing spam / - Enable duplicate detection to avoid redundant uploads / - Don't log email content |  | No scope limits, do-not-use cases, or guardrails are defined. |  |  |
| `public-office-google-ads-manager` | `constraints_boundaries` | `heuristic_only` | `extractable` | `missing` | - "Never Miss Deadlines" |  | No explicit constraints, scope limits, or do-not-use conditions are mentioned. |  |  |
| `public-office-home-assistant` | `constraints_boundaries` | `heuristic_only` | `extractable` | `missing` | **Notifications**: Don't over-notify |  | No direct evidence of scope limits or constraints. |  |  |
| `public-office-invoice-template` | `constraints_boundaries` | `heuristic_only` | `extractable` | `missing` | **Auto-calculate totals (don't trust input)** |  | No mention of scope limits, not-for conditions, or constraints. |  |  |
| `public-office-jira-automation` | `constraints_boundaries` | `heuristic_only` | `explicit` | `missing` | # Release scope |  | No constraints, do-not-use cases, or guardrails mentioned. |  |  |
| `public-office-pipedrive-automation` | `constraints_boundaries` | `heuristic_only` | `extractable` | `missing` | **Rotting Alerts**: Don't let deals stagnate |  | No scope limits, guardrails, or do-not-use conditions are mentioned in the text. |  |  |
| `public-office-quickbooks-automation` | `constraints_boundaries` | `heuristic_only` | `explicit` | `missing` | ### Bank Feed Rules |  | No constraints, scope limits, or do-not-use conditions are mentioned. |  |  |

## How To Use This Packet

- If many `routing_trigger` heuristic-only cases are false positives, refine the definition so broad descriptions do not automatically count as high-quality routing conditions.
- If many `resources_references` heuristic-only cases are false positives, require concrete files, URLs, directories, bundled references, or linked skills.
- If `safety_side_effects` remains sparse after manual review, classify it as proposed/weakly observed rather than an established public-skill convention.
- Use the reviewed cases to finalize observed/extractable/proposed field categories before Step 7 field ablations are interpreted.
