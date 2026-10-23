# Branch review 2 of i22-rulings-round-trips-query-output

**Verdict: DONE.** The suite is green and every check passes. None of the findings is Critical or to be fixed now. Branch review 1's two Critical findings (C1, C2) and its fix-now finding (I1) are resolved, and so are I2, M1, M2, the put-back observation, the refactor observation and the Python-version noqa. The new findings are five Minor observations; one more is carried over from review 1.

## Range

`dc9ece7..5d25307` on `next`: 136 commits. The 17 since review 1's head (55b4057) are a1ff464..5d25307.

Work-items:
- **Through `work run`, from claimed to done:**
  - w94: a207018, 6212f6f, cd39016
  - w96: 2bf920a
  - w97: 625728c
  - w99: 52141df
  - w100: 7de9e66, 22f7453
  - w100's review fix 6512979 was merged in 4103de4 from `work/w100-fix`, after `done -> awaiting-answer` and before `work answer`'s `-> done`. Its Answers attribute it to w100.
- **Merged by hand and withdrawn** (attributed by their merge commits and `## Delivered`, as in review 1):
  - w91: 8f57ccb, f460299 → 6eb48a9
  - w92: adf0d01, 79cc5a1 → 49dd8e6
  - w93: 5eb628a → 58da176
  - w95: 583db74, e6d39e2, 61e6706 → a7a04ab
  - w98: cca993a, 42a13da, ffbbabd → 0218152

## Suite

`Suite: 693 passed, 0 failed at 5d25307 in 13.5 s` (1 skipped, 56 subtests passed; pytest reported 13.24 s).
- **Parallel:** yes. `pytest.ini` has `addopts = -n auto`.
- **In-process:** only in part. The batch-measurement steps call `measure`'s `main` in-process; the other capabilities' steps run the scripts as subprocesses.
- The suite is under 60 s, so this is no finding.
- **Count against review 1's 699:** −3 (`AVersionFileThatHoldsNoVersion`), −1 (deprecated @r42), −3 (deprecated @r9 examples), +1 (@r15) = 693.

## Checks

- **w98's check, `tools check scripts tests`:**
  - ruff "All checks passed!"; vulture "clean"; import-linter "the project states no import contracts". Exit 0.
  - It was run as `python3 <Scripts>/tools check scripts tests`, from the worktree, so the worktree's `ruff.toml` applied. Running the worktree's own `scripts/tools` needed approval.
  - I read both `tools_check.py` files and they are line for line the same, so this counts as verified.
  - No other work-item names a check.
- **`tools check --base dc9ece7`:**
  - ruff: All checks passed!
  - vulture: clean
  - import-linter: "the project states no import contracts". The project has no contracts; this is not `missing`.
- **`tools size --limit 300`:** printed nothing, exit 0. No file is over the limit, touched or not.
- **`features deprecated`:** two scenarios, both already deprecated at Base and outside this initiative:
  - migration-tools @r15 "`migrate run` on a repository with <change> refuses…"
  - work-queue @r1 "add with --part-of, --under and --accepts…"

  The batch-measurement @r42 and work-queue @r9 scenarios that review 1 named (M1, M2) are retired.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run and real mode:** the branch adds or changes no operation that has both modes. No agreement test is owed.

## Removed and weakened tests

**What I searched for in `git diff dc9ece7 HEAD -- tests features`:**
- added `skip` or `xfail`: none
- removed `def` lines: the seven review 1 named, each rewritten in place
- 18 removed `assert` lines: review 1 accounted for each, at its items 5-12
- scenarios removed from `features/`

**For the commits since review 1:**
- **`tests/scripts/test_migrate_upgrade.py::AVersionFileThatHoldsNoVersion`**, 3 tests, removed by w100 (22f7453).
  - What they proved: `status`, `upgrade` and `status --hook` on a version file holding "next" or nothing. They refused and changed nothing, and the hook printed one line and exited 0.
  - Listed in w100's plan §4 (decision 7, the ruling). Holds.
  - Its "nothing" case is now untested: N1.
- **The deprecated batch-measurement @r42 scenario**, retired by w100. Listed in w100's Retires and plan §4. Holds.
- **The deprecated work-queue @r9 outline** (add, retry, withdraw), retired by w100. Listed in w100's Retires and plan §4. Holds. The live @r9 outline still covers those commands and `answer`.
- **`batch_measurement_then_steps.gives_totals`:** strengthened, not weakened. The `if column in wanted` guard is gone (I2).

