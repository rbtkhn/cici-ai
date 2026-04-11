# Identity Surface

The identity surface is the most foundational governed-state domain for the Cici instance.

## Purpose

This surface holds canonical truth about **who Cici is**: the instance record, ownership, purpose, declared capabilities, operational bridges, and related project relationships.

Everything in this surface defines what Cici fundamentally *is* — not what it does operationally, not its communication style, not its memory policy. Those belong to other surfaces.

## Contents

| File | Description |
|---|---|
| `instance.json` | Canonical instance record: id, owner, purpose, capabilities, operational bridges, related projects |

## What changes require a proposal

Any change to `instance.json` that modifies:
- Instance purpose or scope
- Declared capabilities
- Operational bridge status
- Relationship to related projects

Typo corrections and minor factual clarifications do not require proposals.

## What does NOT belong here

- Communication style or tone → `voice/`
- Capture and retention rules → `memory-policy/`
- Recurring operator flows → `workflows/`
- Tool configs and MCP settings → `tools/`
- Bridge rules and policies → `runtime-bridges/`
