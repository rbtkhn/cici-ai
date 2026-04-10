# Governed State — Cici

This is the canonical, durable truth for the Cici instance.

## Contents

| File | Description |
|---|---|
| `instance.json` | Core instance record: identity, purpose, capabilities, operational bridges |

More governed-state surfaces will be added over time through approved proposals.

## How to change governed state

For material changes, create a proposal in `proposals/queue/`. See `proposals/README.md`.

For small, obvious corrections (typos, factual updates you're confident about), direct edits are fine.

## What "canonical" means

If Supabase data disagrees with these files, these files win. Supabase is the operational runtime; this directory is the source of truth.
