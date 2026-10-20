---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/code-research
title: Code research
narrator: the supervisor that started the researcher
group: service
rests_on: [design-decision/scout-on-haiku-at-low-effort, design-decision/worker-results-are-files, design-decision/the-file-set-is-the-claim]
retired: [r2, r7]
---

# Code research

## Purpose
Reads the code and runs the system for one drafted work-item, so that its planner does not have to: why each
accepted scenario is red today, what the system answers today, the tests the change would break, and the file set
that becomes the work-item's claim. It is `code-scout`, started by `work run` on a `drafted` work-item. It builds
nothing and changes nothing in the checkout.

## Behaviour
- [r1] **When** research ends, the researcher shall leave its notes in the notes file and the file set in the result file its brief names, and the checkout unchanged.
- [r4] **When** a work-item is researched, the researcher shall say in the notes why each scenario it accepts is red today, from a run of it.
- [r3] **When** a requirement the work-item accepts changes or replaces one that existing code relies on, the researcher shall list in the notes every place that still makes the old assumption, with the tests that execute it.
- [r5] **When** a work-item is researched, the researcher shall list in the notes the existing tests its accepted requirements make impossible to keep, starting from the tests that execute the code those requirements change.
- [r6] **When** a work-item adds a path that skips a stage, the researcher shall list in the notes every refusal and effect only that stage produces.
- [r8] **When** a probe finds a defect in today's behaviour, the researcher shall report it in the notes with its reproduction.
- [r9] The researcher shall run every probe in a scratch directory, on none of the checkout's data.
- [r10] The researcher shall name in the result's file set every production and test file the work-item must change for its scenarios to pass and for everything that passes today to keep passing, each one a search or a read showed.
- [r11] The researcher shall give in the notes each module on the change's path with its line count and its room under the size limit `CLAUDE.md` states.
- [r12] **If** the researcher cannot do what its brief asks, then the researcher shall stop with the result `NEEDS_CONTEXT`, saying why, and change nothing.

## Implementation, may change
- Haiku at low effort; the notes are `notes.md` in the stage's run directory; probe files under `.shop/scratch/<run>/`.
- `tools refs`, `tests-of` and `untested` first, a text search for what is not a name.
- In the notes, each probe gives its command and what came back, marked `run`; what was concluded from reading is
  marked `read`; each count says whether it came from `refs`, `tests-of` or a text search.
- The result's status is `DONE` or `NEEDS_CONTEXT`, and its summary is under fifteen lines.

## Not yet
- None.
