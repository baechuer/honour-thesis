---
name: api-documentation-writer
description: "Writes developer-facing API documentation from an existing contract, including quickstarts, examples, auth notes, and error explanations."
---

# Api Documentation Writer

Produces docs for an already-designed API.

## Use when

- The API contract exists and the user needs developer docs.
- Examples, quickstarts, and error explanations matter.

## Not for

- Designing the API from scratch.
- Building an MCP server.
- Auditing security architecture.

## Preconditions

- Endpoints, schemas, and auth behavior are already known.
- Target developer audience is identified.

## Workflow

1. Read existing contract.
2. Create quickstart and endpoint docs.
3. Add examples and errors.
4. Return docs with missing-contract questions.

## Writing rules

- Do not invent undocumented endpoint behavior.
- Keep examples consistent with schema.

## Default shape

- Quickstart
- Endpoint docs
- Examples
- Errors/questions
