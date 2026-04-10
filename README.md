# xavier_self — Xavier's Personal Open Brain Instance

> **This is Xavier's personal instance layer.** For the fork of the server code see [Xavier-x01/open-brain-xavier](https://github.com/Xavier-x01/open-brain-xavier). Upstream project: [NateBJones-Projects/OB1](https://github.com/NateBJones-Projects/OB1). Business brand: [BrewMind](https://brewmind.cafe).

This repo holds **configuration and documentation only** — no secrets, no server code. All AI memory captured through this instance (including BrewMind business context, notes, and learnings) lives in Xavier's private Supabase project. See [`docs/personal/README.md`](docs/personal/README.md) for goals and workflow notes.

---

# Open Brain — Instance Documentation

A personal instance of [Open Brain (OB1)](https://github.com/NateBJones-Projects/OB1) — a self-owned, persistent AI memory system built on Supabase and exposed via the Model Context Protocol (MCP). Any MCP-compatible AI (Claude, ChatGPT, Cursor, Gemini) can read from and write to this knowledge base.

> "One database, one AI gateway, one chat channel — any AI plugs in. No middleware, no SaaS."

---

## What Is Open Brain?

Open Brain is not a notes app. It is an **infrastructure layer for thinking** — a PostgreSQL database with vector search and an open protocol on top. When you capture a thought through any connected AI, it lands here. When you ask an AI a question, it searches here for context about you.

Key properties:
- **You own the data** — stored in your own Supabase project
- **Vendor-neutral** — connects to any AI via MCP
- **Semantic search** — finds relevant memories by meaning, not keyword
- **Deduplication** — content fingerprinting prevents duplicate entries
- **~$0.10/month** to run at personal scale

---

## Architecture

```
┌────────────────────────────────────────────────────────┐
│                    AI Clients                          │
│   Claude · ChatGPT · Cursor · Gemini · Any MCP client  │
└──────────────────────┬─────────────────────────────────┘
                       │ MCP (HTTP)
┌──────────────────────▼─────────────────────────────────┐
│              Supabase Edge Function                     │
│            open-brain-mcp  (Deno/TypeScript)            │
│  Tools: capture · search · recent_thoughts · stats      │
│  Auth:  ?key=<MCP_ACCESS_KEY>  (query-param validation) │
└──────────────────────┬─────────────────────────────────┘
                       │ Supabase service role
┌──────────────────────▼─────────────────────────────────┐
│              Supabase (PostgreSQL)                      │
│                                                         │
│  thoughts table                                         │
│  ├── id              uuid (PK)                          │
│  ├── content         text                               │
│  ├── embedding       vector(1536)   ← pgvector          │
│  ├── metadata        jsonb                              │
│  ├── content_fingerprint  text (UNIQUE, dedup key)      │
│  ├── created_at      timestamptz                        │
│  └── updated_at      timestamptz                        │
│                                                         │
│  Functions                                              │
│  ├── match_thoughts()   — cosine similarity search      │
│  └── upsert_thought()   — insert or merge on fingerprint│
│                                                         │
│  Extensions: pgvector                                   │
│  Security:   Row Level Security (service_role policy)   │
└─────────────────────────────────────────────────────────┘
                       │
┌──────────────────────▼─────────────────────────────────┐
│              OpenRouter (AI Gateway)                    │
│  Generates embeddings · Routes to any LLM model         │
└─────────────────────────────────────────────────────────┘
```

### Component Breakdown

| Layer | Technology | Role |
|---|---|---|
| Database | Supabase (PostgreSQL + pgvector) | Stores thoughts, embeddings, metadata |
| Server | Supabase Edge Function (Deno) | MCP server — exposes 4 tools to AI clients |
| AI Gateway | OpenRouter | Embedding generation, model access |
| Protocol | MCP (HTTP transport) | Standardized AI tool interface |
| Auth | Query-param access key | Secures the public MCP endpoint |

### MCP Tools Exposed

| Tool | Description |
|---|---|
| `capture` | Store a new thought with auto-embedding |
| `search` | Semantic (vector) search across all thoughts |
| `recent_thoughts` | Browse the most recently captured entries |
| `stats` | Count of total thoughts, date range, etc. |

---

## Repository Layout

```
xavier_self/
├── README.md              # This file
├── CLAUDE.md              # Context for Claude Code sessions
└── docs/
    └── setup-guide.md     # Complete Supabase setup walkthrough
```

The actual server code lives upstream at [NateBJones-Projects/OB1](https://github.com/NateBJones-Projects/OB1) and is deployed as a Supabase Edge Function — no code lives in this repo beyond configuration and documentation.

---

## Quick Links

- Upstream project: [NateBJones-Projects/OB1](https://github.com/NateBJones-Projects/OB1)
- Full setup guide: [docs/setup-guide.md](docs/setup-guide.md)
- Supabase dashboard: https://supabase.com/dashboard
- OpenRouter: https://openrouter.ai
