# Public-Gold Manual Adjudication - 2026-06-01

Purpose: manually inspect whether each public-gold prompt really has the listed public skill as the best target, rather than trusting automatic retrieval ranks.

Scope:

- Public-gold prompts: 32.
- Skill library: 2401 skills.
- Main evidence inspected: prompt text, public gold skill descriptions/original bodies where needed, closest alternatives, strongest local selector errors, and strongest Qwen reranker errors.
- No skill artifacts were edited during this adjudication.

## Summary

| Decision | Count | Interpretation |
|---|---:|---|
| Keep as strict public-gold case | 21 | The public skill is the best atomic target after reading the prompt and competitors. |
| Keep with acceptable alternatives | 7 | The public skill is defensible, but an equivalent or near-equivalent skill should also count as correct. |
| Revise or exclude before final reporting | 4 | The prompt is not unique enough, or a controlled/generated skill is at least as good as the public gold. |

Gold-label stability read:

- Strict public-only stability: 21/32.
- Gold-or-acceptable stability after adjudication: 28/32.
- This means the public-gold stratum is usable as an external-validity layer only after acceptable alternatives and revised/excluded cases are handled.

## Adjudication Table

| Prompt | Gold Skill | Decision | Manual Rationale |
|---|---|---|---|
| `public_gold_p01_pdf_extraction` | `public-office-pdf-extraction` | Keep strict | The prompt asks for native embedded-text/table/metadata extraction with `pdfplumber`-style output. OCR, PDF Q&A, and layout-table-only extractors are plausible but not better because they miss either native extraction or metadata scope. |
| `public_gold_p02_pdf_ocr` | `public-office-pdf-ocr` | Revise or exclude | The public skill handles scanned PDF OCR, but the prompt also asks for uncertain recognition regions by page. `pdf-ocr-cleaner` is more specific to uncertainty/page anchors and is arguably a better target. Either simplify the prompt to plain OCR or record `pdf-ocr-cleaner` as acceptable. |
| `public_gold_p03_pdf_form_filler` | `public-office-pdf-form-filler` | Keep with acceptable alternatives | The public skill is correct for filling PDF form fields, but `pdf-form-filler` is a near-equivalent controlled skill and should remain acceptable. |
| `public_gold_p04_markitdown_conversion` | `public-markitdown` | Keep strict | The prompt intentionally requires a MarkItDown-style multi-format document-to-Markdown pipeline. Generic converters are plausible but less exact because they do not preserve the named tool/workflow scope. |
| `public_gold_p05_pdf_merge_split` | `public-office-pdf-merge-split` | Keep strict | The task is exactly combine PDFs and split appendix pages. Converter, watermark, compression, and general PDF skills are procedurally weaker. |
| `public_gold_p06_browser_devtools_testing` | `public-addy-agent-browser-testing-with-devtools` | Keep strict | The prompt requires Chrome DevTools MCP runtime inspection, console/network evidence, and screenshots. Playwright/browser automation skills are plausible but not the same workflow. |
| `public_gold_p07_web_accessibility` | `public-addy-web-accessibility` | Revise or exclude | The public skill is valid, but `accessibility-checker` and `accessibility-interaction-auditor` match the exact WCAG/keyboard/focus/label task at least as well. This is not stable as a strict public-gold case unless those are acceptable alternatives or the prompt adds public-skill-specific scope. |
| `public_gold_p08_core_web_vitals` | `public-addy-web-core-web-vitals` | Keep strict | The prompt names LCP, INP, and CLS as the only target. Broader performance, accessibility, SEO, or browser-testing skills are plausible but too broad. |
| `public_gold_p09_systematic_debugging` | `public-oh-my-debugging` | Keep strict | The original public skill defines the exact reproduce, isolate, verify debugging loop. CI, review, or domain-specific failure diagnosers are false positives caused by background scale and weak wrapper metadata, not better gold labels. |
| `public_gold_p10_analyze_ci` | `public-swebench-analyze-ci` | Keep with acceptable alternatives | The public skill is the best PR/GitHub Actions CI-log target. `public-openai-gh-fix-ci`, `ci-failure-debugger`, and `ci-log-root-cause-debugger` are close enough to count as acceptable if the evaluation is task-success oriented rather than public-skill-specific. |
| `public_gold_p11_setup_pre_commit` | `public-mattpocock-setup-pre-commit` | Keep strict | The prompt requires Husky/lint-staged commit-time checks. Git guardrails, CI templates, and one-off fixers are not substitutes. The duplicate `public-oh-my-setup-pre-commit` remains acceptable. |
| `public_gold_p12_git_guardrails` | `public-mattpocock-git-guardrails-claude-code` | Keep strict | The task requires Claude Code pre-tool hooks blocking destructive git commands. Pre-commit formatting hooks and general git workflow skills are not equivalent. The duplicate `public-oh-my-git-guardrails-claude-code` remains acceptable. |
| `public_gold_p13_address_pr_comments` | `public-openai-gh-address-comments` | Keep strict | The prompt requires unresolved GitHub PR review threads and patching requested changes. Generic review-comment resolvers are plausible but lack the GitHub/PR-thread inspection dependency, so they should be labelled tool/dependency misses rather than accepted by default. |
| `public_gold_p14_netlify_deploy` | `public-netlify-deploy` | Keep strict | The deployment target is Netlify CLI and verified Netlify URL. Vercel, Render, Cloudflare, and Kubernetes alternatives are platform-mismatched. |
| `public_gold_p15_cloudflare_deploy` | `public-openai-cloudflare-deploy` | Keep strict | The required platform is Cloudflare Pages/Workers with Wrangler/platform checks. Other deployment skills are platform-mismatched. |
| `public_gold_p16_render_deploy` | `public-openai-render-deploy` | Keep strict | The prompt asks for Render-specific repo analysis, `render.yaml`, and Dashboard deployment path. Other deployment skills are platform-mismatched or too broad. |
| `public_gold_p17_mcp_builder` | `public-anthropic-mcp-builder` | Keep with acceptable alternatives | The public skill is correct for building an MCP server from a third-party API, but `mcp-server-builder` and similar MCP-builder skills are near-equivalent. They should be acceptable if the goal is correct task completion. |
| `public_gold_p18_chatgpt_apps` | `public-openai-chatgpt-apps` | Keep strict | The prompt requires a ChatGPT App with MCP server plus widget UI. Generic MCP-builder skills miss the Apps SDK/widget deliverable. |
| `public_gold_p19_cli_creator` | `public-openai-cli-creator` | Keep strict | The prompt asks for a durable composable CLI from OpenAPI/docs/curl examples, command contract, auth/config, and runtime choice. API documentation or API design skills are adjacent but not the same output artifact. |
| `public_gold_p20_hf_datasets` | `public-huggingface-datasets` | Keep strict | The required workflow is the Hugging Face Dataset Viewer API for subsets, splits, pagination, samples, and schema. HF CLI, model training, and tool-builder skills are adjacent but procedurally weaker. |
| `public_gold_p21_hf_gradio` | `public-huggingface-huggingface-gradio` | Keep with acceptable alternatives | The public skill is correct for Gradio demos, but `gradio-demo-builder` is a direct controlled equivalent. Count it acceptable or make the prompt more Hugging Face public-skill-specific. |
| `public_gold_p22_hf_vision_trainer` | `public-huggingface-huggingface-vision-trainer` | Keep strict | The prompt specifically asks for object-detection/image-dataset fine-tuning and vision labels. LLM trainer, local model, and sentence-transformer alternatives are wrong task families. |
| `public_gold_p23_sentence_transformer_training` | `public-huggingface-train-sentence-transformers` | Keep with acceptable alternatives | The public skill is correct for SentenceTransformer bi-encoder training, but `sentence-transformer-finetuner` is a direct controlled equivalent and should count acceptable if retained in the same library. |
| `public_gold_p24_hf_cli` | `public-huggingface-hf-cli` | Keep strict | The task asks for Hugging Face Hub CLI repo/file/metadata operations from the terminal. Dataset Viewer and custom tool-building are not the requested interface. |
| `public_gold_p25_data_pipeline` | `public-office-data-pipeline` | Keep with acceptable alternatives | The public skill is correct, but `public-office-etl-pipeline` is effectively a duplicate ETL/data-pipeline public skill. It should be an acceptable alternative or one of the duplicate cases should be excluded from strict reporting. |
| `public_gold_p26_database_sync` | `public-office-database-sync` | Keep strict | The prompt asks for two-way PostgreSQL/MySQL synchronization, table mapping, change handling, and conflict rules. General API integration and ETL skills are too broad. |
| `public_gold_p27_contract_review` | `public-office-contract-review` | Revise or exclude | The public skill is valid, but `contract-risk-reviewer` directly matches risky clauses, obligations, renewal traps, liability, and negotiation points. This is not stable as a strict public-gold case unless the prompt adds public-skill-specific document/tool scope or the controlled equivalent is acceptable. |
| `public_gold_p28_suspicious_email` | `public-office-suspicious-email` | Keep strict | The prompt requires phishing/scam/security-threat analysis. Email classification and reply drafting are plausible by topic but procedurally wrong. |
| `public_gold_p29_ai_slides` | `public-office-ai-slides` | Keep strict | The prompt asks for a complete presentation from a topic brief, including outline and polished deck structure. Slide outline, visual audit, theme, or Markdown conversion are partial alternatives only. |
| `public_gold_p30_figma_implement_design` | `public-openai-figma-implement-design` | Keep strict | The prompt requires an existing Figma node to production UI code with 1:1 parity. `public-openai-figma` is a broad parent/router and `figma-generate-design` writes to Figma, so the specific implement-design skill is the best atomic target. |
| `public_gold_p31_skill_creator` | `public-skill-creator` | Revise or exclude | The public skill and local `skill-creator` are essentially the same task, and the local skill is cleaner/atomic. This is weak as a public-gold retrieval case unless the prompt is explicitly about the public/OpenAI skill authoring workflow or the local equivalent is acceptable. |
| `public_gold_p32_security_threat_model` | `public-security-threat-model` | Keep with acceptable alternatives | The public skill is best for repository-grounded threat modeling with trust boundaries, assets, abuse paths, and mitigations. `security-threat-modeler` is a legitimate near-equivalent and should remain acceptable; privacy/security-ops risk reviewers are broader or different. |

