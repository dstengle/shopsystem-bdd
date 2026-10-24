# Plan of w120: work answer's step module passes ruff

Accepts work-queue#r15. A fix of branch review 1's F2 (w113): `tools check` exits 1 on ruff I001 in `tests/scenarios/work_queue_answer_steps.py`.

## 1. What goes green

- **work-queue#r15**, scenarios in `features/work-queue.feature`:
  - "answer with a line break in it is refused, and nothing changes" (Scenario Outline, seven rows: LF, VT, FF, CR, NEL, U+2028, U+2029);
  - "an answer of two lines to a work-item not awaiting-answer is refused as more than one line first".

  None is red today: the notes ran all 8 test nodes of `tests/scenarios/test_work_queue.py` and all pass. They stay green; the work does not turn them red and need not. The red check of this work-item is not a scenario but `tools check` on the step module: it exits 1 with `I001 Import block is un-sorted or un-formatted` at line 2 (notes 1, 6c; run). It goes green when that check exits 0.
- Deprecated scenarios retired: none (the work-item has no Retires section).

## 2. Where the change lands

- `tests/scenarios/work_queue_answer_steps.py`: remove the one surplus blank line between the import block and the `BREAKS` table, the one ruff's I001 diff names (notes 1, 7). No other change.

The researcher's set, unchanged. `scripts/workqueue_answer.py`, `scripts/work` and `tests/scenarios/test_work_queue.py` are on the path and stay untouched (the refusal already holds all seven breaks and runs before the item is found).

## 3. Decisions

None open. The work changes formatting only; nothing the narrator observes changes. r15's behaviour is already what the scenarios pin, and the ordering of refusals is the person's ruling the second scenario pins.

## 4. Tests the decisions break

None. The change is one blank line in a step module; no step, fixture or name changes. Verified from the notes: the only tests of `work answer` are the r13, r14 and r15 scenarios and their steps (section 4, by search, no map), and `test_work_queue.py` imports the step module by `import *`, which a blank line does not touch. The implementer confirms with the 8 r15 nodes and `tools check` on the file, which exit 0 after the change; the project-wide ruff run was not done by the researcher and is worth running once, without widening the file set.

## 5. Open cases

Seen by the probes, outside r15 and this work-item; left for the implementer to name (in its report), not to fix here:
- An empty answer (`""`) to an awaiting-answer item is accepted and written as an empty bullet (notes 6a).
- U+001C (and by Python's `splitlines`, U+001D, U+001E) is accepted as one line, though the test step `has_answer` reading with `splitlines` would see two (notes 6b).
