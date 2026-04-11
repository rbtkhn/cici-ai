# Seed Phase

The Seed Phase is the initialization stage for a new Cici instance. It establishes the basic governed state before any real data flows in.

## Purpose

A new instance begins with intent. The Seed Phase makes that intent explicit and governed: who owns this instance, what it's for, and what capabilities it should have. This record becomes the foundation against which all future governed-state changes are evaluated.

## What the Seed Phase produces

| Artifact | Location | Description |
|---|---|---|
| `seed_intent.json` | `users/<instance>/seed_intent.json` | Instance identity, purpose, capabilities, operational bridges |
| `governed-state/instance.json` | `users/<instance>/governed-state/instance.json` | Canonical instance record (approved durable state) |
| Validated structure | CI check | `scripts/validate-governed-state.py` confirms all required artifacts exist and are well-formed |

## Steps to initialize a new instance

### 1. Copy the template

```bash
cp -r users/_template users/<your-instance-id>
```

### 2. Fill in seed_intent.json

Open `users/<your-instance-id>/seed_intent.json` and replace all `<placeholder>` values:

| Field | Description |
|---|---|
| `instance_id` | Lowercase, hyphen-separated ID (must match directory name) |
| `instance_display_name` | Human-readable name |
| `owner` | Your name |
| `created_at` | ISO 8601 timestamp |
| `purpose` | One or two sentences describing what this instance is for |
| `seed_phase_status` | Set to `active` when ready |
| `capabilities` | List the MCP/system capabilities you intend to enable |
| `operational_bridges` | List Supabase or other runtime bridges you'll connect |

Remove the `_instructions` field before committing.

### 3. Create governed-state/instance.json

Copy `seed_intent.json` content into `governed-state/instance.json`, omitting `_instructions`. This is the first piece of approved governed state.

### 4. Run the readiness check

```bash
python3 scripts/validate-governed-state.py
```

Fix any errors before proceeding.

### 5. Commit

```bash
git add users/<your-instance-id>/
git commit -m "seed: initialize <your-instance-id> instance"
```

### 6. Connect the operational runtime

Follow `docs/setup-guide.md` to configure Supabase and deploy the MCP server.

## What seed_phase_status means

| Value | Meaning |
|---|---|
| `pending` | Template not yet filled in |
| `active` | Instance is initialized and operational |
| `archived` | Instance is no longer active |

## Existing instances

This repo's active instance is `users/cici/` — Xavier's personal instance. It was initialized as part of Phase 1 (2026-04-10).

New forks of this repo should create their own instance directory rather than modifying `users/cici/`.
