# Skill: Stage Evidence

**Purpose:** Extract high-value memories from Supabase and stage them for governed-formation review.

Use this at the start of the promotion pipeline — before synthesis, before proposals.

---

## When to Use This

- Beginning a memory hygiene audit
- Preparing to propose a new memory-policy or capture-habits artifact
- Identifying themes worth canonicalizing in voice or workflows
- Building evidence for a proposal on any governed-state surface

---

## Steps

### 1. Export memories from Supabase

Use the Supabase dashboard SQL editor or your preferred MCP client:

```sql
SELECT
  id,
  content,
  tags,
  fingerprint,
  created_at,
  updated_at
FROM thoughts
ORDER BY created_at DESC
LIMIT 500;
```

Export as JSON array. Save to a local file (gitignored):

```
/tmp/supabase-export-YYYYMMDD.json
```

### 2. Run extraction

```bash
python3 scripts/extract-evidence.py \
  --input /tmp/supabase-export-YYYYMMDD.json \
  --output evidence/ \
  [--tag brewmind] \
  [--since 2026-03-01]
```

Flags:
- `--tag TAG` — filter by specific tag (repeatable)
- `--since DATE` — only export memories from this date forward
- `--dry-run` — preview what would be written without writing

### 3. Review extracted evidence

Open `evidence/` and read through the extracted artifacts. You're looking for:

- **Repeating themes** — same insight in multiple captures
- **Policy crystallization** — a stable decision pattern
- **Identity signals** — how Xavier describes his goals, Cici's purpose, BrewMind's direction
- **Gaps** — things that are clearly important but aren't in governed state yet

### 4. Triage to the right prepared-context subtype

For each evidence item, decide:

| Decision | Action |
|---|---|
| Ready to synthesize into a proposal | Move insights to `prepared-context/synthesis/` |
| Interesting but needs more thought | Move to `prepared-context/pending-review/` |
| Not worth promoting | Leave in `evidence/` (it stays — just don't promote it) |

### 5. Create synthesis documents

In `prepared-context/synthesis/`, write a human-readable draft that:
- Summarizes what the evidence shows
- Argues why it should become governed state
- Identifies the target surface
- Estimates confidence

This becomes the `rationale` for your proposal and the content that the `evidence_refs` field points to.

---

## Tips

- Don't try to extract and synthesize everything at once — focus on one surface per session
- If you're unsure about a theme, put it in `pending-review/` and revisit next time
- High-frequency captures (daily notes, quick thoughts) rarely warrant promotion — look for the 5–10% that are load-bearing
- Tag `#canonical-candidate` in Supabase (if supported) to pre-flag memories worth promoting

---

## Related Skills

- `memory-hygiene-audit.md` — How to identify promotion candidates systematically
- `draft-proposal.md` — What to do after synthesis
- `docs/promotion-doctrine.md` — Full pipeline context
