# Cici — Xavier's Instance

This directory holds the governed state for Cici, Xavier's personal Open Brain instance.

## Identity

- **Instance ID:** `cici`
- **Owner:** Xavier
- **Purpose:** Persistent cross-AI knowledge base for BrewMind and personal thinking
- **Operational runtime:** Supabase (primary, Phase 1)

## Structure

```
users/cici/
├── README.md               ← this file
├── seed_intent.json        ← instance initialization record
└── governed-state/         ← approved durable truth
    ├── README.md
    └── instance.json       ← canonical instance record
```

## Related docs

- Architecture: `README.md` (root)
- Doctrine: `docs/governed-state-doctrine.md`
- Seed Phase: `docs/seed-phase.md`
- Supabase setup: `docs/setup-guide.md`
- BrewMind integration: `docs/brewmind.md`
- Personal workflow: `docs/personal/README.md`

## Proposing changes to governed state

To propose a change to anything in `governed-state/`, create a proposal in `proposals/queue/`. See `proposals/README.md` for instructions.

Direct edits are valid for small, obvious changes that don't require a formal record.
