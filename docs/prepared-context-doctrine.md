# Prepared-Context Doctrine

**Version:** 1.0
**Phase:** 2 (formalized; Phase 1 used Supabase directly)

---

## The Role of Prepared Context

Prepared context is the **staging layer** between raw evidence and approved governed state.

It is where:
- Evidence is normalized and deduplicated
- Multiple captures are synthesized into coherent summaries
- Draft artifacts are assembled before formal proposal
- Session-scoped context is made available to operators without becoming permanent

Prepared context is **revisable and expiring** — it is not immutable like evidence, and not durable like governed state.

---

## Time Semantics

| Layer | Mutability | Retention | Owner |
|---|---|---|---|
| `evidence/` | **Immutable** once written | Long-lived (archive, don't delete) | Canonical |
| `prepared-context/` | **Revisable** and expiring | Medium-lived (days to weeks) | Operational |
| `proposals/queue/` | Immutable once submitted | Until decided | Proposal |
| `users/<id>/governed-state/` | **Durable** (owner-approved changes only) | Permanent | Canonical |
| Supabase runtime memory | Mutable, noisy | Operational lifespan | Operational |
| In-session context | Ephemeral | Single session | Ephemeral |

The key rule: **prepared context is not truth**. It is a working surface. If it expires without being promoted, that is fine — raw evidence still exists in `evidence/` or Supabase.

---

## Subtypes

Prepared context is organized into four subdirectories by function:

### synthesis/

Synthesized context documents produced by aggregating multiple evidence items or runtime memories.

Examples:
- A summary of 30 days of BrewMind captures, synthesized into 5 key themes
- A candidate `capture-habits.md` document drafted from observed patterns
- A cross-AI-client consistency review

Synthesis artifacts are typically the **direct input to a proposal**. When a synthesis document is good enough to propose, it becomes a proposal body or evidence ref.

**Retention:** Until promoted to a proposal or superseded by a newer synthesis.

### session/

Session-scoped context: prepared for a single operator session and not intended to persist.

Examples:
- A working summary of what's in-progress
- A quick list of open proposals and their status
- A pre-session readiness check output

Session artifacts should be **deleted or archived after the session** that created them. Do not let session/ accumulate.

**Retention:** Single session only. Delete after use.

### pending-review/

Context staged for owner review before a proposal is formally created.

Use this when:
- An agent has synthesized something worth proposing but wants owner eyes before formalizing
- Evidence has been extracted from runtime and is ready to review
- Multiple synthesis items should be reviewed together before separate proposals are written

**Retention:** Until the owner reviews and either promotes to a proposal or discards.

### archived/

Expired or superseded prepared-context artifacts that are no longer active but are kept for reference.

Do not delete prepared-context artifacts — move them here instead. This preserves the paper trail without cluttering active subdirectories.

**Retention:** Indefinite (but low priority for review).

---

## Pipeline

```
Supabase runtime memory  ──┐
evidence/                   ├──► scripts/extract-evidence.py
                            │         │
                            ▼         ▼
                  prepared-context/synthesis/
                  prepared-context/pending-review/
                            │
                            ▼  (owner reviews)
                  proposals/queue/
                            │
                            ▼  (owner approves)
                  users/cici/governed-state/<surface>/
```

See `docs/promotion-doctrine.md` for the full pipeline with trigger conditions.

---

## What Does NOT Belong in Prepared Context

- **Raw unprocessed evidence** → `evidence/`
- **Approved durable state** → `users/<id>/governed-state/<surface>/`
- **Pending proposals** → `proposals/queue/`
- **Secrets or credentials** → Supabase secrets / `.env` (gitignored)

---

## Lifecycle of a Prepared-Context Artifact

1. **Created** by extraction script, agent synthesis, or manual curation
2. **Placed** in the appropriate subtype directory
3. **Reviewed** by operator (may be revised multiple times)
4. **Promoted** to a proposal (moves to `proposals/queue/`) — or **archived** (`archived/`)
5. **Referenced** in proposal `evidence_refs` field
6. **Superseded** — original moves to `archived/`, new version takes its place

---

## Phase 1 Note

In Phase 1, this entire layer was handled by Supabase's `upsert_thought()` deduplication. Evidence flowed directly into runtime memory.

The prepared-context layer is now formally declared as a Phase 2 staging surface. It does not replace Supabase — it adds a Git-native review step for high-signal content that deserves promotion to governed state.

---

## Related Docs

- `docs/governed-state-doctrine.md` — Three-layer model
- `docs/promotion-doctrine.md` — Full promotion pipeline
- `docs/change-review-lifecycle.md` — What happens after a proposal is created
- `evidence/README.md` — The layer below prepared context