**Review 1's list, re-checked against the records added since:**
- w92's seven retired supervision scenarios are now listed in w92.md's `## Retires`, @r26 and @r37 among them (63f190e). C1 is resolved.
- w95's retired @r11 outline is now listed in w95.md's `## Retires`. C2 is resolved.

## Allowances

| Work-item | Row | Verified |
|---|---|---|
| w100 | "none" | Holds. Every test change is plan-listed or a retirement the Retires section lists. |
| w94 | `gives_totals`: interim | Review 1's I2: the row still claims more than it holds. The test change it covered is undone, because `gives_totals` is strict again, so the row no longer covers any change. No finding remains. |
| w94, w95, w92, others | as in review 1 | Unchanged since review 1. The rows that held still hold. |

## Cannot verify

- **The probes were not run.** `.shop/scratch/i22-rulings-round-trips-query-output-branch-review/probe.py` needed approval, and a one-line `python3 -c` check of `fromisoformat` did too. Its cases were:
  - `work answer` with `\n`, with `\r`, with no log line, with U+2028, with a form feed and with one line
  - `migrate upgrade` with a later step that raises `ValueError`

  N2, N3 and N4 and the put-back check below are therefore read from the code at the lines named. None of their outputs comes from a run. None is a check a work-item names.

## Findings

No Critical finding, and none to be fixed now. This is the re-review after the fix work-item w100, so anything but invalid data, the system's own fault on input, or a write where a refusal belongs is an observation.

### Review 1's findings
- **C1 (w92, Retires):** resolved in 63f190e.
- **C2 (w95, Retires):** resolved in 63f190e.
- **I1 (w91, refusing a newline):** resolved.
  - work-queue r15 is now the line (spec/capabilities/work-queue.md:31).
  - Its scenario is at features/work-queue.feature:213-219, bound by w100 in 7de9e66 and green.
- **I2, M1, M2:** resolved by w100 (22f7453).
- **The put-back:** resolved. `scripts/migrate_upgrade.py:149` catches `Exception` with `# noqa: BLE001` and its reason (6512979).
  - The risk was that it could swallow a refusal the `try` meant to give. I read lines 132-154: the refusals inside the `try` are returned, not raised, and `KeyboardInterrupt` and `SystemExit` are not `Exception`.
  - The risk was that `git clean -fdq` could delete the person's untracked files. `uncommitted` (migrate_write.py:26-29) refuses to start on any untracked file, and `clean` without `-x` leaves ignored files alone.
- **The refactor observation:** done. The class is removed and the r30 and r31 scenarios are green.
- **The noqa at measure_read.py:16:** the `.replace` is dropped (see N4).

### N1: Minor, w100, observation: a version file holding nothing is no longer tested
- **Where:** `scripts/migrate_upgrade.py:41`, the `"nothing"` branch of `no_version`. Its only test was the removed `AVersionFileThatHoldsNoVersion` (22f7453).
- **What:** the r30 and r31 scenarios give only "next". Nothing now checks that an empty `.shop/plugin-version` refuses with "holds nothing", or that the hook's line says it.
- **Reproduction:**
  - `git show 6865b9a:tests/scripts/test_migrate_upgrade.py` shows the `("", "nothing")` subtests.
  - A grep of `features/migration-tools.feature` for the version file's text finds only "next".
  - w100's plan §5 and its report name this too.
- **Fix:** an Examples row with an empty version file in the r30 outline, through integrating-a-proposal.

### N2: Minor, w91 (bound by w100), observation: the r15 refusal is shadowed by earlier refusals
- **Where:** `scripts/workqueue_answer.py:26-30`. The newline check runs after the status check (26-27) and the log check (`asked_from`, 28).
- **What:** an answer of two lines gets another refusal's message in two cases:
  - to an item that is awaiting-answer but has no log line of its move: "log.jsonl gives no transition of w1 to awaiting-answer…"
  - to an item that is not awaiting-answer: "… is not awaiting-answer…"

  r15 asks for "saying that an answer is one line". Both cases still exit with an error and change nothing.
- **Reproduction:** probe case "r15 no log line", read and not run (see Cannot verify). w100's plan §5 names it as D2.
- **Fix:** test the answer's text first, at line 24.

### N3: Minor, w91, observation: other line breaks pass the one-line check
- **Where:** `scripts/workqueue_answer.py:29`, which checks only `\n` and `\r`.
- **What:** U+2028, U+2029, `\x0b`, `\x0c`, `\x1c`-`\x1e` and `\x85` pass the check. `Run.held` (supervise.py:199) splits on them with `str.splitlines`.
  - A continuation line does not start with "- ", so it joins its bullet and the count is unchanged.
  - An answer like `"A - B"` becomes two `## Answers` bullets. That closes a second question that was never answered (supervise.py:206-208).
