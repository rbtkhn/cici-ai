# Operator Skills

This directory contains portable, step-by-step operator protocols for Cici's governed-formation pipeline.

Skills are **human-readable procedures** — not code. They describe what a person (or an agent operating with human oversight) should do to accomplish a specific governed-formation task.

## Available Skills

| Skill | File | Purpose |
|---|---|---|
| Draft a Proposal | `draft-proposal.md` | Create a formal change proposal for governed state |
| Stage Evidence | `stage-evidence.md` | Extract and stage runtime memories for review |
| Review a Governed Change | `review-governed-change.md` | Evaluate and decide on a proposal in the queue |
| Promote to Governed State | `promote-to-governed-state.md` | Apply an approved proposal to governed-state surfaces |
| Memory Hygiene Audit | `memory-hygiene-audit.md` | Identify and process promotion candidates from runtime memory |

## Relationship to Cursor Rules

`.cursor/rules/operators.mdc` contains quick-reference versions of these protocols.
These docs contain the full, annotated versions.

## Relationship to Governed Workflows

When a skill becomes a stable recurring flow, it should be proposed as a canonical workflow artifact in `users/cici/governed-state/workflows/`.

Skills are operator-facing documentation. Workflow surface artifacts are Cici-canonical declarations.
