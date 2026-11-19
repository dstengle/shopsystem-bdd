---
id: model/example.org/grammar/constructs-request/decisions
area: decisions
kind: core
imports: []
---

# Decisions

## Purpose

The design-decisions a person enters.

```model
object design-decision
  attributes: title, summary (text); tier: check | requirement | judgement
  lifecycle status: accepted → superseded
  relations: supersedes → design-decision (many)

service decisions
  operation enter(title, summary, tier, draft (flag))  outcomes: done → the design-decision | refused: no tier

actor the person kind of agent
```
