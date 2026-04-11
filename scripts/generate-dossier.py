#!/usr/bin/env python3
"""
generate-dossier.py

Generates a human-readable dossier summarizing the current state of the
Cici governed-formation pipeline.

The dossier covers:
  - Governed-state surface health (active vs. stub)
  - Proposal pipeline summary (queue, approved, rejected counts)
  - Evidence and prepared-context inventory
  - Seed phase status
  - Recent events from the event log
  - Open questions and recommended next actions

USAGE

  python3 scripts/generate-dossier.py [options]

  Options:
    --instance ID       Instance to audit (default: cici)
    --output PATH       Write dossier to file (default: stdout)
    --format FORMAT     Output format: markdown | json (default: markdown)
    --recent-events N   Show N most recent events (default: 5)

  Example:
    python3 scripts/generate-dossier.py --instance cici --output /tmp/dossier.md

See docs/promotion-doctrine.md for context on how this fits the pipeline.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a governed-formation dossier for a Cici instance."
    )
    parser.add_argument("--instance", default="cici", help="Instance ID to audit")
    parser.add_argument("--output", default=None, help="Write output to file (default: stdout)")
    parser.add_argument("--format", default="markdown", choices=["markdown", "json"],
                        help="Output format")
    parser.add_argument("--recent-events", type=int, default=5,
                        help="Number of recent events to show")
    return parser.parse_args()


def load_json_safe(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def audit_governed_state(instance_dir):
    gs_dir = instance_dir / "governed-state"
    surface_map_path = gs_dir / "surface-map.json"
    surface_map = load_json_safe(surface_map_path)

    surfaces_found = []
    surfaces_stub = []
    surfaces_active = []

    if surface_map:
        for s in surface_map.get("surfaces", []):
            sid = s.get("id", "?")
            status = s.get("status", "unknown")
            path = gs_dir / sid
            exists = path.is_dir()
            file_count = len(list(path.glob("*.json")) + list(path.glob("*.md"))) - 1 if exists else 0
            # -1 to exclude README.md itself
            file_count = max(0, file_count)

            surfaces_found.append({
                "id": sid,
                "status": status,
                "path_exists": exists,
                "artifact_count": file_count
            })
            if status == "active":
                surfaces_active.append(sid)
            else:
                surfaces_stub.append(sid)
    else:
        # Fallback: scan directories
        if gs_dir.is_dir():
            for d in sorted(gs_dir.iterdir()):
                if d.is_dir():
                    surfaces_found.append({"id": d.name, "status": "unknown",
                                           "path_exists": True, "artifact_count": 0})

    return {
        "surface_map_present": surface_map_path.exists(),
        "surfaces": surfaces_found,
        "active_surfaces": surfaces_active,
        "stub_surfaces": surfaces_stub,
    }


def audit_seed_phase(instance_dir):
    seed_dir = instance_dir / "seed-phase"
    status_path = seed_dir / "status.json"
    criteria_path = seed_dir / "readiness-criteria.json"

    status = load_json_safe(status_path)
    criteria = load_json_safe(criteria_path)

    return {
        "status_file_present": status_path.exists(),
        "criteria_file_present": criteria_path.exists(),
        "seed_phase_status": status.get("seed_phase_status") if status else "unknown",
        "readiness_level": status.get("readiness_level") if status else "unknown",
        "readiness_score": status.get("readiness_score") if status else None,
        "open_stubs": status.get("open_stubs", []) if status else [],
    }


def audit_seed_intent(instance_dir):
    seed_intent_path = instance_dir / "seed_intent.json"
    data = load_json_safe(seed_intent_path)
    if not data:
        return {"present": False}
    return {
        "present": True,
        "instance_id": data.get("instance_id"),
        "owner": data.get("owner"),
        "seed_phase_status": data.get("seed_phase_status"),
    }


def audit_proposals():
    proposals_dir = ROOT / "proposals"
    counts = {"queue": 0, "approved": 0, "rejected": 0}
    queue_items = []

    for dirname, status_key in [("queue", "queue"), ("approved", "approved"), ("rejected", "rejected")]:
        d = proposals_dir / dirname
        if d.is_dir():
            files = sorted(d.glob("*.json"))
            counts[status_key] = len(files)
            if dirname == "queue":
                for f in files:
                    data = load_json_safe(f)
                    if data:
                        queue_items.append({
                            "id": data.get("id", f.name),
                            "status": data.get("status", "?"),
                            "target_surface": data.get("target_surface", "?"),
                            "summary": data.get("summary", "")[:80],
                        })

    return {**counts, "queue_items": queue_items}


def audit_events(n=5):
    event_log_path = ROOT / "proposals" / "events" / "event-log.json"
    data = load_json_safe(event_log_path)
    if not data:
        return {"present": False, "events": []}
    events = data.get("events", [])
    return {
        "present": True,
        "total_events": len(events),
        "recent": events[-n:] if events else []
    }


def audit_evidence():
    evidence_dir = ROOT / "evidence"
    files = [f for f in evidence_dir.glob("*.json")] + [f for f in evidence_dir.glob("*.md")]
    # Exclude README
    files = [f for f in files if f.name.lower() != "readme.md"]
    return {"artifact_count": len(files)}


def audit_prepared_context():
    pc_dir = ROOT / "prepared-context"
    result = {}
    for subdir in ["synthesis", "pending-review", "session", "archived"]:
        d = pc_dir / subdir
        if d.is_dir():
            files = [f for f in d.iterdir() if f.is_file() and f.name.lower() != "readme.md"]
            result[subdir] = len(files)
        else:
            result[subdir] = 0
    return result


def generate_recommendations(gs, seed, proposals, evidence, pc):
    recs = []

    if seed.get("seed_phase_status") != "complete":
        recs.append("SEED: Seed phase not marked complete. Run readiness check.")

    if proposals["queue"] == 0:
        if gs["stub_surfaces"]:
            recs.append(f"PROPOSALS: {len(gs['stub_surfaces'])} surfaces are stubs. "
                        f"Consider drafting proposals to populate: {', '.join(gs['stub_surfaces'][:3])}")
    else:
        recs.append(f"REVIEW: {proposals['queue']} proposal(s) in queue awaiting review.")

    if evidence["artifact_count"] > 0 and pc.get("synthesis", 0) == 0:
        recs.append(f"SYNTHESIS: {evidence['artifact_count']} evidence item(s) not yet synthesized. "
                    "Review evidence/ and create prepared-context/synthesis/ drafts.")

    if pc.get("pending-review", 0) > 0:
        recs.append(f"REVIEW: {pc['pending-review']} item(s) in prepared-context/pending-review/ "
                    "awaiting owner review.")

    if not recs:
        recs.append("No immediate actions needed. Governed formation pipeline is healthy.")

    return recs


def render_markdown(instance_id, gs, seed, proposals, events, evidence, pc, recs, generated_at):
    lines = [
        f"# Governed Formation Dossier: {instance_id}",
        f"\n**Generated:** {generated_at}",
        f"\n---\n",
        "## Seed Phase",
        f"- Status: `{seed.get('seed_phase_status', 'unknown')}`",
        f"- Readiness: `{seed.get('readiness_level', 'unknown')}` "
        f"(score: {seed.get('readiness_score', '?')})",
        f"- Status file: {'present' if seed['status_file_present'] else 'MISSING'}",
        f"- Criteria file: {'present' if seed['criteria_file_present'] else 'MISSING'}",
        "",
        "## Governed-State Surfaces",
        f"Surface map: {'present' if gs['surface_map_present'] else 'MISSING'}",
        "",
        "| Surface | Status | Artifacts |",
        "|---|---|---|",
    ]

    for s in gs["surfaces"]:
        emoji = "active" if s["status"] == "active" else "stub"
        lines.append(f"| {s['id']} | {emoji} | {s['artifact_count']} artifact(s) |")

    lines += [
        "",
        f"Active surfaces: {len(gs['active_surfaces'])} | Stubs: {len(gs['stub_surfaces'])}",
        "",
        "## Proposal Pipeline",
        f"- Queue (awaiting review): **{proposals['queue']}**",
        f"- Approved: {proposals['approved']}",
        f"- Rejected/deferred: {proposals['rejected']}",
    ]

    if proposals["queue_items"]:
        lines.append("")
        lines.append("### In Queue")
        for item in proposals["queue_items"]:
            lines.append(f"- `{item['id']}` [{item['status']}] → `{item['target_surface']}`: {item['summary']}")

    lines += [
        "",
        "## Evidence & Prepared Context",
        f"- Evidence artifacts: {evidence['artifact_count']}",
        f"- Synthesis: {pc.get('synthesis', 0)}",
        f"- Pending review: {pc.get('pending-review', 0)}",
        f"- Session: {pc.get('session', 0)}",
        f"- Archived: {pc.get('archived', 0)}",
        "",
        "## Recent Events",
    ]

    if events["present"] and events["recent"]:
        lines.append(f"Total events: {events['total_events']}")
        lines.append("")
        for e in reversed(events["recent"]):
            lines.append(f"- `{e.get('timestamp', '?')}` — {e.get('action', '?')} "
                         f"`{e.get('proposal_id', '?')}` → {e.get('target_surface', '?')}")
    else:
        lines.append("No events recorded yet.")

    lines += [
        "",
        "## Recommended Actions",
    ]
    for r in recs:
        lines.append(f"- {r}")

    return "\n".join(lines)


def render_json(instance_id, gs, seed, proposals, events, evidence, pc, recs, generated_at):
    return json.dumps({
        "instance_id": instance_id,
        "generated_at": generated_at,
        "seed_phase": seed,
        "governed_state": gs,
        "proposals": proposals,
        "events": events,
        "evidence": evidence,
        "prepared_context": pc,
        "recommendations": recs,
    }, indent=2)


def main():
    args = parse_args()
    instance_dir = ROOT / "users" / args.instance

    if not instance_dir.is_dir():
        print(f"[error] Instance directory not found: {instance_dir}", file=sys.stderr)
        sys.exit(1)

    generated_at = datetime.now(timezone.utc).isoformat()

    gs = audit_governed_state(instance_dir)
    seed = audit_seed_phase(instance_dir)
    proposals = audit_proposals()
    events = audit_events(n=args.recent_events)
    evidence = audit_evidence()
    pc = audit_prepared_context()
    recs = generate_recommendations(gs, seed, proposals, evidence, pc)

    if args.format == "json":
        output = render_json(args.instance, gs, seed, proposals, events, evidence, pc, recs, generated_at)
    else:
        output = render_markdown(args.instance, gs, seed, proposals, events, evidence, pc, recs, generated_at)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Dossier written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
