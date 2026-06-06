---
name: implicit-pdf-table-reconstructor
description: "Works with PDF packets where row, column, label, and page relationships must be reconstructed as structured data."
---

# Implicit Pdf Table Reconstructor

This routine begins by treating the PDF as a spatial object. It looks for tables, repeated labels, invoice-like fields, and relationships between rows and columns. The deliverable is not prose. It is a structured extraction with page and row anchors, plus notes for merged cells or uncertain labels. It is a poor fit when the user only asks a question or wants a Word conversion.
