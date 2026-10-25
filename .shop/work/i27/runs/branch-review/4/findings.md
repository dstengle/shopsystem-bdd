# Branch review of i27 (review 4): findings

**Verdict: DONE.**
- No finding is Critical, and none is triaged fix now.
- Each check i27's work-items name passed at 125b2ad1, and I ran each one myself.
- No code, test, agent, hook or CLAUDE.md file has changed since review 3 (4640ef08). `git diff --name-only 4640ef08 HEAD -- tests scripts agents CLAUDE.md conftest.py hooks skills` prints nothing.
  - The only tracked changes outside `.shop/` are to `spec/` and `features/`, made by i25's and i26's apply and formulate rounds.
  - None of them touches a line i27 accepts (supervision r91-r97 and r66, requests r19, work-queue r25).
- The suite is red at head: 8 scenarios fail. All 8 are scenarios i25 and i26 formulated that have no step definitions yet. None is i27's (N3).

## Range and work-items

- **Range:** `3cbd0c52..125b2ad1` on `i25-review-findings-to-implementation`. Base 3cbd0c52 is the commit that added `.shop/work/i27/initiative.md`.
- **i27's work-items, all green:**
  - **w164** (supervision r91-r97, r66): 0ca611cf, a4e922a6, 12d95e83, between 4910049f and 44e59393.
  - **w165** (requests r19): 34ee952c, between cc16fb45 and f547d55e.
  - **w166** (work-queue r25): 5c876c93, between 117402c4 and 1a6567bd.
- **Commits since review 3 that belong to no i27 work-item.** The branch is shared by i25-i29:
  - **i25:**
    - spec 112fe1b6 and 1c0c4fb6;
    - features 159bdfdf (work-queue r14 changed, r26-r28 added);
    - the merges f13e5b08 and bcdaac6a;
    - `work add` of w173 and w174 (8f74375f, c9c176a7);
    - w174's transitions up to `ready -> claimed` (125b2ad1);
    - w173 `failed`, then retried (b67f622d, c26681df).
  - **i26:**
    - spec 5c441e9e and d07a8b38;
    - features 3d3da4df (requests r20 and r21 added; r4, r5 and r12 changed).
  - **i29:** started (9a45470f, e9a1ad8d), with its integrate round merged (05a71892).
  - **Request q7:** 5187b687 to cf961e01.
  - **Records:** observation 409627b7, and the branch reviews 0adf90f8 (i27 review 3) and 90ff4a17 (i28 review 3).
  - The rest are `work note`, `work answer` and status commits.
- None of these is an i27 finding. They are made by rounds and work-items of the initiatives they belong to, and their own reviews read them.

## Suite

`Suite: 870 passed, 8 failed at 125b2ad1 in 37.3 s`

