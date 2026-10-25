# Branch review of i33

**Verdict: DONE.** No finding is triaged fix now and none is Critical. Every work-item's check was run and passes. Two findings are Minor: one observation and one drop.

## Range

`1caef881..9482770` on `i25-review-findings-to-implementation`. This branch is shared: it also holds the work of i31 (w185, w193), i32 (its branch reviews) and i34 (spec eb30678a, features e8f5572a, w195 drafted and researched). Those initiatives have their own branch reviews. This review covers i33's commits, and runs the suite and the checks over the whole range.

i33's commits:
- spec and features rounds: `af6357e1` (apply), `f1a9ecd3` (formulate, round 8), `50addf01` (formulate, round 9, r120);
- **w192** (work-queue r31, r32, r23): `64c62951`, between `620ec316` (ready -> claimed) and `77954d18` (claimed -> done);
- **w194** (supervision r120, r121, r75, r105): `919e4510` and `6ef3162b`, between `32823806` (ready -> claimed) and `78ecb78d` (claimed -> done);
- `.shop/work`-only hand commits made under the delegation: `59ca81e1`, `13e91f83`, `6e17f0de`.

Every code commit in the range belongs to a work-item: the code commits not listed above are w185's and w193's (i31), each between that item's claimed and done commits. No commit belongs to no work-item.

## Suite

`Suite: 913 passed, 9 failed at 9482770 in 28 s`. That is the full `python3 -m pytest -q -rfEx` (wall time 28 s by `date +%s`; pytest reports 28.33 s).
- It runs in parallel: pytest.ini has `-n auto`.
- It is not in-process: the steps drive `work`, `work run` and the other scripts as subprocesses (tests/scenarios/conftest.py:34, :111).
- It is under 60 s, so this is no finding.
- All 9 failures are rows of i34's r122 Outline ("when the whole suite is run … is counted as …"). w195 accepts them and is `researched`. The `work_items` plugin marks all 9 as expected: "accepted by w195, neither green nor withdrawn". None of them is i33's.

## Checks

- **w192** `python3 -m pytest -q -p work_items --work-item w192`: 156 passed, 1 skipped, 56 subtests passed.
- **w194** `python3 -m pytest -q -p work_items --work-item w194`: 155 passed, 1 skipped, 56 subtests passed.
- **Whole-suite gate** `python3 -m pytest -q -rfEx -p work_items --work-item w194 --whole-suite`: 912 passed, 1 skipped, 9 xfailed, 1 xpassed. The 9 xfailed are w195's rows. The 1 xpassed is also w195's: the r122 row `[before w1's merge-formulated-its changes naming thing#r2-not expected]`. It is i34's to account for.
- **tools check, `== ruff ==`**: 12 errors. None was brought in by w192's or w194's changed lines:
  - `scripts/supervise_analysis.py:4` I001 and `scripts/workqueue.py:248` I001 sit in import blocks the i33 diffs do not touch (the w194 diff changes supervise_analysis.py:17-27; the w192 diff changes workqueue.py:87-93). They were there at Base.
  - `tests/scenarios/test_supervision.py:14` and `tests/scripts/stub_claude.py:189-190` come from i31's commits (`ce5c1bfb`, `aef1793b`).
  - The 7 in `.shop/work/i33/runs/supervision/7-apply/apply.py` and `8-formulate/splice.py` are i33's. See F2.
- **tools check, `== vulture ==`**: clean.
- **tools check, `== import-linter ==`**: "the project states no import contracts". Nothing was missing to read in its place.
- **tools size --limit 300**: printed nothing. The largest files touched are workqueue.py (294) and supervise.py (271).
- **features deprecated**: 7 deprecated scenarios. Three of them are i33's, and their replacements' work-items are green. See F1.
- **features bindings**: "every binding names a scenario".
- **Dry-run and real mode**: none applies. The only `--dry-run` in scripts/ is `git push --dry-run` (supervise_review.py:41, supervise_faults.py:67). That is git's mode, not one of this system's own operations, and i33 does not touch it.

## Removed and weakened tests

I searched `git diff 1caef881 HEAD -- tests features` for removed `def`, `assert`, parametrize, Scenario and Examples lines, and for added skip or xfail.
- **Removed: the scenario "a kept branch review that ended PARTIAL, with no question and no finding, does not list nothing to fix now, and no `measure initiative` is run (deprecated)"** (@r75), with its step `reviewer_partial`, in w194's `919e4510`. It proved that a PARTIAL review with no question is not measured. That is the opposite of what r121 now asks. It is listed under w194's `## Retires` and in its plan's §4. It was removed with its binding. This holds.
- **Rewritten: `started_with_items`** (w194, `6ef3162b`). The fixed text became a regex over w1's and w2's statuses, and no assert changed. The plan's §4 lists it. The deprecated r105 and the r109 scenarios still match it and pass.
- **Changed: `session_answers`** (w194, `919e4510`). It now writes the asked-by-the-log entry only when no log.jsonl exists, and no assert changed. The other scenario using it, r78 at feature:1150, still passes.
- **Renamed to `(deprecated)` in formulate round `f1a9ecd3`**: four scenarios, the old r75 (2), r105 and r23. This is the formulate round's deprecation, not a work-item's change.
- i31's `answered_proposal`/`apply_started` (`a0f2b5ba`, `ce5c1bfb`) are outside i33.

