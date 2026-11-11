# OrgX for Hermes

A configuration-only [Agent Plugins v1](https://agent-plugins.org/) package that connects Hermes to the OrgX remote MCP server at `https://mcp.useorgx.com/mcp`.

OrgX provides organization context and tools for agent work, decisions, artifacts, and execution receipts. Available tools and actions depend on your OrgX account, workspace permissions, OAuth scopes, and service-side approval policies.

## Package contents

- `plugin.json`: portable plugin metadata and the Hermes server trust declaration.
- `mcp.json`: one native Streamable HTTP MCP connection, named `orgx`.
- No Python or JavaScript entrypoint, local executable, dependency installer, skill instructions, hooks, middleware, or background process is bundled.

The package lives in the `integrations/hermes` subdirectory of the MIT-licensed `useorgx/skills` repository. This license covers these packaging files; it does not change the OrgX service or the `useorgx/orgx-mcp` repository license.

## Setup

Use a Hermes release that supports Agent Plugins v1, native Streamable HTTP MCP servers, and the `com.nousresearch.hermes.servers` trust extension.

When a catalog entry is approved, its exact commit pin and `subdir: integrations/hermes` identify this package. For local review, validate this directory with:

```sh
hermes plugins validate integrations/hermes --json
```

Sign in to your own OrgX account through Hermes's native MCP OAuth flow when requested. This package contains no API key, OAuth client secret, token, custom credential handling, or alternative login flow. Do not put credentials in either JSON file.

The `orgx` server is explicitly marked `untrusted` for Hermes's approval policy. Keep Hermes approval protections enabled and approve each requested action only within your intended scope.

## Network and permissions disclosure

Hermes connects to `mcp.useorgx.com` over HTTPS. OAuth authorization may open the OrgX authorization service in your browser. OrgX receives the MCP requests you make and their arguments; the remote service can return account and workspace data authorized by your session.

OrgX tools may read or change workspace records and initiate agent work. Your account permissions and OrgX approval policies control which operations are available. Remote tool definitions and service behavior can evolve independently of this package's commit pin.

This package does not read local files or credential stores, run shell commands, or add telemetry. Hermes itself manages MCP connections and authentication. The remote OrgX service's own terms and privacy policy apply to its use.

## Validation scope

Portable manifest loading and static admission checks can validate this package without an OrgX login. They do not establish that OAuth login, live tool calls, workspace mutations, or end-to-end Hermes execution have been tested. Those require an authorized OrgX account and a separate integration check.
