# Proposals

A proposal is a formal artifact requesting a material change to governed state.

Agents and automations may create proposals. Only the instance owner approves them.

## Lifecycle

```
proposed → under_review → approved   → applied to governed-state/
                       └→ rejected   → archived with decision notes
                       └→ deferred   → archived, may be revisited
                       └→ superseded → replaced by a newer proposal
```

For the full lifecycle — state transitions, conflict resolution, diff generation, and event log format — see `docs/change-review-lifecycle.md`.

## Directories

| Directory | Contents |
|---|---|
| `queue/` | Proposals awaiting review (status: `proposed` or `under_review`) |
| `approved/` | Approved proposals (status: `approved`) |
| `rejected/` | Rejected, deferred, or superseded proposals |
| `events/` | Append-only event log of all decisions |
| `examples/` | Illustrative example proposals (not real — for reference only) |
| `schemas/` | JSON schema for proposal files |

## Creating a proposal

1. Create a new JSON file in `proposals/queue/`
2. Name it: `prop-YYYYMMDD-NNN-short-description.json`
   - Example: `prop-20260410-001-add-brewmind-tag-schema.json`
3. Fill in all required fields from `schemas/proposal.schema.json`
4. Set `status` to `proposed`
5. Commit and push — the CI check will validate the format

## Reviewing a proposal

1. Read the proposal file in `proposals/queue/`
2. If approving:
   - Apply the described change to the relevant `governed-state/` surface
   - Move the proposal file to `proposals/approved/`
   - Set `status` to `approved`, fill in `reviewer` and `decision_notes`, add `decided_at`
3. If rejecting:
   - Move the proposal file to `proposals/rejected/`
   - Set `status` to `rejected`, fill in `reviewer` and `decision_notes`, add `decided_at`

## Required fields

See `schemas/proposal.schema.json` for the full schema.

Minimum required: `id`, `created_at`, `status`, `change_type`, `target_surface`, `summary`, `rationale`, `proposer`

## What counts as "material"

A change is material if it:
- Alters the canonical identity, purpose, or capabilities of the instance
- Changes a schema, policy, or convention that other parts of the system depend on
- Could not easily be reversed without a formal record

Small corrections (typos, formatting) do not need proposals — direct edits are fine.
