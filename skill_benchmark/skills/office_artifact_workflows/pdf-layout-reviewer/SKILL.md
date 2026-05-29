---
name: pdf-layout-reviewer
description: "Reviews rendered PDF pages for layout fidelity, page order, visual artifacts, form placement, table alignment, and page-level reading risks."
---

# PDF Layout Reviewer

Inspects a PDF as a visual artifact rather than only as extracted text.

## Use when

- The user cares about page-level visual fidelity, reading order, or layout defects.
- The PDF contains forms, tables, signatures, columns, figures, or generated pages that may render incorrectly.
- The desired output is a layout review with evidence by page or region.

## Not for

- Extracting a fixed list of fields into a table.
- Running OCR on scanned pages as the main task.
- Converting an office file into Markdown as the main deliverable.

## Preconditions

- A PDF or rendered page evidence is available.
- The user asks for visual/layout correctness, not only content meaning.
- Important page regions, forms, or layout expectations are stated or inferable.

## Workflow

1. Render or inspect representative pages before judging correctness.
2. Check page order, headers, footers, tables, forms, columns, and cropped regions.
3. Compare visual structure against the stated purpose of the document.
4. Record defects with page or region anchors.
5. Separate visual/layout problems from content-summary issues.

## Writing rules

- Use page or region references when possible.
- Do not infer missing field values from layout alone.
- Prioritize visual issues that could change interpretation or usability.

## Default shape

- Page or region
- Observed layout issue
- Why it matters
- Recommended fix or verification
