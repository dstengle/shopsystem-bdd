---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-75/review-1
kind: review
batch: batch-75
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/99
head: 1dfaa7c801ff87c7cae07efb69d7847a04a3e2cd
range: 35a5cb0905e02970e9ca9a5a34dc9b925192e836..1dfaa7c801ff87c7cae07efb69d7847a04a3e2cd
result: clean
---

# batch-75 review 1

## Verdict

The batch builds both items. b69's `work batch reopen` keeps the person's findings file as the batch's next review and sets the batch to `building`. A batch in any other state is refused, naming it. b73's `measure batch` returns each test run's duration and the opening time, along with the figures r1 already returned. r12 retires r1 properly: the id is in `retired:`, and the corpus block, the feature scenario and the cli.toml annotation are all replaced. The runs are clean, and the change is within the size limit and the 300-line rule. The module map has rows for both new modules and for the new test handler. Nothing is to fix now; there are four observations.

## Findings

### f1 Minor observation: no test shows that `work batch done`, `review` or `start` record a timing
- item: b73
- where: tests/scenarios/telemetry_handlers.py:144
The scenario for measurement#r12 writes its test runs and opening time itself, through `batch_timings.kept` in `keep_timings`. `tests/scripts/test_batch_timings.py` tests only the module. A search of `tests/` for `timings`, `test_runs` and `opening_time` finds only those three files. So removing the `batch_timings.timed(...)` wrappers from `scripts/batch_tasks.py:507`, `scripts/batch_review.py:143` and `scripts/batch_base_merge.py:57`, or the `kept(... "opening" ...)` call at `scripts/batch_start.py:485`, would break nothing in the suite. A merged batch would then measure with no test runs while every test still passes. Hardening: add a script test that runs `work batch done` on a task (the batch test templates already exist) and checks for one `done` entry with that task, and the same for `review` and `opening`.

### f2 Minor observation: a batch with no recorded timings shows a test time of "0 seconds"
- item: b73
- where: scripts/batch_timings.py:86
The timings live only in `<git common dir>/shopsystem-bdd/timings.jsonl` and are never committed. A batch measured in another clone, or delivered before this release, gets `test_runs: []`, `test_time_seconds: 0` and `test_time: "0 seconds"`. That reads the same as a batch whose tests took no time. `measure compare` then shows "0 seconds" beside a real figure, though its ratio is safely `-` (`measure_show.ratio` returns `-` when the first value is falsy). The opening time already uses None when nothing was recorded. The test time could too, when there are no runs, so that a comparison made under design-decision 0079 is not misread.

### f3 Minor observation: the opening time includes the wait for the batch lock
- item: b73
- where: scripts/batch_start.py:475
`began = time.monotonic()` is set before `with locked(root):`. A `work batch start` that waits for another batch command's lock counts that wait as opening time. The vocabulary defines opening time as the readiness check, the lay and the scenario run. Starting the clock inside the lock would match that definition.

### f4 Minor observation: `reopen` makes the pull request a draft before its commit, and its extra refusals are untested
- item: b69
- where: scripts/batch_reopen.py:419
`gh pr ready --undo` runs before `batch_plan.commit`. If the commit fails, the pull request is a draft while the batch is still `awaiting-merge` with no review recorded. `work batch reviewed` follows the same gh-then-commit order, so the risk is the same as there. The refusal of a findings file with no `fix now` finding (`scripts/batch_reopen.py:396`) and of a missing file have no test. Neither does the draft step: only r11's review and status and r12's refusal are covered.
