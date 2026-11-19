---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/hooks-are-a-driving-adapter
summary: "Claude Code's SessionStart and UserPromptSubmit hooks drive notifications; hooks/hooks.json and cli.toml's hook entries are their contract, and a hook never fails the session."
date: 2026-11-19
status: accepted
tier: judgement
---

# 0103. Hooks are a driving adapter

## Decision

Claude Code's SessionStart and UserPromptSubmit hooks drive the domain's notifications (a session starts, a prompt is sent). hooks/hooks.json and the entries of spec/adapters/cli.toml with `hook =` are their contract; a hook never fails the session it runs in.
