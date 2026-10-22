---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/trials
title: Trials
narrator: the session that started a trial
group: service
rests_on: [design-decision/the-session-keeps-the-gate, design-decision/the-v3-agents]
retired: []
---

# Trials

## Purpose
Runs one trial and records what it measured: the agent `trial-runner`, started by a session with a plugin tool or
`work run` to run on a real target or a fixture repository and what to measure. It is not a fix and not a review:
it changes nothing but the measurement record it writes, and what the measurement shows is for the session to
decide on. A walking skeleton (design-decision/behaviour-lines-are-ears): it grows from what using it shows.

## Behaviour
- [r1] **When** the `trial-runner` is started with an input naming a plugin tool or `work run`, a real target or a fixture repository, and what to measure, the `trial-runner` shall run that one trial on that target.
- [r2] **While** a trial runs, the `trial-runner` shall read nothing but the target and the plugin's scripts.
- [r3] **While** a trial runs, the `trial-runner` shall change nothing in the repository it was started in but the measurement record it writes.
- [r4] **When** the trial has run, the `trial-runner` shall write one measurement record under `.shop/records/measurements/` naming what it ran, on what target, and what it measured.
- [r5] **When** the `trial-runner` has written its measurement record, the `trial-runner` shall reply naming the record.

## Implementation, may change
- `agents/trial-runner.md`; its model (Sonnet) and its having no dispatch are guaranteed by role-boundaries (r5, r1).

## Not yet
- None.