## Recommended Benchmark Actions

Do not merge public-gold results into the main controlled score yet.

Recommended before final reporting:

1. Move `public_gold_p02_pdf_ocr`, `public_gold_p07_web_accessibility`, `public_gold_p27_contract_review`, and `public_gold_p31_skill_creator` into a revise/exclude queue.
2. Add or confirm acceptable alternatives for near-equivalent cases: `p03`, `p10`, `p17`, `p21`, `p23`, `p25`, and `p32`.
3. Keep broad parent/router hits, such as `public-openai-figma`, as hierarchy failures rather than automatic successes unless the thesis reports task-success rather than atomic-skill retrieval.
4. Report public-gold as a separate external-validity stratum. It should test whether the method generalizes to public-authored skills, not replace the controlled benchmark.

## Interpretation For The Thesis

The public-gold subset is valuable, but it exposes a real issue:

- Some public skills are atomic and clearly retrievable.
- Some public skills have generated or controlled equivalents that are equally good.
- Some public skills are broad wrappers or parents, which makes strict gold labels unstable.
- Therefore, public-gold evidence should be reported with manual adjudication and acceptable alternatives, not as a clean automatic benchmark.

This supports the thesis framing: scalable skill retrieval needs both candidate retrieval and a representation layer that can reason about procedural fit, duplication, hierarchy, and task-specific boundaries.
