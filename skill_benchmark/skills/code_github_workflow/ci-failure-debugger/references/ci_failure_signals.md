# CI Failure Signals

Use this reference only after the CI failure debugger skill is selected.

Common categories:

- Test assertion failure: the product behavior changed or the test expectation is stale.
- Import or module failure: path, dependency, package build, or environment mismatch.
- Type or lint failure: API shape, unused values, formatting, or static contract problem.
- Snapshot failure: rendered output changed and must be checked against intended behavior.
- Timeout or flake: async wait, external dependency, nondeterminism, or resource pressure.
- Workflow configuration failure: missing secret, wrong matrix entry, cache issue, or command typo.

Useful output:

- failing command
- first meaningful error
- likely cause
- minimal fix
- verification command
