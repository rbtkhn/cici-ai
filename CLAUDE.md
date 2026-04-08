# CLAUDE.md — Context for Claude Code Sessions

This file gives Claude Code context about this repository so it can assist effectively.

---

## What This Repo Is

`xavier_self` is a personal instance of [Open Brain (OB1)](https://github.com/NateBJones-Projects/OB1) — a self-owned AI memory system. It is primarily a **configuration and documentation repository**. The runtime server code is deployed as a Supabase Edge Function and is not stored here.

## Project Purpose

- Provide a persistent, cross-AI knowledge base (thoughts, notes, context)
- Connect to Claude, ChatGPT, Cursor, and other MCP clients
- All data lives in a personal Supabase project (PostgreSQL + pgvector)

## Key Facts

- **No application code lives in this repo** — the server is deployed upstream from NateBJones-Projects/OB1
- **Database**: Supabase (PostgreSQL with pgvector extension)
- **Server**: Supabase Edge Function (Deno/TypeScript) at `open-brain-mcp`
- **Protocol**: MCP over HTTP (query-param key auth)
- **AI Gateway**: OpenRouter for embeddings and model routing
- **Cost**: ~$0.10/month at personal scale

## Environment Variables / Secrets (in Supabase)

| Secret name | Description |
|---|---|
| `MCP_ACCESS_KEY` | 64-char hex key securing the MCP endpoint |
| `OPENROUTER_API_KEY` | OpenRouter API key for embeddings |
| `SUPABASE_URL` | Auto-injected by Supabase Edge Functions runtime |
| `SUPABASE_SERVICE_ROLE_KEY` | Auto-injected by Supabase Edge Functions runtime |

## Common Tasks

### Re-deploy the MCP server after upstream updates

```bash
cd <your-project-folder>
curl -o supabase/functions/open-brain-mcp/index.ts \
  https://raw.githubusercontent.com/NateBJones-Projects/OB1/main/server/index.ts
supabase functions deploy open-brain-mcp --no-verify-jwt
```

### Rotate the access key

```bash
openssl rand -hex 32   # generate new key
supabase secrets set MCP_ACCESS_KEY=<new-key>
supabase functions deploy open-brain-mcp --no-verify-jwt
# Update the key in your AI client MCP connection URL
```

### Rotate the OpenRouter key

```bash
supabase secrets set OPENROUTER_API_KEY=<new-key>
```

### Verify the server is alive

```bash
curl "https://YOUR_PROJECT_REF.supabase.co/functions/v1/open-brain-mcp?key=YOUR_ACCESS_KEY"
```

## Architecture Reference

See [README.md](README.md) for the full architecture diagram.

## Setup Reference

See [docs/setup-guide.md](docs/setup-guide.md) for the complete beginner setup walkthrough.
