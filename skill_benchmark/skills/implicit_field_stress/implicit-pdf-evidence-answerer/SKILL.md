---
name: implicit-pdf-evidence-answerer
description: "Works with PDF packets when the user needs a direct answer grounded in page evidence rather than conversion or extraction."
---

# Implicit Pdf Evidence Answerer

This routine is for the moment when a PDF is acting as the source of truth. The operator reads the question first, hunts for the relevant pages, and then gives a direct answer with page anchors. If the request starts drifting toward tables, OCR cleanup, or form entry, this is the wrong routine. A typical response contains the answer, a short evidence trail, and any uncertainty where the PDF does not support the claim.
