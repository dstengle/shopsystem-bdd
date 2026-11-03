---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/code-research
title: Code research
narrator: the script `work run`, which started the researcher
group: guarantees
rests_on: [design-decision/scout-on-haiku-at-low-effort, design-decision/worker-results-are-files, design-decision/the-file-set-is-the-claim, design-decision/workflow-capabilities-are-guarantees]
language: codified-1
retired: []
---

# Code research

## Purpose
Reads the code and runs the system for one drafted work-item, so that its planner does not have to: why each
accepted scenario is red today, what the system answers today, the tests the change would break, and the file set
that becomes the work-item's claim. It is `code-scout`, started by `work run` on a `drafted` work-item. It builds
nothing and changes nothing in the checkout.

## Terms

- **probe** (kind): a command the researcher runs to see today's behaviour, in a scratch directory and on none of the checkout's data.
- **defect** (kind): a fault in today's behaviour that a probe shows, with its reproduction.
- **old assumption** (kind): a place in the code that relies on a requirement the work-item changes or replaces, with the tests that execute it.
- **skipped effect** (kind): a refusal or an effect that only a step of today's processing produces, where a work-item adds a path that skips the step.
- **module** (kind): a Python file of the repository's code or tests.
- **line count** (kind): the number of lines of a module and its room under the size limit `CLAUDE.md` gives.
- **of** (relation scenario → work-item): a scenario of a requirement the work-item accepts.
- **of** (relation line count → module): the line count of a module.
- **broken by** (relation test → work-item): an existing test the work-item's accepted requirements make impossible to keep.
- **changed by** (relation file → work-item): a production or test file the work-item must change for its scenarios to pass and for everything that passes today to keep passing.
- **in** (relation probe → worktree): a probe run on a worktree's files.

## Behaviour

### [g1] Research ends with a result naming the file set
Restates: r1@0.29, r10@0.29, r11@0.29.
- [r1] When the researcher ends a `research` stage, the researcher shall write a result.
- [r2] When the researcher ends a `research` stage, the researcher shall write a file set.
- [r3] When the researcher ends a `research` stage, the researcher shall name every file changed by the work-item.
- [r4] When the researcher ends a `research` stage, the researcher shall write the line count of every module.

### [g2] The researcher changes nothing in the worktree
Restates: r1@0.29.
- [r5] The researcher shall not change a file in a worktree.

### [g3] Research reruns every scenario the work-item accepts
Restates: r4@0.29.
- [r6] When `work run` starts a `research` stage, the researcher shall rerun every scenario of the work-item.

### [g4] Research lists what the work-item's requirements break
Restates: r3@0.29, r5@0.29, r6@0.29.
- [r7] When `work run` starts a `research` stage, the researcher shall list every old assumption.
- [r8] When `work run` starts a `research` stage, the researcher shall list every test broken by the work-item.
- [r9] When `work run` starts a `research` stage, the researcher shall list every skipped effect.

### [g5] A defect a probe finds is written down
Restates: r8@0.29.
- [r10] When a probe finds a defect, the researcher shall write the defect.

### [g6] Probes run outside the checkout's data
Restates: r9@0.29.
- [r11] The researcher shall not start a probe in a worktree.

### [g7] A researcher that cannot do what its brief asks changes nothing
Restates: r12@0.29.
- [r12] If the researcher refuses a brief, then the researcher shall write a result that is `NEEDS_CONTEXT`.
- [r13] If the researcher refuses a brief, then the researcher shall write a reason.
- [r14] If the researcher refuses a brief, then the researcher shall change nothing.

## Implementation, may change
- Haiku at low effort; the notes are `notes.md` in its stage directory; probe files under `.shop/scratch/<stage directory>/`.
- `tools refs`, `tests-of` and `untested` first, a text search for what is not a name.
- In the notes, each probe gives its command and what came back, marked `run`; what was concluded from reading is
  marked `read`; each count says whether it came from `refs`, `tests-of` or a text search. A scenario's being red
  today is said from rerunning it.
- The result's outcome is `DONE` or `NEEDS_CONTEXT`, and its summary is under fifteen lines.

## Not yet
- None.

## Dropped
