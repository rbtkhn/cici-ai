# Memory Policy Surface

**Status: stub** — No governed artifacts yet. Populated through approved proposals.

## Purpose

This surface holds canonical truth about how Cici manages its memory: what to capture, what to retain, when to archive, and how to deduplicate.

## What belongs here (when ready)

- Capture policy: what categories of thought are worth capturing
- Retention thresholds: how long memories stay active before archiving
- Deduplication rules: when to merge vs. keep separate memories
- Hygiene schedule: how often to review and prune low-signal memories
- Tag taxonomy: canonical tag vocabulary and hierarchy
- Source weighting: how to handle conflicts between captures from different AI clients

## How to populate

1. Capture evidence of actual capture patterns from runtime (e.g., Supabase memory export)
2. Synthesize in `prepared-context/synthesis/`
3. Create a proposal in `proposals/queue/` with `target_surface: "memory-policy"`
4. On approval, add the artifact here

## Related surfaces

- `source-priority/` — how to weight sources when they conflict
- `workflows/` — recurring hygiene and maintenance flows
- `runtime-bridges/` — Supabase-specific memory policy implementation details
