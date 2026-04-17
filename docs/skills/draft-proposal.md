# Skill: Draft a Proposal

**Purpose:** Create a formal change proposal for Cici governed state.

Use this when you have identified something that should change in `users/cici/governed-state/` — a new artifact, an update to an existing one, or a policy addition.

---

## When to Use This

- You have synthesized evidence in `prepared-context/synthesis/` and it's ready to propose
- You have observed a pattern in runtime that deserves canonicalization
- You want to add an artifact to a stub surface (voice, memory-policy, workflows, tools, etc.)
- You need to update the identity surface (capabilities, bridges, related projects)

## When NOT to Use This

- The change is a typo correction or obvious factual fix — direct owner edit is fine
- The synthesis isn't ready yet — put it in `prepared-context/pending-review/` first
- You're not sure it's worth proposing — run a memory hygiene audit first

---

## Steps

### 1. Identify the target surface

Open `users/cici/governed-state/surface-map.json` and find the surface this proposal targets.

If the surface is `stub`, your proposal will be adding the first artifact to it.
If the surface is `active`, your proposal updates or extends existing artifacts.

### 2. Gather evidence references

Collect file paths or IDs that support this proposal:
- Files in `evidence/` (from extraction)
- Files in `prepared-context/synthesis/` (from synthesis)
- Supabase thought IDs (if not yet extracted to `evidence/`)

These become the `evidence_refs` field in the proposal.

### 3. Assess confidence

Rate your confidence that this change is correct and valuable: 0.0–1.0.

| Score | Meaning |
|---|---|
| 0.9–1.0 | Very high — backed by strong evidence and clear reasoning |
| 0.7–0.89 | High — solid evidence, minor uncertainty |
| 0.5–0.69 | Medium — reasonable basis, but could go either way |
| < 0.5 | Low — exploratory; consider more synthesis before proposing |

### 4. Create the proposal file

Create `proposals/queue/prop-YYYYMMDD-NNN-short-slug.json`:

```json
{
  "id": "prop-20260411-001-add-memory-policy",
  "created_at": "2026-04-11T10:00:00Z",
  "status": "proposed",
  "change_type": "add",
  "target_surface": "memory-policy",
  "summary": "Add initial memory policy artifact to memory-policy surface",
  "rationale": "After reviewing 60 days of Supabase captures, consistent patterns in what Xavier captures and what he ignores suggest a stable memory policy. Canonicalizing this reduces ambiguity for future capture decisions.",
  "evidence_refs": [
    "prepared-context/synthesis/20260410-capture-pattern-analysis.md"
  ],
  "proposer": "claude-code",
  "confidence": 0.82
}
```

Required fields: `id`, `created_at`, `status`, `change_type`, `target_surface`, `summary`, `rationale`, `proposer`

Optional but recommended: `evidence_refs`, `confidence`

### 5. Validate

```bash
python3 scripts/validate-governed-state.py
```

Fix any errors before committing.

### 6. Commit

```bash
git add proposals/queue/prop-YYYYMMDD-NNN-short-slug.json
git commit -m "proposal: prop-YYYYMMDD-NNN add <short description>"
```

---

## After Submitting

The proposal sits in `proposals/queue/` until the owner reviews it.

The owner will either:
- Approve → apply the change and move to `proposals/approved/`
- Reject → move to `proposals/rejected/` with a decision note
- Defer → move to `proposals/rejected/` with `status: deferred`

See `docs/change-review-lifecycle.md` for the full lifecycle.

---

## Change Types

| Type | Use when |
|---|---|
| `add` | Adding a new artifact or field |
| `update` | Modifying an existing artifact |
| `remove` | Removing an artifact (rarely) |
| `restructure` | Reorganizing surface layout |
| `policy` | Adding or changing a policy document |
