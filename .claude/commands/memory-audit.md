---
name: memory-audit
description: Run a memory hygiene audit. Generates a dossier, identifies promotion candidates across all governed-state stub surfaces, and recommends proposals or synthesis documents.
---

Run a memory hygiene audit for the Cici instance.

Follow `docs/skills/memory-hygiene-audit.md`.

## Step 1 — Generate dossier

```bash
python3 scripts/generate-dossier.py --instance cici
```

If the script fails or produces no output, read these files manually and summarize:
- `users/cici/governed-state/surface-map.json` (which surfaces are stubs vs active)
- `proposals/queue/` (open proposals)
- `evidence/` (what evidence exists)
- `prepared-context/synthesis/` (what synthesis exists)

## Step 2 — Identify gaps

For each surface with `status: "stub"` in `surface-map.json`, ask:
- Is there evidence in `evidence/` or synthesis in `prepared-context/` that could populate this surface?
- Has anyone tried to propose something for it before?

## Step 3 — Scan working docs for stale Tier C content

Search `docs/`, `prepared-context/pending-review/`, and `docs/companion-agent/brewmind-open-loops.md` for:
- Statements presented as facts that have no `[A]` or `[B]` tier annotation
- Claims about BrewMind (pricing, partnerships, launch dates) without a source reference
- Synthesis documents older than 60 days still in pending-review

Flag each one as a potential Tier C leak.

## Step 4 — Present audit report

Structure:

```
## Memory Audit Report — YYYY-MM-DD

### Surface Health
- active: [list]
- stub: [list]

### Pipeline Health
- Evidence items: N
- Synthesis documents: N
- Open proposals: N

### Promotion Candidates
- [Surface]: [brief description of available evidence]

### Tier C Leaks
- [File:line or section]: [what the stale claim is]

### Recommended next steps
1. ...
2. ...
```

## Step 5 — Wait for Xavier

Do not draft proposals or synthesis documents without Xavier's direction.
