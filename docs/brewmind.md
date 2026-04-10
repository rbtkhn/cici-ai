# BrewMind × Open Brain

This document explains what BrewMind is, how it relates to this Open Brain instance, and how the two work together in practice.

---

## What Is BrewMind?

BrewMind is Xavier's café and learning-brand business. It lives publicly at [brewmind.cafe](https://brewmind.cafe) and is built and maintained in the [`xavier-x01/brew_mind`](https://github.com/Xavier-x01/brew_mind) repository (HTML / GitHub Pages).

BrewMind is the **public-facing layer** — the brand, the site, the products, the content.

Open Brain is the **private thinking layer** — the memory stack behind the scenes that any connected AI can search and write to.

---

## How They Fit Together

```
BrewMind (public)          Open Brain (private)
──────────────────         ──────────────────────────────
brewmind.cafe         ←→   xavier_self instance docs
brew_mind repo             open-brain-xavier fork (server)
Brand / content            Captured thoughts, decisions, context
```

They are **deliberately separate systems** — no BrewMind files live inside `open-brain-xavier`, preserving upstream compatibility. The connection is through **habit and the MCP capture workflow**, not shared code.

---

## The Capture Habit

Whenever an AI session touches BrewMind — a new idea, a brand decision, a lesson learned, a content draft — that insight gets saved to Open Brain using the `capture` MCP tool. This builds a searchable, growing memory of everything that has shaped BrewMind over time.

Examples of things worth capturing:

- "Decided the BrewMind homepage hero copy should lead with the learning angle, not the café angle."
- "Researched GitHub Pages custom domain setup — pointed brewmind.cafe via CNAME."
- "Content idea: a weekly 'brew note' format — short, conversational, one insight per post."

### How to capture (any connected AI client)

```
capture: "Your thought here"
```

To tag it as BrewMind-related, include context in the text:

```
capture: "[BrewMind] Decided to use a dark roast color palette — #2C1A0E as primary."
```

---

## What Stays Separate

| Belongs in Open Brain (`xavier_self`) | Belongs in BrewMind (`brew_mind`) |
|---|---|
| Private decisions and rationale | Public site content |
| Research notes and learnings | HTML / CSS / assets |
| Brand strategy thinking | Pages deployment config |
| AI session context | Anything a visitor would see |

---

## Links

| Resource | URL |
|---|---|
| BrewMind public site | [brewmind.cafe](https://brewmind.cafe) |
| BrewMind repo | [xavier-x01/brew_mind](https://github.com/Xavier-x01/brew_mind) |
| Open Brain fork | [xavier-x01/open-brain-xavier](https://github.com/Xavier-x01/open-brain-xavier) |
| Instance docs | [xavier-x01/xavier_self](https://github.com/Xavier-x01/xavier_self) |
| Upstream Open Brain | [NateBJones-Projects/OB1](https://github.com/NateBJones-Projects/OB1) |
