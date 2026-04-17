---
name: review-governed-change
description: Review a specific proposal in proposals/queue/ and present a structured evaluation. Owner decides approve/reject/defer. Pass proposal id as argument.
argument-hint: <proposal-id>
---

Review the proposal: $ARGUMENTS

Follow `docs/skills/review-governed-change.md`.

## Step 1 — Read the proposal

Read `proposals/queue/$ARGUMENTS.json`. If the file does not exist, try matching `proposals/queue/` by partial id and show what you found.

## Step 2 — Evaluate using the checklist

Answer each question explicitly (yes / no / needs clarification):

- [ ] Is `target_surface` a valid surface in `users/cici/governed-state/surface-map.json`?
- [ ] Is the `rationale` convincing? Does it explain *why* this matters?
- [ ] Are `evidence_refs` present and do the referenced files exist?
- [ ] Is `confidence` appropriate for the evidence quality? (flag if < 0.5)
- [ ] Does this conflict with another open proposal in `proposals/queue/`?
- [ ] Is the scope right? (flag if too broad or too narrow)

## Step 3 — Present recommendation

State:
- **Recommendation**: approve / reject / defer
- **Reason**: one sentence
- **If approve**: list exactly which files would be created/changed in `users/cici/governed-state/`

## Step 4 — Wait for Xavier's decision

Do not apply any change. Xavier must say "approve", "reject", or "defer" to proceed.

## Step 5 — On Xavier's decision

**Approve**: run `/promote-to-governed-state $ARGUMENTS`

**Reject or Defer**:
1. Move `proposals/queue/$ARGUMENTS.json` to `proposals/rejected/`
2. Update the proposal JSON with `status`, `reviewer: "Xavier"`, `decided_at`, `decision_notes`
3. Append an entry to `proposals/events/event-log.json`
4. Commit: `git add proposals/rejected/ proposals/events/ && git commit -m "proposal: reject/defer $ARGUMENTS — <brief reason>"`
