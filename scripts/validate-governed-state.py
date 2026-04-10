#!/usr/bin/env python3
"""
validate-governed-state.py

Validates governed-state artifacts in this repository.

Run locally:  python3 scripts/validate-governed-state.py
Run in CI:    same command (called by .github/workflows/validate-governed-state.yml)

Checks:
  1. Required directories exist
  2. Proposal JSON files in queue/approved/rejected/ are valid JSON
  3. Proposals have required fields and valid status/change_type values
  4. Proposal status matches expected values for its directory
  5. seed_intent.json files under users/ have required fields
  6. seed_intent.json instance_id matches the parent directory name
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

REQUIRED_DIRS = [
    "evidence",
    "prepared-context",
    "users",
    "users/_template",
    "proposals",
    "proposals/queue",
    "proposals/approved",
    "proposals/rejected",
    "proposals/schemas",
    "config",
    "bridges/supabase",
]

VALID_STATUSES = {"proposed", "under_review", "approved", "rejected", "deferred", "superseded"}
VALID_CHANGE_TYPES = {"add", "update", "remove", "restructure", "policy"}
REQUIRED_PROPOSAL_FIELDS = [
    "id", "created_at", "status", "change_type",
    "target_surface", "summary", "rationale", "proposer",
]
REQUIRED_SEED_FIELDS = ["instance_id", "owner", "purpose", "seed_phase_status"]

PROPOSAL_DIRS = {
    "proposals/queue":    {"proposed", "under_review"},
    "proposals/approved": {"approved"},
    "proposals/rejected": {"rejected", "deferred", "superseded"},
}

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def check_required_dirs():
    for rel in REQUIRED_DIRS:
        if not (ROOT / rel).is_dir():
            err(f"Required directory missing: {rel}/")


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        err(f"Invalid JSON in {path.relative_to(ROOT)}: {e}")
        return None
    except OSError as e:
        err(f"Cannot read {path.relative_to(ROOT)}: {e}")
        return None


def validate_proposal(path, expected_statuses=None):
    data = load_json(path)
    if data is None:
        return

    rel = str(path.relative_to(ROOT))

    for field in REQUIRED_PROPOSAL_FIELDS:
        if field not in data:
            err(f"{rel}: missing required field '{field}'")

    status = data.get("status")
    if status is not None:
        if status not in VALID_STATUSES:
            err(f"{rel}: invalid status '{status}' — must be one of {sorted(VALID_STATUSES)}")
        elif expected_statuses and status not in expected_statuses:
            warn(f"{rel}: status '{status}' unexpected in this directory (expected: {sorted(expected_statuses)})")

    change_type = data.get("change_type")
    if change_type is not None and change_type not in VALID_CHANGE_TYPES:
        err(f"{rel}: invalid change_type '{change_type}' — must be one of {sorted(VALID_CHANGE_TYPES)}")

    confidence = data.get("confidence")
    if confidence is not None:
        if not isinstance(confidence, (int, float)) or not (0 <= confidence <= 1):
            err(f"{rel}: 'confidence' must be a number between 0.0 and 1.0")

    proposal_id = data.get("id", "")
    if proposal_id and not _valid_proposal_id(proposal_id):
        warn(f"{rel}: id '{proposal_id}' does not match recommended format prop-YYYYMMDD-NNN")


def _valid_proposal_id(proposal_id):
    import re
    return bool(re.match(r'^prop-\d{8}-\d{3,}$', proposal_id))


def validate_proposals():
    for rel_dir, expected_statuses in PROPOSAL_DIRS.items():
        directory = ROOT / rel_dir
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.json")):
            validate_proposal(path, expected_statuses)


def validate_seed_intents():
    for path in sorted(ROOT.glob("users/*/seed_intent.json")):
        # skip the template
        if path.parent.name == "_template":
            continue

        data = load_json(path)
        if data is None:
            continue

        rel = str(path.relative_to(ROOT))
        for field in REQUIRED_SEED_FIELDS:
            if field not in data:
                err(f"{rel}: missing required field '{field}'")

        instance_id = data.get("instance_id", "")
        dir_name = path.parent.name
        if instance_id and instance_id != dir_name:
            err(f"{rel}: instance_id '{instance_id}' does not match directory name '{dir_name}'")

        status = data.get("seed_phase_status")
        if status and status not in {"pending", "active", "archived"}:
            warn(f"{rel}: unexpected seed_phase_status '{status}'")


def main():
    check_required_dirs()
    validate_proposals()
    validate_seed_intents()

    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f"  [warn] {w}")

    if errors:
        print("Errors:")
        for e in errors:
            print(f"  [fail] {e}")
        print(f"\n{len(errors)} error(s) found. Fix them before merging.")
        sys.exit(1)
    else:
        total_warnings = len(warnings)
        print(f"All governed-state artifacts are valid." +
              (f" ({total_warnings} warning(s))" if total_warnings else ""))


if __name__ == "__main__":
    main()
