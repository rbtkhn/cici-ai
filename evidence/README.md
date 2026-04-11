# Evidence

This directory holds raw or source-adjacent imports: captured thoughts, ingested context, and unprocessed inputs before normalization.

## What belongs here

- Raw MCP `capture` outputs staged for review
- Imported content from external sources (notes, documents, logs)
- Unvalidated context that has not yet been normalized or approved

## What does NOT belong here

- Approved durable state — that lives in `users/<instance>/governed-state/`
- Normalized, deduplicated context — that lives in `prepared-context/`

## Lifecycle

```
capture / import
       │
       ▼
   evidence/          ← you are here
       │
       ▼
prepared-context/     ← normalized, deduplicated, staged
       │
       ▼
governed-state/       ← approved durable truth (per-instance)
```

## Phase 1 note

In Phase 1, this directory is a structural placeholder. Most raw evidence currently flows directly into Supabase via the MCP `capture` tool. Future phases may route evidence through this directory for review before ingestion.

See `docs/governed-state-doctrine.md` for the full model.
