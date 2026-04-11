# Template–Instance Contract

**Version:** 1.0
**Applies to:** All instances created from `users/_template/`

---

## What the Template Is

`users/_template/` is the **reusable constitutional scaffold** for Cici-style governed instances.

It provides:
- The standard surface layout (identity, voice, memory-policy, workflows, tools, source-priority, runtime-bridges)
- A `seed_intent.json` with all required fields documented
- A `seed-phase/` directory with readiness criteria and status tracking
- An identity surface with a `README.md` explaining what to create
- A `surface-map.json` stub ready to be filled in

A live instance (like `users/cici/`) is a **filled-in, evolved version** of this template.

---

## What the Contract Guarantees

By copying the template, a new instance **inherits**:

1. **The surface layout** — 7 named governed-state domains, with consistent IDs and purposes
2. **The proposal lifecycle** — proposals target surfaces by ID; `proposals/schemas/proposal.schema.json` is shared
3. **The seed phase protocol** — `readiness-criteria.json` defines the same 9 required criteria
4. **Validator compatibility** — `scripts/validate-governed-state.py` checks the new instance automatically
5. **CI integration** — the GitHub Actions workflow covers all instances under `users/`

---

## Template vs. Live Instance

| Aspect | Template (`users/_template/`) | Live Instance (`users/cici/`) |
|---|---|---|
| Purpose | Reusable scaffold | Specific person's live instance |
| Placeholders | All `<placeholder>` values | All real values |
| Seed phase status | `pending` | `active` or `complete` |
| `_instructions` fields | Present | Removed |
| Governed-state artifacts | None | Accumulates via approved proposals |
| Runtime connection | None | Supabase active |
| Surface map status | All `stub` | Identity `active`; others fill over time |

---

## How to Create a New Instance

```bash
cp -r users/_template users/<your-instance-id>
```

Then follow `docs/seed-phase.md` for the complete initialization walkthrough.

Key steps:
1. Replace all `<placeholder>` values in `seed_intent.json`
2. Remove all `_instructions` fields before committing
3. Create `governed-state/identity/instance.json`
4. Update `governed-state/surface-map.json` with your instance ID
5. Update `seed-phase/status.json` and `readiness-criteria.json`
6. Run `python3 scripts/validate-governed-state.py`
7. Commit with `git commit -m "seed: initialize <id> instance"`

---

## Consuming Template Upgrades

When the template evolves (new surfaces added, schema changes, new readiness criteria), existing live instances should incorporate relevant upgrades.

### How to consume a template upgrade

1. Check what changed in `users/_template/` (via git diff or PR review)
2. For each change, decide:
   - **Structural addition** (new surface, new readiness criterion) → copy the new scaffold to your instance
   - **Policy change** (updated README, revised doctrine) → review and adopt if applicable
   - **Schema change** (new required field in `surface-map.json`, new proposal field) → update your instance's files
3. Create a proposal if the adoption changes governed state materially
4. Update your `seed-phase/status.json` and/or `seed-phase/readiness-criteria.json` if criteria changed

### What does NOT require adoption

- Template placeholder text improvements (no functional change)
- Example or illustration content added to template READMEs
- Changes to `_instructions` helper text

---

## Instance Isolation

Each live instance under `users/` is:
- **Isolated**: its governed state is its own; one instance's proposals don't affect another
- **Self-validating**: the CI validator checks all instances independently
- **Additive**: adding a new instance to `users/` doesn't affect existing ones

Multiple instances can coexist in this repo. Each forks of this repo should typically have exactly one live instance.

---

## Divergence from Template

Live instances WILL diverge from the template over time as governed state accumulates. That is expected and correct.

The template defines the **schema and scaffold**. The live instance defines the **content and truth**.

Divergence is not drift — it is evolution.

---

## Related Docs

- `docs/seed-phase.md` — Full initialization walkthrough
- `docs/seed-phase-readiness.md` — Readiness model
- `users/_template/README.md` — Template-specific instructions
- `docs/governed-state-doctrine.md` — Why this system exists
