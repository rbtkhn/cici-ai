# Seed Phase Readiness Model

**Version:** 1.0
**Applies to:** All instances in this repo

---

## What Is Readiness?

A Cici instance is "fully seeded" when it has established its foundational governed state and is structurally ready for ongoing operation and change review.

Readiness is not about runtime performance — it is about whether the governance skeleton is in place.

---

## Readiness Levels

| Level | Score | Meaning |
|---|---|---|
| `not-seeded` | 0.0–0.49 | Template not filled in. Instance cannot be used. |
| `partially-seeded` | 0.50–0.74 | Some criteria met but identity surface or validation missing. |
| `mostly-seeded` | 0.75–0.99 | Core criteria met but one required step incomplete. |
| `fully-seeded` | 1.0 | All required criteria met. Instance is ready. |

---

## Required Criteria

These must all be met for a `fully-seeded` status:

| ID | Criterion | Verified by |
|---|---|---|
| seed-001 | `seed_intent.json` filled (no placeholders, no `_instructions`) | `validate-governed-state.py` |
| seed-002 | `instance_id` matches directory name | `validate-governed-state.py` |
| seed-003 | `seed_phase_status` = `active` | `validate-governed-state.py` |
| seed-004 | `governed-state/identity/instance.json` exists and is valid | manual / future script |
| seed-005 | `governed-state/surface-map.json` exists | manual / future script |
| seed-006 | `validate-governed-state.py` passes with exit 0 | CI |
| seed-007 | All seed artifacts committed to git | git log |
| seed-008 | Runtime (Supabase) deployed and reachable | manual |
| seed-009 | At least one MCP client connected | manual |

---

## Recommended (Not Required)

| ID | Criterion | Notes |
|---|---|---|
| seed-010 | At least one test capture performed | Strongly recommended before calling the instance production-ready |

---

## Checking Readiness

Automated checks (run locally or in CI):

```bash
python3 scripts/validate-governed-state.py
```

Manual checks (not yet automated):
- Verify `governed-state/identity/instance.json` exists
- Verify `governed-state/surface-map.json` exists
- Check Supabase health: `curl "https://YOUR_PROJECT_REF.supabase.co/functions/v1/open-brain-mcp?key=YOUR_KEY"`

The instance's current readiness status is in `users/<instance>/seed-phase/status.json`.
The full criteria definitions are in `users/<instance>/seed-phase/readiness-criteria.json`.

---

## Readiness Score Calculation

```
score = required_criteria_met / total_required_criteria
```

With 9 required criteria:
- 9/9 = 1.0 → `fully-seeded`
- 8/9 = 0.89 → `mostly-seeded`
- 7/9 = 0.78 → `mostly-seeded`
- 6/9 = 0.67 → `partially-seeded`

---

## When Readiness Changes

The seed phase status is `complete` once `fully-seeded`. It does not regress.

If a capability is later removed or a bridge is decommissioned, those are governed-state changes (requiring proposals) — not seed phase regressions.

The seed phase is a **one-time initialization**. Post-seed evolution is handled through the proposal and review pipeline.

---

## New Instance Checklist

1. `cp -r users/_template users/<your-instance-id>`
2. Fill in `seed_intent.json` (replace placeholders, remove `_instructions`)
3. Create `governed-state/identity/instance.json` from `seed_intent.json`
4. Create `governed-state/surface-map.json` (copy from `_template/governed-state/`)
5. Create `seed-phase/readiness-criteria.json` (copy from `_template/seed-phase/`)
6. Run `python3 scripts/validate-governed-state.py`
7. Commit: `git commit -m "seed: initialize <id> instance"`
8. Connect runtime (see `docs/setup-guide.md`)
9. Create `seed-phase/status.json` marking all steps complete

See `docs/seed-phase.md` for the full walkthrough.
