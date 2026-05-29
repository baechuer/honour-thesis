---
name: public-xlsx
description: "Public-source background skill based on `xlsx`. Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path \u2014 even casually (like \\\"the xlsx in my downloads\\\") \u2014 and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved. Use as an uncontrolled scale distractor with explicit dependency and resource signals."
metadata:
  public_source_name: "xlsx"
  public_origin: "anthropics/skills"
  source_url: "https://github.com/anthropics/skills/tree/main/skills/xlsx"
  raw_url: "https://raw.githubusercontent.com/anthropics/skills/main/skills/xlsx/SKILL.md"
  import_status: "downloaded"
  dependency_profile: "spreadsheet artifact workflow; depends on spreadsheet files, formulas, workbook structure, and possible script/tool support"
---

# Public Imported Background: xlsx

This is a public-source background skill for scale and realism experiments. It is not part of the hand-authored confusable core.

## Source

- Origin: anthropics/skills
- Source page: https://github.com/anthropics/skills/tree/main/skills/xlsx
- Raw artifact: https://raw.githubusercontent.com/anthropics/skills/main/skills/xlsx/SKILL.md
- License note: Many skills in anthropics/skills are Apache-2.0; see source directory for exact license.

The original public `SKILL.md` is stored at `source/SKILL.original.md` when download succeeds. The selection-facing wrapper stays normalized so that public imports do not hide broad internal routing inside the benchmark core.

## Dependency Profile

spreadsheet artifact workflow; depends on spreadsheet files, formulas, workbook structure, and possible script/tool support

## External Dependencies To Preserve

- .xlsx/.xls/.csv files
- spreadsheet formulas
- workbook sheets
- formatting/layout
- possible Python tooling

## Resource And Structure Signals

- file type
- formula recalculation
- sheets
- charts
- formatting
- data analysis

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
