---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/trials
title: Trials
narrator: the session that started a trial
group: guarantees
rests_on: [design-decision/the-session-keeps-the-gate, design-decision/the-v3-agents, design-decision/workflow-capabilities-are-guarantees]
language: codified-2
retired: [g1, r1, g2, r2, g3, r3, g4, r4, g5, r5]
unbuilt: []
---

# Trials

## Purpose
Runs one trial and records what it measured: the agent `trial-runner`, started by a session with a plugin tool or
`work run` to run on a real target or a fixture repository and what to measure. It is not a fix and not a review:
it changes nothing but the measurement record it writes, and what the measurement shows is for the session to
decide on. A walking skeleton (design-decision/behaviour-lines-are-ears): it grows from what using it shows.

## Terms

- **target** (noun): the real target or the fixture repository a trial runs on, with the plugin's scripts. Kind of: thing.

- **reply** (noun): the message a dispatch gives back to the session that started it. Plural: replies. Kind of: text.
- **send** (verb, action): a session gives a dispatch a thing to work on, starting the dispatch with its Agent tool. Forms: sends, sent. Frame: session sends thing to dispatch.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| target | of | trial | one |
| file | in | target |  |
| measurement | of | trial | one |

## Behaviour
### [g6] A trial is started on its target
Restates: r1@0.29.
- [r6] When a session sends a trial to `trial-runner`, `trial-runner` shall start the trial.

### [g7] A trial reads only its target
Restates: r2@0.29.
- [r7] When `trial-runner` starts a trial, `trial-runner` shall read only files in the target of the trial.

### [g8] A trial writes nothing but its measurement
Restates: r3@0.29.
- [r8] When `trial-runner` starts a trial, `trial-runner` shall write only the measurement of the trial.

### [g9] A trial ends with a measurement listing its target
Restates: r4@0.29.
- [r9] When `trial-runner` ends a trial, `trial-runner` shall write a measurement of the trial that lists the target of the trial.

### [g10] The reply lists the measurement
Restates: r5@0.29.
- [r10] When `trial-runner` writes a measurement, `trial-runner` shall write a reply that lists the measurement.

## Implementation, may change
- `agents/trial-runner.md`; its model (Sonnet) and its having no dispatch are guaranteed by role-boundaries.
- The input names a plugin tool or `work run`, a real target or a fixture repository, and what to measure. The record
  is under `.shop/records/measurements/` and names what the trial ran, on what target, and what it measured.

## Not yet
- None.

## Dropped
