# Skill: Memory Hygiene Audit

**Purpose:** Identify promotion candidates in Supabase runtime memory and move the best ones toward governed state.

Run this periodically (monthly recommended) to keep the governed-formation pipeline flowing.

---

## When to Use This

- Monthly maintenance ritual
- Before a major governed-state review session
- When you suspect Supabase has patterns worth canonicalizing
- When the dossier shows evidence is empty but governed-state surfaces are still stubs

---

## Steps

### 1. Generate a current dossier

```bash
python3 scripts/generate-dossier.py --instance cici
```

This gives you a health snapshot: which surfaces are stubs, what's in the pipeline, what proposals are open.

### 2. Export recent Supabase memories

Choose a date range. Monthly audits: last 30 days. Quarterly: last 90 days.

```sql
SELECT id, content, tags, fingerprint, created_at
FROM thoughts
WHERE created_at > NOW() - INTERVAL '30 days'
ORDER BY created_at DESC;
```

Export as JSON to `/tmp/supabase-export-YYYYMMDD.json`.

### 3. Run extraction

```bash
python3 scripts/extract-evidence.py \
  --input /tmp/supabase-export-YYYYMMDD.json \
  --output evidence/ \
  --since YYYY-MM-DD
```

Review what was extracted to `evidence/`.

### 4. Categorize evidence by surface

For each stub surface in `users/cici/governed-state/`, ask:
- "Is there evidence in `evidence/` that could populate this surface?"

| Surface | What to look for |
|---|---|
| voice | How Xavier phrases things, tone patterns, repeated expressions |
| memory-policy | What he captures, what he ignores, tagging habits |
| workflows | Recurring session patterns, what he always does first |
| tools | Which AI client he prefers for which task type |
| source-priority | How he resolves conflicting information |
| runtime-bridges | Any bridge-related decisions or policy notes |

### 5. Synthesize themes

For each surface with evidence, create a synthesis document in `prepared-context/synthesis/`:

```
prepared-context/synthesis/YYYYMMDD-<surface>-analysis.md
```

The synthesis should:
- Describe the observed pattern or policy in plain language
- Cite specific evidence items (by `evidence_id`)
- Estimate how stable and confident this observation is
- Note whether it's ready to propose or needs more data

### 6. Decide on proposals

For each synthesis document, decide:

| Readiness | Action |
|---|---|
| High confidence, clear scope | Draft proposal (`docs/skills/draft-proposal.md`) |
| Medium confidence | Move to `prepared-context/pending-review/` for later |
| Low confidence | Leave in synthesis for more data next cycle |

### 7. Clean up

- Archive session artifacts from `prepared-context/session/` → `prepared-context/archived/`
- Mark evidence items with `promotion_status` if you've moved them forward (optional, manual)
- Re-run dossier to confirm pipeline state is accurate

```bash
python3 scripts/generate-dossier.py --instance cici
```

---

## Signs a Memory Is Worth Promoting

- Appears in 3+ distinct captures over different dates
- Captures a decision or policy, not just a thought
- Would be useful to reference in future sessions from governed state
- Reflects something stable about Xavier's identity, goals, or Cici's operation

## Signs a Memory Should NOT Be Promoted

- It was relevant to a single moment or project
- It's superseded by a newer capture
- It's too specific/tactical (operational, not canonical)
- Xavier has since changed his mind on it

---

## Cadence Recommendation

| Frequency | Scope |
|---|---|
| Monthly | Last 30 days, spot-check key surfaces |
| Quarterly | Last 90 days, all surfaces, deep synthesis |
| Annual | Full retrospective, review archived content, prune stale evidence |

---

## Related Skills

- `stage-evidence.md` — Extraction step in detail
- `draft-proposal.md` — What to do after synthesis
- `docs/promotion-doctrine.md` — Full pipeline reference
