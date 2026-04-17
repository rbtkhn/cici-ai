# Proposal Events

This directory holds the event log for proposal decisions.

## event-log.json

An append-only log of every approval, rejection, and deferral decision.

**Do not edit past entries.** Only append new ones.

### Entry format

```json
{
  "event_id": "evt-YYYYMMDD-NNN",
  "timestamp": "ISO 8601",
  "proposal_id": "prop-YYYYMMDD-NNN-description",
  "action": "approved | rejected | deferred | superseded",
  "reviewer": "owner name",
  "target_surface": "surface id from surface-map.json",
  "notes": "brief decision summary"
}
```

### Adding an entry

After approving or rejecting a proposal:

1. Open `proposals/events/event-log.json`
2. Append a new entry to the `events` array
3. Commit alongside the proposal move

See `docs/change-review-lifecycle.md` for the full decision protocol.
