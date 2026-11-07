---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/trials
title: Trials
narrator: the session that started a trial
group: guarantees
rests_on: [design-decision/the-session-keeps-the-gate, design-decision/the-v3-agents, design-decision/workflow-capabilities-are-guarantees]
language: codified-1
retired: []
---

# Trials

## Purpose
Runs one trial and records what it measured: the agent `trial-runner`, started by a session with a plugin tool or
`work run` to run on a real target or a fixture repository and what to measure. It is not a fix and not a review:
it changes nothing but the measurement record it writes, and what the measurement shows is for the session to
decide on. A walking skeleton (design-decision/behaviour-lines-are-ears): it grows from what using it shows.

## Terms

- **target** (kind): the real target or the fixture repository a trial runs on, with the plugin's scripts. Kind of: thing.

## Behaviour

### [g1] A trial is started on its target
Restates: r1@0.29.
- [r1] When a session runs `trial-runner` on a trial, `trial-runner` shall start the trial.

### [g2] A trial reads only its target
Restates: r2@0.29.
- [r2] `trial-runner` shall read only a target.

### [g3] A trial writes nothing but its measurement record
Restates: r3@0.29.
- [r3] `trial-runner` shall write only a measurement.

### [g4] A trial ends with a measurement record naming its target
Restates: r4@0.29.
- [r4] When `trial-runner` ends a trial, `trial-runner` shall write a measurement and name the target.

### [g5] The reply names the record
Restates: r5@0.29.
- [r5] When `trial-runner` writes a measurement, `trial-runner` shall name the measurement.

## Implementation, may change
- `agents/trial-runner.md`; its model (Sonnet) and its having no dispatch are guaranteed by role-boundaries.
- The input names a plugin tool or `work run`, a real target or a fixture repository, and what to measure. The record
  is under `.shop/records/measurements/` and names what the trial ran, on what target, and what it measured.

## Not yet
- None.

## Dropped
