---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/code-research
title: Code research
narrator: the supervisor that started the researcher
group: service
rests_on: [design-decision/scout-on-haiku-at-low-effort, design-decision/worker-results-are-files, design-decision/the-file-set-is-the-claim]
formulated_as: features/code-research.feature
retired: [r2]
---

# Code research

## Purpose
Reads the code and runs the system for one drafted work-item, so that its planner does not have to: why each
accepted scenario is red today, what the system answers today, the tests the change would break, and the file set
that becomes the work-item's claim. It is `code-scout`, started by `work run` on a `drafted` work-item. It builds
nothing and changes nothing in the checkout.

## Behaviour
- [r1] **When** research ends, its notes are in the notes file the brief names, its result file gives the file set, and the checkout is unchanged.
- [r3] **When** a requirement the work-item accepts changes or replaces one that existing code relies on, the notes list every place that still makes the old assumption, with the tests that execute it.
- [r4] **When** a work-item is researched, the notes say why each scenario it accepts is red today from a run of it, and each probe of today's behaviour with its command and what came back, marked `run`; what was concluded from reading is marked `read`.
- [r5] **When** a work-item is researched, the notes list the existing tests its accepted requirements make impossible to keep, starting from the tests that execute the code those requirements change.
- [r6] **When** a work-item adds a path that skips a stage, the notes list every refusal and effect only that stage produces.
- [r7] Each count in the notes says whether it came from `refs`, `tests-of` or a text search.
- [r8] **When** a probe finds a defect in today's behaviour, the notes report it with its reproduction.
- [r9] Probes run in a scratch directory, never on the checkout's data.
- [r10] The result's file set names every production and test file the work-item must change for its scenarios to pass and for everything that passes today to keep passing, each one a search or a read showed.
- [r11] The notes give each module on the change's path its line count and its room under the size limit `CLAUDE.md` states.
- [r12] The result's status is `DONE` or `NEEDS_CONTEXT`, and its summary is under fifteen lines.

## Implementation, may change
- Haiku at low effort; the notes are `notes.md` in the stage's run directory; probe files under `.shop/scratch/<run>/`.
- `tools refs`, `tests-of` and `untested` first, a text search for what is not a name.

## Not yet
- None.
