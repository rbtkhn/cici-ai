# Cici Instance — Operator Goals and Workflow

This document describes how the current cici-ai operator uses Open Brain alongside BrewMind and what this stack supports long-term.

**Legacy note: formerly Xavier.** Historical repository names, branch names, and older examples may still appear in archived sections below.

---

## Who This Is For

This is a private working document for the instance owner/operator. It is committed to version control so context is not lost between AI sessions, and it contains **no secrets**.

---

## Goals

### 1) BrewMind growth support
[BrewMind](https://brewmind.cafe) is the business context associated with this instance. Open Brain acts as the durable memory layer for:
- capturing ideas, decisions, and lessons learned
- storing voice notes, drafts, and research that connected AI clients can retrieve
- building a searchable history of what was tried and why

### 2) Consistent capture into Open Brain
Any insight worth keeping from conversation, AI sessions, or real-world experience should be captured through the MCP flow so future sessions have better context.

### 3) Safe key handling
Secrets (Supabase keys, MCP access key, OpenRouter key) stay only in:
- Supabase project secrets
- a local password manager or `.env` file excluded by `.gitignore`

Never commit credentials.

---

## Repository map (current)

| Repo | Purpose |
|---|---|
| [`rbtkhn/cici-ai`](https://github.com/rbtkhn/cici-ai) | Active instance workspace: docs, governance, and governed-state scaffolds |
| [`NateBJones-Projects/OB1`](https://github.com/NateBJones-Projects/OB1) | Upstream Open Brain runtime |

---

## Legacy compatibility notes

- Older docs may reference legacy repos/branches such as `xavier_self`, `open-brain-xavier`, or `xavier/*` branch names.
- Treat those labels as historical migration context, not current-state naming.
- Preserve legacy labels only when they are needed for provenance or backtracking old artifacts.
