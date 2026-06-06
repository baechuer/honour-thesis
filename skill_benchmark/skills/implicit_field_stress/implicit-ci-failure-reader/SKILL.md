---
name: implicit-ci-failure-reader
description: "Reads CI output to identify the first meaningful failure, likely root cause, and rerun or fix sequence."
---

# Implicit Ci Failure Reader

The routine starts in the logs, not the source diff. It looks for the first non-cascading error, then connects that error to tests, dependencies, environment variables, build commands, or platform assumptions. The answer should quote log evidence and propose the smallest rerun sequence. Release-note writing and normal code review belong elsewhere.
