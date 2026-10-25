# Branch review of i27 (review 8): findings

**Verdict: DONE_WITH_CONCERNS.**
- No finding is Critical, and none is triaged fix now. Every check that i27's work-items name passed at 225d3ed2.
- **The one concern:** i27's own r95 scenario (w164) failed once in the suite run at head.
  - It passed when run alone, and it passed in a second full run.
  - I could not read why it failed (see Cannot verify). Rounds actually running side by side, which would break r95, is not ruled out.
- None of the commits since review 7 (eca9d404) is i27's.
  - Two of them add to files in i27's filesets: i29's w175 (959cba20, requests r22) and i29's w179 (0c654848, supervision r15).
  - w175 closes F8.

## Range and work-items

- **Range:** `3cbd0c52..225d3ed2` on `i25-review-findings-to-implementation`. Base 3cbd0c52 is the commit that added `.shop/work/i27/initiative.md`.
- **i27's work-items, all green. Their commits are unchanged since review 1:**
  - **w164** (supervision r91-r97 and r66): 0ca611cf, a4e922a6 and 12d95e83.
  - **w165** (requests r19): 34ee952c.
  - **w166** (work-queue r25): 5c876c93.
- **The code and feature commits since review 7, none of them i27's:**
  - **959cba20** (i29's w175, green): `workqueue_request.request` refuses an empty `--delegation` (requests r22). The step is in `requests_write_steps.py`.
  - **0c654848** (i29's w179, green): `supervise_worker.Workers` `keep_named:230-238` skips a result value that the file system refuses as a name (supervision r15). The given-step is in `supervision_given.py`.
  - **2f3698be** (i30): features for supervision r117 and r110, r19 changed to 80 turns, and the old @r19 deprecated.
  - **a30cfe25** (i31): features for supervision r111-r116, r83 reformulated, and the old @r83 deprecated.
  - **Other:** spec, answer, note, merge, status and records commits; branch review 7 of i27 (46ee3735) and the branch reviews of other initiatives.

## Suite

`Suite: 20 failed, 875 passed at 225d3ed2 in 48.30 s`

- **The run:** `python3 -m pytest -q -p no:cacheprovider -rf`. It also had 1 skipped and 56 subtests passed.
- **Parallel:** yes. `pytest.ini` sets `-n auto`.
- **In-process:** no. The steps run `scripts/work` as a subprocess, with `tests/scripts/stub_claude.py` standing in for `claude`.
- Under 60 s, so its speed is not a finding.
- **What the 20 failures are:**
  - **18 are `StepDefinitionNotFoundError`** on scenarios that other initiatives have formulated but not yet implemented:
    - i31's r111-r116 and the new r83;
    - i30's r110 and r117;
    - i29's r105-r109, the ones still failing.
  - **1 is an `AssertionError`:** "a researcher is given … a limit of 80 turns". That is i30's changed r19, whose code is not yet written.
  - **1 is i27's:** the @r95 scenario "`work run` started with no initiative runs the integrate, apply and formulate rounds of different initiatives one at a time" (w164). See F11.
- **Diagnostic runs** (not the suite line):
  - **The r95 scenario alone** (`-n0 -k one_at_a_time`): passed.
  - **A second full run:** `19 failed, 876 passed in 27.36 s`. r95 passed in it.
- No other scenario of supervision r91-r97 or r66, requests r19 or work-queue r25 failed in either run.

## Checks

- **`pytest -p work_items --work-item w164`:** 152 passed, 1 skipped.
- **`pytest -p work_items --work-item w165`:** 143 passed, 1 skipped.
- **`pytest -p work_items --work-item w166`:** 143 passed, 1 skipped.
- **`tools check --base 3cbd0c52`:**
  - **ruff:** 33 errors, up from 22.
    - **The 11 new ones** are all in tracked round helpers in stage directories (N1):
      - `.shop/work/i30/runs/supervision/3-formulate/splice.py`;
      - `.shop/work/i31/runs/supervision/2-apply/apply.py`;
      - `.shop/work/i31/runs/supervision/3-formulate/splice.py`.
    - **The rest are as before:**
      - 4 on lines w164 added (F2);
      - i28's `supervision_intake_steps.py:84` and `supervision_proposal_steps.py:96`;
      - `stub_claude.py:186-187` from before Base;
      - the older helpers.
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts". The heading does not say `missing`.
- **`tools size --limit 300`:** printed nothing.
- **`features deprecated`:** 6 scenarios:
  - migration-tools @r15;
  - supervision @r19 (new, i30), @r83 (new, i31) and @r102;
  - work-queue @r1 and @r9.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** not applicable. The only `--dry-run` in `scripts/` is git's own `git push --dry-run`, and it is unchanged.

## Removed and weakened tests

**What I searched:** the `-` lines of `git diff eca9d404 HEAD -- scripts tests features`. For the range before that, reviews 1-7.

**Since review 7:**
- **`tests/`:** no line removed. The diff only adds: `refused_empty_delegation` and `implementer_gives_long_sentence`.
- **`features/`:** the only `-` lines are the `@r19` and `@r83` tags and their Scenario titles.
  - Both scenarios are kept, tagged deprecated, beside the new versions that i30 and i31 formulated.
  - Those are other initiatives' feature commits, not i27's.

**In i27's own commits, the one weakened test is still** `supervision_rounds_steps.py` `second_not_refused` (w164, a4e922a6). w164's plan lists it under "Tests the decisions break".

## Allowances

- **w164:** one row, `second_not_refused`. It holds, and the test has not changed since.
- **w165:** none.
- **w166:** none.

## Cannot verify

- **Why @r95 (w164) failed in the suite run at 225d3ed2.** The output of the failing run was not kept. I named the scenario but did not save its error text, and I could not reproduce the failure:
  - it passed alone;
  - it passed in a second full run;
  - `--keep-duplicates` gave one run, not many;
  - `pytest-repeat` is not installed;
  - a probe script that ran the scenario 24 times under load was refused approval.
- So I cannot tell which of these is true:
  - (a) the stand-in's 1-second `linger` (`supervision_all_steps.py:104`) is too short when the machine is loaded, a test fault;
  - (b) `supervise_all`'s round lock (`:44`) lets two rounds overlap under load, which breaks r95.
- No check that a work-item names went unverified.
- **The probes of F3-F5 were not run.** Chained commands and probe scripts are refused approval here. `supervise_change.py` is unchanged since review 1.

## Findings

F1-F7, F9 and F10 still hold. `git diff --stat eca9d404 HEAD` does not list `supervise_change.py`, `supervise_rounds.py`, `supervise_brief.py`, `supervise_all.py` or `workqueue_start.py`.

- **F11** (Important, w164, cannot verify, so it goes to the person): `features/supervision.feature:885` @r95 fails intermittently in the suite at head.
  - **What's wrong:** the scenario failed once in the suite run (48.30 s, a loaded run) and passed in a second full run (27.36 s) and when run alone.
  - **Why it matters:**
    - If the cause is (b) under Cannot verify, `work run` can run two initiatives' rounds side by side, against r95.
    - If it is (a), the suite is flaky, and a flaky scenario turns a merge red at random.
  - **The fix:**
    - First, keep the failure text. Run the scenario repeatedly under `-n auto` load, for example with `pytest-repeat`, or with a loop of `pytest -n0` beside a full run.
    - If the overlap assertion (`serial_rounds_apart`, `supervision_all_steps.py:124-128`) is what fails, the lock in `supervise_all.py:44` is incomplete, and that is fix now.
    - If `serial_rounds_started` (`:118-120`) or a timeout is what fails, give the stand-in's wait a margin instead of `linger: 1`. That is drop or observation.
- **F1** (Minor, no work-item, observation): the spec, features and proposals for i27's bootstrap were made by hand: 9ed288cf, 18cd9812 and 5d1bd783.
- **F2** (Minor, w164, drop): the 4 ruff errors on lines w164 added:
  - `supervise_brief.py:84` ISC004;
  - `supervision_all_steps.py:111` FURB167 and `:127` RUF007;
  - `test_supervision.py:14` I001.
- **F3** (Minor, w164, observation): `supervise_change.py:45`. A capability name becomes a file name with no check.
  - i29's r107 now asks `work run` to refuse it. Its scenario still lacks steps.
- **F4** (Minor, w164, observation): `supervise_change.py:22-31,44-51`. Two entries for one capability overwrite each other.
- **F5** (Minor, w164, observation): `supervise_change.py:26-30`. Ids are not checked against their form.
- **F6** (Minor, w164, observation): `supervise_rounds.py:107-109`. A failed commit leaves the proposals uncommitted.
- **F7** (Minor, w164, observation): the apply brief does not name the kept drafts. i29's r108 asks for this, and its scenario still lacks steps.
- **F8: closed.**
  - 959cba20 (i29's w175, green) refuses `--delegation ""` and a delegation of only whitespace: `workqueue_request.py:93-94`. The check runs before anything is written.
  - The `delegation=None` path, which is r19's (w165), is unchanged, and w165's check passes.
- **F9** (Minor, w166, drop): `workqueue_start.py:48`. The commit subject uses the `work:` prefix.
- **F10** (Minor, no work-item, observation): `work run` leaves records uncommitted. i29's r106 asks for that commit, and its scenario still lacks steps.

**N1** (Minor, no work-item, observation): tracked round helpers in stage directories give 25 of `tools check`'s 33 ruff errors.
- There are now eight of them: the five from review 7 and the three listed under Checks.
- **Why it matters:** they hide the code's own errors in `check`'s output.
- **Fix:** exclude `.shop/` from `check`, or keep round helpers in scratch.

**N2** (Minor, not i27, observation): supervision @r102 is still deprecated while w171 (i28) is green, and so is work-queue @r9 while w140 (i24) is green.

**N3** (Minor, not i27, observation): 19 scenarios fail at head because other initiatives' formulated lines have no code yet:
- 18 lack step definitions;
- 1 is r19's new turn limit.

**N4** (Minor, no work-item, observation): this review is the eighth. It started although no commit of i27's, and no line i27 accepts, changed.

**What I checked against i27's lines.**
- **The risk I named:** that 959cba20 changed what r19 (w165) asks for, since `workqueue_request.py` is in w165's fileset.
  - **What I verified:** the new refusal applies only when `delegation is not None` and is blank. The writing of `delegation:` is untouched, and w165's run passes.
- **The risk I named:** that 0c654848 changed the kept-file handling w164 relies on.
  - **What I verified:** it only wraps `resolve()` and `is_file()` in a `try`. A value that resolves to a file is kept as before.
- No code that no line asks for is in i27's commits. No behaviour contradicts a line or a Purpose.

## Shape

- **Size limit 300:** met. `tools size` prints nothing.
- **Still stale:**
  - the CLAUDE.md `scripts/supervise*.py` row, which does not name the integrate round's ending (r91, r96) or r95's lock on rounds;
  - the `supervise_rounds.py:1-3` docstring, which does not name them either.
  - **The check that would show it fixed:** the row and the docstring both name the integrate round and r95.
- **Rows that are met:**
  - `supervise_change.py`, `supervise_all.py` and `supervise_drafts.py`;
  - `workqueue_start.py`, `workqueue_request.py` and `scripts/work`;
  - `tests/scenarios/`.
- **No unreached code or steps:** vulture is clean, and so is `features bindings`.

## Coupling

- **New coupling:** none in i27's code, which is unchanged.
- **Existing coupling relied on:** the `error_max_turns` subtype of `claude -p` (`supervise_faults.py`).
  - r91 keeps the drafts however a round ends, so if that subtype changed, nothing of i27's work would be lost.
  - The stable form is the plugin's own `result.json` status, which the code already reads first.
- **The r95 scenario relies on timing:** the stand-in's `linger` of 1 s (F11).

## Observations

One line each, with its reproduction:
- **F11:**
  - `python3 -m pytest -q -p no:cacheprovider -rf` at 225d3ed2 gave `20 failed, 875 passed … in 48.30s`, with `test_work_run_started_with_no_initiative_runs_the_integrate_apply_and_formulate_rounds_of_different_initiatives_one_at_a_time` FAILED.
  - The same command again gave `19 failed, 876 passed … in 27.36s`, without it.
  - `pytest -n0 -k one_at_a_time tests/scenarios/test_supervision.py` gave `2 passed`.
- **F3-F7, F9 and F10:** as in review 7. The files are unchanged.
- **N1:** `python3 <Scripts>/tools check --base 3cbd0c52` lists the eight helper files, 25 errors in all.
- **N2:** `features deprecated` lists supervision @r102 and work-queue @r9.
- **N3:** the `-rf` summary above. Every entry but r95's and r19's (80 turns) is a `StepDefinitionNotFoundError`.
- **N4:** `git diff --stat eca9d404 HEAD -- scripts tests` lists only `supervise_worker.py`, `workqueue_request.py`, `requests_write_steps.py` and `supervision_given.py`, all of them i29's.
