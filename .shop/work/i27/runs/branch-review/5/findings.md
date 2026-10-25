# Branch review of i27 (review 5): findings

**Verdict: DONE.**
- No finding is Critical, and none is triaged fix now.
- I ran each check that i27's work-items name, at c6673e6a, and each one passed.
- No code, test, agent, hook or CLAUDE.md file has changed since review 4 (125b2ad1).
  - `git diff --name-only 125b2ad1 HEAD -- tests scripts agents CLAUDE.md conftest.py hooks skills pytest.ini` prints nothing.
- The suite is red at head: 16 scenarios fail, 8 more than at review 4. Every failure is a `StepDefinitionNotFoundError`, on a scenario that a formulate round of i25, i26 or i29 committed. None is i27's (N3).

## Range and work-items

- **Range:** `3cbd0c52..c6673e6a` on `i25-review-findings-to-implementation`. Base 3cbd0c52 is the commit that added `.shop/work/i27/initiative.md`.
- **i27's work-items, all green:**
  - **w164** (supervision r91-r97 and r66): 0ca611cf, a4e922a6 and 12d95e83, between 4910049f and 44e59393.
  - **w165** (requests r19): 34ee952c, between cc16fb45 and f547d55e.
  - **w166** (work-queue r25): 5c876c93, between 117402c4 and 1a6567bd.
- **Commits since review 4 (37), none of them i27's.** They belong to the initiatives that share the branch:
  - **i29:**
    - spec 7c548d23 (requests r22 added);
    - features 6cd77b2b (requests @r22);
    - its round merges 56cda243, cab9306a and 8038d315;
    - w175 added, researched, then `awaiting-answer`;
    - its supervision gate, which tracked `.shop/work/i29/runs/supervision/1-gate/mk.py`.
  - **i25 and i26:**
    - features 46fef129 (supervision r98, r100 and r101 added; r9, r67 and r82 changed, with the old scenarios deprecated);
    - w173 and w174 transitions, w174 `withdrawn`, w176 added;
    - 986dbcbb, the ids of their capability-proposals, set by hand once.
  - **i30:** started (4fbc25cd).
  - **Request q8:** 2c256e93 to c6673e6a.
  - **Records:** observation 99346b49, and the branch reviews 5fc387ed (i27 review 4) and 3d533646 (i28 review 4).
- Each of these commits is made by a round or work-item of its own initiative, and that initiative's reviews read it. None is an i27 finding.

## Suite

`Suite: 870 passed, 16 failed at c6673e6a in 32.6 s`

- **Wall time:** 32.6 s from `time`; pytest gives 32.36 s. The run also had 1 skipped and 56 subtests passed.
- **Parallel:** yes. `pytest.ini` sets `addopts = -n auto -m "not fixture"`.
- **In-process:** no. The When steps run `scripts/work` as a subprocess, with `tests/scripts/stub_claude.py` standing in for `claude`.
- The suite runs in under 60 s, so its speed is not a finding.
- **The 16 failures** are all `StepDefinitionNotFoundError`:
  - **The 8 from review 4:**
    - requests r4, r5, r12, r20 and r21;
    - work-queue r26, r27 and r28.
  - **8 new since review 4:**
    - requests r22;
    - supervision r9 (new), r67 (new, both Examples rows), r82 (new), r98, r100 and r101.
  - No scenario of supervision r91-r97 or r66, requests r19 or work-queue r25 fails.

## Checks

- **`pytest -p work_items --work-item w164`:** 152 passed, 1 skipped.
- **`pytest -p work_items --work-item w165`:** 143 passed, 1 skipped.
- **`pytest -p work_items --work-item w166`:** 143 passed, 1 skipped.
- **`tools check --base 3cbd0c52`:** 12 ruff errors. The 10 from review 4 are still there, and 2 are new.
  - **ruff, the errors on lines w164 added** (4; F2, Minor, drop):
    - `scripts/supervise_brief.py:82` ISC004;
    - `tests/scenarios/supervision_all_steps.py:111` FURB167 and `:127` RUF007;
    - `tests/scenarios/test_supervision.py:14` I001.
  - **ruff, the errors in i28's step definitions** (2):
    - `supervision_intake_steps.py:65` FURB167;
    - `supervision_proposal_steps.py:96` RUF100.
  - **ruff, the errors in tracked gate helpers** (4; N1):
    - `.shop/work/i26/runs/supervision/1-gate/mk.py` `:1` I001 and `:19` SIM115;
    - new: `.shop/work/i29/runs/supervision/1-gate/mk.py` `:1` I001 and `:15` SIM115.
  - **ruff, the errors from before Base** (2): `tests/scripts/stub_claude.py:186` and `:187` FURB167.
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts". The heading does not say `missing`.
- **`tools size --limit 300`:** printed nothing.
- **`features deprecated`:** 11 scenarios.
  - **The 8 from review 4:**
    - migration-tools @r15;
    - requests @r4, @r5 and @r12;
    - supervision @r102 (w171 is green);
    - work-queue @r1, @r9 (w140 is green) and @r14.
  - **3 new:** supervision @r9, @r67 and @r82 (46fef129). Their replacements fail for lack of steps, so no work-item for them is green.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** not applicable. The only `--dry-run` in `scripts/` is `git push --dry-run` (`supervise_review.py:41`, `supervise_faults.py:67`), which is git's own check. That code is unchanged since review 4.

