---
name: service-mesh-traffic-debugger
description: "Debugs service mesh traffic routing, mTLS, retries, traffic splits, destination rules, and sidecar configuration."
---

# Service Mesh Traffic Debugger

Handles mesh-specific operational failures.

## Use when

- The user provides service mesh manifests or routing symptoms.
- Traffic splits, mTLS, sidecars, retries, or destination rules matter.

## Not for

- Writing Prometheus alerts.
- Reviewing app-level retries only.
- Writing incident narrative.

## Preconditions

- Mesh config or symptoms are available.
- The environment uses a service mesh.

## Workflow

1. Inspect virtual services, destination rules, policies, and sidecars.
2. Check traffic routing and mTLS assumptions.
3. Identify retry/split conflicts.
4. Return fix and verification checks.

## Writing rules

- Do not treat mesh config as plain app code.
- State namespace and service assumptions.

## Default shape

- Mesh object
- Traffic issue
- Evidence
- Fix/verification
