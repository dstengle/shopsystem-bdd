# Branch review of i60 (review 5)

**Verdict: DONE_WITH_CONCERNS.** The whole suite passes at the head, and i60's two delivered work-items, w233 (supervision#r211) and w235 (`work delegate` and its UserPromptSubmit hook, requests r65–r68, r70–r72), have no finding to fix now. Two things still need attention:

- **Finding 1 (carried over from reviews 2–4, Important, fix now):** i54/w232's `work show <request>` still leaves out every line that has no line outcome. The commit is in this range. w232 is `awaiting-answer` on this very question. Fix it under w232, and do not draft it again in i60.
- **`tools check` exits 1** on eight ruff errors (Finding 4, Finding 5). None of them is in a file w233 or w235 wrote.

Review 4's data-loss finding (i60-requests lost r65–r71) was repaired by hand in `556cba3b`. Its cause in `work run` is raised as q34, so it is now an observation (Finding 3).

## Range and work-items

- **Range:** `ae85edd3a2ce3488f4d930ac5814845eea5e6178..dfd35e160395d06871b12d900c10508980511ba3` on `main`.
- **i60** is `started` and fulfils q39. It holds:
  - **w233:** `green`, under supervision, accepts supervision#r211. Its transition commits are `6b7926df` to `91d43216`. Its only change is `4e206ec4` (steps).
  - **w234:** `withdrawn` (`9602238a`). It accepted r72 alone, after the proposal's lists were cut.
  - **w235:** `green`, under requests, accepts requests r65, r66, r67, r68, r70, r71 and r72. Its transition commits are `0a215b99` to `dfd35e16`. Its changes are `ed25c279` and `ab71c3fc`.
  - **Capability-proposals:** i60-supervision is `formulated`. i60-requests is `formulated`, with adds r65–r68 and r70–r72, and removes r69.
- **Every other commit is marked `none`** (Finding 2). This is because i60 runs on `main`, so other initiatives' commits are in its range.

## Suite

`Suite: 1080 passed, 0 failed at dfd35e16 in 35.52 s`

- **Other results:** 1 skipped, 16 xfailed, 6 xpassed, 56 subtests passed. Exit 0.
- **The 16 xfailed:**
  - 11 are w212's requests scenarios ("accepted by w212");
  - 5 are work-queue r62 cases ("accepted by work-queue").
- **Since review 4:** the 10 r65–r71 failures are now passes.
- **Parallel:** yes, `-n auto` (pytest-xdist).
- **In-process:** no. The step definitions run the scripts as subprocesses (`tests/scenarios/conftest.py:33-34`, verified in review 4; unchanged in the range). The suite is under 60 s, so this is no finding.
- **Dry-run against real mode:** the system has no dry-run mode of one operation of its own (review 2). No agreement test is owed.

## Checks

All runs are at `dfd35e16`.

- **w233's check:** `w233.md` names no `check:`.
  - Its scenarios, `pytest -n auto -p work_items --work-item w233`: exit 0, `182 passed, 1 skipped, 56 subtests passed in 6.99s`.
  - Both r211 examples ran. The warnings name `[before]` and `[after]`.
- **w234's scenarios** (withdrawn): exit 0, `181 passed, 1 skipped, 56 subtests passed in 4.92s`.
- **w235's check:** `w235.md` names no `check:`.
  - Its scenarios: exit 0, `191 passed, 1 skipped, 56 subtests passed in 4.79s`.
- **tools check `== ruff ==`:** exit 1, eight errors.
  - `.shop/work/i60/runs/requests/23-formulate/splice.py:2:5`, `:3:5` and `:8:1`: SIM115.
  - `.shop/work/i60/runs/requests/29-formulate/splice.py:2:5`, `:3:5` and `:8:1`: SIM115. This file is new since review 4 (Finding 4).
  - `tests/scenarios/test_supervision.py:14:1`: I001 (Finding 5).
  - `tests/scenarios/work_queue_list_steps.py:134:12`: RUF015 (Finding 5).
- **tools check `== vulture ==`:** clean.
- **tools check `== import-linter ==`:** "the project states no import contracts". No heading says `missing`.
- **tools size:** exit 0, printed nothing. No file is over the limit, touched or not.
- **features deprecated:** exit 0, 19 deprecated scenarios.
  - r23 ×2 are deprecated for r62. The r62 outline is still xfail ("accepted by work-queue"), so its work-item is not `green`.
  - r34 and r35 are "for: removal". Their replacements r60 and r61 belong to w232, which is `awaiting-answer`.
  - The `<reply>` delegation scenario reads "for: r209 and r210 | no scenario has that title". This predates the range (review 4).
  - No deprecated scenario has a replacement whose work-item is `green`.
