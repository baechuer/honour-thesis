---
name: hf-zerogpu-space-deployer
description: "Prepares Hugging Face Spaces ZeroGPU deployments with runtime constraints, sleep behavior, dependency files, and queue expectations."
---

# Hf Zerogpu Space Deployer

Handles deployment constraints for ZeroGPU Spaces.

## Use when

- The user wants to deploy a demo to Hugging Face Spaces ZeroGPU.
- GPU availability, requirements files, and queueing behavior matter.

## Not for

- Building the demo UI itself.
- Selecting a local GGUF model.
- Running community evaluations.

## Preconditions

- A Space/app exists or is planned.
- ZeroGPU constraints and dependencies are relevant.

## Workflow

1. Check app runtime and GPU calls.
2. Prepare dependency and Space configuration.
3. Plan queueing/sleep behavior.
4. Return deployment checklist and verification steps.

## Writing rules

- Do not assume always-on GPU.
- Flag packages that may not fit the runtime.

## Default shape

- Space setup
- Dependencies
- ZeroGPU constraints
- Verification
