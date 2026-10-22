---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-session-keeps-the-gate
summary: "The session the person talks to keeps the gate and decides from short replies, while rounds, a trial-runner and work run do the work in files."
date: 2026-10-22
status: accepted
source: [initiative/i16, observation/2026-10-21-session-keeps-the-gate, design-decision/the-v3-agents]
by: "the person, 2026-10-22, delegating the drafting decisions to the coordinator's recommendations"
---

# 0059. The session keeps the gate

## Decision

The session the person talks to keeps the gate and decides; the work is done by dispatches and scripts. An agent
the session dispatches replies in a few lines and leaves the rest in files, and the session reads a file only to
decide. `initiative-round` gains the job `gate`, which writes the gate page's data as files under
`<drafts path>/gate/` that the session publishes; the session reads the person's answers, not the drafts, and the
job `apply` applies exactly the approved drafts. A new agent, `trial-runner` (Sonnet, no dispatch), runs one trial
of a plugin tool or `work run` and writes one measurement record under `.shop/records/measurements/`. A fix to
code that a review or a trial finds is a work-item delivered by `work run`; a new scenario or a new examples row it needs is written by
the `feature-formulator` through a `formulate` round, never by the implementer. Each initiative keeps one
ledger, `.shop/scratch/run/ledger-<initiative>.md`, one line an event, archived under `.shop/records/archive/` when
`work run` exits with every work-item of the initiative `green` or `withdrawn`.
