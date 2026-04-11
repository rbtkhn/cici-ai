# Workflows Surface

**Status: stub** — No governed artifacts yet. Populated through approved proposals.

## Purpose

This surface holds canonical truth about recurring operator flows: the repeatable, named sequences of actions that Xavier runs as part of maintaining and evolving Cici.

## What belongs here (when ready)

- Named workflow definitions (e.g., weekly-review, memory-hygiene-audit, capture-session)
- Trigger conditions for each workflow (time-based, event-based, manual)
- Promotion triggers: when a runtime memory pattern should flow toward governed state
- Maintenance rituals: archiving, deduplication, proposal review cadence
- First-session protocol: what to do when opening Cici for the first time in a session

## How to populate

Use the operator skills in `docs/skills/` to identify recurring flows, then propose them here.

1. Document the flow in `prepared-context/synthesis/`
2. Create a proposal in `proposals/queue/` with `target_surface: "workflows"`
3. On approval, add the workflow definition here

## Relationship to docs/skills/

`docs/skills/` holds **portable operator protocols** — step-by-step instructions for common operations.
This surface holds **canonical workflow definitions** — approved, durable declarations of how Cici operates.

Skills are operator-facing. Workflow surface artifacts are Cici-canonical.

## Related surfaces

- `memory-policy/` — memory hygiene intersects with workflow scheduling
- `tools/` — workflow steps often invoke specific tools
