---
title: "97 Telco APIs, Two Tools, 730 Tokens"
layout: post
date: 2026-02-27 18:00
tag:
- MCP
- CAMARA
- agents
- telecom
- APIs
category: blog
author: jaime
headerImage: false
---

How we gave AI agents access to the entire CAMARA telco API surface using Cloudflare's Code Mode pattern, a `node:vm` sandbox, and dynamic OIDC authentication.

## The problem with 199 endpoints

[CAMARA](https://camaraproject.org) is the industry standard for telco network APIs. Backed by GSMA and the Linux Foundation, it defines standardized APIs for SIM swap detection, device location, number verification, quality of service, carrier billing, and dozens more. As of February 2026, there are 97 APIs with 199 endpoints across 8 categories, spread over 91 GitHub repositories.

The [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) is the standard way to give AI agents access to external tools. The traditional approach is one tool per endpoint. With 199 CAMARA endpoints, that means 199 tool descriptions in the LLM's context window, roughly 40,000 tokens. That's most of the context window gone before the user even asks a question.

CAMARA itself [published a position](https://camaraproject.org/2026/01/12/camara-charts-a-path-for-network-aware-ai-applications-with-mcp/) on MCP integration in January 2026, recognizing the potential for network-aware AI applications. But the scale problem remained unsolved.

## Code Mode: Cloudflare's insight

In January 2026, Cloudflare [introduced Code Mode](https://blog.cloudflare.com/code-mode-mcp/) for their MCP server. Instead of exposing ~4,000 API endpoints as individual tools, they collapsed everything into two:

- `search(code)` — the LLM writes JavaScript that runs against the full OpenAPI spec
- `execute(code)` — the LLM writes JavaScript that calls the API

The LLM receives only TypeScript type signatures, a product list, and a few example snippets, about 1,000 tokens. From this, it can write arbitrary queries against the spec and construct any API call. The server just executes the code in a sandbox.

The key insight: **no AI runs on the server**. The client's LLM is the intelligence. The server is just a sandboxed execution environment.

## Building camara-mcp

We applied Code Mode to the entire CAMARA ecosystem. The result is [camara-mcp](https://github.com/jaimewin/camara-mcp), a Node.js MCP server with two tools and ~730 tokens of context overhead.

### The spec pipeline

The first challenge was getting all 97 API specs into a single searchable structure. CAMARA APIs live across 91 repositories under `github.com/camaraproject/`, each with OpenAPI YAML files in `code/API_definitions/`.

```bash
$ npm run fetch-specs

Fetching CAMARA repos...
Found 79 API repos (after filtering)
  SimSwap: 2 spec(s)
  DeviceLocation: 3 spec(s)
  QualityOnDemand: 3 spec(s)
  ...

Downloaded 98 spec files into data/raw/
Processing specs...
  97 APIs, 199 endpoints → data/spec.json + data/products.json
Done!
```

The pipeline crawls all repos via the GitHub API, downloads every YAML, resolves all `$ref` pointers inline (same approach as Cloudflare's spec processor), and merges everything into a single 6MB `spec.json`. It also extracts a categorized product list mapping each API to one of CAMARA's 8 categories.

### What the LLM sees

The search tool description is about 730 tokens. It includes:

- A compact category summary: `Authentication and Fraud Prevention: SIM Swap, Number Verification, Device Swap (+9 more)`
- TypeScript interfaces for `spec.paths`, `OperationInfo`, and `PathItem`
- Three example JavaScript snippets showing how to query the spec

That's it. The LLM never sees the 6MB spec. It writes JavaScript code that runs against it in a `node:vm` sandbox.

### The sandbox

Both tools run LLM-generated code in `node:vm` with restricted globals:

The **search sandbox** provides the `spec` object (read-only), `console` (captured to logs), and safe built-ins (`JSON`, `Object`, `Array`, etc.). No `fetch`, no `require`, no network access.

The **execute sandbox** provides `camara.request()`, an HTTP client restricted to the configured operator gateway. The bearer token is injected by the server into the HTTP headers. The LLM-generated code cannot access, log, or exfiltrate the token.

## The demo

Here's the actual flow from our test with [Kiro](https://kiro.dev):

```
User: "Check if +34666555444 had a SIM swap in the last 24 hours"

→ Agent calls @camara/search:
  async () => {
    const results = [];
    for (const [path, methods] of Object.entries(spec.paths)) {
      for (const [method, op] of Object.entries(methods)) {
        if (path.includes('sim-swap')) {
          results.push({ method, path, summary: op.summary, requestBody: op.requestBody });
        }
      }
    }
    return results;
  }

→ Found: POST /sim-swap/vwip/check

→ Agent calls @camara/execute:
  async () => {
    return camara.request({
      method: "POST",
      path: "/sim-swap/vwip/check",
      body: { phoneNumber: "+34666555444", maxAge: 24 }
    });
  }

→ Result: { swapped: false }
→ Agent: "No SIM swap detected in the last 24 hours"
```

Two tool calls. Natural language in, natural language out. The LLM figured out the right endpoint, the right HTTP method, the right request body, all from the type signatures and examples.

## Dynamic OIDC authentication

The most interesting part is what happens when the token is invalid. CAMARA APIs use OIDC with per-API scopes (e.g., `sim-swap:check`, `location:read`). Each operator has its own OIDC provider.

When the executor gets a 401 from the operator, it doesn't fail. Instead:

1. Discovers the operator's OIDC configuration via `GET {apiRoot}/.well-known/openid-configuration`
2. Infers the required scope from the request path (`/sim-swap/vwip/check` → `sim-swap:check`)
3. Attempts a `client_credentials` grant with the inferred scope
4. Caches the token and retries the request

Here's what the mock gateway logs look like:

```
POST /sim-swap/vwip/check                              → 401 (invalid token)
GET  /.well-known/openid-configuration                 → 200
POST /token grant=client_credentials scope=sim-swap:check → 200 (token=mock-cc-9d2c215b)
POST /sim-swap/vwip/check                              → 200 (mocked)
```

The entire OIDC flow happens inside one `execute()` call. The LLM doesn't even know auth happened. The scope is inferred from the API path, matching CAMARA's convention. The OpenAPI spec's `security` field is also available in search results, so the LLM can discover required scopes before calling execute.

This means the server works with any CAMARA-compliant operator without pre-configured tokens. Point it at an operator's gateway, provide client credentials, and the executor handles discovery, token acquisition, and caching automatically.

## What's novel

The combination of four elements is what makes this interesting:

1. **Spec-driven scope discovery**: OAuth scopes are extracted from the OpenAPI specification's `security` field, not pre-configured. The LLM can read the spec to discover what auth is needed before making a request.

2. **MCP as consent broker**: MCP's auth challenge mechanism can broker consent between the user, the AI agent, and the operator's OIDC provider. The consent chain: user → MCP client → MCP server → operator OIDC → network API.

3. **Credential isolation**: The bearer token is injected into the sandbox's HTTP client by the server. The LLM-generated code running in `node:vm` cannot access it. No prompt injection can exfiltrate credentials.

4. **Federated multi-operator**: The same two tools work across any CAMARA-compliant operator. OIDC discovery is dynamic. No hardcoded integrations per operator.

## Try it

```bash
git clone https://github.com/jaimewin/camara-mcp
cd camara-mcp
npm install
npm run fetch-specs

# Start mock operator gateway
npm run dev:mock &

# Connect via MCP (stdio)
CAMARA_API_ROOT=http://localhost:9091 CAMARA_API_TOKEN=mock-token npx tsx src/index.ts
```

Or add to your MCP client config:

```json
{
  "mcpServers": {
    "camara": {
      "command": "npx",
      "args": ["tsx", "/path/to/camara-mcp/src/index.ts"],
      "env": {
        "CAMARA_API_ROOT": "http://localhost:9091",
        "CAMARA_API_TOKEN": "mock-token"
      }
    }
  }
}
```

97 APIs. 199 endpoints. 730 tokens. Two tool calls per query.

The code is at [github.com/jaimewin/camara-mcp](https://github.com/jaimewin/camara-mcp).
