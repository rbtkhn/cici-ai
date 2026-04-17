# Tools Surface

**Status: stub** — No governed artifacts yet. Populated through approved proposals.

## Purpose

This surface holds canonical truth about the tools Cici uses: MCP client configurations, AI gateway preferences, integration policies, and tool-selection principles.

## What belongs here (when ready)

- MCP tool preferences: which tools are primary vs. fallback
- AI client policies: Claude vs. ChatGPT vs. Cursor routing preferences
- Gateway configuration: OpenRouter model routing preferences
- Tool trust levels: which tools may write to governed state vs. proposal-only
- Integration status: which tool integrations are active, pending, or deprecated

## Note on secrets

No secrets, API keys, or credentials belong here. Those live in Supabase secrets and `.env` (gitignored).

This surface holds *policies and preferences*, not credentials.

## How to populate

1. Identify recurring tool decisions or preferences from evidence/runtime
2. Synthesize in `prepared-context/synthesis/`
3. Create a proposal in `proposals/queue/` with `target_surface: "tools"`
4. On approval, add the policy here

## Related surfaces

- `runtime-bridges/` — Supabase-specific bridge configuration (separate from general tool policy)
- `workflows/` — workflows invoke tools; canonical tool config informs workflow definitions
