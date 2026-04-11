# Promotion Doctrine

**Version:** 1.0
**Applies to:** Cici — Xavier's personal OB1 instance

---

## What Is Promotion?

Promotion is the pipeline by which **runtime memory becomes durable governed truth**.

Cici sits on two foundations:
1. **Supabase runtime memory** — high-volume, operational, noisy, searchable
2. **Git-governed truth** — curated, canonical, durable, owner-approved

Promotion is the bridge between them. Without it, runtime memory stays operationally useful but never becomes canonical. With it, the most valuable patterns, policies, and insights from runtime can be elevated into the permanent record.

---

## The Full Pipeline

```
Supabase runtime memory
         │
         │  (scripts/extract-evidence.py)
         ▼
    evidence/
         │
         │  (manual curation or synthesis script)
         ▼
    prepared-context/synthesis/
         │
         │  (owner or agent drafts proposal)
         ▼
    proposals/queue/
         │
         │  (owner reviews and approves)
         ▼
    users/cici/governed-state/<surface>/
         │
         │  (optional: scripts/generate-dossier.py)
         ▼
    dossier: governed-state diff summary
         │
         │  (optional: runtime back-propagation)
         ▼
    Supabase updated to reflect new canonical truth
```

---

## Promotion Triggers

Not every runtime memory should be promoted. Promotion makes sense when:

| Trigger | Description | Example |
|---|---|---|
| **Pattern repetition** | The same insight appears in 3+ distinct captures | "Xavier always qualifies BrewMind as a slow-build project" |
| **Policy crystallization** | A recurring decision pattern is ready to be codified | Capture habits that have stabilized over 30+ days |
| **Schema consensus** | A tag or category appears consistently enough to warrant official taxonomy | `#brewmind`, `#strategy` usage is consistent across AI clients |
| **Identity clarification** | A capture updates or refines how Cici understands Xavier's purpose or goals | New business direction should update `identity/instance.json` |
| **Conflict resolution** | Runtime and governed-state disagree; owner needs to adjudicate | Supabase has data that contradicts current `identity/instance.json` |
| **Explicit operator flag** | Xavier manually marks a memory or synthesis for promotion | Any memory tagged with a to-be-defined promotion tag |

---

## Stage 1: Evidence Extraction

**Script:** `scripts/extract-evidence.py` (stub — see that file for implementation guidance)

Extract high-value items from Supabase into `evidence/`:

1. Query Supabase for memories matching a promotion criteria (tag, date range, pattern)
2. Export to structured JSON or Markdown in `evidence/`
3. Each evidence file should include:
   - Source (Supabase thought ID or fingerprint)
   - Capture timestamp
   - Original content
   - Any existing tags

Evidence is **immutable once written**. Do not edit evidence files after creation.

---

## Stage 2: Synthesis

In `prepared-context/synthesis/`:

1. Review extracted evidence
2. Identify the core insight, pattern, or policy worth preserving
3. Draft a synthesis document: a human-readable summary of what the evidence shows and why it matters
4. Name it: `YYYYMMDD-<slug>.md`

The synthesis is **your argument for why this should become governed state**. It becomes the `rationale` of the proposal and the `evidence_refs` list.

---

## Stage 3: Proposal

In `proposals/queue/`:

1. Create a proposal JSON following `proposals/schemas/proposal.schema.json`
2. Set `target_surface` to the correct governed-state surface
3. Set `evidence_refs` to point to the synthesis document
4. Set `confidence` based on how certain you are this is worth canonicalizing
5. Set `proposer` to your identity (or `claude-code` if automated)

Use `docs/skills/draft-proposal.md` for the step-by-step operator protocol.

---

## Stage 4: Owner Review

Owner reviews the proposal in `proposals/queue/`. See `docs/change-review-lifecycle.md` for the full review protocol.

On approval:
1. Apply the change to `users/cici/governed-state/<surface>/`
2. Move proposal to `proposals/approved/`
3. Record the decision in `proposals/events/event-log.json`

---

## Stage 5: Optional Runtime Back-Propagation

After approving a governed-state change, optionally update Supabase to reflect the new canonical truth.

This is not required. The governed-state files are canonical regardless of whether Supabase reflects them.

When back-propagation is appropriate:
- The governed change affects how the MCP server should behave
- A new tag taxonomy should be applied to existing memories
- An updated capture policy should influence future `upsert_thought()` calls

Back-propagation is **manual** in Phase 1 and Phase 2. Future phases may automate this.

---

## Stage 6: Dossier Generation

After any approved promotion, generate a dossier:

```bash
python3 scripts/generate-dossier.py --instance cici
```

The dossier summarizes:
- What governed-state surfaces are active vs. stub
- What proposals were approved in the last N days
- What evidence is pending synthesis
- What synthesis is pending proposal

This gives a quick health check on the state of the governed formation pipeline.

---

## What Should NOT Be Promoted

- High-frequency operational memories (daily captures with no lasting insight)
- Session-scoped notes that were useful in the moment
- Redundant or duplicative content already covered by existing governed state
- Anything with < 0.5 confidence unless the operator is deliberately exploring

When in doubt: synthesize it, review it, then decide. Don't skip straight to promotion.

---

## Related Docs

- `docs/prepared-context-doctrine.md` — Staging layer details
- `docs/change-review-lifecycle.md` — Review protocol
- `docs/skills/promote-to-governed-state.md` — Operator skill for promotion
- `docs/skills/memory-hygiene-audit.md` — How to identify promotion candidates
- `scripts/extract-evidence.py` — Evidence extraction script
- `scripts/generate-dossier.py` — Dossier generator
