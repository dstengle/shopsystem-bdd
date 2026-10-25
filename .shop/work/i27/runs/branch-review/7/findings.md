# Branch review of i27 (review 7): findings

**Verdict: DONE.**
- No finding is Critical, and none is triaged fix now.
- I ran each check that i27's work-items name, at eca9d404. Each one passed.
- None of the commits since review 6 (f647911b) is i27's.
  - Two other work-items changed files in w164's and w165's filesets: i26's w178 (641f95a9) and i25's w176 (a2d1083e).
  - Both only add to them. Neither changes what i27's lines ask for, and w164-w166's scenarios still pass.
- The suite is red at head: 8 scenarios fail, down from 11 at review 6.
  - Every failure is a `StepDefinitionNotFoundError` on a scenario that another initiative formulated (N3).
  - Five of the eight are i29's new supervision r105-r109. Their work-item, w181, is `drafted`.

## Range and work-items

- **Range:** `3cbd0c52..eca9d404` on `i25-review-findings-to-implementation`. Base 3cbd0c52 is the commit that added `.shop/work/i27/initiative.md`.
- **i27's work-items, all green. Their commits are unchanged since reviews 1-6:**
  - **w164** (supervision r91-r97 and r66): 0ca611cf, a4e922a6 and 12d95e83.
  - **w165** (requests r19): 34ee952c.
  - **w166** (work-queue r25): 5c876c93.
- **The code and spec commits since review 6, none of them i27's:**
  - **641f95a9, i26's w178** (supervision r9, r67, r82, r100 and r101; `green`):
    - adds `asked()` to `scripts/supervise.py` and calls it from `supervise_all.run_all`;
    - adds `asked_here` to `scripts/workqueue_request.py`;
    - changes the intake steps;
    - removes the deprecated scenarios @r9, @r67 and @r82, which w178 accepts.
  - **a2d1083e, i25's w176** (work-queue r14 and r26-r28; `done`):
    - adds `--change` and `--accept` to `work answer`;
    - removes the deprecated work-queue @r14 scenario, which w176 accepts.
  - **Spec and features:**
    - 3bfdba68 and d073c518 (i29): supervision r105-r109, with their scenarios;
    - 31738369 (i30): formulation r23.
  - **Other:** answer, note, merge and status commits; records commits cebadf9d and 1d0dcdeb; branch review 6 of i27 (ed5396f5) and of i28.

## Suite

`Suite: 874 passed, 8 failed at eca9d404 in 22.00 s`

