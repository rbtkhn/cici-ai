# Users

Each subdirectory here represents one instance of this system — one person's governed state.

## Structure

```
users/
├── _template/          ← template for creating a new instance
└── cici/               ← Xavier's personal instance (this repo's active instance)
    ├── README.md
    ├── seed_intent.json
    └── governed-state/
```

## Template

To create a new instance, copy `_template/` to `users/<your-instance-id>/` and fill in `seed_intent.json`.

See `docs/seed-phase.md` for the full initialization walkthrough.

## Governed state

Each instance's `governed-state/` subdirectory is the canonical, durable truth for that instance. Changes to governed state must go through the proposal review process described in `proposals/README.md`.

## Instance naming

Instance IDs should be lowercase, hyphen-separated, and stable. Do not rename an instance directory after initialization — rename would break historical references.
