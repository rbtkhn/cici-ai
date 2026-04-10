# Supabase Bridge

Supabase is an operational bridge in this system. It is not the canonical source of governed truth.

## What Supabase provides

| Capability | Detail |
|---|---|
| **Vector search** | pgvector (cosine similarity) over the `thoughts` table |
| **MCP server runtime** | Supabase Edge Functions host the `open-brain-mcp` Deno server |
| **Credentials management** | `MCP_ACCESS_KEY`, `OPENROUTER_API_KEY` stored as project secrets |
| **API gateway** | HTTP endpoint for AI clients (Claude, ChatGPT, Cursor, Gemini) |
| **Deduplication** | `upsert_thought()` + `content_fingerprint` prevents duplicate memories |
| **Operational dashboard** | Web UI for querying and inspecting thought data |

## What Supabase does not own

- The governed state of this instance (`users/cici/governed-state/`)
- The authority model (`config/authority-map.json`)
- The proposal review queue (`proposals/`)
- The doctrine (`docs/governed-state-doctrine.md`)

## Relationship to governed state

During Phase 1, Supabase remains the primary runtime. Governed-state files capture the authoritative record that Supabase should reflect, not the other way around.

If Supabase data diverges from governed state, governed state wins.

## Configuration references

- Setup: `docs/setup-guide.md`
- Architecture: `README.md`
- Doctrine: `docs/governed-state-doctrine.md`
- Compatibility guarantees: `docs/migration-compatibility.md`

## Future direction

Later phases may introduce local-first sync so that Supabase becomes a secondary mirror rather than the primary store. Phase 1 does not implement this — Supabase remains primary for all runtime operations.
