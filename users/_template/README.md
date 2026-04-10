# Instance Template

This is the template for creating a new Cici instance.

## How to initialize a new instance

1. Copy this directory to `users/<your-instance-id>/`
2. Fill in `seed_intent.json` with your instance details
3. Follow the Seed Phase walkthrough in `docs/seed-phase.md`
4. Run the readiness check: `python3 scripts/validate-governed-state.py`
5. Commit your initialized instance directory

## What to fill in

- `seed_intent.json` — instance identity, purpose, capabilities, operational bridges
- `governed-state/` — start empty; governed state accumulates through approved proposals

## Naming rules

- Instance IDs must be lowercase and hyphen-separated (e.g. `my-instance`)
- Do not rename after initialization — rename breaks historical references
- The instance ID in `seed_intent.json` must match the directory name

## Next steps after initialization

Once your `seed_intent.json` is in place and validated, proceed with the Supabase setup guide (`docs/setup-guide.md`) to connect your operational runtime.
