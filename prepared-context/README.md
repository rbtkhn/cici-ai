# Prepared Context

This directory holds normalized, deduplicated, and staged context — evidence that has been processed and is ready for review before being approved into governed state.

## What belongs here

- Normalized imports (cleaned, deduplicated, fingerprinted)
- Staged context awaiting owner review or proposal generation
- Transformation artifacts from evidence → governed-state pipelines

## What does NOT belong here

- Raw unprocessed evidence — that belongs in `evidence/`
- Approved durable state — that belongs in `users/<instance>/governed-state/`

## Lifecycle

```
evidence/             ← raw imports
     │
     ▼
prepared-context/     ← you are here (normalized, staged)
     │
     ▼  (generates proposal)
proposals/queue/      ← awaiting owner review
     │
     ▼  (on approval)
governed-state/       ← approved durable truth
```

## Phase 1 note

In Phase 1, this directory is a structural placeholder. Normalization and deduplication currently occur inside the Supabase `upsert_thought()` function at the database layer. Future phases may introduce explicit prepared-context artifacts as an intermediate step.

See `docs/governed-state-doctrine.md` for the full model.