## Removed and weakened tests

**What I searched:**
- the `-` lines of `git diff 125b2ad1 HEAD -- tests features`, the part of the branch since review 4;
- for the range before that, reviews 1-4, whose searches covered `git diff 3cbd0c52 125b2ad1 -- tests features`.

**Since review 4:**
- **`tests/`:** nothing changed.
- **`features/`:** only formulate rounds changed it (46fef129 and 6cd77b2b). No work-item did.
  - The only `-` lines are the old supervision r9, r67 and r82 scenario headers.
  - Each of those scenarios is still there, tagged `@deprecated` with a `Deprecated for:` line, beside its replacement.
  - Nothing was removed.

**The one weakened test in i27's commits is still** `tests/scenarios/supervision_rounds_steps.py` `second_not_refused` (w164, a4e922a6).
- w164's plan lists it under "Tests the decisions break", so it is not a finding.

## Allowances

- **w164:** one row, `second_not_refused`. It holds, as reviews 1-4 found, and the test has not changed since.
- **w165:** "none".
- **w166:** "none".

## Cannot verify

- **The probe of `supervise_change`'s change-list handling was not run.**
  - I wrote `.shop/scratch/i27-branch-review/probe_change.py` for four change lists, each against a temporary initiative directory:
    - the capability `initiative`;
    - the capability `../escaped`;
    - the same capability twice;
    - ids of another capability, and a malformed id.
  - Running it was refused ("This command requires approval"), as in reviews 1-4. I tried no other route, and I deleted the directory.
  - So F3-F5 rest on reading `scripts/supervise_change.py:23-30,45`, which is unchanged.
  - This is not a check any work-item names, and all of those passed.

## Findings

**The findings of reviews 2-4 still hold.** The code they name has not changed.
- **F1** (Minor, no work-item, observation): the spec, features and proposals for i27's bootstrap were made by hand (9ed288cf, 18cd9812 and 5d1bd783).
- **F2** (Minor, w164, drop): the 4 ruff errors on lines w164 added (listed above).
- **F3** (Minor, w164, observation): `supervise_change.py:45`. A capability name becomes a file name with no check: `initiative` overwrites initiative.md, and `../x` writes outside the initiative's directory.
- **F4** (Minor, w164, observation): `supervise_change.py:22-31,44-51`. Two entries for one capability overwrite each other.
- **F5** (Minor, w164, observation): `supervise_change.py:26-30`. An id is not checked against `<capability>#r<n>` or `term/<term>`.
- **F6** (Minor, w164, observation): `supervise_rounds.py:107-109`. A failed commit leaves the proposals uncommitted.
- **F7** (Minor, w164, observation): the apply brief does not name the kept drafts.
- **F8** (Minor, w165, observation): `workqueue_request.py:87` stores `--delegation ""`.
  - **New since review 4:** requests r22 (7c548d23, i29) now asks for that refusal. Its work-item is w175 (i29), which is `awaiting-answer` on whether a delegation of only whitespace counts as empty.
  - Until w175 is green, the code does what r19 asked and not what r22 asks. That gap is i29's line, not yet implemented. It is not a contradiction in i27's work.
- **F9** (Minor, w166, drop): `workqueue_start.py:48`. The commit subject uses the `work:` prefix.
- **F10** (Minor, no work-item, observation): `work run` left measurements uncommitted (7d8572d6, ab63bd6c).

