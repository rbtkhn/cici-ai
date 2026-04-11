# Source Priority Surface

**Status: stub** — No governed artifacts yet. Populated through approved proposals.

## Purpose

This surface holds canonical truth about how Cici weights and trusts information from different sources when they conflict or overlap.

## What belongs here (when ready)

- Source hierarchy: governed-state > evidence > prepared-context > runtime memory
- Conflict resolution rules: what to do when Supabase and governed-state disagree
- AI client source weighting: how to treat captures from Claude vs. ChatGPT vs. Cursor
- Temporal priority: newer vs. older capture weighting
- Confidence thresholds: minimum confidence for evidence to be eligible for promotion

## The default hierarchy

Until this surface is explicitly governed, the default hierarchy is:

```
1. users/<instance>/governed-state/  ← canonical truth (always wins)
2. evidence/                          ← raw but attributed
3. prepared-context/                  ← processed but not yet approved
4. Supabase runtime memory            ← operational, high volume, noisy
5. In-session context                 ← ephemeral, session-scoped
```

This default is documented here for reference. To override any part of it, create a proposal.

## How to populate

1. Identify source conflicts or priority decisions from evidence/runtime
2. Draft policy in `prepared-context/synthesis/`
3. Create a proposal in `proposals/queue/` with `target_surface: "source-priority"`
4. On approval, add the policy here

## Related surfaces

- `memory-policy/` — memory policy includes how long sources are retained
- `runtime-bridges/` — Supabase is a primary source; its trust level is governed here