No weakening by i33 beyond these.

## Allowances

- w192: "none". The only test change is one added Then step (`add_refused_for_status`). Holds.
- w194, `session_answers`, setup: its diff changes no assert, no expected value and no case. Holds.
- w194, `started_with_items`, setup: the same holds; the same text still matches. Holds.

## Cannot verify

Nothing that bears on the verdict. One gap: a probe of `work add` into an initiative with an unrecognised status (O2) could not be run, because the shell refused to run a scratch script. O2 rests on reading workqueue.py:90-93.

## Findings

- **F1, Minor (w192 and w194; the cause is hand commit `59ca81e1`), observation.** Three deprecated scenarios remain although their replacements' work-items are green.
  - The scenarios: features/supervision.feature:1063 (@r75 "… `measure initiative` is run on the initiative (deprecated)"), features/supervision.feature:1459 (@r105 "… is set done (deprecated)") and features/work-queue.feature:70 (@r23 "… sets the initiative to done (deprecated)").
  - The cause: `59ca81e1` widened w192's `accepts` with r23, and w194's with r75 and r105, by hand. Neither got the `## Retires` entries r73 would have listed.
  - Why it matters: they still pass, because each has a green work-item, but they pin the old wording and add dead weight to the suite.
  - Fix: retire the three with `features retire` in a work-item that lists them under Retires.
  - Reproduction: `python3 <Scripts>/features deprecated` prints them.
- **F2, Minor (i33's apply and formulate rounds, no work-item), drop.** Two scripts are committed in stage directories under `.shop/work/i33/runs/supervision/`: `7-apply/apply.py` and `8-formulate/splice.py`. They fail ruff with SIM115 ×6, RUF015 and I001. They are tracked Python files no one runs again, and they show up in every `tools check --base`.

No Important or Critical finding:
- **Behaviour against the lines:**
  - `workqueue.add` refuses a `done` or `abandoned` initiative with exit 1, before numbering or writing anything (r32, r7).
  - `_holds` needs a `green` work-item (workqueue_done.py:31; r23, r31). That is the one condition behind `holds` and `becomes`, so withdraw, retry, request resolve and `set_done` all follow it.
  - `lists_nothing` ignores the status (supervise_analysis.py:19-26; r121).
  - `pull_through` runs `analyse` and `set_done` only when a work-item is green (supervise.py:222; r75, r105, r97).
- **Risk checked: another path to `analyse` or `set_done` that skips the r75 guard.** Grep finds calls only at supervise.py:222-224.
- **Code no line asks for:** none. The refusal's wording is mechanism. The guard in front of `set_done` serves r105's "at least one work-item that is green".

## Shape

- Size: every file touched is at or under 300 lines.
- Module map: each change sits in its row. `scripts/workqueue.py` is the `work` command. `scripts/workqueue_done.py` is the done condition. `scripts/supervise_analysis.py` is the measure of a finished initiative. `scripts/supervise.py` is under `supervise*`. The steps are in `tests/scenarios/<capability>_*_steps.py` (supervision_analysis_steps, supervision_delegation_steps, supervision_done_steps, work_queue_add_steps).
- Unreached code: `reviewer_partial` was removed with its scenario, and vulture is clean.
- No refactor called for.

## Coupling

i33 adds only `pytest_bdd.parsers.re` in two step modules. That is pytest-bdd's published API, already used across tests/scenarios. No new reliance on anything outside a contract.

## Observations

- **O1. r121 lets a review that did not review close the initiative.** A kept branch review that gives BLOCKED or NEEDS_CONTEXT with no question is taken as listing nothing, so the initiative is measured and set done. This is what r121 ("whatever its status") and its Outline ask. It is noted because a NEEDS_CONTEXT reviewer has, by its contract, not reviewed. Reproduction: `python3 -m pytest -q -k "kept_branch_review_whose_result_gives_outcome"`, where the BLOCKED and NEEDS_CONTEXT rows pass and `measure initiative` runs.
- **O2. `work add` checks the status exactly.** It refuses only the exact strings `done` and `abandoned` (workqueue.py:92), so a status of `Done`, or no status line, lets the add go ahead. Reproduction: by reading the code (the probe was refused, see Cannot verify).
- **O3. A done initiative refused inside drafting has no handling.** `work run`'s drafting (supervise.py:210, `self.draft()`, outside the round's `try`) into an initiative that is already `done` would now get the `Refused` from `work add`. No scenario drives it, and the w192 plan left it open.
- **O4. An all-withdrawn initiative gets no notice.** It gets a branch review and then nothing: no measurement, no done, and no line telling the person why (w194 plan §5). Reproduction: the r75 Outline row "w1 is withdrawn and w2 is withdrawn" passes with `measure initiative` not run.
- **O5. The suite at HEAD is red on i34's work, not i33's.** It fails on w195's r122 rows, and one r122 row xpasses under `--whole-suite`. That is i34's to account for when w195 is planned.
