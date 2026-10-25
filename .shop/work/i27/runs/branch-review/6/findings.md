# Branch review of i27 (review 6): findings

**Verdict: DONE.**
- No finding is Critical, and none is triaged fix now.
- I ran each check that i27's work-items name, at f647911b, and each one passed.
- None of the 45 commits since review 5 (c6673e6a) is i27's.
  - Two other initiatives' work-items touched files in i27's filesets: i25's w173 (`scripts/supervise_brief.py`) and i26's w177 (`scripts/work`, `scripts/workqueue_request.py`, `tests/scenarios/requests_write_steps.py`).
  - Their changes only add code. They change no line that i27 accepts, and w164-w166's scenarios still pass.
- The suite is red at head: 11 scenarios fail, down from 16 at review 5. Every failure is a `StepDefinitionNotFoundError` on a scenario that another initiative formulated (N3).

## Range and work-items

- **Range:** `3cbd0c52..f647911b` on `i25-review-findings-to-implementation`. Base 3cbd0c52 is the commit that added `.shop/work/i27/initiative.md`.
- **i27's work-items, all green; their commits are unchanged since reviews 1-5:**
  - **w164** (supervision r91-r97 and r66): 0ca611cf, a4e922a6 and 12d95e83.
  - **w165** (requests r19): 34ee952c.
  - **w166** (work-queue r25): 5c876c93.
- **Commits since review 5 (45), none of them i27's:**
  - **i25's w173** (supervision r98): b6c4feb1 adds `Briefs.findings_lines` to `scripts/supervise_brief.py`. w173 is `done`.
  - **i26's w177** (requests r4, r5, r12, r20 and r21):
    - db4d07f2 adds `work ask` and `work reply` to `scripts/work` and `scripts/workqueue_request.py`, with their step definitions;
    - it puts `## Questions` and `## Answers` into the request template;
    - it updates the CLAUDE.md row for `workqueue_request.py`;
    - it removes the deprecated requests scenarios @r4, @r5 and @r12, which w177 accepts. w177 is `green`.
  - **Formulate round 7fed86a0:** adds supervision @r15.
  - **Other:**
    - i29's answer rounds, and the work-item w179 added;
    - d365c763, which commits stage directories that crashed sessions left behind;
    - i30 notes and merges, i31 started from q8, and branch review 5 of i28 and of i27.

## Suite

`Suite: 873 passed, 11 failed at f647911b in 22.12 s`

