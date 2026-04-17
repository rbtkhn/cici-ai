---
name: draft-proposal
description: Create a formal change proposal for a Cici governed-state surface. Pass the target surface as an argument (e.g. /draft-proposal memory-policy).
argument-hint: <target-surface>
---

Create a new proposal in `proposals/queue/` for the surface: $ARGUMENTS

Follow the steps in `docs/skills/draft-proposal.md` exactly.

## Required actions

1. Read `users/cici/governed-state/surface-map.json` to confirm `$ARGUMENTS` is a valid surface and its current status.

2. Read any relevant files in `evidence/` or `prepared-context/synthesis/` that support this proposal.

3. Determine the next available proposal number:
   - List `proposals/queue/`, `proposals/approved/`, `proposals/rejected/` to find the highest existing NNN for today's date (YYYYMMDD = today).
   - Increment by 1.

4. Draft the proposal JSON at `proposals/queue/prop-YYYYMMDD-NNN-<slug>.json`:

```json
{
  "id": "prop-YYYYMMDD-NNN-<slug>",
  "created_at": "<ISO timestamp>",
  "status": "proposed",
  "change_type": "<add|update|remove|restructure|policy>",
  "target_surface": "$ARGUMENTS",
  "summary": "<one line>",
  "rationale": "<why this matters and what evidence supports it>",
  "evidence_refs": [],
  "proposer": "claude-code",
  "confidence": 0.0
}
```

5. Show Xavier the draft and ask for approval before writing it.

6. On approval: write the file, then run `python3 scripts/validate-governed-state.py` and fix any errors.

7. Echo back: "Proposal `<id>` written to queue. Awaiting your review."

**Do not apply any governed-state change** — only queue the proposal.
