#!/usr/bin/env python3
"""
extract-evidence.py

Extracts high-value memories from a Supabase runtime export and writes them
as structured evidence artifacts to evidence/.

STAGE 1 of the Cici promotion pipeline:
  Supabase runtime → evidence/ → prepared-context/ → proposals/ → governed-state/

See docs/promotion-doctrine.md for the full pipeline.

---

USAGE

  python3 scripts/extract-evidence.py --input <supabase-export.json> [options]

  Options:
    --input PATH      Path to Supabase memory export JSON (required)
    --output DIR      Target directory (default: evidence/)
    --tag TAG         Filter by tag (repeatable: --tag brewmind --tag strategy)
    --since DATE      Only include memories captured after DATE (YYYY-MM-DD)
    --min-score N     Only include memories with semantic score >= N (if scored)
    --dry-run         Print what would be written, don't write files

  Example:
    python3 scripts/extract-evidence.py \\
      --input /tmp/supabase-export-2026-04-11.json \\
      --tag brewmind \\
      --since 2026-03-01 \\
      --output evidence/

---

SUPABASE EXPORT FORMAT

Export your Supabase memories via:

  SELECT
    id,
    content,
    tags,
    fingerprint,
    created_at,
    updated_at
  FROM thoughts
  ORDER BY created_at DESC;

Save as JSON array: [ { "id": "...", "content": "...", ... }, ... ]

---

EVIDENCE FILE FORMAT

Each exported memory produces one file in evidence/:

  evidence/<YYYYMMDD>-<fingerprint-prefix>-<slug>.json

  {
    "evidence_id": "ev-<YYYYMMDD>-<fingerprint-prefix>",
    "source": "supabase",
    "source_id": "<supabase thought id>",
    "fingerprint": "<dedup fingerprint>",
    "captured_at": "<ISO 8601>",
    "exported_at": "<ISO 8601>",
    "content": "<original thought content>",
    "tags": ["tag1", "tag2"],
    "promotion_status": "raw",
    "notes": ""
  }

promotion_status values:
  raw           → just extracted, not yet reviewed
  in-synthesis  → referenced in a prepared-context/synthesis/ document
  proposed      → referenced in a proposal in proposals/queue/
  promoted      → change approved and merged into governed-state/
  archived      → reviewed and decided not to promote

---

IMPLEMENTATION STATUS

This script is a documented stub. The extraction logic is not yet implemented.
Implement this script when Supabase export access is available.

To implement:
  1. Parse the input JSON (Supabase thought array)
  2. Filter by --tag and --since arguments
  3. For each memory, compute a slug from the content (first 5 words, lowercase, hyphenated)
  4. Write the evidence JSON artifact to evidence/
  5. Print a summary: N memories extracted, N skipped (tag filter), N skipped (date filter)

---
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
EVIDENCE_DIR = ROOT / "evidence"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract Supabase memories into evidence/ artifacts."
    )
    parser.add_argument("--input", required=True, help="Path to Supabase export JSON")
    parser.add_argument("--output", default=str(EVIDENCE_DIR), help="Output directory")
    parser.add_argument("--tag", action="append", dest="tags", default=[], help="Filter by tag")
    parser.add_argument("--since", default=None, help="Only include memories after YYYY-MM-DD")
    parser.add_argument("--min-score", type=float, default=None, help="Min semantic score")
    parser.add_argument("--dry-run", action="store_true", help="Print without writing")
    return parser.parse_args()


def load_export(path):
    try:
        with open(path) as f:
            data = json.load(f)
        if not isinstance(data, list):
            print(f"[error] Expected JSON array in {path}", file=sys.stderr)
            sys.exit(1)
        return data
    except (json.JSONDecodeError, OSError) as e:
        print(f"[error] Cannot read {path}: {e}", file=sys.stderr)
        sys.exit(1)


def slugify(text, max_words=5):
    words = text.lower().split()[:max_words]
    slug = "-".join(w.strip(".,!?;:'\"") for w in words if w.strip(".,!?;:'\""))
    return slug or "untitled"


def filter_memories(memories, tags=None, since=None):
    filtered = []
    skipped_tag = 0
    skipped_date = 0

    since_dt = None
    if since:
        since_dt = datetime.fromisoformat(since).replace(tzinfo=timezone.utc)

    for m in memories:
        if tags:
            memory_tags = m.get("tags") or []
            if isinstance(memory_tags, str):
                memory_tags = [t.strip() for t in memory_tags.split(",")]
            if not any(t in memory_tags for t in tags):
                skipped_tag += 1
                continue

        if since_dt:
            captured = m.get("created_at", "")
            try:
                captured_dt = datetime.fromisoformat(captured.replace("Z", "+00:00"))
                if captured_dt < since_dt:
                    skipped_date += 1
                    continue
            except (ValueError, AttributeError):
                pass

        filtered.append(m)

    return filtered, skipped_tag, skipped_date


def build_evidence_artifact(memory, exported_at):
    content = memory.get("content", "")
    source_id = str(memory.get("id", ""))
    fingerprint = memory.get("fingerprint", source_id[:8])
    fp_prefix = fingerprint[:8] if fingerprint else source_id[:8]
    captured_at = memory.get("created_at", exported_at)

    try:
        date_prefix = datetime.fromisoformat(
            captured_at.replace("Z", "+00:00")
        ).strftime("%Y%m%d")
    except (ValueError, AttributeError):
        date_prefix = datetime.now(timezone.utc).strftime("%Y%m%d")

    slug = slugify(content)
    evidence_id = f"ev-{date_prefix}-{fp_prefix}"
    filename = f"{date_prefix}-{fp_prefix}-{slug}.json"

    tags = memory.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]

    return filename, {
        "evidence_id": evidence_id,
        "source": "supabase",
        "source_id": source_id,
        "fingerprint": fingerprint,
        "captured_at": captured_at,
        "exported_at": exported_at,
        "content": content,
        "tags": tags,
        "promotion_status": "raw",
        "notes": ""
    }


def main():
    args = parse_args()
    output_dir = Path(args.output)

    memories = load_export(args.input)
    exported_at = datetime.now(timezone.utc).isoformat()

    filtered, skipped_tag, skipped_date = filter_memories(
        memories,
        tags=args.tags or None,
        since=args.since
    )

    print(f"Loaded {len(memories)} memories from export.")
    if skipped_tag:
        print(f"  Skipped {skipped_tag} (tag filter: {args.tags})")
    if skipped_date:
        print(f"  Skipped {skipped_date} (date filter: since {args.since})")
    print(f"  Extracting {len(filtered)} memories to {output_dir}/")

    if not args.dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    for memory in filtered:
        filename, artifact = build_evidence_artifact(memory, exported_at)
        target = output_dir / filename

        if args.dry_run:
            print(f"  [dry-run] would write: {target.relative_to(ROOT)}")
        else:
            if target.exists():
                print(f"  [skip] already exists: {filename}")
                continue
            with open(target, "w") as f:
                json.dump(artifact, f, indent=2)
            written += 1

    if not args.dry_run:
        print(f"\nDone. Wrote {written} evidence artifacts to {output_dir}/")
        print("Next step: review evidence/ and synthesize in prepared-context/synthesis/")
        print("See docs/promotion-doctrine.md for the full pipeline.")
    else:
        print(f"\nDry-run complete. {len(filtered)} artifacts would be written.")


if __name__ == "__main__":
    main()
