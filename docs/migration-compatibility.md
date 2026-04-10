# Migration Compatibility Notes

## Phase 1 — Git-First Governed State (additive)

**Date:** 2026-04-10  
**Type:** Additive — no breaking changes

---

## What changed in Phase 1

Phase 1 added a file-based governed-state layer on top of the existing Supabase-backed system. It did not remove or modify any existing functionality.

### Files added

| Path | Purpose |
|---|---|
| `evidence/` | Structural placeholder for raw evidence imports |
| `prepared-context/` | Structural placeholder for normalized staged context |
| `users/cici/` | Cici instance governed state |
| `users/_template/` | Template for new instances |
| `proposals/` | Proposal review queue and schema |
| `config/authority-map.json` | Authority model |
| `bridges/supabase/` | Supabase bridge documentation |
| `docs/governed-state-doctrine.md` | Architectural doctrine |
| `docs/seed-phase.md` | Instance initialization walkthrough |
| `scripts/validate-governed-state.py` | CI validation script |
| `.github/workflows/validate-governed-state.yml` | GitHub Actions CI check |

### Files modified

| Path | Change |
|---|---|
| `README.md` | Added governed-state model overview and new directory listing |
| `CLAUDE.md` | Added reference to new Phase 1 structure |

---

## Compatibility guarantees

### Existing Supabase users

If you already have Cici set up with a working Supabase project and MCP connection:

- **Nothing broke.** All Supabase configuration, SQL schemas, Edge Functions, and AI client connections work exactly as before.
- The new `users/cici/governed-state/` files are additive. They document and govern state that Supabase operationalizes; they do not change how Supabase runs.
- The setup guide (`docs/setup-guide.md`) is unchanged.

### Forks and new instances

If you forked this repo before Phase 1:

- Pull the Phase 1 changes into your fork.
- Copy `users/_template/` to `users/<your-instance-id>/` and fill in your instance details.
- Run `python3 scripts/validate-governed-state.py` to confirm your fork is valid.
- You do not need to rename `users/cici/` — just add your own instance directory alongside it, or replace it if you prefer a clean fork.

---

## What has NOT changed

- Supabase is still the primary runtime
- MCP tools (`capture`, `search`, `recent_thoughts`, `stats`) work unchanged
- Key rotation procedures are unchanged
- Setup guide SQL schema is unchanged
- No server-side code was modified (server lives upstream in NateBJones-Projects/OB1)

---

## Future phases (not yet implemented)

Later phases may:

- Introduce local-first sync so Supabase becomes a secondary mirror
- Route evidence through `evidence/` before Supabase ingestion
- Require prepared-context normalization as an explicit step
- Expand proposal automation (agent-generated proposals from capture events)

None of this is committed yet. Phase 2 details will be described in a future migration note when implemented.

**There are no breaking changes planned for Phase 2 that would affect the existing Supabase runtime.**
