---
name: hf-local-model-selector
description: "Selects Hugging Face or GGUF models for local hardware based on memory, quantization, task, latency, and quality tradeoffs."
---

# Hf Local Model Selector

Chooses a model that can actually run on the user's local machine.

## Use when

- The user gives hardware constraints or local inference requirements.
- The decision depends on memory, quantization, model family, or latency.

## Not for

- Inspecting dataset rows.
- Fine-tuning an embedding model.
- Publishing a paper page.

## Preconditions

- Hardware budget and task type are known.
- The user wants model selection rather than training.

## Workflow

1. Identify task and local hardware limits.
2. Compare model sizes, quantization, runtime, and quality.
3. Recommend candidates and fallback options.
4. Give install or verification checks.

## Writing rules

- Do not choose a model larger than the stated memory budget.
- State quality/speed tradeoffs.

## Default shape

- Recommended model
- Why it fits hardware
- Tradeoffs
- Setup check