- **features bindings:** exit 0, "every binding names a scenario".

## Removed and weakened tests

What I searched the change for:

- deleted `def test_` or step functions;
- dropped Examples rows or parametrize cases;
- `assert`s removed or loosened;
- skip or xfail added;
- changed step patterns;
- scenarios removed from `features/`.

What I found:

- **`tests/scenarios/requests_flow_steps.py:99` `show_prints`** (i54/w232, `a5d6b59b`) is loosened. It used to assert the whole `show` output and now asserts only its first line. It proved that `work show` printed just `<request> delivered asker`. w232's plan lists it under "Tests the decisions break" (reviews 2–4), so it is no finding.
- **`tests/scenarios/work_queue_list_steps.py:56` `prints_question`** (w232) moved from `parsers.parse` to an anchored `parsers.re`. The assertion is unchanged, so it is not weakened.
- **`tests/scenarios/requests_steps.py:59-65` `the_upstream_runs`** (w235, `ed25c279`) gains a delegate branch. Resolve's branch is unchanged under `elif`, and no assertion changes. It is listed in w235's plan §4.
- **`tests/scenarios/supervision_delegation_steps.py:14-40`** (w233, `4e206ec4`): the old Given keeps its pattern and writes the same two files through `start_i1` and `write_q1`. Nothing is weakened.
- **`features/`:** formulate rounds tagged r23 ×2, r34 and r35 `@deprecated`. Nothing was removed. No work-item commit touches `features/`.
- **No skip or xfail was added.**

## Allowances

- **w233's report:** "none". `4e206ec4` changes no `assert`, expected value or case, so the claim holds.
- **w235's report:** "none". `ed25c279` and `ab71c3fc` only add steps and extend one step's argument parsing, so the claim holds.
- **w232's report (i54):** "none". Its loosened test is in its plan's list.

## Cannot verify

None. Every check comes from a run at `dfd35e16`.

## Findings

### 1. Important (fix now): `work show <request>` leaves out every line that has no line outcome

- **Work-item:** i54/w232, commit `a5d6b59b`. It is still w232's open question (`.shop/work/i54/w232.md:14`), and w232 is `awaiting-answer`.
- **File:** `scripts/workqueue_list.py:85-88`. The test `if outcome is not None:` prints a line only when it has an outcome. I re-read it at the head, and it is unchanged.
- **What is wrong:** work-queue r59 asks for the request's "lines with their line outcomes". A request not yet settled is shown with fewer lines, or with none. That is a wrong answer.
- **Fix:**
  - Print every line, with its outcome or `no outcome yet`.
  - Do it under w232 (answer its question with `--change`). Do not draft it again in i60.
- **Test that would show it (not run):** `work show q1`, where line 2 has no outcome, asserting that line 2 is printed.

### 2. Minor (observation): the range holds commits of no i60 work-item, three of them hand edits of workflow files

- **Work-item:** none.
- **Where:** every commit in the brief's `## Commits` is marked `none`, except w233's, w234's and w235's.
- **Commits that carry code:** only i54's `afc4aa72` (w231) and `a5d6b59b` (w232).
- **Commits that change `features/`:** only formulate rounds: `698c1d44`, `bb2caae9`, `fe960a7a`, `19c0bc4d`, `9172f19e` and `64726942`.
- **Hand edits of workflow files:**
  - `556cba3b`: the proposal's `adds` restored.
  - `c0d2f0e2`: i60 set from `done` back to `started`.
  - `9b453fd2`: the delegation of q39, q40 and q41 reworded by hand. This edits the request file directly, against design-decision 0067 ("never by editing what the request is kept in"). It was made before `work delegate` existed. Now that `work delegate` exists, later rewordings go through it.
- **Why it matters:**
  - Other initiatives' faults (Finding 1) hold up i60's review.
  - Hand repairs bypass the checks `work` makes.
- **Fix:** give a branch review only the commits of the initiative's own nodes, or run each initiative on its own branch. Make repairs through `work` commands where one exists.

### 3. Minor (observation): the cause of review 4's data loss is still in `work run`, raised as q34

