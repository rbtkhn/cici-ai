# Runtime Bridges Surface

**Status: stub** — No governed artifacts yet. Populated through approved proposals.

## Purpose

This surface holds canonical truth about Cici's operational bridge policies: how Supabase and other runtime connections are governed, what they're permitted to do, and how conflicts between them and governed state are resolved.

This is **operational policy**, not identity truth. The runtime bridges themselves (Supabase, MCP) live outside this repo — this surface governs how Cici *relates* to them.

## What belongs here (when ready)

- Bridge registration: which bridges are active, pending, or deprecated
- Permissions model: what each bridge may read/write vs. propose
- Sync policy: how and when to synchronize governed state with runtime state
- Back-propagation rules: whether approved governed changes should flow to the runtime
- Conflict resolution: what to do when a bridge and governed state diverge
- Deprecation plan: how to retire a bridge safely

## Current active bridges

| Bridge | Status | Docs |
|---|---|---|
| Supabase | active (primary runtime) | `bridges/supabase/README.md` |

Bridge status above reflects `users/cici/governed-state/identity/instance.json`. That remains canonical. This surface will hold the *policy* governing bridge behavior.

## How to populate

1. Draft bridge policy from current operational assumptions
2. Synthesize in `prepared-context/synthesis/`
3. Create a proposal in `proposals/queue/` with `target_surface: "runtime-bridges"`
4. On approval, add the policy here

## Related surfaces

- `identity/` — operational bridges are *listed* in identity; *governed* here
- `source-priority/` — bridge trust level is cross-referenced
- `tools/` — MCP tool policies live in tools; bridge policies live here
