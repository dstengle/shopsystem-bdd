# Branch review of i27 (review 9): findings

**Verdict: DONE.**
- No finding is Critical, and none is triaged fix now.
- Every check that i27's work-items name passed at ce37512e, and I ran each one myself.
- This review re-reviews the fix work-item w187, which answers review 8. It closes F4 and the Shape item.
- F11 (r95 failing at random) got only a margin. No run captured the failure.
  - At ce37512e, r95 passed in the suite and in the w164 and w187 runs.
  - Reading the code shows the lock covers every integrate, apply and formulate round, so reading (b), rounds overlapping, is not supported.
  - On a re-review, F11 is an observation.
- F3, F7 and F10 are now closed by i29's lines r107, r108 and r106, which are green.

## Range and work-items

- **Range:** `3cbd0c52..ce37512e` on `i25-review-findings-to-implementation`. Base 3cbd0c52 is the commit that added `.shop/work/i27/initiative.md`.
- **i27's work-items, all green:**
  - **w164** (supervision r91-r97, r66): 0ca611cf, a4e922a6, 12d95e83. Unchanged since review 1.
  - **w165** (requests r19): 34ee952c. Unchanged.
  - **w166** (work-queue r25): 5c876c93. Unchanged.
  - **w187** (fix of review 8, accepts supervision r91-r97, r66): **bd765f03**, the one commit between `1b5a84f7 work: w187 ready -> claimed` and `8b3775cd work: w187 claimed -> done`, leaving out `work run`'s `work:` commits.
    - It changes `CLAUDE.md`, `supervise_change.py`, `supervise_rounds.py` (docstring only), `supervision_all_steps.py` and the new `tests/scripts/test_supervise_change.py`.
    - Every file is in its fileset. Nothing under `features/` changed.
- **Other initiatives' commits since review 8 (225d3ed2) that touch i27's files:**
  - **i29's w181:**
    - 4d3113e1 (r107): `Changes.unknown` and the refusal in `supervise_rounds.py:106-125`.
    - 5048b72e (r108): `kept_path`.
    - c482f4f8 (r106) and 07d5c24c (r105, r109): `supervise_done.py` and `set_done` in `supervise.py:218`.
    - d87a295b: the r92 Given `integrate_with_changes` now also writes `spec/capabilities/other.md`.
  - **i30's w184:**
    - b1b8562c (r110): a fix is reviewed in the same run, `supervise.py:210-215`.
    - d40c0d26 (r117): a gate with no question asks for approval.
    - cd134f29: r19 at 80 turns, and the deprecated 40-turn @r19 is retired.
