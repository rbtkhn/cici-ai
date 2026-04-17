# Change-Review Lifecycle

**Version:** 1.0
**Applies to:** All governed-state proposals in this instance

---

## Overview

Every material change to governed state in Cici follows a formal proposal lifecycle. This document defines every state, transition, and handling rule.

---

## State Machine

```
                        ┌─────────────┐
                        │   proposed   │  ← agents/automations write to proposals/queue/
                        └──────┬───────┘
                               │  owner picks up for review
                               ▼
                        ┌─────────────┐
                        │ under_review │  ← owner is actively evaluating
                        └──────┬───────┘
                               │
               ┌───────────────┼────────────────┐
               │               │                │
               ▼               ▼                ▼
         ┌──────────┐   ┌──────────┐   ┌─────────────┐
         │ approved │   │ rejected │   │  deferred   │
         └────┬─────┘   └────┬─────┘   └──────┬──────┘
              │              │                 │
              ▼              ▼                 └──► back to queue
    applied to          proposals/                 (later review)
    governed-state/     rejected/
              │
              ▼
       proposals/approved/
```

Additionally, any proposal in any state may be marked:

```
superseded  ←  replaced by a newer, better-scoped proposal
```

Superseded proposals move to `proposals/rejected/` with a `decision_notes` field indicating the superseding proposal ID.

---

## States

| State | Directory | Meaning |
|---|---|---|
| `proposed` | `proposals/queue/` | Written by agent or automation. Awaiting owner attention. |
| `under_review` | `proposals/queue/` | Owner is actively reading and evaluating. |
| `approved` | `proposals/approved/` | Owner approved. Change has been applied to governed state. |
| `rejected` | `proposals/rejected/` | Owner rejected. Change will not be applied. |
| `deferred` | `proposals/rejected/` | Not ready yet. May be revisited. Kept for reference. |
| `superseded` | `proposals/rejected/` | Replaced by a newer proposal. Retained for history. |

---

## Transitions

### proposed → under_review
- Owner opens the proposal file in `proposals/queue/`
- Updates `status` to `under_review`
- No other changes required at this stage

### under_review → approved
1. Owner applies the described change to the relevant `governed-state/<surface>/` path
2. Moves the proposal file to `proposals/approved/`
3. Sets `status: approved`
4. Fills in `reviewer`, `decided_at`, and `decision_notes`
5. Records the event in `proposals/events/event-log.json`

### under_review → rejected
1. Owner does not apply the change
2. Moves the proposal file to `proposals/rejected/`
3. Sets `status: rejected`
4. Fills in `reviewer`, `decided_at`, and `decision_notes` (required: explain why)
5. Records the event in `proposals/events/event-log.json`

### under_review → deferred
1. Owner is not ready to decide
2. Moves the proposal file to `proposals/rejected/` (deferred proposals archive there)
3. Sets `status: deferred`
4. Fills in `reviewer`, `decided_at`, and `decision_notes` (required: what needs to change before revisiting)

### any → superseded
1. A newer proposal covers the same scope
2. Older proposal moves to `proposals/rejected/`
3. Sets `status: superseded`
4. `decision_notes` must reference the superseding proposal ID

---

## Conflict Resolution Policy

When two proposals target the same `target_surface` and conflict:

1. **Last-writer rule**: The most recently submitted proposal supersedes older ones targeting the same surface/path. Older proposals are marked `superseded`.
2. **Owner override**: The owner may choose to merge intent from multiple proposals into a single outcome. In that case, both originals are marked `superseded` and a new proposal is created describing the merged change.
3. **Scope splitting**: If two proposals target different files within the same surface, they can both proceed independently.

---

## Diff Generation

When applying an approved proposal to governed state, generate a minimal diff:

1. **Before**: Note the current state of the target file(s) (or "does not exist")
2. **After**: Apply the change
3. **Record**: The `decision_notes` field in the approved proposal should reference what changed

For major structural changes, a human-readable diff may be appended to `decision_notes`:

```
decision_notes: "Applied. Added capture-habits.json to memory-policy surface. 
Diff: +1 file (48 lines). No existing artifacts modified."
```

---

## Event Log

Every approval or rejection SHOULD be recorded in `proposals/events/event-log.json`.

Event log format (append only):

```json
{
  "events": [
    {
      "event_id": "evt-20260410-001",
      "timestamp": "2026-04-10T14:00:00Z",
      "proposal_id": "prop-20260410-001-add-brewmind-tag-schema",
      "action": "approved",
      "reviewer": "Xavier",
      "target_surface": "memory-policy",
      "notes": "Applied tag schema to memory-policy surface."
    }
  ]
}
```

The event log provides a lightweight audit trail without requiring inspection of individual proposal files.

---

## What Counts as Material

A change is material if it:
- Alters the canonical identity, purpose, or capabilities of the instance
- Changes a schema, policy, or convention that other parts of the system depend on
- Could not easily be reversed without a formal record
- Affects the trust model, source priorities, or bridge policies

Small corrections (typos, formatting, factual updates the owner is confident about) do **not** need proposals. Direct owner edits are valid.

---

## Proposal Quality Bar

Before marking a proposal `under_review`, the owner should verify:

- [ ] All required fields are present (validated by CI)
- [ ] `target_surface` names a real surface in `governed-state/surface-map.json`
- [ ] `rationale` explains *why* this change matters, not just what it does
- [ ] `evidence_refs` are provided where applicable
- [ ] `confidence` is set (0.0–1.0) to indicate proposer certainty

Proposals that fail these checks should be `rejected` with a note to resubmit with corrections.

---

## Related Docs

- `proposals/README.md` — How to create a proposal
- `proposals/schemas/proposal.schema.json` — Formal schema
- `docs/governed-state-doctrine.md` — Why this system exists
- `docs/promotion-doctrine.md` — How runtime memories become proposals
