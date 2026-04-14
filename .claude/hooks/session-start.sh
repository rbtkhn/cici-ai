#!/bin/bash
# SessionStart hook for Cici
# Runs at the start of every Claude Code session.
# Surfaces open proposals and open loops so Claude always has fresh context.
# This implements the startup ceremony from docs/companion-agent/brewmind-companion-contract.md Section H.

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

echo "=== Cici Session Start ==="
echo ""

# --- Open proposals ---
QUEUE_DIR="$REPO_ROOT/proposals/queue"
PROPOSAL_COUNT=$(find "$QUEUE_DIR" -name "*.json" 2>/dev/null | wc -l | tr -d ' ')

if [ "$PROPOSAL_COUNT" -gt 0 ]; then
  echo "OPEN PROPOSALS ($PROPOSAL_COUNT):"
  for f in "$QUEUE_DIR"/*.json; do
    id=$(python3 -c "import json,sys; d=json.load(open('$f')); print(d.get('id','?'))" 2>/dev/null)
    surface=$(python3 -c "import json,sys; d=json.load(open('$f')); print(d.get('target_surface','?'))" 2>/dev/null)
    summary=$(python3 -c "import json,sys; d=json.load(open('$f')); print(d.get('summary','?'))" 2>/dev/null)
    echo "  - $id [$surface]: $summary"
  done
else
  echo "OPEN PROPOSALS: none"
fi

echo ""

# --- Open loops ---
LOOPS_FILE="$REPO_ROOT/docs/companion-agent/brewmind-open-loops.md"
if [ -f "$LOOPS_FILE" ]; then
  echo "OPEN LOOPS FILE: present"
  # Count lines with "open" status marker
  OPEN_LOOPS=$(grep -ic "status.*open\|open$" "$LOOPS_FILE" 2>/dev/null || echo 0)
  echo "  Lines referencing 'open': $OPEN_LOOPS"
else
  echo "OPEN LOOPS FILE: missing — create it early in this session (DOCSYNC)"
fi

echo ""
echo "Current lane: PLAN (default). Xavier must say 'execute' to switch."
echo "=========================="