- **Wall time:** 22.12 s, from pytest's own summary line. The run also had 1 skipped and 56 subtests passed.
- **Parallel:** yes. `pytest.ini` sets `addopts = -n auto -m "not fixture"`.
- **In-process:** no. The steps run `scripts/work` as a subprocess, with `tests/scripts/stub_claude.py` standing in for `claude`.
- The suite runs in under 60 s, so its speed is not a finding.
- **The 11 failures** are all `StepDefinitionNotFoundError`; a grep of the output counts 11 of them.
  - **Requests:** the empty delegation (r22, i29's w175, `researched`).
  - **Supervision:**
    - r9;
    - r67, both Examples rows;
    - r82;
    - the intake round's question;
    - the asker's turn at exit;
    - r15 (new, 7fed86a0).
  - **Work-queue:** the three r26-r28 answer scenarios.
- **Since review 5:**
  - 6 failures are gone: requests r4, r5, r12, r20 and r21 (w177), and supervision r98 (w173).
  - 1 is new: supervision r15.
- No scenario of supervision r91-r97 or r66, requests r19 or work-queue r25 fails.

## Checks

- **`pytest -p work_items --work-item w164`:** 152 passed, 1 skipped.
- **`pytest -p work_items --work-item w165`:** 143 passed, 1 skipped.
- **`pytest -p work_items --work-item w166`:** 143 passed, 1 skipped.
- **`tools check --base 3cbd0c52`:**
  - **ruff:** 12 errors, the same 12 as in review 5.
    - The ISC004 that review 5 gave at `scripts/supervise_brief.py:82` is now at `:84`. w173's two inserted lines moved it.
    - Of the 12, the 4 on lines w164 added are F2. The rest are N1, i28's steps, and `stub_claude.py` from before Base.
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts". The heading does not say `missing`.
- **`tools size --limit 300`:** printed nothing.
- **`features deprecated`:** 8 scenarios.
  - migration-tools @r15;
  - supervision @r9, @r67, @r82 and @r102;
  - work-queue @r1, @r9 and @r14.
  - requests @r4, @r5 and @r12 are gone: w177 accepted them and removed them.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** not applicable. The only `--dry-run` in `scripts/` is still `git push --dry-run`, which is git's own check. That code is unchanged.

## Removed and weakened tests

**What I searched:**
- the `-` lines of `git diff c6673e6a HEAD -- tests features`;
- for the range before that, reviews 1-5.

**Since review 5:**
- **`tests/`:** only `+` lines, in `requests_write_steps.py` and `supervision_answers_steps.py`. Both are w173's and w177's new steps.
- **`features/`:** the only removals are the deprecated requests scenarios @r4, @r5 and @r12.
  - Each had a `Deprecated for:` replacement, which is still there and passes.
  - w177 accepts requests#r4, #r5 and #r12, and is `green`.
  - That removal is i26's to review, not i27's.

**The one weakened test in i27's commits is still** `supervision_rounds_steps.py` `second_not_refused` (w164, a4e922a6).
- w164's plan lists it under "Tests the decisions break", so it is not a finding.

## Allowances

- **w164:** one row, `second_not_refused`. It holds, and the test has not changed since.
- **w165:** none.
- **w166:** none.

## Cannot verify

- **No check that a work-item names went unverified.**
- **The probe of `supervise_change`'s change-list handling (F3-F5) was not run again.** Running it was refused approval in reviews 1-5.
  - Here, two commands that chained `pytest` were refused as well, so I wrote no probe.
  - `scripts/supervise_change.py` is unchanged since review 5, so F3-F5 still rest on reading the code.

## Findings

**F1-F10 (reviews 2-5) still hold.** The code they name is unchanged since review 5. `git diff --stat c6673e6a HEAD` does not list `supervise_change.py`, `supervise_rounds.py` or `workqueue_start.py`.
- **F1** (Minor, no work-item, observation): the spec, features and proposals for i27's bootstrap were made by hand (9ed288cf, 18cd9812 and 5d1bd783).
- **F2** (Minor, w164, drop): the 4 ruff errors on lines w164 added:
  - `supervise_brief.py:84` ISC004;
  - `supervision_all_steps.py:111` FURB167 and `:127` RUF007;
  - `test_supervision.py:14` I001.
- **F3** (Minor, w164, observation): `supervise_change.py:45`. A capability name becomes a file name with no check.
- **F4** (Minor, w164, observation): `supervise_change.py:22-31,44-51`. Two entries for one capability overwrite each other.
- **F5** (Minor, w164, observation): `supervise_change.py:26-30`. Ids are not checked against their form.
- **F6** (Minor, w164, observation): `supervise_rounds.py:107-109`. A failed commit leaves the proposals uncommitted.
- **F7** (Minor, w164, observation): the apply brief does not name the kept drafts.
- **F8** (Minor, w165, observation): `workqueue_request.py:87`. `--delegation ""` is stored.
  - requests r22 asks for the refusal. Its work-item, i29's w175, is now `researched`, and its scenario fails for lack of steps.
  - This is a gap in i29's line, not a contradiction in i27's work.
- **F9** (Minor, w166, drop): `workqueue_start.py:48`. The commit subject uses the `work:` prefix.
- **F10** (Minor, no work-item, observation): `work run` leaves records uncommitted when it crashes.
  - A third instance since review 5: d365c763, "i29's answer sessions' stage directories and log lines, left uncommitted when the fourth crashed work run's thread".

**N1** (Minor, no work-item, observation): two tracked gate helpers each give two ruff errors. They are `.shop/work/i26/runs/supervision/1-gate/mk.py` and `.shop/work/i29/runs/supervision/1-gate/mk.py`.
- **Fix:** exclude stage directories from `check`, or keep gate helpers in scratch.

**N2** (Minor, not i27, observation): supervision @r102 is still deprecated while w171 (i28) is green, and so is work-queue @r9 while w140 (i24) is green.

**N3** (Minor, not i27, observation): the suite at head fails 11 scenarios for lack of step definitions. All of them are scenarios that other initiatives formulated.
- **Why it matters:** each implementer's whole-suite run on this shared branch starts red.
- **Fix:** none for i27.

**N4** (Minor, no work-item, observation): this review is the sixth. It started although no commit of i27's, and no line that i27 accepts, changed. Under supervision r27, other initiatives' commits on the shared branch each start another i27 review.
- **Fix:** a line that limits r27 to commits touching the initiative's work-items or their filesets.

**What I checked against i27's lines.**
- **The risk I named:** that w173's and w177's edits, in files of w164's and w165's filesets, changed what r91-r97, r66 or r19 ask for.
- **What I verified:**
  - **w173:** `findings_lines` is added only under `stage == "implement"`, and returns nothing unless the log shows `done -> awaiting-answer -> ready`. It does not touch the integrate brief (r92) or the apply and formulate briefs.
  - **w177:**
    - The request template gains two empty sections. The `delegation:` frontmatter written at `workqueue_request.py:88` is as w165 left it.
    - `ask` and `reply` are new subcommands, and `request`'s `--delegation` parsing is untouched.
  - The w164, w165 and w166 scenario runs pass (above).
- **No code that no line asks for** is in i27's commits. No behaviour contradicts a line or a Purpose, apart from F8's gap, which is i29's to close.

## Shape

- **Size limit 300:** met. `tools size` prints nothing.
- **Still stale:**
  - the CLAUDE.md `scripts/supervise*.py` row, which does not name the integrate round's ending (r91, r96) or r95's lock on rounds;
  - the `supervise_rounds.py:1-3` docstring, which does not name them either.
  - **The check that would show it fixed:** the row and the docstring both name the integrate round and r95.
- **The `workqueue_request.py` row** was brought up to date by w177. It is not an i27 change.
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
- **F3-F5:** read at `scripts/supervise_change.py:23-30,45`. The probe was refused in reviews 1-5 and was not run here.
- **F6:** read at `scripts/supervise_rounds.py:107-109`.
- **F7:** `grep -n drafts scripts/supervise_brief.py` finds only the integrate brief.
- **F8:** read at `workqueue_request.py:87-88`. `.shop/work/i29/w175.md` is `status: researched` with `accepts: [requests#r22]`. The suite fails `test_request_with_an_empty_delegation_is_refused_and_nothing_changes` with `StepDefinitionNotFoundError`.
- **F10:** `git log --format=%s -1 d365c763` says "left uncommitted".
- **N1:** `python3 <Scripts>/tools check --base 3cbd0c52` lists both gate `mk.py` files, at I001 and at SIM115.
- **N2:** `features deprecated` lists supervision @r102 and work-queue @r9.
- **N3:** `python3 -m pytest -q -p no:cacheprovider` at f647911b gives `11 failed, 873 passed`. `grep -c StepDefinitionNotFoundError` on its output gives 11.
- **N4:** `git diff --stat c6673e6a HEAD` lists none of `supervise_change.py`, `supervise_rounds.py`, `supervise_all.py` or `workqueue_start.py`.
  - The changes it does list in w164's and w165's fileset files are w173's and w177's.
