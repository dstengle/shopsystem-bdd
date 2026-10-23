# Review of w110: measure reads what i22 left

**Verdict: DONE_WITH_CONCERNS.** One Important finding, triaged fix now: a stage that has figures is also named as a
stage whose session.json is empty, whenever its work-item ran that stage more than once. i22's own data shows it
(w97 review).

## Commits reviewed

The branch `work/w110` is gone. The commits are those between `b07ef8f work: w110 ready -> claimed` and
`dfae804 work: w110 claimed -> done` on the checked-out history, less `work run`'s `work:` commits:

- 5d88909 measure: an empty session.json gives its stage without figures, named (r57)
- aecf1e7 measure: a transcript line is split on the newline only (r58)
- 2e956ab measure: Z times read as UTC steps, contract text, retire deprecated r47 outline (r59)

These are the same three commits the implementer's result.json lists. Every file they touch is in the work-item's
fileset. `batch_measurement_transcripts.py` was not touched, and the report says so.

## Removed and weakened tests

I searched the diff for deleted `@scenario`, `def test_`, step functions and `assert` lines, removed Examples rows,
`skip`/`xfail`, and edits to `features/`.

- **features/batch-measurement.feature: the "(deprecated)" @r47 Scenario Outline (2 examples) was removed.** It
  proved that a non-empty session.json or transcript of an unknown shape is refused, naming the file, and that
  nothing is written. The plan lists it under "Tests the decisions break". The work-item lists it under Retires
  (delivery#r17). Its binding is the `scenarios(...)` call, so removing the outline removes the binding. The live
  @r47 outline, which this commit leaves unchanged, still covers the refusal. **Allowed.**
- **batch_measurement_then_steps.py:152 `gives_totals`.** Before, it asserted stages, sessions, every token column,
  round trips, cost and time, and any table missing one of those raised KeyError. Now it asserts only the columns
  the table names. For the r42 tables, which name every column, it asserts exactly what it did before. The plan
  lists it under "Tests the decisions break". **Allowed.**
- **batch_measurement_world.py:31 `stamp`.** It now passes a full ISO time through unchanged. The plan listed this
  change on `transitions_between`; the implementer made it in `stamp` instead. The effect is the same: a clock
  time such as "10:00" is still formatted as before, so the r41/r42 scenarios assert what they did. Not a
  weakening.

No other test was removed or weakened.

## Allowances

The report's `## Tests changed under an allowance` says "none". No `setup` or `interim` row needs checking, and the
two test changes above are covered by the plan's list.

## Cannot verify

- The report's suite figure ("690 passed, 6 failed" at start) and its "8 passed" final run: I did not run the
  suite. `work run` runs it at the merge.

## Findings

### 1. Important, fix now: the "empty session.json" mark reaches every run of the same stage (w110)

**Where:** `scripts/measure_read.py:74` builds the key; `scripts/measure_build.py:43-44` matches it.

**What is wrong:** `read_session_jsons` records an empty session.json under the key
`(work-item dir, stage name without its number)`. For example, `runs/w97/5-review` becomes `("w97", "review")`.
`stages_of` then marks every start the log gives for `(work-item, stage)` with `session_json: "empty"`. A
work-item that ran a stage twice, where only one run's session.json is empty, gets both stages marked. The stage
that has its turns, tokens and cost is then also named as a stage whose session.json is empty. That contradicts
batch-measurement#r57, and the measurement gives a wrong answer.

**Why it matters:** repeated stages are common in real data. Plan stages are re-run, and reviews and implements
are re-run after a failure. Examples: w95 has 3-implement and 4-implement; w97 has 2-plan and 3-plan, and
5-review and 6-review. i22 is the initiative this work-item exists to read. Its one empty session.json is
`w97/5-review`, and `w97/6-review` is not empty.

**Reproduction:** a read-only probe, `.shop/scratch/w110-4-review/test_probe_empty_key.py`, calls
`measure_build.figures_of("i22-rulings-round-trips-query-output", root)` and prints w97's review stages. It writes
no record.

```
{"session": "835f2b57-…", "turns": null, "cost": null, "session_json": "empty"}
{"session": "5caf92b6-…", "turns": 27, "cost": 0.6072765999999999, "session_json": "empty"}
totals {"stages": 45, "sessions": 44}
```

**Fix:** tie each empty file to one stage run, not to the stage name. The n-th start the log gives for
`(work-item, stage)` is the run in the n-th `<k>-<stage>` directory, ordered by k, so pair them by that order.
A smaller fix is to give the mark only to a stage that got no figures. Then a stage cannot carry both figures and
the mark, though a stage with no figures could still take another run's mark. Add an r57 example in which the
same stage runs twice, once with an empty session.json and once with figures.

### 2. Minor, drop: the step change landed in `stamp`, not in `transitions_between` as the plan said

`tests/scenarios/batch_measurement_world.py:31`. The report notes the deviation and the effect is equivalent, so
nothing needs to change.

## Other checks

- **Code no line asks for:** none found. The `session_json: "empty"` field serves r57. The contract text in
  `scripts/measure` restates r47 and r57. `json_rows` is also used to read log.jsonl, so a U+2028 inside a log
  line is now read as one line too. That is the same reader that serves r58, not new behaviour of its own; the
  plan names it as an open case.
- **Behaviour against the Purpose and the rests_on decisions:** an empty file means a zero-byte file, and a
  whitespace-only file is still refused (plan decision 1). This agrees with 0018 measure-refuses-unknown-shapes.
  The totals follow the work-item's ruling (reading B).
- **`tools check --base b07ef8f`:**
  - ruff: All checks passed!
  - vulture: clean
  - import-linter: the project states no import contracts
- **`tools size --limit 300`:** printed nothing. The touched files are measure_read.py 141 lines, measure_build.py
  126, given_steps 226, then_steps 185 and reading_steps 50.

## Commands run

- `git log --format=%H -1 --grep="^work: w110 ready -> claimed$" work/w110`: the branch is not found, so it is gone
- `git log --format='%H %s' -1 --grep=...` for the claimed and done commits on HEAD
- `git log --format='%h %s' --stat b07ef8f..dfae804`
- `git diff b07ef8f 2e956ab`
- `git show 2e956ab:scripts/measure_build.py` (stages_of); `grep` for the log calls in `scripts/supervise*.py`
- Glob over `runs/*/*-implement/session.json`; `ls` of the w95 and w97 runs; `wc -c` of the i22 session.json files;
  `grep` of the w97 start events in i22's log.jsonl
- `python3 -m pytest -q -s -n0 -p no:cacheprovider .shop/scratch/w110-4-review/test_probe_empty_key.py`
- `python3 <Scripts>/tools check --base b07ef8f…`; `python3 <Scripts>/tools size --limit 300`; `wc -l` of the
  touched files
- `git status --porcelain`: empty
