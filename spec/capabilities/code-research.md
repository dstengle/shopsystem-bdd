---
id: shopsystem-bdd/code-research
title: Code research
narrator: the session that plans a batch
group: service
rests_on: [decision/scout-on-haiku-at-low-effort, decision/slice-budget-refused-by-plan]
formulated_as: features/code-research.feature
retired: []
---

# Code research

## Purpose
Reads the code and runs the system so the planning session does not have to: a Lands probe, a consequence
sweep for a decision, or one task's research. It is `code-scout`. It builds nothing and changes nothing in
the checkout.

## Behaviour
- [r1] **When** research ends, its notes are in the file the dispatch named and its reply is a few lines; the checkout is unchanged.
- [r2] **When** a Lands probe is asked, the reply gives counts of production and test modules that spell the old form, a floor rather than everything the change reaches, with the searches that found them; the notes name the modules.
- [r3] **When** a consequence sweep is asked for a decision, the notes list every place that still holds the old assumption, with the tests that execute it.
- [r4] **When** a task is researched, the notes say why each scenario is red today from a run of it, and each probe of today's behaviour with its command and what came back, marked `run`; what was concluded from reading is marked `read`.
- [r5] **When** a task is researched, the notes list the existing tests its decisions make impossible to keep, starting from the tests that execute the changed code.
- [r6] **When** a slice adds a path that skips a stage, the notes list every refusal and effect only that stage produces.
- [r7] Each count in the notes says whether it came from `refs`, `tests-of` or a text search.
- [r8] **When** a probe finds a defect in today's behaviour, the notes report it with its reproduction.
- [r9] Probes run in a scratch directory, never on the checkout's data.

## Implementation, may change
- Haiku at low effort; notes under `.superpowers/scout/<run>/`, probe files under `.superpowers/scratch/<run>/`.
- The research gives the line count and room of every module on the change's path.

## Not yet
- The scout pulls drafted work-items and leaves them researched — trigger: initiative i5 is approved.
