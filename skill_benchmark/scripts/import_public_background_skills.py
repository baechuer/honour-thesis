#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import shutil
import urllib.request
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PublicSkill:
    slug: str
    source_name: str
    source_url: str
    raw_url: str
    origin: str
    license_note: str
    dependency_profile: str
    external_dependencies: list[str]
    resource_signals: list[str]
    fallback_description: str


@dataclass(frozen=True)
class PublicRepository:
    owner: str
    repo: str
    branch: str
    origin: str
    path_prefix: str
    source_base: str
    raw_base: str
    slug_prefix: str
    license_note: str
    skip_path_markers: tuple[str, ...] = ()


PUBLIC_SKILLS = [
    PublicSkill(
        slug="public-security-threat-model",
        source_name="security-threat-model",
        source_url="https://github.com/openai/skills/tree/main/skills/.curated/security-threat-model",
        raw_url="https://raw.githubusercontent.com/openai/skills/main/skills/.curated/security-threat-model/SKILL.md",
        origin="openai/skills",
        license_note="See source skill directory for license.",
        dependency_profile="repository-grounded AppSec threat modeling; depends on repo path, architecture evidence, and optional prompt-template references",
        external_dependencies=["repository files", "architecture summary", "references/prompt-template.md", "references/security-controls-and-assets.md"],
        resource_signals=["references", "output contract", "repo evidence", "threat taxonomy"],
        fallback_description="Repository-grounded threat modeling for trust boundaries, assets, attacker capabilities, abuse paths, and mitigations.",
    ),
    PublicSkill(
        slug="public-playwright-interactive",
        source_name="playwright-interactive",
        source_url="https://github.com/openai/skills/tree/main/skills/.curated/playwright-interactive",
        raw_url="https://raw.githubusercontent.com/openai/skills/main/skills/.curated/playwright-interactive/SKILL.md",
        origin="openai/skills",
        license_note="See source skill directory for license.",
        dependency_profile="browser and Electron QA workflow; depends on Playwright, persistent JS REPL handles, local app target, and viewport/screenshot evidence",
        external_dependencies=["Playwright", "js_repl", "local dev server", "browser runtime", "screenshots"],
        resource_signals=["tool setup", "runtime handles", "desktop/mobile viewports", "functional QA", "visual QA"],
        fallback_description="Persistent browser and Electron interaction for iterative UI debugging and functional plus visual QA.",
    ),
    PublicSkill(
        slug="public-netlify-deploy",
        source_name="netlify-deploy",
        source_url="https://github.com/openai/skills/tree/main/skills/.curated/netlify-deploy",
        raw_url="https://raw.githubusercontent.com/openai/skills/main/skills/.curated/netlify-deploy/SKILL.md",
        origin="openai/skills",
        license_note="See source skill directory for license.",
        dependency_profile="deployment workflow; depends on Netlify project context, CLI/API configuration, build output, and deploy verification",
        external_dependencies=["Netlify account or project", "Netlify CLI/API", "build command", "environment variables", "deployment URL"],
        resource_signals=["deployment target", "build logs", "project config", "environment config", "verification URL"],
        fallback_description="Deploys or prepares deployment of web projects to Netlify with build and verification context.",
    ),
    PublicSkill(
        slug="public-skill-creator",
        source_name="skill-creator",
        source_url="https://github.com/openai/skills/tree/main/skills/.system/skill-creator",
        raw_url="https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md",
        origin="openai/skills",
        license_note="See source skill directory for license.",
        dependency_profile="skill authoring workflow; depends on target workflow examples, SKILL.md conventions, optional scripts/references/assets",
        external_dependencies=["target workflow examples", "SKILL.md frontmatter", "optional scripts", "optional references", "optional assets"],
        resource_signals=["progressive disclosure", "skill anatomy", "metadata", "optional bundled resources"],
        fallback_description="Creates or updates agent skills with instructions, resources, scripts, metadata, and packaging shape.",
    ),
    PublicSkill(
        slug="public-skill-installer",
        source_name="skill-installer",
        source_url="https://github.com/openai/skills/tree/main/skills/.system/skill-installer",
        raw_url="https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-installer/SKILL.md",
        origin="openai/skills",
        license_note="See source skill directory for license.",
        dependency_profile="skill installation workflow; depends on GitHub or catalog source, local skill path, and install command behavior",
        external_dependencies=["GitHub repository or catalog", "local skill directory", "network access", "installer command"],
        resource_signals=["registry lookup", "download path", "local install path", "restart requirement"],
        fallback_description="Installs agent skills from known catalogs, GitHub directories, or local packages.",
    ),
    PublicSkill(
        slug="public-xlsx",
        source_name="xlsx",
        source_url="https://github.com/anthropics/skills/tree/main/skills/xlsx",
        raw_url="https://raw.githubusercontent.com/anthropics/skills/main/skills/xlsx/SKILL.md",
        origin="anthropics/skills",
        license_note="Many skills in anthropics/skills are Apache-2.0; see source directory for exact license.",
        dependency_profile="spreadsheet artifact workflow; depends on spreadsheet files, formulas, workbook structure, and possible script/tool support",
        external_dependencies=[".xlsx/.xls/.csv files", "spreadsheet formulas", "workbook sheets", "formatting/layout", "possible Python tooling"],
        resource_signals=["file type", "formula recalculation", "sheets", "charts", "formatting", "data analysis"],
        fallback_description="Creates, edits, analyzes, and works with spreadsheet files and workbook artifacts.",
    ),
    PublicSkill(
        slug="public-pdf",
        source_name="pdf",
        source_url="https://github.com/anthropics/skills/tree/main/skills/pdf",
        raw_url="https://raw.githubusercontent.com/anthropics/skills/main/skills/pdf/SKILL.md",
        origin="anthropics/skills",
        license_note="Many skills in anthropics/skills are Apache-2.0; see source directory for exact license.",
        dependency_profile="PDF artifact workflow; depends on page rendering, text extraction, layout evidence, and document-specific utilities",
        external_dependencies=["PDF file", "page rendering", "text extraction", "layout inspection", "possible Python/PDF tools"],
        resource_signals=["pages", "layout", "forms", "text extraction", "rendered evidence"],
        fallback_description="Reads, creates, edits, renders, or extracts information from PDF files.",
    ),
    PublicSkill(
        slug="public-docx",
        source_name="docx",
        source_url="https://github.com/anthropics/skills/tree/main/skills/docx",
        raw_url="https://raw.githubusercontent.com/anthropics/skills/main/skills/docx/SKILL.md",
        origin="anthropics/skills",
        license_note="Many skills in anthropics/skills are Apache-2.0; see source directory for exact license.",
        dependency_profile="Word document artifact workflow; depends on DOCX structure, styling, comments, tracked edits, and render verification",
        external_dependencies=[".docx file", "Word document structure", "comments or revisions", "templates", "rendering tools"],
        resource_signals=["document styles", "tracked changes", "comments", "templates", "rendered verification"],
        fallback_description="Creates, edits, extracts, or reviews Word/DOCX document artifacts.",
    ),
    PublicSkill(
        slug="public-pptx",
        source_name="pptx",
        source_url="https://github.com/anthropics/skills/tree/main/skills/pptx",
        raw_url="https://raw.githubusercontent.com/anthropics/skills/main/skills/pptx/SKILL.md",
        origin="anthropics/skills",
        license_note="Many skills in anthropics/skills are Apache-2.0; see source directory for exact license.",
        dependency_profile="presentation artifact workflow; depends on slide structure, speaker notes, visual layouts, templates, and render checks",
        external_dependencies=[".pptx file", "slide layouts", "speaker notes", "template assets", "rendering tools"],
        resource_signals=["slides", "layouts", "notes", "theme", "visual QA", "export"],
        fallback_description="Creates, edits, extracts, or reviews PowerPoint/PPTX presentation artifacts.",
    ),
    PublicSkill(
        slug="public-huggingface-datasets",
        source_name="huggingface-datasets",
        source_url="https://github.com/huggingface/skills/tree/main/skills/huggingface-datasets",
        raw_url="https://raw.githubusercontent.com/huggingface/skills/main/skills/huggingface-datasets/SKILL.md",
        origin="huggingface/skills",
        license_note="See source repository for license.",
        dependency_profile="dataset discovery and extraction workflow; depends on Hugging Face Dataset Viewer API, dataset subset/split metadata, pagination, filtering, and download URLs",
        external_dependencies=["Hugging Face Dataset Viewer API", "dataset repository", "subset/split names", "pagination", "parquet or JSONL URLs"],
        resource_signals=["dataset rows", "subsets", "splits", "filters", "download links", "API calls"],
        fallback_description="Fetches and inspects Hugging Face dataset metadata, rows, filters, downloads, and statistics.",
    ),
    PublicSkill(
        slug="public-brainstorming",
        source_name="brainstorming",
        source_url="https://github.com/obra/superpowers/tree/main/skills/brainstorming",
        raw_url="https://raw.githubusercontent.com/obra/superpowers/main/skills/brainstorming/SKILL.md",
        origin="obra/superpowers via SkillRet preview",
        license_note="SkillRet metadata reports MIT for this source; see upstream repository for exact terms.",
        dependency_profile="creative design-planning workflow; depends on user intent, requirements, constraints, and design alternatives",
        external_dependencies=["user goals", "requirements", "constraints", "design alternatives"],
        resource_signals=["intent exploration", "requirements", "design options", "before implementation"],
        fallback_description="Explores user intent, requirements, and design before creative or implementation work.",
    ),
    PublicSkill(
        slug="public-writing-plans",
        source_name="writing-plans",
        source_url="https://github.com/obra/superpowers/tree/main/skills/writing-plans",
        raw_url="https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-plans/SKILL.md",
        origin="obra/superpowers via SkillRet preview",
        license_note="SkillRet metadata reports MIT for this source; see upstream repository for exact terms.",
        dependency_profile="implementation planning workflow; depends on spec, requirements, task decomposition, and validation strategy",
        external_dependencies=["requirements/spec", "project context", "implementation constraints", "test strategy"],
        resource_signals=["plan before code", "tasks", "risks", "validation", "implementation order"],
        fallback_description="Writes implementation plans for multi-step tasks before touching code.",
    ),
    PublicSkill(
        slug="public-api-design-principles",
        source_name="api-design-principles",
        source_url="https://github.com/wshobson/agents/tree/main/plugins/backend-development/skills/api-design-principles",
        raw_url="https://raw.githubusercontent.com/wshobson/agents/main/plugins/backend-development/skills/api-design-principles/SKILL.md",
        origin="wshobson/agents via SkillRet preview",
        license_note="SkillRet metadata reports MIT for this source; see upstream repository for exact terms.",
        dependency_profile="API design workflow; depends on endpoint/resource model, REST or GraphQL patterns, versioning, error model, and client usability",
        external_dependencies=["API specification", "resource model", "client requirements", "versioning policy", "error semantics"],
        resource_signals=["REST", "GraphQL", "resource naming", "pagination", "error behavior", "developer experience"],
        fallback_description="Applies REST and GraphQL API design principles to new or reviewed API specifications.",
    ),
    PublicSkill(
        slug="public-architecture-patterns",
        source_name="architecture-patterns",
        source_url="https://github.com/wshobson/agents/tree/main/plugins/backend-development/skills/architecture-patterns",
        raw_url="https://raw.githubusercontent.com/wshobson/agents/main/plugins/backend-development/skills/architecture-patterns/SKILL.md",
        origin="wshobson/agents via SkillRet preview",
        license_note="SkillRet metadata reports MIT for this source; see upstream repository for exact terms.",
        dependency_profile="backend architecture pattern workflow; depends on system boundaries, domain model, dependency direction, and maintainability constraints",
        external_dependencies=["backend codebase", "domain model", "architecture constraints", "dependency boundaries"],
        resource_signals=["Clean Architecture", "Hexagonal Architecture", "DDD", "refactoring", "maintainability"],
        fallback_description="Supports backend architecture design and refactoring using established architecture patterns.",
    ),
    PublicSkill(
        slug="public-markitdown",
        source_name="markitdown",
        source_url="https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/markitdown",
        raw_url="https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/markitdown/SKILL.md",
        origin="K-Dense-AI/scientific-agent-skills via public skill directory",
        license_note="SkillRet metadata reports MIT for this source; see upstream repository for exact terms.",
        dependency_profile="document conversion workflow; depends on Microsoft MarkItDown-style conversion tools and input file types",
        external_dependencies=["MarkItDown or equivalent converter", "PDF/DOCX/PPTX/XLSX/image files", "OCR support when needed"],
        resource_signals=["file conversion", "Markdown output", "OCR", "office documents", "scientific documents"],
        fallback_description="Converts files and office documents to Markdown, including PDFs, office files, images, and web sources.",
    ),
]


