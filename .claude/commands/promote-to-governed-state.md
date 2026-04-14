---
name: promote-to-governed-state
description: Apply an approved proposal to the correct governed-state surface. Only run this after Xavier has explicitly approved the proposal. Pass proposal id as argument.
argument-hint: <proposal-id>
---

Apply approved proposal: $ARGUMENTS

Follow `docs/skills/promote-to-governed-state.md` exactly.

## Pre-flight checks

1. Read `proposals/queue/$ARGUMENTS.json`.
2. Confirm `status` is `"proposed"` (not already approved or rejected).
3. Read `users/cici/governed-state/surface-map.json` — confirm `target_surface` is valid.

## Apply the change

Based on `change_type`:

- **add**: Create the new file at `users/cici/governed-state/<target_surface>/`. Content comes from `evidence_refs` synthesis documents.
- **update**: Edit the existing file. Note what changed.
- **remove**: Delete the file (rare). Confirm with Xavier before deleting.
- **restructure**: Multiple moves. Document full diff in `decision_notes`.
- **policy**: Create/update a `.md` policy document in the target surface.

## Update surface-map.json

If this is the first artifact in a stub surface, change `"status": "stub"` to `"status": "active"` in `users/cici/governed-state/surface-map.json`.

## Move proposal to approved

1. Copy `proposals/queue/$ARGUMENTS.json` → `proposals/approved/$ARGUMENTS.json`
2. Delete `proposals/queue/$ARGUMENTS.json`
3. Update fields in the approved file:
   ```json
   "status": "approved",
   "reviewer": "Xavier",
   "decided_at": "<ISO timestamp>",
   "decision_notes": "<what was created/changed>"
   ```

## Append to event log

Add to `proposals/events/event-log.json`:
```json
{
  "event_id": "evt-YYYYMMDD-NNN",
  "timestamp": "<ISO timestamp>",
  "proposal_id": "$ARGUMENTS",
  "action": "approved",
  "reviewer": "Xavier",
  "target_surface": "<surface>",
  "notes": "<brief description of what changed>"
}
```

## Commit

```bash
git add users/cici/governed-state/
git add proposals/approved/$ARGUMENTS.json
git add proposals/events/event-log.json
git commit -m "governed: apply $ARGUMENTS to <surface> — <what changed>"
```

## Echo completion

State: "Applied `$ARGUMENTS`. [What was created/changed.] Event logged."
