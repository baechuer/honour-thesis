---
name: spreadsheet-formula-auditor
description: "Audits spreadsheet formulas, references, assumptions, sheet dependencies, and calculation risks without changing the workbook's analysis goal."
---

# Spreadsheet Formula Auditor

Checks spreadsheet calculation logic rather than extracting rows or designing charts.

## Use when

- The user asks whether formulas, references, assumptions, or linked sheets are correct.
- The workbook contains calculation chains, named assumptions, lookup formulas, or summary tabs.
- The output should identify formula risk and verification checks.

## Not for

- Summarising a spreadsheet as a business report.
- Creating a visual chart from clean data.
- Extracting document fields from PDFs or forms.

## Preconditions

- A workbook, CSV plus formula notes, or sheet description is available.
- The task includes formula correctness, dependency, or assumption risk.
- Expected outputs or validation criteria are stated or inferable.

## Workflow

1. Map sheets, inputs, formulas, outputs, and linked assumptions.
2. Check formulas for broken references, inconsistent ranges, hard-coded values, and copy errors.
3. Trace material outputs back to input assumptions.
4. Identify checks that can confirm or falsify the calculation.
5. Report risks by impact and required verification.

## Writing rules

- Do not treat formula audit as general data analysis.
- Call out assumptions separately from formula errors.
- Preserve sheet and cell references when available.

## Default shape

- Sheet or formula area
- Issue or risk
- Evidence
- Verification or fix
