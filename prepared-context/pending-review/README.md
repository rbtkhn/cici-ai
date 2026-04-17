# Prepared Context — Pending Review

This directory holds **context staged for owner review** before a proposal is formally created.

## Purpose

Not every synthesis artifact is immediately ready to be a proposal. Sometimes:
- An agent has extracted and synthesized something that needs owner eyes first
- Multiple related items should be reviewed together before separate proposals
- Something is close but needs clarification before being committed to a proposal

Place those artifacts here.

## How it works

1. Agent or extraction script places a draft artifact here
2. Owner reviews the artifact in the next available session
3. Owner either:
   - **Promotes**: moves artifact to `../synthesis/` and uses it to draft a formal proposal
   - **Discards**: moves to `../archived/` with a note, or deletes if clearly not useful
   - **Requests more info**: annotates the artifact and leaves it here for another pass

## Naming convention

```
<YYYYMMDD>-review-<short-slug>.[md|json]
```

Example: `20260411-review-capture-habit-patterns.md`

## Retention

Until the owner reviews and decides. Do not let `pending-review/` accumulate unreviewed items for more than ~2 weeks — stale items should be archived or discarded.

See `docs/prepared-context-doctrine.md` for the full doctrine.