- **Reproduction:** probe case "U+2028", read and not run. w100's plan names it as D1.
- **Fix:** refuse when `len(text.splitlines()) > 1`.

### N4: Minor, w100, observation: `moment` reading "Z" has no test
- **Where:** `scripts/measure_read.py:16` (22f7453).
- **What:**
  - It relies on Python 3.11's `fromisoformat` reading a trailing `Z`. The scripts need 3.11 anyway (`datetime.UTC`).
  - Claude Code's transcripts write times such as `2026-10-22T09:55:00.123Z`.
  - A grep of `tests/` for a time ending in `Z` finds none. A change back to an older reading would pass the suite.
- **Keep as a test** (tests/scripts): `measure_read.moment("2026-10-22T09:55:00.123Z", "t") == datetime.datetime(2026, 10, 22, 9, 55, 0, 123000, tzinfo=datetime.UTC)`.

### N5: Minor, no work-item, observation (records)
- **What:** these commits since review 1 belong to no work-item:
  - a1ff464: review 1's record
  - 3d23f19: w100 drafted
  - 63f190e: the r15 line and its scenario, added under `features/` by formulation, and w92's and w95's Retires
  - 2dc3aea and 71f6d6a: w100's Retires, edited by the coordinator
- **Also:** w100's lint fix (6512979, merged in 4103de4) came in outside its claimed → done.
- Review 1's M3 list stands for the commits before it.
- **Fix:** none needed for the product.

## Shape

- **Size, 300 lines (CLAUDE.md:5):** met. `tools size` printed nothing.
- **Module map (CLAUDE.md:9-28):**
  - `scripts/workqueue_answer.py`: has its row (CLAUDE.md:20). Met.
  - `scripts/migrate_upgrade.py:149`: `migrate upgrade`. Met.
  - `scripts/measure_read.py:16`: `measure`'s reading. Met.
  - `tests/scenarios/work_queue_answer_steps.py:7-18`: the r15 steps, `<capability>_*_steps.py`. Met. The step imports `snapshot` lazily from `test_work_queue`, as `work_queue_add_steps` does.
  - `tests/scripts/test_migrate_upgrade.py`: a test of the scripts that no scenario drives (the move check). Met.
- Review 1's Shape findings stand for the rest of the branch.
- **Dead code:**
  - vulture is clean.
  - `transcript_inside` (batch_measurement_given_steps.py:142) is still reached through `transcript_inside_with_trips`, as w100's report says.
  - `stages_sessions_took` still defaults turns and round trips when a table lacks them. No table lacks them any more. Observation: making it strict is complete when every `the stages' sessions took` table gives both columns and the default branch is removed with the suite green.
  - `Merge.failed_claimed`'s path to awaiting-answer (supervise_merge.py:81-91) is still reached by no scenario. It predates the branch (review 1).

## Coupling

The coupling is unchanged since review 1:
- **Claude Code's transcript store** (measure_read.py:96-110, `round_trips` and `store_dir`): relies on unpublished layout and row shape.
- **An unpinned ruff** (tools_env.py:17) against about 400 rule codes named in ruff.toml.
- **Python 3.11:** `datetime.UTC`, and now `fromisoformat` reading `Z` (N4). The "older Pythons" comment is gone.

## Observations

Each one is read from the code; the probe needed approval (see Cannot verify).

- **N1** (w100): an empty version file is untested. Reproduction: `git show 6865b9a:tests/scripts/test_migrate_upgrade.py`, then a grep of features/migration-tools.feature for the version text, which finds only "next".
- **N2** (w91/w100): a two-line answer to an item with no log line says "log.jsonl gives no transition…", not "an answer is one line". Reproduction: probe.py case "r15 no log line" (`work answer w1 $'a\nb'` with no log.jsonl).
- **N3** (w91): `work answer w1 $'A - B'` is accepted and becomes two `## Answers` bullets under `Run.held`. Reproduction: probe.py case "U+2028".
- **N4** (w100): no test gives `moment` a "Z" time. Keep as a test: the assertion in N4.
- **Carried from review 1** (w91/w92): one answer to an item with two questions returns it to its stage with the second question still open (supervise.py:206-208). Reproduction: `work answer w1 "Only the first"` on an item whose `## Questions` has "First?" and "Second?".
- **Carried from review 1** (w94): a session in several project directories reads the first one sorted (measure_read.py:101-104).
- **Carried from review 1** (w99): held text with a newline in it breaks the hook's one line (migrate_upgrade.py:41, 77).
