# Governed State Doctrine

**Version:** 2.0
**Phase:** 2 (Formation + Review)
**Status:** Active

---

## The Rule

Git-managed files are the canonical source of truth for durable state in this system.

Operational databases, hosted services, and runtime caches are derivative. They accelerate access and enable features, but they do not own the truth.

---

## Four Layers

| Layer | Purpose | Location | Mutability |
|---|---|---|---|
| **Evidence** | Raw imports, captured thoughts, unprocessed inputs | `evidence/` | Immutable once written |
| **Prepared Context** | Normalized, staged context ready for review | `prepared-context/` | Revisable, expiring |
| **Governed State** | Approved durable truth, split into surfaces | `users/<instance>/governed-state/<surface>/` | Durable (owner-approved changes only) |
| **Runtime** | Operational memory: Supabase, MCP, in-session | Supabase (external) | Mutable, noisy, non-canonical |

---

## Governed-State Surfaces

Governed state is split into named domains. Each surface holds a specific category of canonical truth:

| Surface | Contents |
|---|---|
| `identity/` | Instance record: id, owner, purpose, capabilities, bridges |
| `voice/` | Communication style, tone, persona notes |
| `memory-policy/` | Capture rules, retention thresholds, deduplication |
| `workflows/` | Recurring operator flows, maintenance rituals |
| `tools/` | MCP tool configs, AI gateway preferences |
| `source-priority/` | Source trust levels, conflict resolution rules |
| `runtime-bridges/` | Supabase bridge policy, sync rules |

The full surface registry is in `users/<instance>/governed-state/surface-map.json`.

---

## How Durable State Changes

Material changes to governed state must go through a proposal.

1. A proposal artifact is created in `proposals/queue/`
2. The instance owner reviews it
3. On approval, the change is applied and the proposal moves to `proposals/approved/`
4. The decision is recorded in `proposals/events/event-log.json`
5. Rejected proposals move to `proposals/rejected/` with a decision note

Agents and automations may create proposals. Only the owner approves them.

Small, obvious corrections do not need formal proposals — direct edits by the owner are valid.

See `docs/change-review-lifecycle.md` for the full lifecycle including conflict resolution and diff policy.

---

## The Promotion Pipeline

Runtime memory can become governed truth through a formal pipeline:

```
Supabase runtime  →  evidence/  →  prepared-context/synthesis/  →  proposals/queue/  →  governed-state/
```

See `docs/promotion-doctrine.md` for trigger conditions, extraction scripts, and back-propagation notes.

---

## Supabase

Supabase is a supported operational bridge. It provides:

- Vector search and semantic indexing over memories
- Edge Function compute for the MCP server
- Real-time access from AI clients (Claude, ChatGPT, Cursor, Gemini)
- Credentials management and dashboard visibility

**Supabase is not canonical.** If Supabase data diverges from governed state, governed state wins.

Supabase is the primary runtime. The governed-state layer is additive — it does not replace Supabase.

---

## Authority

Five classes of write authority exist in this system:

| Class | Who | Where |
|---|---|---|
| **Canonical** | Instance owner | `users/<instance>/governed-state/<surface>/`, `config/`, `docs/` |
| **Proposal** | Agents, automations | `proposals/queue/` only |
| **Staging** | Agents, scripts, operator | `evidence/`, `prepared-context/` |
| **Operational** | Runtime services (Supabase, MCP) | Supabase database (external) |
| **Ephemeral** | Any process | In-memory / gitignored temp files |

See `config/authority-map.json` for the full authority model.

---

## What This Is Not

- This is not a fully local-first system — Supabase remains the operational runtime
- Every thought capture does not require a formal proposal
- Supabase is not being removed
- This is not bureaucracy — it is legibility

---

## Phase 1 → Phase 2 Progress

**Phase 1** established:
- File-based governed state scaffold
- Proposal review queue
- Authority model
- Seed Phase initialization pattern
- Lightweight CI validation

**Phase 2** adds:
- Governed-state surface split (7 named domains)
- Formal Seed Phase readiness model with artifact tracking
- Full change-review lifecycle (conflict resolution, event log, diff policy)
- Prepared-context doctrine with typed subtypes (synthesis, session, pending-review, archived)
- Runtime-memory → governed-truth promotion pipeline
- Dossier generation and pipeline health checks
- Portable operator skills and Cursor rules
- Template–instance contract and upgrade guidance

Phase 3 and beyond will expand local-first defaults, automate back-propagation, and may reduce Supabase dependency for core operations.
