---
name: web-data-extractor
description: Extracts structured information from web pages, search results, listings, tables, or online sources into a reusable data format.
---

# Web Data Extractor

Turns web page content into structured data.

## Use when

- The user wants information pulled from a page or set of pages.
- The task asks for listings, tables, prices, names, dates, links, facts, or source-grounded fields.
- The output should be structured and reusable rather than a screenshot or UI test result.

## Not for

- Capturing how a page looks.
- Filling a form or completing an interactive flow.
- Testing a UI for regressions.
- Debugging frontend code.

## Preconditions

- The target page, route, or flow is available, described, or can be opened in a browser-like environment.
- The user has stated whether the goal is observation, interaction, testing, extraction, debugging, or accessibility review.

## Workflow

1. Identify the target pages and fields to extract.
2. Inspect the page content and source context.
3. Extract only information visible or source-grounded in the page.
4. Preserve links, qualifiers, missing values, and uncertainty.
5. Return a compact structured result.

## Output pattern

- Structured table or field list.
- Source/page reference for extracted values.
- Missing or ambiguous fields.

## Writing rules

- Do not infer missing values unless clearly labeled as inference.
- Preserve source links or page references when useful.
- Prefer tables or field lists over narrative prose.
- Note access, pagination, or dynamic-loading limits.
