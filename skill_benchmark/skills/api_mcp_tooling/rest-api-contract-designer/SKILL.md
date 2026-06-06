---
name: rest-api-contract-designer
description: "Designs REST API resources, endpoints, request/response schemas, status codes, pagination, and error behavior."
---

# Rest Api Contract Designer

Creates a new API contract rather than reviewing an existing one.

## Use when

- The user needs a new REST API design.
- Resources, schemas, status codes, and errors must be specified.

## Not for

- Building an MCP server.
- Writing developer documentation from an existing API.
- Planning webhook delivery.

## Preconditions

- Domain objects and client needs are known.
- The API does not already have a final contract.

## Workflow

1. Identify resources and operations.
2. Define schemas and status codes.
3. Specify pagination/filtering/errors.
4. Return contract outline and examples.

## Writing rules

- Do not skip error models.
- Separate API design from implementation details.

## Default shape

- Resources
- Endpoints
- Schemas
- Errors/examples