- **Wall time:** 37.3 s from `time` (pytest's own figure: 36.92 s). The run also had 1 skipped and 56 subtests passed.
- **Parallel:** yes (`pytest.ini`: `addopts = -n auto -m "not fixture"`).
- **In-process:** no. The When steps run `scripts/work` as a subprocess, with `tests/scripts/stub_claude.py` standing in for `claude`.
- The suite runs in under 60 s, so its speed is not a finding.
- **The 8 failures** are all `StepDefinitionNotFoundError` on scenarios added since review 3:
  - `test_requests.py`, 5 scenarios:
    - r20, the upstream asking a question;
    - r21, the asker answering it;
    - the new r4, r5 and r12 scenarios.
  - `test_work_queue.py`, 3 scenarios: r26, r27 and r28, the reviewer's answer with `--change`, with `--accept`, and with neither.
  - No i27 scenario fails. See N3.

## Checks

- **`pytest --work-item w164`:** 152 passed, 1 skipped.
- **`pytest --work-item w165`:** 143 passed, 1 skipped.
- **`pytest --work-item w166`:** 143 passed, 1 skipped.
- **`tools check --base 3cbd0c52`:** 10 ruff errors, the same 10 as review 3.
  - **ruff:**
    - **4 on lines w164 added** (F2, Minor, drop):
      - `scripts/supervise_brief.py:82` ISC004;
      - `tests/scenarios/supervision_all_steps.py:111` FURB167 and `:127` RUF007;
      - `tests/scenarios/test_supervision.py:14` I001.
    - **2 from i28:**
      - `supervision_intake_steps.py:65` FURB167;
      - `supervision_proposal_steps.py:96` RUF100.
    - **2 in `.shop/work/i26/runs/supervision/1-gate/mk.py`** (N1): `:1` I001 and `:19` SIM115.
    - **2 from before Base:** `tests/scripts/stub_claude.py:186` and `:187` FURB167.
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts". The heading does not say `missing`.
- **`tools size --limit 300`:** printed nothing.
- **`features deprecated`:** 8 scenarios.
  - **4 that review 3 listed:**
    - migration-tools @r15;
    - work-queue @r1;
    - work-queue @r9 (w140 is green);
    - supervision @r102 (w171 is green).
  - **4 new:**
    - requests @r4, @r5 and @r12 (i26's 3d3da4df);
    - work-queue @r14 (i25's 159bdfdf).
    - The work-items that would make their replacements pass are not green: w174 is `claimed`, and i26 has no work-item yet.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** not applicable. The only `--dry-run` in `scripts/` is `git push --dry-run` (`supervise_review.py:41`, `supervise_faults.py:67`), which is git's own check.

## Removed and weakened tests

**What I searched:**
- `git diff 4640ef08 HEAD -- tests features`, the part since review 3;
- for the range before that, reviews 1-3, whose searches covered every `-` line of `git diff 3cbd0c52 4640ef08 -- tests features`.

**Since review 3:**
- **`tests/`:** nothing changed.
- **`features/`:** only formulate rounds of i25 and i26 changed it, and no work-item did.
  - Their `-` lines are the old scenarios of requests r4, r5 and r12 and work-queue r14. Each is now tagged `@deprecated`, with a `Deprecated for:` line, beside its replacement.
  - The new work-queue r14 outline drops the `a reviewer | done` row. r27, which is new, covers that case, and the old outline stays as deprecated.
  - None of this is i27's.

**The one weakened test in i27's commits is still** `tests/scenarios/supervision_rounds_steps.py` `second_not_refused` (w164, a4e922a6).
- w164's plan lists it under "Tests the decisions break", so this is not a finding.

## Allowances

- **w164:** one row, `second_not_refused`. It holds, as reviews 1-3 found, and the test has not changed since.
- **w165:** "none".
- **w166:** "none".

## Cannot verify

- **The probe of `supervise_change`'s change-list handling was not run.**
  - I wrote `.shop/scratch/i27-branch-review/probe_change.py` for four change lists, run against a temporary initiative directory:
    - capability `initiative`;
    - capability `../escaped`;
    - the same capability twice;
    - an id of another capability and a malformed id.
  - Running it was refused ("This command requires approval"), as in reviews 1-3. I tried no other route, and I deleted the directory.
  - F3-F5 rest on reading `scripts/supervise_change.py:21-31,45`, which is unchanged.
  - This is not a check any work-item names; all of those passed.

## Findings

**The findings of reviews 2 and 3 still hold, unchanged.** The code they name has not changed since.
- **F1** (Minor, no work-item, observation): spec, features and proposals made by hand for i27's bootstrap (9ed288cf, 18cd9812, 5d1bd783).
- **F2** (Minor, w164, drop): ruff, 4 errors (listed above).
- **F3** (Minor, w164, observation): `supervise_change.py:45`. A capability name becomes a file name with no check: `initiative` overwrites initiative.md, and `../x` writes outside the initiative's directory.
- **F4** (Minor, w164, observation): `supervise_change.py:21-31,44-51`. Two entries for one capability overwrite each other.
- **F5** (Minor, w164, observation): `supervise_change.py:26-30`. An id is not checked against `<capability>#r<n>` or `term/<term>`.
- **F6** (Minor, w164, observation): `supervise_rounds.py:107-109`. A failed commit leaves the proposals uncommitted.
- **F7** (Minor, w164, observation): the apply brief does not name the kept drafts.
- **F8** (Minor, w165, observation): `workqueue_request.py:87`. `--delegation ""` is stored.
- **F9** (Minor, w166, drop): `workqueue_start.py:48`. The subject uses the `work:` prefix.
- **F10** (Minor, no work-item, observation): measurements left uncommitted by `work run` (7d8572d6, ab63bd6c).

q5 (i29) asks for F3, F7, F8 and F10.

**N1** (Minor, no work-item: i26's gate round, dbbf9089, observation): `.shop/work/i26/runs/supervision/1-gate/mk.py` is still tracked, and ruff still counts it.

**N2** (Minor, not i27: i28, w171, observation): supervision @r102's old scenario is still deprecated while w171 is green. So is work-queue @r9, with w140 green.

**N3. Minor | not i27 (i25's 159bdfdf, i26's 3d3da4df) | observation.**
- **What:** the suite at the branch's head fails 8 scenarios: requests r4, r5, r12, r20 and r21, and work-queue r26, r27 and r28. Each fails because it has no step definition.
  - Formulate rounds of i25 and i26 committed them to the shared initiative branch before any work-item implements them.
  - w174 (work-queue r26-r28) is `claimed`. i26 has no work-item for requests r20 and r21.
- **Why it matters:**
  - Every implementer that `work run` starts on this branch, for any initiative, gets a brief whose whole-suite run (supervision r24) ends red for reasons outside its work-item.
  - A branch review of any initiative here reads a red suite.
  - Nothing is wrong in i27's code.
- **Fix:** none for i27. The failures end when w174 is green and i26's work-items for requests r20 and r21 are done.
  - If a red suite between formulate and implement is not wanted on a shared branch, a line has to say so. It could, for example, have formulate-round scenarios skipped or marked until their work-item claims them.

**N4. Minor | no work-item | observation.**
- **What:** this review, like review 3, was started although no i27 work-item and no line i27 accepts changed. The commits since review 3 are other initiatives' work on the shared branch.
- **Why it matters:** supervision r27 starts a branch review whenever the initiative branch holds a commit that no kept review has read. On a branch shared by five initiatives, any initiative's commit starts another review of i27, which costs a session each time.
- **Fix:** no i27 change. A line could limit r27 to commits that touch the initiative's work-items or the files they changed.

**What I checked against i27's lines.**
- **The risk I named:** that i25's and i26's spec changes since review 3 changed a line i27 accepts, or contradicted one.
- **What I verified:**
  - `git diff 4640ef08 HEAD -- spec` changes requests r4, r5 and r12, work-queue r14, and supervision r9 and r82. It adds requests r20 and r21, work-queue r26-r28, and supervision r98, r100 and r101.
  - It does not change r91-r97, r66, r19 or r25.
  - The new supervision r9 and r82 add a condition that no request whose asker is this context is in the asker's turn. That does not touch r94 or r97 (no branch review and no measure for an initiative with no work-item).
  - The w164-w166 scenario runs above pass.
- **No code that no line asks for** in i27's commits, and no behaviour that contradicts a line or a Purpose. The code is unchanged since review 3, which found the same.

## Shape

- **Size limit 300:** met. `tools size` prints nothing.
- **CLAUDE.md, the `scripts/supervise*.py` row, is still stale**, and so is the `supervise_rounds.py:1-3` docstring. They name the apply and formulate rounds but neither the integrate round's ending (r91, r96) nor r95's lock on rounds.
  - The check that would show this fixed: the row and the docstring both name the integrate round and r95.
- **Rows that are met:**
  - `supervise_change.py`, `supervise_all.py` and `supervise_drafts.py`;
  - `workqueue_start.py`, `workqueue_request.py` and `scripts/work`;
  - `tests/scenarios/` (one `<capability>_*_steps.py` module a concern).
- **No unreached code or steps:** vulture is clean and `features bindings` is clean.

## Coupling

- **New coupling since review 3:** none, because no code changed.
- **Existing coupling relied on:** the `error_max_turns` subtype of `claude -p` (`supervise_faults.py`).
  - r91 keeps the drafts whichever way a round ends, so a change in that subtype loses nothing of i27's.
  - The stable form would be the plugin's own `result.json` status, which it already reads first.

## Observations

One line each, with its reproduction:
- **F3-F5:** read at `scripts/supervise_change.py:21-31,45`. The probe `.shop/scratch/i27-branch-review/probe_change.py` was refused approval.
- **F6:** `scripts/supervise_rounds.py:107-109` (read).
- **F7:** `grep -n drafts scripts/supervise_brief.py` finds only the integrate brief.
- **F8:** `work request … --delegation ""` writes `delegation: ""` (`workqueue_request.py:87`, read).
- **F10:** the subjects of 7d8572d6 and ab63bd6c say "left uncommitted".
- **N1:** `python3 scripts/tools check --base 3cbd0c52` lists `.shop/work/i26/runs/supervision/1-gate/mk.py:1` and `:19`.
- **N2:** `features deprecated` lists supervision @r102 and work-queue @r9; w171 and w140 are `green`.
- **N3:** `python3 -m pytest -q` at 125b2ad1 gives `8 failed, 870 passed`. Each failure is a `StepDefinitionNotFoundError` in `test_requests.py` or `test_work_queue.py`.
- **N4:** `git diff --name-only 4640ef08 HEAD -- tests scripts agents CLAUDE.md conftest.py hooks skills` prints nothing.
- **Stale module-map row:** CLAUDE.md, the `scripts/supervise*.py` row, and `supervise_rounds.py:1-3`.
