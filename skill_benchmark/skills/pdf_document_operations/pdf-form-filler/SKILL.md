---
name: pdf-form-filler
description: "Fills existing PDF form fields from supplied values and checks missing required fields or validation constraints."
---

# Pdf Form Filler

Writes values into a PDF form rather than extracting or summarising its content.

## Use when

- The user has a fillable form and values to enter.
- The output should be a completed form or a field-completion checklist.

## Not for

- Extracting fields from an invoice.
- Answering questions from a PDF.
- Converting a PDF to DOCX.

## Preconditions

- A form PDF and source values are available.
- Required fields and validation rules are known or discoverable.

## Workflow

1. Map supplied values to form fields.
2. Check required fields and allowed formats.
3. Fill or prepare field-value instructions.
4. Report missing values and validation risks.

## Writing rules

- Do not invent missing form values.
- Separate filled values from missing required fields.

## Default shape

- Field
- Value
- Status
- Missing or validation issue
