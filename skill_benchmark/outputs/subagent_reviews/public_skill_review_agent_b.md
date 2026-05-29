# Public Skill Review - Agent B

Scope: manual evidence-grounded review of the five requested public `SKILL.original.md` files only. Statuses use `explicit`, `implicit`, `missing`, and `ambiguous`; every `explicit` or `implicit` entry includes a short exact quote from the relevant skill file.

## public-huggingface-datasets

- routing_trigger: explicit - "Use this skill for Hugging Face Dataset Viewer API workflows"
- input_precondition: explicit - "Resolve `config` + `split` with `/splits`."
- output_artifact: explicit - "fetch subset/split metadata, paginate rows, search text, apply filters, download parquet URLs"
- workflow_procedure: explicit - "## Core workflow"
- constraints_boundaries: explicit - "`length` max is usually `100` for row-like endpoints."
- dependencies_tools: explicit - "Base URL: `https://datasets-server.huggingface.co`"
- resources_references: explicit - "`Validate dataset`: `/is-valid?dataset=<namespace/repo>`"
- examples_tests: explicit - "Pagination pattern:"
- safety_side_effects: explicit - "Keep filtering and searches read-only and side-effect free."
- portability_environment: explicit - "Gated/private datasets require `Authorization: Bearer <HF_TOKEN>`."
- hierarchy_links: explicit - "use the `hf-cli` skill"

## public-markitdown

- routing_trigger: explicit - "Convert files and office documents to Markdown."
- input_precondition: explicit - "Supports 15+ file formats"
- output_artifact: explicit - "converting various file formats to Markdown"
- workflow_procedure: explicit - "## Quick Start"
- constraints_boundaries: explicit - "Control which file formats you support:"
- dependencies_tools: explicit - "pip install 'markitdown[all]'"
- resources_references: explicit - "See `references/api_reference.md` for complete API documentation"
- examples_tests: explicit - "## Common Use Cases"
- safety_side_effects: implicit - "Requires API calls (costs may apply)"
- portability_environment: explicit - "## Docker Usage"
- hierarchy_links: explicit - "Use the **scientific-schematics** skill"

## public-netlify-deploy

- routing_trigger: explicit - "Use when the user asks to deploy, host, publish, or link a site/repo on Netlify"
- input_precondition: explicit - "Valid web project in current directory"
- output_artifact: explicit - "**Deploy URL**: Unique URL for this deployment"
- workflow_procedure: explicit - "## Workflow"
- constraints_boundaries: explicit - "The deployment might take a few minutes. Use appropriate timeout values."
- dependencies_tools: explicit - "Netlify CLI: Installed via npx"
- resources_references: explicit - "Netlify CLI Docs: https://docs.netlify.com/cli/get-started/"
- examples_tests: explicit - "## Example Full Workflow"
- safety_side_effects: explicit - "Never commit secrets to Git"
- portability_environment: explicit - "When sandboxing blocks the deployment network calls, rerun with `sandbox_permissions=require_escalated`."
- hierarchy_links: explicit - "## Bundled References (Load As Needed)"

## public-office-ads-copywriter

- routing_trigger: explicit - "Multi-platform ad copy generation for Google Ads, Meta/Facebook, TikTok, LinkedIn"
- input_precondition: implicit - "**Request**: \"Create Google Ads copy for a project management SaaS tool\""
- output_artifact: explicit - "Generate high-converting ad copy"
- workflow_procedure: implicit - "## Ad Copy Frameworks"
- constraints_boundaries: explicit - "max_chars: 30"
- dependencies_tools: ambiguous - The file lists model compatibility but no operational tool dependency. Evidence for model metadata: "recommended:"
- resources_references: missing - No external resources, reference files, or documentation links found.
- examples_tests: explicit - "## Output Example"
- safety_side_effects: missing - No safety, compliance, claim substantiation, or side-effect guidance found.
- portability_environment: explicit - "languages:"
- hierarchy_links: explicit - "related_skills:"

## public-office-data-analysis

- routing_trigger: explicit - "Analyze spreadsheet data, generate insights, create visualizations, and build reports from Excel/CSV data."
- input_precondition: explicit - "formats: [xlsx, csv, xls]"
- output_artifact: explicit - "type: report"
- workflow_procedure: explicit - "1. Share your spreadsheet or data file"
- constraints_boundaries: explicit - "## Limitations"
- dependencies_tools: explicit - "server: office-mcp"
- resources_references: missing - No external resources, reference files, or documentation links found.
- examples_tests: explicit - "## Output Formats"
- safety_side_effects: explicit - "Cannot guarantee 100% accuracy on OCR'd data"
- portability_environment: explicit - "languages:"
- hierarchy_links: explicit - "related_skills:"

## Calibration Notes

- Metadata-heavy skills can inflate counts: frontmatter `description`, `input`, `output`, `mcp`, `languages`, and `related_skills` often provide real evidence, but they are less procedural than body text.
- I counted concrete endpoint lists, bundled reference files, and external links as `resources_references`; I did not count ordinary templates as resources unless they pointed to reusable files or docs.
- Some fields are vulnerable to undercounting in creative skills: `public-office-ads-copywriter` has many platform limits and templates, but little explicit guidance on inputs, safety, tools, or references.
- `safety_side_effects` was only marked present when the text itself mentioned read-only behavior, secrets, costs, network deployment, accuracy caveats, or similar operational risk; I did not add advertising compliance concerns without textual support.