- **Commits in the range that belong to no work-item:**
  - The ones of i27 itself are unchanged from review 8 (F1).
  - Since review 8, the rest are `work`, `records` and branch-review commits, plus 0eb572a2 (a hand edit of w184 and w185's Retires). That is i30/i31's, not i27's.

## Suite

`Suite: 885 passed, 10 failed at ce37512e in 56.26 s`

- **The run:** `python3 -m pytest -q -p no:cacheprovider -rf`. It also had 1 skipped and 56 subtests passed. The wall time is pytest's own figure.
- **Parallel:** yes. `pytest.ini` has `addopts = -n auto`.
- **In-process:** no. The steps run `scripts/work` as a subprocess, with `tests/scripts/stub_claude.py` standing in for `claude`.
- It is under 60 s, so its speed is not a finding.
- **The 10 failures** are all `StepDefinitionNotFoundError` on i31's formulated, unimplemented scenarios:
  - @r111 (`supervision.feature:865`), @r114 (`:975`), @r116 (`:962`);
  - @r115, four examples (`:1299`);
  - the new @r83 (`:1246`);
  - two formulate-question scenarios, @r112 and @r113.
- None is i27's. The @r95 scenario passed in this run.

## Checks

- **`pytest -p work_items --work-item w164`:** 153 passed, 1 skipped, 56 subtests passed (23.65 s).
- **`pytest -p work_items --work-item w165`:** 144 passed, 1 skipped, 56 subtests passed.
- **`pytest -p work_items --work-item w166`:** 144 passed, 1 skipped, 56 subtests passed.
- **`pytest -p work_items --work-item w187`:** 153 passed, 1 skipped, 56 subtests passed (17.17 s).
- **`tools check --base 3cbd0c52`:**
  - **ruff:** 34 errors (review 8 had 33).
    - **25 are in tracked round helpers** under `.shop/work/i2x/runs/` (N1).
    - **2 are on w187's lines:**
      - `supervision_all_steps.py:127` RUF007, which is still there (R1);
      - `test_supervise_change.py:7` RUF100, which is new (R2).
    - **2 more are on lines w164 added** (F2): `supervise_brief.py:89` ISC004 and `test_supervision.py:14` I001.
    - **Not i27's:**
      - `supervise_analysis.py:4` I001 (i29);
      - `supervision_intake_steps.py:84` FURB167 (i28);
      - `supervision_proposal_steps.py:118` RUF100;
      - `stub_claude.py:189-190` FURB167, from before Base.
    - w187 fixed review 8's `supervision_all_steps.py:111` FURB167.
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts". The heading does not say `missing`.
- **`tools size --limit 300`:** printed nothing.
- **`features deprecated`:** 5 scenarios: migration-tools @r15, supervision @r83 and @r102, and work-queue @r1 and @r9. The deprecated @r19 was retired by i30's w184.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** not applicable. `scripts/` has no dry-run mode of its own. The only `--dry-run` is git's `git push --dry-run`, which is unchanged.

## Removed and weakened tests

**What I searched:** every `-` line of `git diff -U0 225d3ed2 HEAD -- tests features`. For the range before that, reviews 1-8.

- **In w187's commit:**
  - `supervision_all_steps.py:104` `linger` 1 -> 3.
    - The stand-in waits *up to* that long for another worker to start (`stub_claude.py:35-36,208-210`).
    - This is a setup value. A longer wait leaves more time for an overlap to show. `serial_rounds_apart`'s `ended < started` is unchanged, so the test is not weakened.
  - `:111` `re.M` -> `re.MULTILINE`: the same flag.
  - `:127` `zip(..., strict=False)`: the same behaviour.
  - No test was deleted, and no assert, parametrize case, skip or xfail was touched. The plan's "Tests the decisions break" says none, and that agrees.
- **In other initiatives' commits, on i27's scenarios:** `supervision_integrate_steps.py:43-45` `integrate_with_changes` (r92, w164's step) now writes `spec/capabilities/other.md` (d87a295b, i29).
  - It is setup only, needed because r107 refuses a capability that nothing holds. No assert changed.
  - Both r92 scenarios pass.
- **Not i27's:**
  - `supervision.feature` lost the deprecated 40-turn @r19, retired by i30 under Retires (cd134f29);
  - `reviewer_lists` became a list of results (r110);
  - the `questions_hold` and `{name} is green` step patterns were narrowed.
  - None of these asserts less.
- **In i27's own commits, the one weakened test is still** `supervision_rounds_steps.py` `second_not_refused` (w164, a4e922a6). It is listed in w164's plan.

## Allowances

- **w164:** one row, `second_not_refused`. It holds, and the test has not changed since.
- **w165, w166:** none.
- **w187:** "none". The only test-side change that might need one is the linger value. It changes no `assert`, expected value or parametrize case, so it would hold as `setup`.

## Cannot verify

- **No check that a work-item names went unverified.**
- **F11's cause.** Neither w187 nor this review captured the r95 failure under load. Loop and probe commands are refused approval here.
  - **What I verified instead, by reading:**
    - `supervise_all.py:44` makes one `threading.Lock` and gives it to every `Run` (`:46`).
    - `supervise_rounds.py:58-64` holds it around the whole of `run_round` for each kind in `SERIAL` (`:18`): the session, the merge and the commits.
    - `round()` is the only caller of `run_round`.
  - So rounds overlapping (reading (b)) has no path in the code. The cause that remains is the test's timing or the stand-in's record.
- **The probe of w187's merge** (one id under `adds` in one entry and under `changes` in another; a bare entry) was refused approval. O2 is from reading `supervise_change.py:58-62`.

## Findings

On this re-review of the fix work-item w187, anything but invalid data, the system's own fault on input, or a write where a refusal belongs is an observation. w187 adds no code that no line asks for:
- the merge serves r92 ("a `drafted` capability-proposal for each capability the change list names");
- the dropping of repeated ids serves it too.

- **F4: closed** (w187). `supervise_change.py:58-64` merges every entry for one capability into one proposal.
  - `tests/scripts/test_supervise_change.py:19-26` went red (`assert 3 == 2`, per the report) and is green.
  - **The risk I named:** the merge reorders proposals for distinct capabilities, which would break r92's two-initiatives ids.
  - **What I verified:** `merged` is an insertion-ordered dict keyed by capability, and both @r92 scenarios pass in the w164 and w187 runs.
- **Shape item of review 8: closed** (w187).
  - The `CLAUDE.md:28` `scripts/supervise*.py` row names r91, r96 and r95.
  - The `supervise_rounds.py:1-6` docstring names the integrate round's ending and `round_lock`.
- **F3: closed** by i29's r107 (4d3113e1, green).
  - `Changes.unknown` (`supervise_change.py:38-43`) keeps only names that are stems of `spec/capabilities/*.md` or of a kept draft.
  - A name with `/` or `..` is never such a stem, so it gets no file (`supervise_rounds.py:106-110`).
- **F7: closed** by r108 (5048b72e): `kept_path` is given as the drafts path.
- **F10: closed** by r106 (c482f4f8). The @r106 scenario passes.
- **F11** (Minor, w164/w187, observation): `features/supervision.feature:872` @r95 failed once in review 8's loaded run.
  - w187 gave the stand-in a margin (`linger: 3`) and kept the strict assertion, as its plan's third branch allows.
  - It passed in all three runs here.
  - The lock was verified by reading (Cannot verify). What is left is a possible flaky test, not a wrong answer.
- **R1** (Minor, w187, observation): `tests/scenarios/supervision_all_steps.py:127` still gives RUF007.
  - **What's wrong:** the report says "F2: ruff fixes at the two lines". `strict=False` does not answer "prefer `itertools.pairwise()`", so the report claims more than the commit does.
  - **Fix:** `for (_, _, _, ended), (_, _, started, _) in itertools.pairwise(found):`.
- **R2** (Minor, w187, observation): `tests/scripts/test_supervise_change.py:7`, a new RUF100 (the `# noqa: E402` is unused).
  - **Why it matters:** it adds to `check`'s count.
  - **Fix:** drop the `noqa`.
- **F1** (Minor, no work-item, observation): the spec, features and proposals of i27's bootstrap were made by hand: 9ed288cf, 18cd9812, 5d1bd783. Unchanged.
- **F2** (Minor, w164, drop): `supervise_brief.py:89` ISC004 and `test_supervision.py:14` I001 remain.
- **F5** (Minor, w164, observation): `supervise_change.py:26-30`. Ids are not checked against their form. Unchanged.
- **F6** (Minor, w164, observation): `supervise_rounds.py:118-120`. A failed commit leaves the proposals uncommitted. Unchanged.
- **F9** (Minor, w166, drop): `workqueue_start.py:48`, the `work:` prefix in the commit subject. Unchanged.

**What I checked against i27's lines, in other initiatives' changes to i27's files:**
- **The risk I named:** that r107's filtering (`supervise_rounds.py:106-110`) drops proposals r92 asks for.
  - **What I verified:** it removes only capabilities nothing holds. Both @r92 scenarios, and @r91, @r93 and @r96, pass.
- **The risk I named:** that i30's re-review loop (`supervise.py:210-215`) gives a review to an initiative with no work-item, against r94 and r97.
  - **What I verified:** the loop sits inside `if self.items() and all(...)`, which is unchanged, and @r94 and @r97 pass.
- No behaviour contradicts a line or a Purpose.

## Shape

- **Size limit 300:** met. `tools size` prints nothing.
- **`CLAUDE.md` module map:**
  - The `scripts/supervise*.py` row is met (`CLAUDE.md:28`).
  - The `scripts/supervise_change.py` row ("one drafted capability-proposal for each capability it names") is now met in fact, at `supervise_change.py:58-64`.
  - The `tests/scripts/` row is met: `test_supervise_change.py` tests a case no scenario drives.
- **No unreached code or steps:** vulture is clean, and so is `features bindings`.

## Coupling

- **New coupling:** none in w187.
- **Existing coupling:** the `error_max_turns` subtype of `claude -p` (`supervise_faults.py`), as in review 8.
  - r91 keeps the drafts however a round ends, so a change to that subtype would lose nothing of i27's work.
- **The r95 scenario relies on timing:** the stand-in's `linger` of 3 s (F11).
  - **What would make it stable:** the record shows each round's end before the next round's start, whatever the wait. That is what `serial_rounds_apart` already asserts.

## Observations

One line each, with its reproduction:
- **F11:** `python3 -m pytest -q -p no:cacheprovider -rf` at ce37512e gave `10 failed, 885 passed … in 56.26s`, and r95 was not among the failures. `pytest -p work_items --work-item w164` and `--work-item w187` gave 153 passed each.
- **R1, R2:** `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 3cbd0c52` lists `supervision_all_steps.py:127:49: RUF007` and `test_supervise_change.py:7:48: RUF100`.
- **O2** (Minor, w187, observation; from reading `supervise_change.py:58-62`, the probe refused):
  - One id under `adds` in one entry and under `changes` (or `removes`) in another is written in both lists of the one proposal.
  - An entry that names only a capability gives a proposal with three empty lists.
  - No line names either case. The w187 report names both.
- **N1:** `tools check` lists 25 errors in tracked round helpers under `.shop/work/i26`, `i29`, `i30` and `i31` `runs/`. Exclude `.shop/` from `check`, or keep the helpers in scratch.
- **N2** (not i27): `features deprecated` lists supervision @r102 while w171 (i28) is green, and work-queue @r9 while w140 (i24) is green.
- **N3** (not i27): the suite's 10 failures are i31's formulated scenarios with no steps yet (the `-rf` summary above).
- **N4:** this review is the ninth of i27, and the first since review 8 to contain an i27 commit (bd765f03).
