---
name: implicit-trace-path-diagnoser
description: "Uses distributed trace spans to locate latency, failed calls, dependency bottlenecks, and missing instrumentation."
---

# Implicit Trace Path Diagnoser

This routine follows spans across services. It reads timing, parent-child relationships, failed spans, retries, and dependency calls, then identifies the critical path. The output is a trace-based diagnosis with caveats. It is not for writing dashboard panels or Prometheus alert rules.
