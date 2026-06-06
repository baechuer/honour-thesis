---
name: gradio-demo-builder
description: "Builds a Gradio demo interface around a model, dataset, or inference pipeline with inputs, outputs, examples, and launch constraints."
---

# Gradio Demo Builder

Creates an interactive demo rather than training or evaluating a model.

## Use when

- The user wants a web demo for a model or pipeline.
- Inputs, outputs, examples, and UI behavior matter.

## Not for

- Choosing a model for local hardware.
- Running benchmark evaluation.
- Publishing a research paper page.

## Preconditions

- A model/pipeline or callable function exists.
- The desired demo inputs and outputs are known.

## Workflow

1. Identify model inputs and outputs.
2. Design Gradio components and examples.
3. Add validation and error display.
4. Return app scaffold and launch instructions.

## Writing rules

- Do not turn a demo request into a training plan.
- Keep UI components aligned with model I/O.

## Default shape

- Components
- Examples
- App scaffold
- Launch checks
