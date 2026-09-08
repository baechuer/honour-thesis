# V7 B36+C6 runtime preflight integrity

Status: `PASS_DETERMINISTIC_ZERO_INFERENCE_RUNTIME_PREFLIGHT_REPLAY`.

- V7 matrix: 36 core + 6 fixed-candidate bridge configurations
- Python packages: 27 exact distributions
- SkillRouter snapshots: 2 exact revisions, 17 pinned runtime files
- Smoke evidence: 12 supplied verified cases; no case rerun by this builder
- Primary local runtime: MPS bfloat16, default SDPA, exact-token-length unpadded buckets, batch at most 16
- Long-sequence probes: 4 supplied observations; none rerun by this builder
- Adaptation gate: 7,500-token/256-overlap/max-window is proposed, not approved; I3C/I3-flat length audits remain pending
- Network calls: 0
- Model forward passes: 0
- Labels/results read: false
- Execution authorised: false
- Current-process blockers: MPS_UNAVAILABLE_IN_CURRENT_VERIFIER_PROCESS, DASHSCOPE_API_KEY_ABSENT_FROM_CURRENT_PROCESS, PROSPECTIVE_LOSSLESS_7500_TOKEN_256_OVERLAP_MAX_WINDOW_ADAPTATION_PENDING_APPROVAL, I3C_AND_I3_FLAT_TOKEN_LENGTH_AUDITS_PENDING

Artifact hashes:

- `runtime_inventory.json`: `3bc874eaa23ed699c71ee7007039374868cb65ab69ce05823b67ea3a5b955b54`
- `README.md`: `48f0fcbd00afb8ca50a95e3407e16301e168bd3f6e7987b18cbee6fb4ac713b9`

Tooling hashes:

- builder: `f485b90a09bd8760cc539a1c22a60d302bc6b28f2b2e05c7c5e66af1d0663c78`
- verifier: `859b36b92109a009076b1fc9230c387ac6f76dd200c1450962fa02d4fde94d87`
- tests: `6e267e1806bb89ce684f116e7f2ca6339f080cf7a4011bbecb4781fe79e5efb7`

This PASS validates only deterministic inventory, hashes and contracts. A separate V7 runner and explicit execution authorisation are still required.