**N1. Minor | no work-item (i26's gate round dbbf9089; i29's supervision gate) | observation.**
- **What:** each gate session left a helper tracked: `.shop/work/i26/runs/supervision/1-gate/mk.py`, and now `.shop/work/i29/runs/supervision/1-gate/mk.py`. ruff counts both.
- **Why it matters:** `tools check` grows noisier with each gate.
- **Fix:** exclude stage directories from `check`, or have the gate session keep its helpers in scratch.

**N2. Minor | not i27 (i28's w171; i24's w140) | observation.**
- supervision @r102 is still deprecated while w171 is green, and so is work-queue @r9 while w140 is green.

**N3. Minor | not i27 (formulate rounds 159bdfdf, 3d3da4df, 46fef129 and 6cd77b2b) | observation.**
- **What:** the suite at head fails 16 scenarios, up from 8 at review 4, each for lack of a step definition.
- **Why it matters:** every implementer `work run` starts on this shared branch gets a whole-suite run that is red for reasons outside its work-item. Nothing is wrong in i27's code.
- **Fix:** none for i27. If a red suite between formulate and implement is not wanted on a shared branch, a line has to say so.

**N4. Minor | no work-item | observation.**
- **What:** this review, like reviews 3 and 4, was started although no i27 work-item and no line i27 accepts changed.
- **Why it matters:** supervision r27 starts a review whenever the branch holds a commit that no kept review has read. On this branch, other initiatives' commits each start another session reviewing i27.
- **Fix:** none for i27. A line could limit r27 to commits that touch the initiative's work-items or their files.

**What I checked against i27's lines.**
- **The risk I named:** that the spec and features changes since review 4 changed, or contradicted, a line i27 accepts.
- **What I verified:**
  - `git diff 125b2ad1 HEAD -- spec` adds only requests r22.
  - The features diff adds requests r22 and supervision r98, r100 and r101, and changes supervision r9, r67 and r82.
  - None of these is r91-r97, r66, r19 or r25. r67 is the intake round, not r66.
  - r22 narrows r19's input: see F8.
  - The w164-w166 scenario runs pass.
- **No code that no line asks for** is in i27's commits, and no behaviour that contradicts a line or a Purpose, apart from F8's gap, which is i29's to close. The code is unchanged since review 4, which found the same.

## Shape

- **Size limit 300:** met. `tools size` prints nothing.
- **Still stale:** the CLAUDE.md `scripts/supervise*.py` row and the `supervise_rounds.py:1-3` docstring. They name the apply and formulate rounds, but not the integrate round's ending (r91, r96) or r95's lock on rounds.
  - **The check that would show it fixed:** the row and the docstring both name the integrate round and r95.
- **Rows that are met:**
  - `supervise_change.py`, `supervise_all.py` and `supervise_drafts.py`;
  - `workqueue_start.py`, `workqueue_request.py` and `scripts/work`;
  - `tests/scenarios/`.
- **No unreached code or steps:** vulture is clean, and so is `features bindings`.

## Coupling

- **New coupling since review 4:** none, because no code changed.
- **Existing coupling relied on:** the `error_max_turns` subtype of `claude -p` (`supervise_faults.py`).
  - r91 keeps the drafts however a round ends, so if that subtype changed, none of i27's work would be lost.
  - The stable form is the plugin's own `result.json` status, which the code already reads first.

## Observations

One line each, with its reproduction:
- **F3-F5:** read at `scripts/supervise_change.py:23-30,45`; running the probe was refused approval.
- **F6:** read at `scripts/supervise_rounds.py:107-109`.
- **F7:** `grep -n drafts scripts/supervise_brief.py` finds only the integrate brief.
- **F8:** read at `workqueue_request.py:87`. `.shop/work/i29/w175.md` accepts requests#r22 and is `awaiting-answer`. The suite fails `test_request_with_an_empty_delegation_is_refused_and_nothing_changes` for lack of steps.
- **F10:** the subjects of 7d8572d6 and ab63bd6c say "left uncommitted".
- **N1:** `python3 <Scripts>/tools check --base 3cbd0c52` lists both gate `mk.py` files, at `:1` I001 and at SIM115.
- **N2:** `features deprecated` lists supervision @r102 and work-queue @r9; w171 and w140 are `green`.
- **N3:** `python3 -m pytest -q` at c6673e6a gives `16 failed, 870 passed`, each failure a `StepDefinitionNotFoundError`.
- **N4:** `git diff --name-only 125b2ad1 HEAD -- tests scripts agents CLAUDE.md conftest.py hooks skills pytest.ini` prints nothing.
- **Stale module-map row:** CLAUDE.md's `scripts/supervise*.py` row, and `supervise_rounds.py:1-3`.
