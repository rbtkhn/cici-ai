# Prepared Context

This directory is the **staging layer** between raw evidence and approved governed state.

Content here is normalized, synthesized, and staged for review. It is **revisable and expiring** — not immutable like evidence, and not durable like governed state.

## Subdirectories

| Directory | Purpose | Retention |
|---|---|---|
| `synthesis/` | Synthesized summaries ready to become proposals | Until promoted or superseded |
| `pending-review/` | Staged for owner review before proposal creation | Until owner decides (max ~2 weeks) |
| `session/` | Session-scoped working context | Single session only — delete after use |
| `archived/` | Expired or superseded artifacts | Indefinite (low priority) |

## Lifecycle

```
evidence/             ← raw imports (immutable)
     │
     ▼
prepared-context/     ← you are here (revisable, expiring)
  ├── synthesis/       ← aggregated, ready to propose
  ├── pending-review/  ← waiting for owner eyes
  ├── session/         ← ephemeral session notes
  └── archived/        ← expired (don't delete, archive)
     │
     ▼  (generates proposal)
proposals/queue/      ← awaiting owner review
     │
     ▼  (on approval)
governed-state/       ← approved durable truth
```

## Time semantics

| Layer | Mutability | Retention |
|---|---|---|
| `evidence/` | Immutable | Long-lived |
| `prepared-context/` | Revisable | Days to weeks |
| `governed-state/` | Durable (owner-only changes) | Permanent |
| Supabase runtime | Mutable, noisy | Operational |

## Full doctrine

See `docs/prepared-context-doctrine.md` for the full doctrine including pipeline, subtypes, and promotion guidance.
