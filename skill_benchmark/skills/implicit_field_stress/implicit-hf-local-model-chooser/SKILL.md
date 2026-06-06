---
name: implicit-hf-local-model-chooser
description: "Chooses local Hugging Face or GGUF models by task, memory budget, quantization, runtime, and latency constraints."
---

# Implicit Hf Local Model Chooser

This routine starts from hardware reality. It compares model size, quantization, runtime, task fit, and expected latency, then recommends candidates that fit the user's machine. It does not audit dataset rows, build demos, or run benchmark evaluations unless those are explicitly the next step.
