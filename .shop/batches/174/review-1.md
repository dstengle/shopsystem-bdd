---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-174/review-1
kind: review
batch: batch-174
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/196
head: b406c968fe932620fbaccc532e4e1c1d3f0549c7
range: 04ac1fb634d196a17a6398dd18d0445190ca8bb1..b406c968fe932620fbaccc532e4e1c1d3f0549c7
result: clean
---

# batch-174 review 1

## Verdict

The batch builds b876's one line, measurement#r13. `work batch start` times each phase of the opening and keeps it as a `phase` timings line. `batch_timings.figures` reads back the last opening's phases. `measure batch` returns them in its figures, each with its duration, and keeps them in its record, since `**timed` is spread into the record. `measure show` prints them as a table of their own. No test is removed or weakened: the one equality changed in `test_batch_timings` only adds the new `opening_phases` key. The `.feature` change is the generated one; `features generate --check` exits 0. Every run exits 0. The size is within the limit. Nothing goes against a judgement decision or `CLAUDE.md`. There are two observations and nothing to fix now.

## Findings

### f1 Minor observation: the module map says `measure compare` prints the opening phases, which it does not
- item: b876
- where: docs/reference/modules.md:253
The new `batch_timings.py` row says `opening_phases` is read back by `measure batch`, "which `measure show` prints (the opening phases a table of their own, b876) and `measure compare` prints". I read `scripts/measure_batch_show.py:100-101`: the compare rows still name only test time and opening time, and no `opening_phases` entry is there. No line asks compare to print phases, so the code is right and the row overstates it. Fix: change the row to say only `measure show` prints the phases.

### f2 Minor observation: the stopwatch test's upper time bounds may fail under the suite's parallel load
- item: b876
- where: tests/scripts/test_phases.py:18
The test asserts `0.04 <= found["pick"] < 0.1` after `time.sleep(0.05)` and `found["compile"] < 0.3` after 0.15 s of sleep. With 32 xdist workers on a loaded machine, a sleep can overrun 0.1 s by more than 50 ms, and the test then fails although the code is right. Fix: loosen or drop the upper bounds, or mark the test `budget` so it is run again once when it fails.