DISCOVERY_REPOSITORIES = [
    PublicRepository(
        owner="anthropics",
        repo="skills",
        branch="main",
        origin="anthropics/skills",
        path_prefix="skills/",
        source_base="https://github.com/anthropics/skills/tree/main",
        raw_base="https://raw.githubusercontent.com/anthropics/skills/main",
        slug_prefix="public-anthropic",
        license_note="Many skills in anthropics/skills are Apache-2.0; see source directory for exact license.",
        skip_path_markers=("template/",),
    ),
    PublicRepository(
        owner="openai",
        repo="skills",
        branch="main",
        origin="openai/skills",
        path_prefix="skills/.curated/",
        source_base="https://github.com/openai/skills/tree/main",
        raw_base="https://raw.githubusercontent.com/openai/skills/main",
        slug_prefix="public-openai",
        license_note="See source skill directory for license.",
        skip_path_markers=("skills/.system/",),
    ),
    PublicRepository(
        owner="claude-office-skills",
        repo="skills",
        branch="main",
        origin="claude-office-skills/skills",
        path_prefix="",
        source_base="https://github.com/claude-office-skills/skills/tree/main",
        raw_base="https://raw.githubusercontent.com/claude-office-skills/skills/main",
        slug_prefix="public-office",
        license_note="See source repository for license and skill-specific terms.",
        skip_path_markers=("_template/",),
    ),
    PublicRepository(
        owner="huggingface",
        repo="skills",
        branch="main",
        origin="huggingface/skills",
        path_prefix="skills/",
        source_base="https://github.com/huggingface/skills/tree/main",
        raw_base="https://raw.githubusercontent.com/huggingface/skills/main",
        slug_prefix="public-huggingface",
        license_note="See source repository for license and skill-specific terms.",
        skip_path_markers=(),
    ),
    PublicRepository(
        owner="akillness",
        repo="oh-my-skills",
        branch="main",
        origin="akillness/oh-my-skills",
        path_prefix=".agent-skills/",
        source_base="https://github.com/akillness/oh-my-skills/tree/main",
        raw_base="https://raw.githubusercontent.com/akillness/oh-my-skills/main",
        slug_prefix="public-oh-my",
        license_note="See source repository for license and skill-specific terms.",
        skip_path_markers=(),
    ),
    PublicRepository(
        owner="addyosmani",
        repo="agent-skills",
        branch="main",
        origin="addyosmani/agent-skills",
        path_prefix="skills/",
        source_base="https://github.com/addyosmani/agent-skills/tree/main",
        raw_base="https://raw.githubusercontent.com/addyosmani/agent-skills/main",
        slug_prefix="public-addy-agent",
        license_note="See source repository for license and skill-specific terms.",
        skip_path_markers=(),
    ),
    PublicRepository(
        owner="addyosmani",
        repo="web-quality-skills",
        branch="main",
        origin="addyosmani/web-quality-skills",
        path_prefix="skills/",
        source_base="https://github.com/addyosmani/web-quality-skills/tree/main",
        raw_base="https://raw.githubusercontent.com/addyosmani/web-quality-skills/main",
        slug_prefix="public-addy-web",
        license_note="See source repository for license and skill-specific terms.",
        skip_path_markers=(),
    ),
    PublicRepository(
        owner="mattpocock",
        repo="skills",
        branch="main",
        origin="mattpocock/skills",
        path_prefix="skills/",
        source_base="https://github.com/mattpocock/skills/tree/main",
        raw_base="https://raw.githubusercontent.com/mattpocock/skills/main",
        slug_prefix="public-mattpocock",
        license_note="See source repository for license and skill-specific terms.",
        skip_path_markers=("skills/deprecated/",),
    ),
    PublicRepository(
        owner="kepano",
        repo="obsidian-skills",
        branch="main",
        origin="kepano/obsidian-skills",
        path_prefix="skills/",
        source_base="https://github.com/kepano/obsidian-skills/tree/main",
        raw_base="https://raw.githubusercontent.com/kepano/obsidian-skills/main",
        slug_prefix="public-obsidian",
        license_note="See source repository for license and skill-specific terms.",
        skip_path_markers=(),
    ),
    PublicRepository(
        owner="GeniusHTX",
        repo="SWE-Skills-Bench",
        branch="main",
        origin="GeniusHTX/SWE-Skills-Bench",
        path_prefix="skills/",
        source_base="https://github.com/GeniusHTX/SWE-Skills-Bench/tree/main",
        raw_base="https://raw.githubusercontent.com/GeniusHTX/SWE-Skills-Bench/main",
        slug_prefix="public-swebench",
        license_note="See source repository for license and skill-specific terms.",
        skip_path_markers=(),
    ),
    PublicRepository(
        owner="lbussell",
        repo="agent-skills",
        branch="main",
        origin="lbussell/agent-skills",
        path_prefix="skills/",
        source_base="https://github.com/lbussell/agent-skills/tree/main",
        raw_base="https://raw.githubusercontent.com/lbussell/agent-skills/main",
        slug_prefix="public-lbussell",
        license_note="See source repository for license and skill-specific terms.",
        skip_path_markers=(),
    ),
    PublicRepository(
        owner="numman-ali",
        repo="n-skills",
        branch="main",
        origin="numman-ali/n-skills",
        path_prefix="skills/",
        source_base="https://github.com/numman-ali/n-skills/tree/main",
        raw_base="https://raw.githubusercontent.com/numman-ali/n-skills/main",
        slug_prefix="public-n-skills",
        license_note="See source repository for license and skill-specific terms.",
        skip_path_markers=(),
    ),
    PublicRepository(
        owner="tmchow",
        repo="agent-skills",
        branch="main",
        origin="tmchow/agent-skills",
        path_prefix="",
        source_base="https://github.com/tmchow/agent-skills/tree/main",
        raw_base="https://raw.githubusercontent.com/tmchow/agent-skills/main",
        slug_prefix="public-tmchow",
        license_note="See source repository for license and skill-specific terms.",
        skip_path_markers=(),
    ),
    PublicRepository(
        owner="vercel-labs",
        repo="skills",
        branch="main",
        origin="vercel-labs/skills",
        path_prefix="skills/",
        source_base="https://github.com/vercel-labs/skills/tree/main",
        raw_base="https://raw.githubusercontent.com/vercel-labs/skills/main",
        slug_prefix="public-vercel",
        license_note="See source repository for license and skill-specific terms.",
        skip_path_markers=(),
    ),
]


