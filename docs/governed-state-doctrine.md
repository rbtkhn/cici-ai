# Governed State Doctrine

**Version:** 1.0  
**Phase:** 1 (Foundation)  
**Status:** Active

---

## The Rule

Git-managed files are the canonical source of truth for durable state in this system.

Operational databases, hosted services, and runtime caches are derivative. They accelerate access and enable features, but they do not own the truth.

---

## Three Layers

| Layer | Purpose | Location |
|---|---|---|
| **Evidence** | Raw imports, captured thoughts, unprocessed inputs | `evidence/` |
| **Prepared Context** | Normalized, deduplicated, staged context ready for review | `prepared-context/` |
| **Governed State** | Approved durable truth | `users/<instance>/governed-state/` |

Evidence and prepared context may be ephemeral or cached. Governed state is durable.

---

## How Durable State Changes

Material changes to governed state must go through a proposal.

1. A proposal artifact is created in `proposals/queue/`
2. The instance owner reviews it
3. On approval, the change is applied and the proposal moves to `proposals/approved/`
4. Rejected proposals move to `proposals/rejected/` with a decision note

Agents and automations may create proposals. Only the owner approves them.

Small, obvious corrections do not need formal proposals — direct edits by the owner are valid.

---

## Supabase

Supabase is a supported operational bridge. It provides:

- Vector search and semantic indexing over memories
- Edge Function compute for the MCP server
- Real-time access from AI clients (Claude, ChatGPT, Cursor, Gemini)
- Credentials management and dashboard visibility

**Supabase is not canonical.** If Supabase data diverges from governed state, governed state wins.

During Phase 1, Supabase remains the primary runtime. The governed-state layer is additive — it does not replace or disable Supabase.

---

## Authority

Four classes of write authority exist in this system:

| Class | Who | Where |
|---|---|---|
| **Canonical** | Instance owner | `users/<instance>/governed-state/`, `config/`, `docs/` |
| **Proposal** | Agents, automations | `proposals/queue/` only |
| **Operational** | Runtime services (Supabase, MCP) | Supabase database (external) |
| **Ephemeral** | Any process | In-memory / gitignored temp files |

See `config/authority-map.json` for the full authority model.

---

## What This Is Not

- This is not a fully local-first system yet — Phase 1 is the foundation
- Supabase is not being removed
- Every thought capture does not require a formal proposal
- This is not bureaucracy — it is legibility

---

## Phase 1 Scope

Phase 1 establishes the structural foundation:

- File-based governed state scaffold
- Proposal review queue
- Authority model
- Seed Phase initialization pattern
- Lightweight CI validation

Phase 2 and beyond will expand local-first defaults, improve sync, and may reduce Supabase dependency for core operations.
