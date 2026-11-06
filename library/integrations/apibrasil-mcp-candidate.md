# APIBrasil MCP consumption reference

This resource points to the APIBrasil team's knowledge base and examples for
consuming its remote MCP server from AI clients, IDEs and automation platforms.
It is a documented candidate, not a server installed or connected in The Office
V2 or in the user's Codex configuration.

## Source record

- Knowledge base and examples:
  [APIBrasil/apibrasil-mcp-client](https://github.com/APIBrasil/apibrasil-mcp-client)
- Reviewed: 2026-10-23 at revision
  [`f030daeb4c47df65380bb0f07eccfdec3561aa03`](https://github.com/APIBrasil/apibrasil-mcp-client/commit/f030daeb4c47df65380bb0f07eccfdec3561aa03).
- The repository license is MIT for its client/documentation code. This does
  not grant free or unlimited use of APIBrasil services.
- Documented remote MCP endpoint:
  `https://mcp.apibrasil.cloud/mcp` (Streamable HTTP).
- The repository also documents an HTTP API gateway at
  `https://gateway.apibrasil.io/api/v2`.
- Start with the repository's [README](https://github.com/APIBrasil/apibrasil-mcp-client/blob/f030daeb4c47df65380bb0f07eccfdec3561aa03/README.md),
  [credential guide](https://github.com/APIBrasil/apibrasil-mcp-client/tree/f030daeb4c47df65380bb0f07eccfdec3561aa03/conceitos/credenciais),
  [dynamic discovery guide](https://github.com/APIBrasil/apibrasil-mcp-client/tree/f030daeb4c47df65380bb0f07eccfdec3561aa03/conceitos/descoberta)
  and [troubleshooting guide](https://github.com/APIBrasil/apibrasil-mcp-client/tree/f030daeb4c47df65380bb0f07eccfdec3561aa03/conceitos/troubleshooting).

## Integration boundary

The upstream documentation describes remote Streamable HTTP and a local
`mcp-remote` bridge for clients that require stdio. A client configuration
requires APIBrasil credentials, and service calls may consume credits or incur
subscription charges. Never store credentials in this catalog, commit them, or
configure a global client automatically. Before a real connection, identify the
specific service and data involved, check current pricing and terms, keep
credentials in the host's approved secret store, and get the applicable user
authorization.

Status: **CATALOGED_NOT_EXECUTED / NOT_CONNECTED / NOT_VALIDATED**. No account,
credential, installation, MCP handshake, tool call or API call was performed.
