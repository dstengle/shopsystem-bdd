---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-122/review-1
kind: review
batch: batch-122
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/145
head: 6f25879161015a62823474b6e0427a81a8f56fe8
range: 2e389faa94e8b211d2743af137e0f3ee0c24eb10..6f25879161015a62823474b6e0427a81a8f56fe8
result: clean
---

# batch-122 review 1

## Verdict

The batch builds every line of b705, b702 and b703, and b709's operation table names `--reply`. All five runs exit 0, as they did at the base. Nothing needs fixing before the merge. There are three observations: r152's wording says more than the poll does, the reference page leaves out `look at failure`, and the change is over the size limit.

## Findings

### f1 Minor observation: r152 obliges `build task` even when one running task is built, where the poll answers `finish task`
- item: b702
- where: scripts/batch_next.py:955
r152 says that with two running tasks and no failed task, the poll returns `build task` and every running task. It does not require that no running task is built yet; the r145 it retires did ("holds no kept change that cites the item"). `pick` returns `finish task` with the one built task whenever any running task is built (lines 955-958). It returns `build task` only when none of them is built.

So with two running tasks, one built, r152 asks for `build task` with both, and the code returns `finish task` with one. r144 asks for `finish task` in the same state, so the two lines both apply there. `spec logic` does not report a clash, because the two lines return two different batch steps.

b702's notes make this call on purpose: finish task comes first, and the readiness bar could write no scenario for a "no kept change cites the item" condition. The code follows those notes and r144, so this does not hold the merge.

Suggested follow-up: a later item retires r152 with a line that excludes built tasks, once the grammar can generate a scenario for that condition.

### f2 Minor observation: the commands reference leaves out `look at failure` and `fix task`
- item: b703
- where: docs/reference/commands.md:60
This batch rewrote the paragraph on `shop work batch next`, but its list of instructions and its order ("stop, review change, fix finding, park item, finish task, build task, prepare task, submit batch") still have neither `fix task` (b696) nor the new `look at failure` (b703). The module docstring and the CLAUDE.md row for `scripts/batch_next.py` give the full order.

Line 65 of the rewritten paragraph also runs past the page's wrap width.

The report text of `look at failure` (scripts/batch_next.py:990) tells the driver to fix "the task of the item that broke them". The step is only given when no task's item is found to have broken them.

### f3 Minor observation: the change is over the review size limit
- item: -
- where: -
`## Size` gives 36 files, +1049 -199 against a limit of 1000 changed lines.

- b705 makes most of it: `scripts/backlog_relied.py`, `tests/scenarios/readiness_handlers_port.py`, `tests/scenarios/drafting_handlers_relied.py`, `tests/scripts/test_backlog_relied.py` and the section, render and renumber changes.
- b702 and b703 make most of the rest: `scripts/batch_next.py`, the poll's handlers and scenario worlds, and the corpus blocks.
