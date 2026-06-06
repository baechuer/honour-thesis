---
name: mcp-server-builder
description: "Builds MCP server tools or resources with schemas, transport assumptions, capability boundaries, and client usage examples."
---

# Mcp Server Builder

Wraps capabilities for model clients through MCP.

## Use when

- The user wants an MCP server or tool/resource definitions.
- Tool schemas, resources, and client invocation matter.

## Not for

- Designing a REST API for external clients.
- Planning webhook retries.
- Writing generic auth docs.

## Preconditions

- The local/service capabilities to expose are known.
- MCP client and transport assumptions are relevant.

## Workflow

1. Identify tools/resources to expose.
2. Define input/output schemas.
3. Specify transport and auth assumptions.
4. Return server structure and usage examples.

## Writing rules

- Do not expose overly broad filesystem or network access.
- Keep tool boundaries narrow.

## Default shape

- Tools/resources
- Schemas
- Server structure
- Client examples
