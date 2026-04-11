# Config

Runtime doctrine and authority configuration for this instance.

## Files

| File | Purpose |
|---|---|
| `authority-map.json` | Defines who may write what, and through which mechanism |

## Authority model

The authority map distinguishes four write classes:

1. **Canonical** — owner-controlled governed state writes (direct edit or approved proposal)
2. **Proposal** — agent/automation proposals that await owner review
3. **Operational** — runtime writes to Supabase, caches, indexes (not canonical)
4. **Ephemeral** — in-memory or temp state, never committed to git

See `authority-map.json` for the full definitions and surface assignments.

## Doctrine

The architectural doctrine for this system lives in `docs/governed-state-doctrine.md`.
