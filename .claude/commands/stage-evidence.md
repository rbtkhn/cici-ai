---
name: stage-evidence
description: Stage evidence from Supabase exports or raw captures into the evidence/ pipeline. Pass an optional tag filter as argument (e.g. /stage-evidence brewmind).
argument-hint: [tag-filter]
---

Stage evidence for promotion pipeline review. Tag filter (if provided): $ARGUMENTS

Follow `docs/skills/stage-evidence.md`.

## Step 1 — Check for a Supabase export

Look for a recent export file in `/tmp/supabase-export-*.json`. If none exists, tell Xavier:

> "No Supabase export found in /tmp/. Please run the SQL export from your Supabase dashboard and save to /tmp/supabase-export-YYYYMMDD.json, then re-run /stage-evidence."

Stop here if no export is found.

## Step 2 — Run extraction

```bash
python3 scripts/extract-evidence.py \
  --input /tmp/supabase-export-YYYYMMDD.json \
  --output evidence/ \
  $( [ -n "$ARGUMENTS" ] && echo "--tag $ARGUMENTS" )
```

If the script is not yet implemented, list what files exist in `evidence/` and ask Xavier how to proceed.

## Step 3 — Review and triage

Read the extracted files in `evidence/`. For each, categorize:

| Category | Action |
|---|---|
| Ready to synthesize | Note for `prepared-context/synthesis/` |
| Interesting but uncertain | Note for `prepared-context/pending-review/` |
| Not worth promoting | Leave in `evidence/` |

## Step 4 — Present triage summary

List:
- N items ready for synthesis (by surface)
- N items for pending review
- N items left in evidence only

Ask Xavier: "Would you like me to draft synthesis documents for the ready items?"

## Step 5 — On Xavier's approval

For each synthesis-ready cluster, create `prepared-context/synthesis/YYYYMMDD-<surface>-analysis.md` with:
- Observed pattern in plain language
- Evidence item citations (by filename)
- Confidence estimate
- Target surface
- Whether it's ready to propose or needs more data
