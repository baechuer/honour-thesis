---
name: xlsx-formula-model-builder
description: "Builds spreadsheet formula models from assumptions, inputs, outputs, formulas, sheet structure, and validation checks."
---

# Xlsx Formula Model Builder

Creates spreadsheet logic rather than auditing an existing file.

## Use when

- The user wants a workbook model or formulas built.
- Inputs, assumptions, outputs, and validation formulas matter.

## Not for

- Automating Airtable.
- Extracting meeting action items.
- Classifying emails.

## Preconditions

- Business assumptions and desired outputs are available.
- Spreadsheet formulas are the desired artifact.

## Workflow

1. Map assumptions and outputs.
2. Design sheets and formulas.
3. Add checks and sensitivities.
4. Return formula model outline.

## Writing rules

- Do not hard-code assumptions without labelling them.
- Keep formulas auditable.

## Default shape

- Sheets
- Inputs
- Formulas
- Checks
