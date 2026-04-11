# Prepared Context — Synthesis

This directory holds **synthesized context documents**: aggregated, structured summaries produced from multiple evidence items or runtime memories.

## Purpose

Synthesis artifacts are the primary input to formal proposals. When you observe a pattern in captures, extract a theme across many memories, or want to propose a new governed-state artifact, a synthesis document is where you draft it.

## Lifecycle

```
evidence/ + Supabase runtime
         │
         ▼  (scripts/extract-evidence.py or manual)
synthesis/<draft-name>.md or .json
         │
         ▼  (owner reviews, iterates)
proposals/queue/prop-YYYYMMDD-NNN.json  ← synthesis becomes proposal body or evidence_ref
```

## Naming convention

```
<YYYYMMDD>-<short-slug>.[md|json]
```

Examples:
- `20260411-brewmind-capture-themes.md`
- `20260415-memory-policy-draft.json`
- `20260420-voice-calibration-notes.md`

## Retention

Keep until promoted to a proposal or superseded by a newer synthesis.
Move superseded artifacts to `../archived/` rather than deleting.

See `docs/prepared-context-doctrine.md` for the full doctrine.
