# Skill: Promote to Governed State

**Purpose:** Apply an approved proposal change to the correct governed-state surface.

This is the final step before runtime back-propagation (optional).

---

## When to Use This

After the owner has decided to approve a proposal in `proposals/queue/`.

---

## Steps

### 1. Identify the target

Read the approved proposal:
- `target_surface` — which surface directory to write to
- `change_type` — what kind of change: `add`, `update`, `remove`, `restructure`, `policy`
- `summary` and `rationale` — understand what the change is and why

Find the target path: `users/cici/governed-state/<target_surface>/`

### 2. Apply the change

#### If change_type = "add"
Create the new file at the appropriate path:

```bash
# Example: adding capture-habits.json to memory-policy surface
users/cici/governed-state/memory-policy/capture-habits.json
```

The content comes from the synthesis document in `evidence_refs` (usually in `prepared-context/synthesis/`).

#### If change_type = "update"
Edit the existing file. Note what changed in your commit message.

#### If change_type = "remove"
Delete the file. This is rare — ensure the proposal rationale is strong before removing canonical artifacts.

#### If change_type = "restructure"
Multiple files may move. Document the full diff in `decision_notes`.

#### If change_type = "policy"
Create or update a policy document (usually `.md` format) in the target surface.

### 3. Update the proposal file

Move from `proposals/queue/` to `proposals/approved/` and update:

```json
{
  "status": "approved",
  "reviewer": "Xavier",
  "decided_at": "2026-04-11T14:00:00Z",
  "decision_notes": "Applied. Created memory-policy/capture-habits.json (42 lines). No conflicts."
}
```

### 4. Update surface-map.json (if needed)

If this is the first artifact in a stub surface, update `surface-map.json` to change the surface `status` from `stub` to `active`:

```json
{
  "id": "memory-policy",
  "status": "active",
  ...
}
```

Also update `users/cici/governed-state/README.md` table accordingly.

### 5. Append to event log

Add an entry to `proposals/events/event-log.json`:

```json
{
  "event_id": "evt-20260411-001",
  "timestamp": "2026-04-11T14:00:00Z",
  "proposal_id": "prop-20260411-001-add-capture-habits",
  "action": "approved",
  "reviewer": "Xavier",
  "target_surface": "memory-policy",
  "notes": "Applied. Created memory-policy/capture-habits.json."
}
```

### 6. Commit

Stage all changed files together:

```bash
git add users/cici/governed-state/
git add proposals/approved/prop-YYYYMMDD-NNN-slug.json
git add proposals/events/event-log.json
git commit -m "governed: apply prop-YYYYMMDD-NNN to <surface> — <short description>"
```

Commit message convention: `governed: apply <proposal-id> to <surface> — <what changed>`

---

## Optional: Runtime Back-Propagation

After promotion, consider whether the new governed truth should be reflected in Supabase:

- New tag taxonomy → apply tags to existing memories via SQL update
- Updated capture policy → no Supabase change needed (policy governs future behavior)
- Updated identity → no Supabase change needed (Supabase doesn't store identity)
- New bridge rules → may require Supabase function redeploy

Back-propagation is manual in Phase 1. See `docs/promotion-doctrine.md` for guidance.

---

## Related Skills

- `review-governed-change.md` — The decision step before this one
- `docs/change-review-lifecycle.md` — Full lifecycle reference
- `docs/promotion-doctrine.md` — Why promotion matters