- **Wall time:** 22.00 s, from pytest's own summary line. The run also had 1 skipped and 56 subtests passed.
- **Parallel:** yes. `pytest.ini` sets `-n auto`.
- **In-process:** no. The steps run `scripts/work` as a subprocess, with `tests/scripts/stub_claude.py` standing in for `claude`.
- The suite runs in under 60 s, so its speed is not a finding.
- **The 8 failures**, all `StepDefinitionNotFoundError`:
  - **requests r22:** the empty delegation (i29's w175, `claimed`).
  - **supervision r15** (i29's w179, `claimed`).
  - **supervision r105-r109** (i29's w181, `drafted`):
    - r108, both Examples rows;
    - r109;
    - r106;
    - r105;
    - r107.
- **Since review 6:**
  - 9 failures are gone: supervision r9, r67 (both rows), r82, the intake question and the asker's turn (w178), and work-queue r26-r28 (w176).
  - 6 are new: r105-r109.
- No scenario of supervision r91-r97 or r66, requests r19 or work-queue r25 fails.

## Checks

- **`pytest -p work_items --work-item w164`:** 152 passed, 1 skipped.
- **`pytest -p work_items --work-item w165`:** 143 passed, 1 skipped.
- **`pytest -p work_items --work-item w166`:** 143 passed, 1 skipped.
- **`tools check --base 3cbd0c52`:**
  - **ruff:** 22 errors, up from 12. The 10 new ones are all in tracked stage-directory helpers (N1):
    - `.shop/work/i29/runs/supervision/5-apply/splice.py`;
    - `.shop/work/i29/runs/supervision/6-formulate/splice.py`;
    - `.shop/work/i31/runs/supervision/1-gate/gq.py`.
  - **The rest of ruff is as before:**
    - 4 on lines w164 added (F2);
    - i28's `supervision_intake_steps.py:84` (bcc41527) and `supervision_proposal_steps.py:96` (2e0f2555);
    - `stub_claude.py` from before Base;
    - the two older `mk.py` helpers.
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts". The heading does not say `missing`.
- **`tools size --limit 300`:** printed nothing.
- **`features deprecated`:** 4 scenarios: migration-tools @r15, supervision @r102, and work-queue @r1 and @r9.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** not applicable. The only `--dry-run` in `scripts/` is git's own `git push --dry-run`, and that code is unchanged.

## Removed and weakened tests

**What I searched:**
- the `-` lines of `git diff f647911b HEAD -- tests features`;
- for the range before that, reviews 1-6.

**Since review 6:**
- **`tests/`:** the only removals are in `supervision_intake_steps.py`, by w178 (i26). They are the steps of the deprecated @r67 scenario that w178 removed:
  - `intake_writes`;
  - the `Kind: intake` then-step;
  - `lines_have_outcomes`;
  - the `JUDGED` constant.
  - That removal is i26's to review, not i27's.
- **`features/`:** the only removals are the deprecated supervision @r9, @r67 and @r82 (w178, `green`) and work-queue @r14 (w176, `done`).
  - Each of them is accepted by the work-item that removed it.
  - The replacement of each one passes.

**In i27's own commits, the one weakened test is still** `supervision_rounds_steps.py` `second_not_refused` (w164, a4e922a6).
- w164's plan lists it under "Tests the decisions break", so it is not a finding.

## Allowances

- **w164:** one row, `second_not_refused`. It holds, and the test has not changed since.
- **w165:** none.
- **w166:** none.

## Cannot verify

- **No check that a work-item names went unverified.**
- **The probe of `supervise_change`'s change-list handling (F3-F5) was not run.** Chained shell commands are refused approval here, as they were in earlier reviews.
  - `scripts/supervise_change.py` is unchanged since review 6, so F3-F5 rest on reading the code.

## Findings

F1-F10 (reviews 2-6) still hold. `git diff --stat f647911b HEAD` does not list `supervise_change.py`, `supervise_rounds.py`, `supervise_brief.py` or `workqueue_start.py`.

- **F1** (Minor, no work-item, observation): the spec, features and proposals for i27's bootstrap were made by hand: 9ed288cf, 18cd9812 and 5d1bd783.
- **F2** (Minor, w164, drop): the 4 ruff errors on lines w164 added:
  - `supervise_brief.py:84` ISC004;
  - `supervision_all_steps.py:111` FURB167 and `:127` RUF007;
  - `test_supervision.py:14` I001.
- **F3** (Minor, w164, observation): `supervise_change.py:45`. A capability name becomes a file name with no check.
  - **New:** i29's r107 now asks `work run` to refuse a capability that neither `spec/capabilities/` nor the drafts have. Its work-item, w181, is `drafted`.
- **F4** (Minor, w164, observation): `supervise_change.py:22-31,44-51`. Two entries for one capability overwrite each other.
- **F5** (Minor, w164, observation): `supervise_change.py:26-30`. Ids are not checked against their form.
- **F6** (Minor, w164, observation): `supervise_rounds.py:107-109`. A failed commit leaves the proposals uncommitted.
- **F7** (Minor, w164, observation): the apply brief does not name the kept drafts.
  - **New:** i29's r108 asks for this, and w181 is `drafted`. Its scenario fails for lack of steps (two rows).
- **F8** (Minor, w165, observation): `workqueue_request.py:87`. `--delegation ""` is stored.
  - requests r22 asks for the refusal. Its work-item, i29's w175, is now `claimed`.
- **F9** (Minor, w166, drop): `workqueue_start.py:48`. The commit subject uses the `work:` prefix.
- **F10** (Minor, no work-item, observation): `work run` leaves records uncommitted.
  - cebadf9d records i26's measurement and analysis "left uncommitted".
  - i29's r106 now asks for that commit. It is w181's.

**N1** (Minor, no work-item, observation): tracked helpers in stage directories give 14 of `tools check`'s 22 ruff errors. There are now five of them:
- `.shop/work/i26/runs/supervision/1-gate/mk.py`;
- `.shop/work/i29/runs/supervision/1-gate/mk.py`;
- `.shop/work/i29/runs/supervision/5-apply/splice.py`;
- `.shop/work/i29/runs/supervision/6-formulate/splice.py`;
- `.shop/work/i31/runs/supervision/1-gate/gq.py`.

**Why it matters:** they hide the code's own errors in `check`'s output.

**Fix:** exclude `.shop/` from `check`, or keep round helpers in scratch.

**N2** (Minor, not i27, observation): supervision @r102 is still deprecated while w171 (i28) is green, and so is work-queue @r9 while w140 (i24) is green.

**N3** (Minor, not i27, observation): the suite at head fails 8 scenarios for lack of step definitions. All of them are other initiatives' formulated lines whose work-items are not yet done.
- **Fix:** none for i27.

**N4** (Minor, no work-item, observation): this review is the seventh. It started although no commit of i27's, and no line i27 accepts, changed.
- **Fix:** a line that limits r27 to commits touching the initiative's work-items or their filesets.

**What I checked against i27's lines.**
- **The risk I named:** that w178's edits to `supervise.py`, `supervise_all.py` and `workqueue_request.py`, and w176's edits, changed what r66, r91-r97 or r19 ask for. All three files are in w164's or w165's filesets.
- **What I verified:**
  - **`supervise_all.run_all:82-83`:**
    - The exit code is computed as before, then passed through `asked()`.
    - The per-initiative refusal is unchanged (r66, `:63-67`), and so is the round lock (r95, `:44`).
    - `run_all` calls `pull_through`, not `Run.run`, so `asked()` prints once.
  - **`workqueue_request.asked_here`:** a new reader only. Writing `delegation:` (r19) is untouched.
  - **The w164, w165 and w166 scenario runs** pass (above).
- **No code no line asks for** is in i27's commits. No behaviour contradicts a line or a Purpose, apart from F8's gap, which is i29's r22 to close.

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

## Observations

One line each, with its reproduction:
- **F3-F5:** read at `scripts/supervise_change.py:23-30,45`. Not probed, because chained commands are refused.
- **F6:** read at `scripts/supervise_rounds.py:107-109`.
- **F7:** `grep -n drafts scripts/supervise_brief.py` finds only the integrate brief. r108 is in `spec/capabilities/supervision.md` (3bfdba68).
- **F8:** read at `workqueue_request.py:87-88`. `.shop/work/i29/w175.md` is `status: claimed` with `accepts: [requests#r22]`.
- **F10:** `git log --format=%s -1 cebadf9d` says "(left uncommitted; q5)".
- **N1:** `python3 <Scripts>/tools check --base 3cbd0c52` lists the five helper files above, 14 errors in all.
- **N2:** `features deprecated` lists supervision @r102 and work-queue @r9.
- **N3:** `python3 -m pytest -q -p no:cacheprovider -rf` at eca9d404 gives `8 failed, 874 passed`, each failure a `StepDefinitionNotFoundError`.
- **N4:** `git diff --stat f647911b HEAD -- scripts tests` lists only `supervise.py`, `supervise_all.py`, `supervise_intake.py`, `workqueue_request.py`, `work`, `workqueue_answer.py` and their steps. All of those changes are w178's and w176's.