FRONTMATTER_RE = re.compile(r"^---\s*(.*?)\s*---", re.DOTALL)
NAME_RE = re.compile(r"^name:\s*[\"']?(.+?)[\"']?\s*$", re.MULTILINE)
DESCRIPTION_RE = re.compile(r"^description:\s*[\"']?(.+?)[\"']?\s*$", re.MULTILINE | re.DOTALL)


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "skill-benchmark-importer/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def fetch_json(url: str) -> dict[str, object]:
    request = urllib.request.Request(url, headers={"User-Agent": "skill-benchmark-importer/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "unknown"


def title_from_source_name(source_name: str) -> str:
    return source_name.replace("-", " ").replace("_", " ")


def inferred_profile(source_name: str, path: str) -> tuple[str, list[str], list[str], str]:
    joined = f"{source_name} {path}".lower()
    dependencies = ["user-provided task context", "source material named in the request"]
    signals = [title_from_source_name(source_name), "public SKILL.md metadata"]
    profile = f"public workflow for {title_from_source_name(source_name)}; depends on the source artifact and task context named by the user"
    fallback = f"Public skill for {title_from_source_name(source_name)} workflows."

    def add(items: list[str], *values: str) -> None:
        for value in values:
            if value not in items:
                items.append(value)

    if "pdf" in joined:
        add(dependencies, "PDF file", "page rendering or text extraction", "layout evidence")
        add(signals, "PDF", "pages", "layout", "extraction")
        profile = "PDF-focused workflow; depends on file type, page content, layout evidence, and possible OCR or conversion tooling"
        fallback = "Public skill for PDF reading, extraction, conversion, layout review, or document operations."
    if any(token in joined for token in ["docx", "word", "office-to-md", "md-to-office"]):
        add(dependencies, "DOCX or Office document", "document structure", "styles or comments")
        add(signals, "Word", "DOCX", "styles", "tracked changes")
    if any(token in joined for token in ["xlsx", "excel", "sheets", "spreadsheet"]):
        add(dependencies, "spreadsheet workbook", "sheet names", "formulas", "tables or charts")
        add(signals, "spreadsheet", "formulas", "workbook", "charts")
    if any(token in joined for token in ["ppt", "pptx", "slides", "presentation"]):
        add(dependencies, "slide deck", "layout/theme", "speaker notes or visual assets")
        add(signals, "slides", "deck", "layout", "visual QA")
    if any(token in joined for token in ["browser", "playwright", "webapp", "screenshot"]):
        add(dependencies, "browser runtime", "target URL or app", "screenshots", "test flow")
        add(signals, "browser", "DOM", "screenshots", "interaction flow")
        profile = "browser or webapp testing workflow; depends on a target app, runtime state, interaction flow, and visual evidence"
    if any(token in joined for token in ["deploy", "netlify", "vercel", "cloudflare", "render"]):
        add(dependencies, "deployment target", "build command", "environment variables", "deployment logs")
        add(signals, "deployment", "build logs", "environment config", "verification URL")
    if any(token in joined for token in ["api", "mcp", "openai", "claude"]):
        add(dependencies, "API documentation", "authentication context", "schema or tool contract")
        add(signals, "API", "tool contract", "auth", "schema")
    if any(token in joined for token in ["notion", "slack", "gmail", "jira", "asana", "airtable", "linear", "teams", "stripe", "shopify", "quickbooks"]):
        add(dependencies, "external SaaS workspace", "account permissions", "records or API access")
        add(signals, "external service", "workspace", "automation", "permissions")
        profile = "external-service workflow; depends on account permissions, workspace records, API behavior, and side-effect constraints"
    if any(token in joined for token in ["security", "threat", "suspicious"]):
        add(dependencies, "security evidence", "system context", "threat or control taxonomy")
        add(signals, "security", "threats", "controls", "risk")
    if any(token in joined for token in ["invoice", "finance", "valuation", "stock", "saas-metrics", "expense"]):
        add(dependencies, "financial records", "amounts or assumptions", "accounting period")
        add(signals, "finance", "amounts", "metrics", "assumptions")
    if any(token in joined for token in ["data", "dataset", "pipeline", "etl", "analytics"]):
        add(dependencies, "dataset or export", "schema", "processing rules")
        add(signals, "data", "schema", "pipeline", "quality")
    if any(token in joined for token in ["figma", "design", "theme", "brand", "image", "infographic"]):
        add(dependencies, "design brief", "brand constraints", "visual assets")
        add(signals, "design", "brand", "visual", "assets")

    return profile, dependencies, signals, fallback


def discover_repository_skills(repository: PublicRepository) -> list[PublicSkill]:
    tree_url = (
        f"https://api.github.com/repos/{repository.owner}/{repository.repo}/git/trees/"
        f"{repository.branch}?recursive=1"
    )
    data = fetch_json(tree_url)
    discovered: list[PublicSkill] = []
    for item in data.get("tree", []):
        if not isinstance(item, dict):
            continue
        path = str(item.get("path", ""))
        if not path.endswith("/SKILL.md"):
            continue
        if repository.path_prefix and not path.startswith(repository.path_prefix):
            continue
        if any(marker in path for marker in repository.skip_path_markers):
            continue

        source_name = path.rsplit("/", 1)[0].rsplit("/", 1)[-1]
        source_name = slugify(source_name)
        slug = f"{repository.slug_prefix}-{source_name}"
        source_url = f"{repository.source_base}/{path.rsplit('/', 1)[0]}"
        raw_url = f"{repository.raw_base}/{path}"
        profile, dependencies, signals, fallback = inferred_profile(source_name, path)
        discovered.append(
            PublicSkill(
                slug=slug,
                source_name=source_name,
                source_url=source_url,
                raw_url=raw_url,
                origin=repository.origin,
                license_note=repository.license_note,
                dependency_profile=profile,
                external_dependencies=dependencies,
                resource_signals=signals,
                fallback_description=fallback,
            )
        )
    return discovered


def all_public_skills() -> list[PublicSkill]:
    merged: list[PublicSkill] = []
    seen_slugs: set[str] = set()
    seen_raw_urls: set[str] = set()

    def add(skill: PublicSkill) -> None:
        if skill.slug in seen_slugs or skill.raw_url in seen_raw_urls:
            return
        seen_slugs.add(skill.slug)
        seen_raw_urls.add(skill.raw_url)
        merged.append(skill)

    for skill in PUBLIC_SKILLS:
        add(skill)

    for repository in DISCOVERY_REPOSITORIES:
        try:
            for skill in discover_repository_skills(repository):
                add(skill)
        except Exception as exc:  # noqa: BLE001 - discovery should degrade to curated imports.
            print(f"Warning: could not discover {repository.origin}: {exc}")

    return merged


def extract_frontmatter_value(text: str, pattern: re.Pattern[str], fallback: str) -> str:
    match = FRONTMATTER_RE.search(text)
    if not match:
        return fallback
    frontmatter = match.group(1)
    value = pattern.search(frontmatter)
    if not value:
        return fallback
    extracted = value.group(1).strip()
    return " ".join(extracted.split()) or fallback


def wrapper_text(skill: PublicSkill, original_text: str | None, status: str, error: str | None) -> str:
    original_name = skill.source_name
    original_description = skill.fallback_description
    if original_text:
        original_name = extract_frontmatter_value(original_text, NAME_RE, skill.source_name)
        original_description = extract_frontmatter_value(
            original_text,
            DESCRIPTION_RE,
            skill.fallback_description,
        )

    dependency_lines = "\n".join(f"- {item}" for item in skill.external_dependencies)
    signal_lines = "\n".join(f"- {item}" for item in skill.resource_signals)
    error_note = f"\nImport note: original download failed: {error}\n" if error else ""
    description = (
        f"Public-source background skill based on `{original_name}`. "
        f"{original_description} Use as an uncontrolled scale distractor with explicit dependency and resource signals."
    )
    description_yaml = json.dumps(description)

    return f"""---
name: {skill.slug}
description: {description_yaml}
metadata:
  public_source_name: {json.dumps(original_name)}
  public_origin: {json.dumps(skill.origin)}
  source_url: {json.dumps(skill.source_url)}
  raw_url: {json.dumps(skill.raw_url)}
  import_status: {json.dumps(status)}
  dependency_profile: {json.dumps(skill.dependency_profile)}
---

# Public Imported Background: {original_name}

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: {skill.origin}
- Source page: {skill.source_url}
- Raw artifact: {skill.raw_url}
- License note: {skill.license_note}

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.
{error_note}
## Dependency Profile

{skill.dependency_profile}

## External Dependencies To Preserve

{dependency_lines}

## Resource And Structure Signals

{signal_lines}

## Use when

- The retrieval setting needs realistic public-skill noise around this capability.
- The selector should consider tool requirements, file types, resource links, or external systems as part of skill suitability.
- The task is closer to this public skill's dependency profile than to a controlled core skill.

## Not for

- Replacing a controlled gold-label core skill in the main confusable evaluation.
- Hiding a second routing problem inside the selected skill.
- Treating public-source imports as cleanly annotated gold labels.

## Benchmark Role

This skill is intended for large-library and dependency-aware retrieval settings. It helps test whether skill representations preserve information such as required tools, file formats, repository context, external services, and optional resources.
"""


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    family_dir = repo_root / "skills" / "public_imported_background"
    if family_dir.exists():
        shutil.rmtree(family_dir)
    family_dir.mkdir(parents=True)

    manifest = []
    public_skills = all_public_skills()
    for skill in public_skills:
        skill_dir = family_dir / skill.slug
        source_dir = skill_dir / "source"
        source_dir.mkdir(parents=True)

        original_text: str | None = None
        status = "downloaded"
        error = None
        try:
            original_text = fetch_text(skill.raw_url)
            (source_dir / "SKILL.original.md").write_text(original_text, encoding="utf-8")
        except Exception as exc:  # noqa: BLE001 - importer should keep going for partial availability.
            status = "download_failed"
            error = str(exc)

        (skill_dir / "SKILL.md").write_text(
            wrapper_text(skill, original_text, status, error),
            encoding="utf-8",
        )
        record = {
            "slug": skill.slug,
            "source_name": skill.source_name,
            "origin": skill.origin,
            "source_url": skill.source_url,
            "raw_url": skill.raw_url,
            "import_status": status,
            "error": error,
            "dependency_profile": skill.dependency_profile,
            "external_dependencies": skill.external_dependencies,
            "resource_signals": skill.resource_signals,
        }
        (source_dir / "IMPORT.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
        manifest.append(record)

    (family_dir / "IMPORT_MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    downloaded = sum(1 for item in manifest if item["import_status"] == "downloaded")
    print(f"Imported {len(manifest)} public background skills ({downloaded} downloaded originals).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
