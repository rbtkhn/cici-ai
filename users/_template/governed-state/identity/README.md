# Identity Surface

**Status: stub** — Fill during Seed Phase initialization.

## What to create here

After copying the template and filling in `seed_intent.json`, create:

```
governed-state/identity/instance.json
```

Copy content from `seed_intent.json` (omit `_instructions`). Add `established_at` field with the date you initialized the instance.

This is the first canonical governed-state artifact for your instance.

## Required fields in instance.json

| Field | Description |
|---|---|
| `instance_id` | Must match your directory name |
| `instance_display_name` | Human-readable name |
| `owner` | Your name |
| `purpose` | One or two sentences |
| `established_at` | ISO 8601 timestamp |
| `governed_state_version` | Start with `"1.0"` |
| `capabilities` | List of MCP capabilities |
| `operational_bridges` | Supabase and other runtime bridges |
| `related_projects` | Linked repos and their relationships |

## Next steps

Once `instance.json` is created:
1. Update `surface-map.json` — change the `identity` surface status to `"active"`
2. Update `governed-state/README.md` — mark identity as active in the table
3. Update `seed-phase/status.json` — mark `governed-state-initialized` step complete
4. Run `python3 scripts/validate-governed-state.py`
