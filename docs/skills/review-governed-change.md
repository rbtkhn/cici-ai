# Skill: Review a Governed Change

**Purpose:** Evaluate a proposal in `proposals/queue/` and make a decision.

This is an **owner-only** operation. Agents may surface proposals; only Xavier approves them.

---

## When to Use This

- `proposals/queue/` has one or more proposals awaiting review
- Running a regular review cadence (e.g., weekly)
- A new proposal was just submitted and you want to act on it immediately

---

## Steps

### 1. Open the proposal

```bash
ls proposals/queue/
cat proposals/queue/prop-YYYYMMDD-NNN-slug.json
```

Or open the file in your editor.

### 2. Evaluate the proposal

Ask:

- [ ] **Is the target surface correct?** Does `target_surface` name a real surface in `surface-map.json`?
- [ ] **Is the rationale convincing?** Does the proposal explain *why* this matters?
- [ ] **Is the evidence solid?** Are `evidence_refs` present and do they support the claim?
- [ ] **Is the confidence appropriate?** Proposals with low confidence may need more synthesis first.
- [ ] **Is there a conflict?** Does this overlap with another proposal in the queue?
- [ ] **Is this the right scope?** Is the proposal too broad (should be split) or too narrow (should be merged)?

### 3. Make your decision

#### Approving

1. Apply the described change to `users/cici/governed-state/<surface>/`
   - If adding a new artifact: create the file
   - If updating: edit the existing file
   - If removing: delete the file (rare; keep a note in `decision_notes`)
2. Move the proposal file to `proposals/approved/`
3. Update the proposal:
   ```json
   "status": "approved",
   "reviewer": "Xavier",
   "decided_at": "2026-04-11T14:00:00Z",
   "decision_notes": "Applied. Created memory-policy/capture-habits.json."
   ```
4. Append to `proposals/events/event-log.json`
5. Commit:
   ```
   git add users/cici/governed-state/ proposals/approved/ proposals/events/
   git commit -m "governed: apply prop-YYYYMMDD-NNN to <surface>"
   ```

#### Rejecting

1. Do NOT apply any change to governed state
2. Move the proposal file to `proposals/rejected/`
3. Update the proposal:
   ```json
   "status": "rejected",
   "reviewer": "Xavier",
   "decided_at": "2026-04-11T14:00:00Z",
   "decision_notes": "The evidence doesn't yet support a canonical capture policy. Revisit after 30 more days of observation."
   ```
4. Append to event log
5. Commit:
   ```
   git add proposals/rejected/ proposals/events/
   git commit -m "proposal: reject prop-YYYYMMDD-NNN — <brief reason>"
   ```

#### Deferring

Deferral = "not now, but maybe later."

1. Move to `proposals/rejected/` (deferred proposals archive there)
2. Update proposal:
   ```json
   "status": "deferred",
   "reviewer": "Xavier",
   "decided_at": "2026-04-11T14:00:00Z",
   "decision_notes": "Defer. Interesting but needs synthesis of voice patterns first. Revisit in Q3."
   ```
3. Append to event log
4. Commit

#### Superseding (conflict handling)

If a newer proposal makes this one obsolete:

1. Move old proposal to `proposals/rejected/`
2. Set `status: "superseded"`, reference the newer proposal in `decision_notes`
3. Continue reviewing the newer proposal

---

## Review Cadence Recommendation

Once proposals accumulate, a regular cadence prevents queue buildup:
- Weekly: scan queue, process obvious decisions
- Monthly: deeper review of deferred proposals; consider if they should be re-proposed

When the `workflows` surface is populated, this cadence should be canonicalized there.

---

## Related Skills

- `promote-to-governed-state.md` — Detailed apply step
- `draft-proposal.md` — What agents do before review
- `docs/change-review-lifecycle.md` — Full lifecycle reference
