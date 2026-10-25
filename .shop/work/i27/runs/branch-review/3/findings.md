# Branch review of i27 (review 3): findings

**Verdict: DONE.**
- No finding is Critical, and none is triaged fix now.
- I ran each check i27's work-items name, and each tool the review calls for, at 4640ef08, and each passed or is reported below.
- i27's own code is as it was at review 2 (b82d2c75), but for what i28's work-items changed in it since (see "Since review 2"). F1-F10 of review 2 still hold. They are carried below and not repeated in full.

## Range and work-items

- **Range:** `3cbd0c52..4640ef08` on `i25-review-findings-to-implementation`. Base 3cbd0c52 is the commit that added `.shop/work/i27/initiative.md`.
- **i27's work-items, all green:**
  - **w164** (supervision r91-r97, r66): 0ca611cf, a4e922a6, 12d95e83, between 4910049f and 44e59393.
  - **w165** (requests r19): 34ee952c, between cc16fb45 and f547d55e.
  - **w166** (work-queue r25): 5c876c93, between 117402c4 and 1a6567bd.
- **Commits since review 2 that belong to no i27 work-item.** The branch is shared, so the range now holds other initiatives' work:
  - **i28's work-items** w167-w172. Their code commits are 12f0b295, 50788670, fa6929fb, bcc41527, 55eea183, 2e0f2555, a414d2bd and a1ff989a, each inside its own `claimed`/`done` window. i28's own branch reviews 1 and 2 (cb04d752, 6a6271af) reviewed them.
  - **i28's hand bootstrap** (1649e9d2), and its spec and formulate commits (f85f0d23, 7e6266ca, 79f4b429, 7636eb12). They are like i27's F1: made outside any work-item, and recorded in i28's ledger.
  - **i25's and i26's rounds:** merges 729dd3a0 and 4827eb0b, notes and status commits, and 27 `work answer` commits.
  - **Records:** ab63bd6c (i28's measurement, committed by hand; this is F10 again). 4640ef08 starts i29 for q5.
  - None of these is an i27 finding. Review 1 reviewed i27's work-items and review 2 re-checked them; this review checks only whether later commits changed them. See N1 for one commit outside every work-item that put code under `.shop/`.

## Suite

`Suite: 867 passed, 0 failed at 4640ef08 in 32.6 s`

- 32.6 s is the wall time from `time`; pytest's own figure is 32.28 s. The run also had 1 skipped and 56 subtests passed.
- **Parallel:** yes (`pytest.ini`: `addopts = -n auto -m "not fixture"`).
- **In-process:** no. The When steps run `scripts/work` as a subprocess, with `tests/scripts/stub_claude.py` standing in for `claude`.
- The suite runs in under 60 s, so this is not a finding.

## Checks

- **`pytest --work-item w164`:** 152 passed, 1 skipped (the extra one since review 2 is i28's added r92 case).
- **`pytest --work-item w165`:** 143 passed, 1 skipped.
- **`pytest --work-item w166`:** 143 passed, 1 skipped.
- **`tools check --base 3cbd0c52`:** exit 1.
  - **ruff:** 10 errors.
    - **4 on lines w164 added** (review 2's F2, Minor, drop):
      - `scripts/supervise_brief.py:82` ISC004 (it was :74);
      - `tests/scenarios/supervision_all_steps.py:111` FURB167 and `:127` RUF007;
      - `tests/scenarios/test_supervision.py:14` I001.
      - Review 2's fifth, `supervision_integrate_steps.py:72`, is gone: i28 changed `re.M` to `re.MULTILINE`.
    - **2 from i28's work-items** (not i27's):
      - `tests/scenarios/supervision_intake_steps.py:65` FURB167;
      - `tests/scenarios/supervision_proposal_steps.py:96` RUF100.
    - **2 in `.shop/work/i26/runs/supervision/1-gate/mk.py`:** `:1` I001 and `:19` SIM115 (N1).
    - **2 from before Base:** `tests/scripts/stub_claude.py:186` and `:187` FURB167.
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts". The heading does not say `missing`.
- **`tools size --limit 300`:** printed nothing. Of the files i27 touched, the largest are `supervise.py` (248 lines) and `supervise_brief.py` (143).
- **`features deprecated`:** 4 scenarios.
  - migration-tools @r15, work-queue @r1 and work-queue @r9 are as in review 2.
  - supervision @r102 is new: i28's 7636eb12 deprecated it, and see N2.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** not applicable. The only `--dry-run` in `scripts/` is `git push --dry-run`, which is git's own check.

## Removed and weakened tests

**What I searched:**
- every `-` line of `git diff 3cbd0c52 HEAD -- tests features`, as reviews 1 and 2 did;
- again since review 2, in `git diff b82d2c75 HEAD -- tests features`.

**What I looked for:** deleted test functions, dropped parametrize or Examples rows, removed or loosened asserts, added skips or xfails, removed scenarios.

**The one weakened test is still** `tests/scenarios/supervision_rounds_steps.py` `second_not_refused` (w164, a4e922a6).
- **What it proved:** the second `work run` exits 0 with no `work:` error.
- **What it asserts now:** for the r84 integrate case, no "not committed" in stderr, and that a second integrate round was started.
- w164's plan lists it under "Tests the decisions break", so this is not a finding.

**Since review 2, nothing was removed or loosened.**
- The `-` lines are import rewrites, `re.M` changed to `re.MULTILINE` in `listed`, and the stub's `kind` regex widened to capture the node name (`stub_claude.py:186`).
- That stub change only adds the `round:<kind>:<name>` key, and keys that already existed resolve as before.
- `features/` changed only by additions, plus the deprecation tag on the r102 scenario that 7636eb12 replaced. That commit is a formulate round, not a work-item.

## Allowances

- **w164:** one row, `second_not_refused`. The plan lists it; I checked it against a4e922a6 as review 2 did.
- **w165:** "none". 34ee952c only adds steps.
- **w166:** "none". 5c876c93 removes and loosens no assertion.

## Cannot verify

- **The probe of `supervise_change`'s change-list handling was not run.**
  - I wrote `.shop/scratch/i27-branch-review/probe_change.py` for five change lists:
    - capability `initiative`;
    - capability `../escaped`;
    - the same capability twice;
    - another capability's id;
    - a malformed id.
  - It was refused ("This command requires approval"), as in reviews 1 and 2. I tried no other route, and I deleted the directory.
  - F3-F5 therefore rest on reading `scripts/supervise_change.py:22-31,45`. Line 45 is still `path = self.dir / (one["capability"] + ".md")`, with no check of the name or of the form of an id.
  - This is not a check any work-item names; all of those passed.

## Findings

**Review 2's findings still hold:**
- **F1** (Minor, no work-item, observation): spec, features and proposals made by hand.
- **F2** (Minor, w164, drop): ruff, now 4 errors (listed above).
- **F3** (Minor, w164, observation): `supervise_change.py:45`. A capability name becomes a file name with no check: `initiative` overwrites initiative.md, and `../x` writes outside the directory.
- **F4** (Minor, w164, observation): `:21-31`. Two entries for one capability overwrite each other.
- **F5** (Minor, w164, observation): `:27-29`. An id is not checked against `<capability>#r<n>` or `term/<term>`.
- **F6** (Minor, w164, observation): `supervise_rounds.py:107-109`. A failed commit leaves the proposals uncommitted.
- **F7** (Minor, w164, observation): the apply brief does not name the kept drafts. The gate brief now names the proposal's adds, changes and removes (i28's r104), but still not the drafts path.
- **F8** (Minor, w165, observation): `workqueue_request.py:87`. `--delegation ""` is stored.
- **F9** (Minor, w166, drop): `workqueue_start.py:48`. The subject uses the `work:` prefix.
- **F10** (Minor, no work-item, observation): the measurement was left uncommitted. It happened again for i28 (ab63bd6c).

Accepted lines of q5 already ask for F3, F7, F8 and F10. i29, started at 4640ef08, fulfils q5.

**N1. Minor | no work-item (i26's gate round, dbbf9089) | observation.**
- **What:** `.shop/work/i26/runs/supervision/1-gate/mk.py` is a tracked Python file, a helper that the gate session wrote into its stage directory. `work run` committed it with the stage directory, in a status commit.
- **Why it matters:** ruff now counts it in every `tools check`, and CLAUDE.md's rules (size, lint) cover every tracked Python file. A session's scratch script is project code no line asks for.
- **Fix:** keep only the stage's own records (`brief.md`, `result.json`, `session.json` and the stage's outputs) when committing a stage directory, or exclude `*.py` under `.shop/work/*/runs/` from `tools check`. Either way, it should be decided by a line.

**N2. Minor | not i27 (i28, w171) | observation.**
- **What:** supervision @r102's old scenario is deprecated (7636eb12), and w171, which accepts supervision#r102, is green. The deprecated scenario was not retired with its binding.
- This is the same pattern as work-queue @r9 and w140 in review 2.
- **Fix:** retire both in a work-item that lists them under Retires.

**Since review 2: i28's changes to i27's code, checked against i27's lines.**
- **`supervise_change.py:47-49`:** a proposal's id is now `<initiative>-<capability>` (r92, as i28 changed it). r92 still holds: a `drafted` proposal is written for each capability, with its ids. w164's r92 scenarios pass.
- **`supervise_all.py:29-35`** starts the initiative of an accepted, unfulfilled request (r103) before it takes the open initiatives.
  - **The risk I named:** that this would move something before r66's or r10's refusals.
  - **What I verified:** it calls `run.check()` on every open initiative and `Intake.check()` on every request before the first `start`, and then calls `check()` again on all of them (`:30-38`).
  - r66 holds: every initiative that is neither done nor abandoned is still taken.
- **`supervise_brief.py:76`:** the integrate brief gains a line of ids drafted elsewhere (r102). It leaves r91's drafts path and r92's change-list form as they were.
- **No code that no line asks for**, in i27's commits or in the changes to them.
- **No behaviour that contradicts a line or a Purpose:** r91-r97, r66, r19 and r25 are each still met, as the work-item runs above show.

## Shape

- **Size limit 300:** met.
- **CLAUDE.md:28, the `scripts/supervise*.py` row, is still stale** (review 2's observation). It and the `supervise_rounds.py:1-3` docstring name only the apply and formulate rounds (r70, r71, r80, r83), not the integrate round's ending or r95's round lock.
  - The check that would show this fixed: the row and the docstring both name the integrate round and r95.
- **Rows that are met:**
  - `supervise_change.py` (CLAUDE.md:29);
  - `supervise_all.py` (:30);
  - the new `supervise_drafts.py` row (:32, i28);
  - `workqueue_start.py`, `workqueue_request.py`, `scripts/work` and `tests/scripts/`.
- **No unreached code or steps:** vulture is clean and `features bindings` is clean.

## Coupling

- **New coupling in i27:** none. The `changes` field is the plugin's own result.
- **Existing coupling relied on:** the `error_max_turns` subtype of `claude -p` (`supervise_faults.py`). r91 keeps the drafts on every ending, so a change in that subtype loses nothing.

## Observations

One line each, with its reproduction:
- **F3-F5:** read at `scripts/supervise_change.py:22-31,45`. The probe `.shop/scratch/i27-branch-review/probe_change.py` was refused approval.
- **F6:** `supervise_rounds.py:107-109` (read).
- **F7:** `grep -n drafts scripts/supervise_brief.py` finds only the integrate brief.
- **F8:** `work request … --delegation ""` writes `delegation: ""` (`workqueue_request.py:87`, read).
- **F10:** ab63bd6c's and 7d8572d6's subjects say the measurement was "left uncommitted".
- **N1:** `python3 scripts/tools check --base 3cbd0c52` lists `.shop/work/i26/runs/supervision/1-gate/mk.py:1` and `:19`; `git log --diff-filter=A -- <that path>` gives dbbf9089.
- **N2:** `features deprecated` lists supervision @r102; `grep -E '^(status|accepts)' .shop/work/i28/w171.md` gives `green` and `[supervision#r102]`.
- **Stale deprecation:** work-queue @r9 is still deprecated while w140 is green.
- **Stale module-map row:** CLAUDE.md:28 and `supervise_rounds.py:1-3`.
