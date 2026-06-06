---
name: implicit-visual-diff-reviewer
description: "Compares expected and current visual states across screenshots and viewports to classify layout regressions."
---

# Implicit Visual Diff Reviewer

This routine assumes there is an expected visual state and a current visual state. It compares spacing, clipping, text overflow, contrast changes, responsive layout, and image placement. It ignores backend guesses unless the screenshots support them. The useful artifact is a viewport-specific list of visual differences and severity.
