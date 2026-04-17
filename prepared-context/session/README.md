# Prepared Context — Session

This directory holds **session-scoped context**: artifacts prepared for a single operator session that are not intended to persist.

## Purpose

Session artifacts are working notes, pre-flight summaries, and in-session checklists. They help operators orient quickly without polluting synthesis or governed state with transient content.

## What belongs here

- Pre-session readiness check outputs
- Working summaries of open proposals
- In-session operator notes
- Quick status snapshots (what's in queue, what's in synthesis)
- Temporary diffs or comparisons

## Lifecycle

**Create → use → delete (or archive).**

Do not let `session/` accumulate. After a session:
1. Delete artifacts that served their purpose
2. If an artifact contains something worth keeping, move it to `../synthesis/` or `../pending-review/`
3. Never promote a session artifact directly to a proposal without synthesis review

## Naming convention

```
<YYYYMMDD>-session-<short-slug>.md
```

Example: `20260411-session-open-proposals-status.md`

See `docs/prepared-context-doctrine.md` for the full doctrine.
