# Cici Rename Inventory (2026-04-25)

Purpose: classify `Xavier` references so current-state text can be Cici-first while preserving historical provenance.

Canonical legacy fence phrase: **Legacy note: formerly Xavier.**

| Path | Hit snippet | Category | Action |
|---|---|---|---|
| `README.md` | `Xavier's Personal Open Brain Instance` | Active-state text | Rewrite to `cici-ai` / Cici-first and move old naming to explicit legacy note. |
| `CLAUDE.md` | `xavier_self is a personal instance` | Active-state text | Rewrite repo identity and behavioral references to owner/repo-neutral wording. |
| `docs/personal/README.md` | `Xavier's Personal Goals & Workflow` | Active-state text | Rewrite as Cici operator workflow with short historical migration note. |
| `docs/seed-phase.md` | `Xavier's personal instance` | Active-state text | Rewrite to Cici instance wording; keep date continuity. |
| `docs/governed-state-doctrine.md` | (no owner-name hit) | Active-state text | No rename needed. |
| `users/cici/README.md` | `Cici — Xavier's Instance` | Historical reference | Keep for now as historical marker if it reflects archival state; add legacy note in future pass if surfaced in onboarding. |
| `docs/personal/work-journal/README.md` | `for Xavier's AI skill-building practice` | Historical reference | Keep for now; add legacy note if reused as current onboarding text. |
| `proposals/approved/*.json` and logs | reviewer fields with `Xavier` | Frozen evidence quote/title | Keep verbatim; do not rewrite immutable provenance logs. |

## Allowed containers for legacy mentions

- README rename continuity section
- Dedicated alias/migration sections
- Revision/history blocks
- Immutable evidence/proposal records

## 2026-04-30 active-state pass

The active authority layer has been migrated to Cici-first owner/operator wording in:

- `users/cici/governed-state/identity/instance.json`
- `users/cici/seed_intent.json`
- `config/authority-map.json`
- `docs/session-bootstrap-prompt.md`
- `.cursor/rules/governance.mdc`
- `.claude/modes/_shared.md`

Remaining `Xavier` references inside approved proposals, proposal event logs, examples, and historical rename notes are provenance unless a later audit classifies a specific file as current-state text.