- **Work-item:** none (i60-requests).
- **File:** `scripts/supervise_change.py:59-72` (`rewrite_lists`). It replaces the lists of the proposal a re-integrate round was started for. It is outside this range's change.
- **The state now:** `.shop/work/i60/requests.md:8-10` holds r65–r68 and r70–r72 again (`556cba3b`).
- **The cause is raised:**
  - q34 ("A redraft of some of a proposal's lines keeps its other ids") is `accepted`.
  - q38, which covers an initiative set `done` early (here by `work withdraw` of w234, while r65–r72 were unbuilt), is `accepted`.
- **Reproduction:** ledger line 16, and review 4's Finding 1.
- **Test that would show it (not run):** an integrate round restarted under supervision r186 for a proposal whose `adds` holds applied ids, giving a change list that names one other id. Assert that the earlier ids stay.

### 4. Minor (observation): formulate rounds' helper scripts stay tracked under i60's runs and fail `tools check`

- **Work-item:** none (i60-requests, formulate rounds 23 and 29).
- **Files:**
  - `.shop/work/i60/runs/requests/23-formulate/splice.py:2,3,8`
  - `.shop/work/i60/runs/requests/29-formulate/splice.py:2,3,8` (new since review 4)
- **Fix:** exclude `.shop/` from ruff and vulture, or have `work run` leave a session's helper scripts out of a stage's kept files.
- **Reproduction:** the brief's `### tools check`, exit 1, with SIM115 six times.

### 5. Minor (observation): two ruff errors older than the range, in files the range touched

