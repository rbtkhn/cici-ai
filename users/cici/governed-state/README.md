# Governed State — Cici

This is the canonical, durable truth for the Cici instance. If any runtime or external system disagrees with these files, these files win.

## Surface Layout

Governed state is organized into named domains (surfaces). Each surface holds a specific category of canonical truth.

| Surface | Path | Status | Contents |
|---|---|---|---|
| **identity** | `identity/` | active | Instance record: id, owner, purpose, capabilities, bridges |
| **voice** | `voice/` | stub | Communication style, tone, persona notes |
| **memory-policy** | `memory-policy/` | stub | Capture rules, retention thresholds, deduplication |
| **workflows** | `workflows/` | stub | Recurring operator flows, maintenance rituals |
| **tools** | `tools/` | stub | MCP configs, AI gateway preferences, integration policies |
| **source-priority** | `source-priority/` | stub | Source weighting, conflict resolution, trust levels |
| **runtime-bridges** | `runtime-bridges/` | stub | Supabase bridge policy, sync rules, back-propagation |

The full surface registry is in `surface-map.json`.

## Status meanings

| Status | Meaning |
|---|---|
| `active` | Has canonical governed-state artifacts. Changes require proposals. |
| `stub` | Directory exists. No artifacts yet. Populated through approved proposals. |

## How to change governed state

For material changes, create a proposal in `proposals/queue/`. See `proposals/README.md` and `docs/change-review-lifecycle.md`.

For small, obvious corrections (typos, factual updates), direct owner edits are fine.

## What "canonical" means

If Supabase data disagrees with these files, these files win. Supabase is the operational runtime; this directory is the source of truth.
