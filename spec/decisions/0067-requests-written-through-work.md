---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/requests-written-through-work
summary: "Each side writes its part of a request only through `work`, each part by its own command, the asker its lines and answers and the upstream each line outcome, its questions and the resolution, never by editing what the request is kept in; `work turn` only passes the turn, and how `work` keeps a request is its own and may change."
date: 2026-10-23
status: accepted
revisit_when: the person gives the detail of turns they reserved at the Approval of 2026-10-23
source: [observation/2026-10-23-open-initiatives-closed, observation/2026-10-21-session-keeps-the-gate]
by: "the person, 2026-10-23, approving the design note 2026-10-23-requests-and-the-context-loop-design (its Approval: \"The request is written through a tool\"); the coordinator, 2026-10-24, under the person's delegation (\"Please get everying delivered. Do not stop to ask me questions or permission.\"), answering gate B round 1 on how a turn is sealed"
---

# 0067. Requests are written through work

## Decision

In this bounded context the tool through which a request is written is `scripts/work`. The asker writes the
request's lines and its answers, and the upstream writes each line outcome, its questions and the resolution, each
explicitly through a `work` command, never by editing what the request is kept in. Each part is written by its own
command, in its side's turn only (today `work outcome` for a line outcome), and `work turn` only passes the turn to
the other side. This sealing of a turn is the coordinator's reading under the person's delegation, open to the
detail of turns the person will give later. The spec speaks of the request, not of its file: how `work` keeps a
request (today a file under its upstream's `.shop/work/requests/`) is in the capability's Implementation section and
may change.
