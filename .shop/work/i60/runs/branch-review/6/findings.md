# Branch review of i60 (review 6)

**Verdict: DONE_WITH_CONCERNS.** The whole suite passes at the head, and i60's own work-items have no new finding:

- w233 (supervision#r211) is `green`.
- w235 (`work delegate` and its hook, requests r65–r68 and r70–r72) is `green`.
- w234 is `withdrawn`.

The review goes to the person for two reasons:

- **Finding 1 (carried from reviews 2–5, Important, fix now):** i54/w232's `work show <request>` still leaves out every line that has no line outcome. The commit is in this range. w232 is still `awaiting-answer` on this very question.
- **`tools check` exits 1** with 12 ruff errors. There were 8 at review 5. None of the 12 is in a file that w233 or w235 wrote (Findings 4, 5 and 11).

New since review 5 (`dfd35e16`): this range now holds i63's w236 and w237, i48's w238 (in progress), and intakes q43–q45. Among these, one test assertion was narrowed under an allowance that does not hold (Finding 12, Important, observation).

## Range and work-items

- **Range:** `ae85edd3a2ce3488f4d930ac5814845eea5e6178..f6ff81c0925b69fbe09318de1c2ec94ab05ad52c` on `main`.
- **i60** is `started` and fulfils q39. It holds:
  - **w233:** `green`, under supervision, accepts supervision#r211.
    - Transitions: `6b7926df` to `91d43216`.
    - Change: `4e206ec4` (steps only).
  - **w234:** `withdrawn` (`9602238a`).
  - **w235:** `green`, under requests, accepts r65–r68 and r70–r72.
    - Transitions: `0a215b99` to `dfd35e16`.
    - Changes: `ed25c279` and `ab71c3fc`.
  - **Proposals:** i60-supervision and i60-requests are both `formulated`.
- **Every other commit is marked `none`** (Finding 2). i60 runs on `main`, so other initiatives' commits fall in its range:
  - i54: w231, w232;
  - i61, i62;
  - i63: w236, w237, now `done`;
  - i48: w238, `awaiting-answer`;
  - i57: abandoned;
  - intakes q40–q45.

## Suite

`Suite: 1084 passed, 0 failed at f6ff81c in 51.69 s`

- **Other results:** 1 skipped, 18 xfailed, 6 xpassed, 56 subtests passed. Exit 0.
- **The 18 xfailed:**
  - 11 are w212's requests scenarios;
  - 2 are w238's supervision r188 and r189 (new since review 5);
  - 5 are work-queue r62 cases.
- **Parallel:** yes, `-n auto` (pytest-xdist; the output shows "bringing up nodes").
- **In-process:** no. The step definitions run the scripts as subprocesses (`tests/scenarios/conftest.py`, verified in review 4; the range does not change it).
- **Under 60 s,** so the subprocess design is no finding. At 51.69 s it is close, up from 35.52 s at review 5. The r214–r218 and r188/r189 scenarios run whole `work run`s.
- **Dry-run against real mode:** the system has no dry-run mode of an operation, so no agreement test is owed. This is unchanged since review 2.

## Checks

All runs are at `f6ff81c0`.

- **w233's check:** `w233.md` names no `check:`.
  - Its scenarios: exit 0, `182 passed, 1 skipped, 56 subtests passed in 5.59s`.
  - Both r211 examples (`[before]` and `[after]`) appear in the run's warnings, so they ran.
- **w234's scenarios** (withdrawn): exit 0, `181 passed, 1 skipped, 56 subtests passed in 5.38s`.
- **w235's check:** `w235.md` names no `check:`.
  - Its scenarios: exit 0, `191 passed, 1 skipped, 56 subtests passed in 5.16s`.
- **tools check `== ruff ==`:** exit 1, 12 errors.
  - `.shop/work/i60/runs/requests/23-formulate/splice.py:2,3,8` SIM115 (Finding 4).
  - `.shop/work/i60/runs/requests/29-formulate/splice.py:2,3,8` SIM115 (Finding 4).
  - `.shop/work/i63/runs/supervision/1-gate/mk.py:1` I001 and `:10` SIM115. New: i63's gate round (Finding 4).
  - `tests/scenarios/test_supervision.py:14` I001 (Finding 5).
  - `tests/scenarios/work_queue_list_steps.py:134` RUF015 (Finding 5).
  - `tests/scripts/stub_claude.py:208` and `:209` FURB167. New: the file was touched by `fd8364d1` (Finding 11).
- **tools check `== vulture ==`:** clean.
- **tools check `== import-linter ==`:** "the project states no import contracts". No heading says `missing`.
- **tools size:** exit 0, printed nothing. No file is over the limit, touched or not.
- **features deprecated:** exit 0, 20 deprecated scenarios.
  - **New:** r28 is deprecated "for: removal" (`566b7302`, an i63 formulate round). In effect r218 replaces it, and r218's work-item, i63/w236, is `green`. This is named under Findings, item 13.
  - **r23 ×2** are deprecated for r62. The r62 outline is still xfail ("accepted by work-queue"), so it is not green.
  - **r34 and r35** are "for: removal". Their replacements r60 and r61 are w232's, which is `awaiting-answer`.
  - **The `<reply>` delegation scenario** reads "for: r209 and r210 | no scenario has that title". This predates the range.
- **features bindings:** exit 0, "every binding names a scenario".

## Removed and weakened tests

What I searched the change for:

- deleted `def test_` or step functions;
- dropped Examples rows or parametrize cases;
- `assert`s removed, loosened or narrowed;
- skip or xfail added;
- step patterns changed;
- scenarios removed from `features/`.

What I found:

- **`tests/scenarios/supervision_faults_steps.py:146-148` `is_failed`** (i63/w236, `94f0a748`). **This is new since review 5.**
  - The clean-status assertion `git status --porcelain -- .shop/work == ""` now excludes `.shop/work/i2`.
  - It proved that `.shop/work/` as a whole is back to its last commit after a fault.
  - w236's plan (`.shop/work/i63/runs/w236/2-plan/plan.md:29-36`) lists "None" under "Tests the decisions break".
  - The report's allowance row does not hold (Finding 12).
- **`tests/scenarios/requests_flow_steps.py:99` `show_prints`** (i54/w232, `a5d6b59b`) is loosened from the whole output to its first line. w232's plan lists it (reviews 2–5).
- **`tests/scenarios/work_queue_list_steps.py:56` `prints_question`** moved from `parsers.parse` to an anchored `parsers.re`. Its assertion is unchanged.
- **`tests/scenarios/requests_steps.py:59-65` `the_upstream_runs`** (w235) gains a delegate branch. Resolve's branch is unchanged. It is listed in w235's plan §4.
- **`tests/scenarios/supervision_delegation_steps.py:14-40`** (w233): the old Given keeps its pattern and its files. Nothing is weakened.
- **`tests/scripts/stub_claude.py:100-120, 236-240`** (`fd8364d1`, i63/w237): git calls now retry while `index.lock` is held. Failure still raises (`check_returncode`), so nothing is weakened.
- **`features/`:** formulate rounds added r188, r189, r211, r214–r216, r218, r59–r62 and r65–r72. They tagged r23 ×2, r28, r34 and r35 `@deprecated`. Nothing was removed, and no work-item's commit touches `features/`.
- **No skip or xfail was added by hand.** The w238 xfails come from `work_items` (its scenarios are not yet green).

## Allowances

- **w233:** "none". It holds.
- **w235:** "none". It holds.
- **i63/w236, `4-implement/report.md:11`:** `is_failed — setup/interim: pathspec of the clean-status assertion excludes .shop/work/i2`. It does not hold:
  - **as `setup`:** the diff changes the `assert` itself (its pathspec), so what it checks is narrower;
  - **as `interim`:** `is_failed` was first committed before `Base`; only the Given steps came "from this initiative".

  See Finding 12.
- **i63/w237:** "none". `fd8364d1` changes the stub, not an assertion. It holds.
- **i54/w232:** "none". Its loosened test is in its plan.

## Cannot verify

None. Every check comes from a run at `f6ff81c0`.

## Findings

### 1. Important (fix now): `work show <request>` leaves out every line that has no line outcome

- **Work-item:** i54/w232, commit `a5d6b59b`. w232 is `awaiting-answer` on this question.
- **File:** `scripts/workqueue_list.py:85-88`. `if outcome is not None:` prints a line only when it has an outcome. I re-read it at the head, and it is unchanged.
- **What is wrong:** work-queue r59 asks for the request's "lines with their line outcomes". A request not yet settled is shown with fewer lines, or with none. That is a wrong answer.
- **Fix:** print every line, with its outcome or `no outcome yet`. Do it under w232 (answer its question with `--change`), not as a new i60 item.
- **Test that would show it (not run):** `work show q1`, where line 2 has no outcome, asserting that line 2 is printed.

### 2. Minor (observation): the range holds commits of no i60 work-item, and more hand edits of workflow files

- **Work-item:** none.
- **Where:** every commit is marked `none` except those of w233, w234 and w235.
- **Commits that carry code:**
  - i54: `afc4aa72` (w231) and `a5d6b59b` (w232);
  - i63: `d8f57cc8` and `94f0a748` (w236), `a9cb7536` and `fd8364d1` (w237).
- **Hand edits:**
  - i60: `556cba3b` and `c0d2f0e2`;
  - requests: `9b453fd2`;
  - i63: `28ce4056` and `a411ea7a`, proposal ids restored after redrafts (q34 again);
  - w238 statuses: `ef8e1609` and `f7659913`, set by hand from `claimed`/`failed` to `ready`;
  - `74132b41`: q31 withdrawn and i57 abandoned.
- **Why it matters:**
  - Other initiatives' commits, and their faults, hold up i60's review.
  - Hand edits bypass `work`'s checks.
- **Fix:** give a branch review only the commits of its initiative's own nodes, or run each initiative on its own branch. Give `work retry` a way to return to `ready` after an implement failure; two hand edits say it lacks one.

### 3. Minor (observation): q34's cause hit again in i63, and its fix is under way as i48/w238

- **Work-item:** none (i63's proposals). The fix is i48/w238 (r188, r189), which is `awaiting-answer`.
- **File:** `scripts/supervise_change.py` (`rewrite_lists`), outside this range's change.
- **Reproduction:** `28ce4056` and `a411ea7a` restore i63's proposal ids by hand. The suite's xfail lines for r188 and r189 ("accepted by w238") show the fix is not yet green.

### 4. Minor (observation): round helper scripts stay tracked under `.shop/work/*/runs/` and fail `tools check`

- **Work-item:** none (i60 formulate rounds 23 and 29, and i63 gate round 1).
- **Files:**
  - `.shop/work/i60/runs/requests/23-formulate/splice.py:2,3,8`
  - `.shop/work/i60/runs/requests/29-formulate/splice.py:2,3,8`
  - `.shop/work/i63/runs/supervision/1-gate/mk.py:1,10` (new)
- **Fix:** exclude `.shop/` from ruff and vulture, or have `work run` leave a session's helper scripts out of a stage's kept files.
- **Reproduction:** the brief's `### tools check`, exit 1.

### 5. Minor (observation): two ruff errors older than their hunks, in files the range touched

- **Errors:**
  - `tests/scenarios/test_supervision.py:14` I001;
  - `tests/scenarios/work_queue_list_steps.py:134` RUF015.
- **Fix:** run `ruff --fix`, and use `next(...)`.
- **Reproduction:** the brief's `### tools check`.

### 6. Minor (observation): r72 is shown by a session double

- **Work-item:** w235.
- **File:** `tests/scenarios/requests_session_steps.py:19-29`.
- **What is not shown:** that a live session obeys the hook. This follows the plan's Decision 6, on supervision r120's precedent.
- **Test that would show it (not run):** none in the suite. Only an observed session would show it.

### 7. Minor (observation): `work show <request> --json` gives none of what r59 lists

- **Work-item:** w232 (i54).
- **File:** `scripts/workqueue_list.py:102`. The JSON object is `{request, status, turn}` only.
- **Test that would show it (not run):** `work show q1 --json` on the r59 fixture.

### 8. Minor (observation): `request_parts` crashes on a section entry whose number is not an integer

- **Work-item:** w232 (i54).
- **File:** `scripts/workqueue_list.py:85,89,93`. `int(e[0])` is applied to whatever precedes `". "` in an entry. Today `work` writes only numbered entries.
- **Test that would show it (not run):** `work show q1` with `## Lines` holding `x. y`, asserting a refusal and exit 1.

### 9. Minor (observation): 6 xpassed scenarios that the suite's output does not name

- **Work-item:** unknown.
- **What is wrong:** the run uses `-rfEx`, and `work_items` marks expected failures non-strict.
- **Fix:** add `-rX` to the whole-suite run, or make the expected failures strict.
- **Test that would show it (not run):** the whole-suite command with `-rX`.

### 10. Minor (drop): the w235 reviewer's two findings

- The hook does not read its stdin (`scripts/migrate_prompt.py:31-36`).
- The hook's text is repeated on every prompt (`:24-28`).

### 11. Minor (observation): `stub_claude.py` keeps two ruff errors in a file `fd8364d1` touched

- **Work-item:** i63/w237 (`fd8364d1`, between w237's claim and done).
- **File:** `tests/scripts/stub_claude.py:208-209` FURB167 (`re.M`). Both lines are outside the commit's hunks, so the errors are older than it.
- **Fix:** use `re.MULTILINE`.
- **Reproduction:** the brief's `### tools check`.

### 12. Important (observation): `is_failed`'s clean-status assertion was narrowed under an allowance that does not hold

- **Work-item:** i63/w236, commit `94f0a748`.
- **File:** `tests/scenarios/supervision_faults_steps.py:146-148`.
- **What is wrong:**
  - The assertion that `.shop/work/` is clean after a fault now excludes `.shop/work/i2`.
  - The report calls this `setup/interim`, but the `assert` itself changed, and the step predates `Base`.
  - The plan's "Tests the decisions break" says "None".
- **Why it matters:**
  - Any `is_failed` scenario with an i2 no longer checks i2's part of the checkout.
  - In the r218 scenario, i2's change is meant to be left alone by i1's run (r215) and taken in by i2's own sessions, but nothing now checks that it ends committed or put back. The comment says the outcome is timing-dependent.
  - Single-initiative scenarios have no i2, so for them the narrowing changes nothing.
- **Fix:**
  - Restore the full check, or assert i2's path separately as either committed by i2 or as i2's session left it.
  - Have the plan list the change, or answer it as a question.
- **Triage:** observation. No wrong answer, crash or data loss follows from it. It is hardening of the test.
- **Reproduction:** the diff hunk at `supervision_faults_steps.py:143-148`, and `.shop/work/i63/runs/w236/4-implement/report.md:11`.

### 13. Minor (observation): r28 is deprecated "for removal" though r218 replaces it, and r218 is green

- **Work-item:** none (formulate round `566b7302`). r218 belongs to i63/w236, which is `green`.
- **File:** `features/supervision.feature:569-571`.
- **What it means:** `features deprecated` cannot tell that r28's replacement is delivered, so the scenario is not removed when it could be.
- **Fix:** retire r28's scenario and its binding now, or mark it "for: r218".
- **Reproduction:** the brief's `### features deprecated` line for r28, and the spec diff, where r28 is in `retired` and r218 is added.

### Risks checked, no finding

- **`supervise_faults.checkout_changes`** (`scripts/supervise_faults.py:104-129`, i63):
  - Other runs' `run.rel(run.dir) + "/"` are skipped before the own-path and log checks.
  - So i2's `log.jsonl` is no longer rewritten by i1's run. That matches r215.
  - A single-initiative group has no "others", so r218 and r28's put-back stay as before.
  - It serves r214, r215, r216 and r218. It is not code that no line asks for.
- **`git_retry` in the stub:** it keeps `check` behaviour for git (it raises once the deadline passes or on any other error). Non-git Bash is unchanged.
- **i60's own code** (w235's `delegate` and hook, w233's steps): unchanged since review 5. Its checks there hold:
  - the field round-trip through `supervise_answers`;
  - insert-before-`---`;
  - refusal before write;
  - the hook at exit 0.
- **Code that no line asks for:** none.
  - `delegate` serves r65–r71.
  - `migrate prompting` serves r72.
  - `request_parts` serves work-queue r59.
  - `checkout_changes` serves r214–r218.
  - The stub change is test infrastructure.

## Shape

- **CLAUDE.md size limit:** met. `tools size` printed nothing.
- **Module map:**
  - `scripts/migrate_prompt.py`: a new concern with a new row (`CLAUDE.md:19`). Met.
  - `scripts/workqueue_request.py`: `delegate` sits under a row that names it. Met.
  - `scripts/work` and `scripts/migrate`: parsing and dispatch only. Met.
  - `scripts/supervise_faults.py`: under `scripts/supervise*.py` ("faults"). Met.
  - `scripts/workqueue_list.py`: `request_parts` sits under `work show <target>`. Met.
  - `hooks/hooks.json`: the row names only "the plugin's SessionStart hook", but the file also holds UserPromptSubmit and PreCompact. Partly met. Fix: widen the row.
  - `tests/scenarios/`: `requests_session_steps.py` and `supervision_merge_steps.py` are one module a concern. Met.
  - `tests/scripts/stub_claude.py`: a test double under `tests/scripts/`. Met.
- **Code and steps that no scenario reaches:** none found.
  - The new `supervision_faults_steps.py` Givens and Thens are used by r214, r215, r216 and r218.
  - `supervision_merge_steps.py` is used by r187.
  - `write_q1(None)` is used by r211 `after`.
  - Step `two_sessions_change` is used by r218.
  - Step `another_session_changes` is still used by the deprecated r28.
- **Behaviour against Purpose:** nothing in w233 or w235 contradicts a line. The one contradiction is Finding 1 (work-queue r59, w232).

## Coupling

- **pytest-bdd on pytest internals:** `PytestRemovedIn10Warning` (`pytest_bdd/compat.py:28`). This breaks under pytest 10. Fix: pin `pytest<10`, or upgrade pytest-bdd.
- **Unregistered marks:** `deprecated` and r209–r218 warn `PytestUnknownMarkWarning`, and would break under `--strict-markers`. Fix: register them in the conftest.
- **Claude Code's hook contract:** `UserPromptSubmit` relies on the published event name, `${CLAUDE_PLUGIN_ROOT}`, and stdout being added to context on exit 0. It also relies on one point that is not published: that the hook's cwd is the session's repository (`Path.cwd()`; the stdin `cwd` field is ignored). If that changed, the hook would fall silent and break nothing. Fix: read `cwd` from stdin and fall back to `Path.cwd()`.
- **git:** driven through its CLI, on published behaviour.
  - The stub's retry depends on the stderr text naming `index.lock`. That is not a published contract, but it is long stable, and a change would only bring back a flaky failure.
  - Fix: retry on any non-zero exit while `.git/index.lock` exists.

## Observations

- **F2:** the brief's `## Commits` marks every commit `none` except those of w233, w234 and w235. Hand edits: `556cba3b`, `c0d2f0e2`, `9b453fd2`, `28ce4056`, `a411ea7a`, `ef8e1609`, `f7659913`, `74132b41`.
- **F3:** i63's proposal ids were restored by hand twice. The fix, w238 (r188, r189), is xfail in the suite run. Not run.
- **F4:** the brief's `### tools check` shows SIM115 ×7 and I001 ×1 under `.shop/work/*/runs/`.
- **F5:** the brief's `### tools check` shows I001 at `test_supervision.py:14` and RUF015 at `work_queue_list_steps.py:134`.
- **F6:** `requests_session_steps.py:27` shows the double acting on the hook's text. A live session's obedience was not run.
- **F7:** `workqueue_list.py:102` gives JSON with three keys. Not run.
- **F8:** `workqueue_list.py:85` calls `int(e[0])` on any entry. Not run.
- **F9:** the brief shows "6 xpassed" and no XPASS line. Not run with `-rX`.
- **F11:** the brief's `### tools check` shows FURB167 at `stub_claude.py:208` and `:209`.
- **F12:** `supervision_faults_steps.py:148` holds `":(exclude).shop/work/i2"`. w236's report row says `setup/interim`. Not run.
- **F13:** `features deprecated` shows r28 "for: removal", while r218 (w236, `green`) replaces it.
- **hooks.json row:** `CLAUDE.md` says "SessionStart hook", while `hooks/hooks.json` holds three hooks.