- **Errors:**
  - `tests/scenarios/test_supervision.py:14` I001 (that file was touched by `afc4aa72`);
  - `tests/scenarios/work_queue_list_steps.py:134:12` RUF015 (outside `a5d6b59b`'s hunk).
- **Fix:** run `ruff --fix` on the import block, and use `next(...)`.

### 6. Minor (observation): r72 is shown by a session double

- **Work-item:** w235.
- **File:** `tests/scenarios/requests_session_steps.py:19-29`.
- **What the scenario shows:** that the hook tells the session the right thing, and that `work delegate` writes the delegation. The double runs `work delegate` when the hook's text names `work delegate`, "same reply" and the form `The person, <date>: "<the person…`.
- **What it does not show:** that a live session obeys. This is the plan's Decision 6, on supervision r120's precedent.
- **What I read:** this session's own UserPromptSubmit hook printed the intended text at the head's plugin. Real sessions are already reached.
- **Test that would show it (not run):** none in the suite. Only an observed session would show it.

### 7. Minor (observation): `work show <request> --json` gives none of what r59 lists

- **Work-item:** w232 (i54).
- **File:** `scripts/workqueue_list.py:102`. The JSON object is `{request, status, turn}` only.
- **Fix:** add the lines, outcomes, questions, answers and resolution, or write a line that limits the JSON form.
- **Test that would show it (not run):** `work show q1 --json` on the r59 fixture.

### 8. Minor (observation): `request_parts` crashes on a section entry whose number is not an integer

- **Work-item:** w232 (i54).
- **File:** `scripts/workqueue_list.py:85,89,93`. `int(e[0])` is applied to whatever precedes `". "` in an entry, so an entry such as `a. text` raises ValueError and a traceback. Today `work` itself writes only numbered entries.
- **Test that would show it (not run):** `work show q1` with `## Lines` holding `x. y`, asserting a refusal and exit 1.

### 9. Minor (observation): 6 xpassed scenarios that the suite's output does not name

- **Work-item:** unknown, probably w232's r59–r61.
- **What is wrong:** the run uses `-rfEx`, and the expected failures are not strict (`work_items.py:112`, `strict=False`, from review 4).
- **Fix:** make the expected failures strict, or add `-rX` to the whole-suite run.
- **Test that would show it (not run):** the whole-suite command with `-rX`.

### 10. Minor (drop): the w235 reviewer's two findings

- **The hook does not read its stdin** (`scripts/migrate_prompt.py:31-36`). Its output does not depend on the prompt, so behaviour is unaffected.
- **The hook's text is repeated on every prompt** (`:24-28`). The only cost is context.
- **Triage:** drop, as w235's review triaged them.

### Risks checked, no finding

- **The delegate field round-trip.** `work delegate` writes `json.dumps(text)` (`workqueue_request.py:1001`). `supervise_answers.py:44-48` reads `delegation` and decodes it with `json.loads` when it is quoted. So r72's text, with its inner double quotes, is read back word for word, and supervision#r211's live read picks it up.
- **Insert when absent.** The field goes before the closing `\n---` of the frontmatter, the same boundary that `field` and `_with_field` use (`workqueue_request.py:71-78`).
- **Refusals change nothing.** `Refused` is raised inside `edit`, before `workqueue.committed` writes anything (`_change`, `:81-86`).
- **The hook stays at exit 0.**
  - `top_level` returns None outside git (`migrate_write.py:20-23`).
  - `workqueue.requests` globs, so a missing directory gives nothing (`workqueue.py:117-124`).
  - `Refused` is caught (`migrate_prompt.py:18-21`).
- **Code no line asks for:** none.
  - `delegate` serves r65–r68 and r70–r71.
  - `migrate prompting` and the hook entry serve r72.
  - The refusal text and exit codes are mechanism.
  - `request_parts` and `sections` serve work-queue r59.

## Shape

- **CLAUDE.md size limit:** met. `tools size` printed nothing, and `migrate_prompt.py` is 36 lines.
- **Module map:**
  - `scripts/migrate_prompt.py`: a new concern with a new row (`CLAUDE.md:19`). Met.
  - `scripts/workqueue_request.py`: `delegate` (`:211-227`) is under the row that now names `delegate`. Met.
  - `scripts/work`: `cmd_delegate` and the subparser are argument parsing and dispatch only. Met.
  - `scripts/migrate`: `prompting` dispatches to `migrate_prompt.run`. Met.
  - `hooks/hooks.json`: the row names only "the plugin's SessionStart hook", but the file now also holds the UserPromptSubmit entry (and already held PreCompact). The rule is partly met. Fix: widen the row to name each hook.
  - `tests/scenarios/`: `requests_session_steps.py` and `supervision_merge_steps.py` are one `<capability>_*_steps.py` module a concern. Met.
  - `scripts/workqueue_list.py`: `request_parts` is under its row (`work show <target>`). Met.
- **Code and steps no scenario reaches:** none found.
  - `write_q1(None)` is reached by the r211 `after` example.
  - The delegate branch of `the_upstream_runs` is reached by r65–r71.
  - Every new Given and Then in `requests_write_steps.py` is used by r65–r68.
- **Behaviour against Purpose:** nothing in w233 or w235 contradicts the Purpose or a Behaviour line of supervision or requests. The one contradiction of a line is Finding 1 (work-queue r59, w232).

## Coupling

- **pytest-bdd on pytest internals.** `pytest_bdd/compat.py:28` passes a nodeid and a baseid, and the run warns `PytestRemovedIn10Warning`. This breaks under pytest 10. Fix: pin `pytest<10`, or upgrade pytest-bdd.
- **Unregistered marks.** The tags `deprecated`, `r209`, `r210` and `r211` warn `PytestUnknownMarkWarning`, and they would break under `--strict-markers`. Fix: register them in the conftest.
- **Claude Code's hook contract.** The new `UserPromptSubmit` hook relies on three published points: the event name, `${CLAUDE_PLUGIN_ROOT}`, and stdout being added to the prompt's context on exit 0. It also relies on one point that is not published: that the hook runs with its cwd in the session's repository. It reads `Path.cwd()` and ignores the `cwd` field of the stdin JSON. If the harness ran hooks from elsewhere, the hook would fall silent and break nothing. Fix: read `cwd` from the stdin JSON and fall back to `Path.cwd()`.
- **git.** It is driven through its CLI only, on published behaviour. Stable.

## Observations

- **F2:** the brief's `## Commits` marks every commit `none` except those of w233, w234 and w235. Hand edits: `556cba3b`, `c0d2f0e2`, `9b453fd2`.
- **F3:** `.shop/work/i60/requests.md:8` is restored. The cause is `supervise_change.py:59-72`, raised as q34 and q38 (both `accepted`). Not run.
- **F4:** the brief's `### tools check` shows SIM115 six times, in `23-formulate/splice.py` and `29-formulate/splice.py`.
- **F5:** the brief's `### tools check` shows I001 and RUF015.
- **F6:** `requests_session_steps.py:27` shows the double acting on the hook's text. A live session's obedience is not run.
- **F7:** `workqueue_list.py:102` gives the JSON with three keys. Not run.
- **F8:** `workqueue_list.py:85` calls `int(e[0])` on any entry. Not run.
- **F9:** the brief shows "6 xpassed" with no XPASS line. Not run with `-rX`.
- **hooks.json row:** `CLAUDE.md` says "the plugin's SessionStart hook", while `hooks/hooks.json` holds SessionStart, UserPromptSubmit and PreCompact.
