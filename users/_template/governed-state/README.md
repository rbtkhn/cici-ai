# Governed State

This directory holds the approved durable truth for this instance.

It starts empty. Governed state accumulates over time through approved proposals.

## What belongs here

- Instance identity and profile records
- Approved schemas, tag definitions, capture habits
- Any durable configuration that has been explicitly approved by the instance owner

## What does NOT belong here

- Unapproved proposals — those live in `proposals/queue/`
- Raw evidence — that lives in `evidence/`
- Operational or cache data — that lives in Supabase (the operational bridge)

## How state enters here

1. A proposal is created in `proposals/queue/`
2. The owner reviews and approves it
3. The approved change is applied to this directory
4. The proposal moves to `proposals/approved/`

Direct edits by the owner are also valid (for small, obvious changes that don't warrant a formal proposal).

See `proposals/README.md` for the full proposal lifecycle.
