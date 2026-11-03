# Branch review of i55

**Verdict: DONE_WITH_CONCERNS.** w239 (requests r64) and w240 (work-queue r62) do what their plans say. Their only changes under `features/` remove the deprecated scenarios their Retires sections name. The one changed test (`merged` case) is listed in w240's plan. Every check given passes or has nothing in i55's files. One finding is Important and triaged fix now, and it is about the initiative, not either work-item. The spec commit `deda9fa6` applied i55's lines requests r50–r58, work-queue r47 and supervision r184–r186, and retired requests r13, r34, r39, r41 and r43. Those ids are no longer on any i55 capability-proposal (the requests proposal now adds only r64 and removes only r14). So no formulate round or work-item will ever build them. You can see it in the code: `work list` prints no request turn although r50 asks for one, while `work show` with no target still prints the turn under the retired r13. The scenarios of the five retired ids are still live, under their retired tags.

## Range and work-items

- Range: `c53a7c25e23b..3d02f4a1f41f` on `main` (the initiative branch is `main`, so the range also holds the work of i45, i47–i54, i56–i64).
- i55's work-items, both `green`:
  - **w239** (requests#r64@0.29, under requests). Commits: 386cf9f2 (add), b7a8d60c, 22701db3, 595e0603, 558fcc6a, **cae12e0c** (code), c3e61a3c, 7a38e59f, 33bc15e8, 2a17f3b1, **fce410f4** (fix of 4-review's Critical), 4f7fee4c, b2456bcc.
  - **w240** (work-queue#r62@0.29, under work-queue). Commits: fd189cea (add), 5aaa3919, 1f355881, 7a71427c, 5d18f340, d373345d, 1e3fab75, 3c1de94d, **8b68f278** (code), **aff8ddf1** (retire), 4db47633, 3d02f4a1.
- i55's proposals: requests `formulated` (adds r64, removes r14); work-queue `formulated` (adds r62, removes r23); supervision `awaiting-answer` (adds r212, r213; removes r149, r32, r9, r105; open question "The apply round of supervision gave no change list; which capabilities' lines did it apply?").

## Suite

Suite: 1089 passed, 0 failed at 3d02f4a1 in 33.32 s (1 skipped, 13 xfailed, 3 xpassed, 56 subtests passed). Exit 0. Command: `python3 -m pytest -q -n auto -rfEx -p work_items --work-item w239 --whole-suite`.
- Parallel: yes (`-n auto`, xdist).
- In-process: no. The `run` fixture (tests/scenarios/conftest.py:27-35) runs each script with `subprocess.run([sys.executable, SCRIPTS/script, ...])`. The suite takes 33 s, under 60 s, so this is not a finding.
- Dry-run against real mode: the system has no dry-run mode of an operation. The only `--dry-run` is `git push --dry-run`, the push verification in supervise_review.py:55 and supervise_faults.py:71. So there is no agreement test to look for.

## Checks

All runs below are at 3d02f4a1.

- **w239's scenarios** (`pytest -q -n auto -p work_items --work-item w239`): exit 0, 182 passed, 1 skipped, 56 subtests passed, 6.60 s.
- **w240's scenarios** (`... --work-item w240`): exit 0, 187 passed, 1 skipped, 56 subtests passed, 4.37 s.
- **tools check** (`--base c53a7c25`): exit 1.
  - `== ruff ==`: 28 errors. None is in a file w239 or w240 touched: workqueue_list.py, workqueue_status.py, requests_show_steps.py, workqueue_done.py, work_queue_status_steps.py and test_workqueue_done.py are clean.
    - 19 are in workflow scratch scripts under `.shop/work/i50`, `i59`, `i60` and `i63` runs.
    - 9 are in test files other initiatives touched: supervision_integrate_steps.py:87 RUF059, supervision_proposal_steps.py:102/137 RUF100, test_supervision.py:14 I001, work_queue_list_steps.py:134 RUF015, stub_claude.py:208/209 FURB167, test_supervise_answers.py:9/10 RUF100.
    - w239's 4-review ran the same check at cae12e0c and also counted 28, none in w239's files. So i55's commits added none.
  - `== vulture ==`: `tests/scenarios/work_queue_status_steps.py:100: unused variable 'notes'`. w240 touched this file, but the hit was already there before (w240's 5-review saw the same `ledger_of_twelve(repo, notes)` at line 77 at the base). See finding 4.
  - `== import-linter ==`: "the project states no import contracts". No contract to check.
- **tools size**: exit 0, no output. No tracked Python file is over 300 lines.
- **features deprecated**: exit 0. 18 deprecated scenarios are listed, none of them i55's. w239's r14 scenario and w240's two r23 scenarios are gone from the list. One pointer is broken: supervision r163's "for: r209 and r210 | no scenario has that title". See finding 5.
- **features bindings**: exit 0, "every binding names a scenario".

## Removed and weakened tests

I searched the change for deleted `def test_` functions, deleted step definitions, removed scenarios and examples, changed parametrize cases, removed or loosened `assert`s, and added skip or xfail marks.

i55's work-items:
- **w239, cae12e0c**: scenario "status with no initiative prints, with its date, each observation no initiative's or request's source names (deprecated)" (@r14, requests.feature). It proved that `work status` lists uncited observations with their dates. Removed. It is listed under w239's Retires and in plan §4. The binding is file-wide, so no binding was removed.
- **w239, cae12e0c**: step `runs_status` ("the session runs `work status`", requests_show_steps.py:49), replaced by `runs_list`. This is a step, not a test. Its only user was the retired scenario.
- **w240, aff8ddf1**: the @r23 Outline "a command whose change leaves an initiative with a green work-item … sets the initiative to done (deprecated)" (4 examples) and the @r23 scenario "retry that makes an initiative's last open work-item green again sets the initiative to done (deprecated)". They proved done on withdraw and on retry. Both removed, both listed under w240's Retires. Their behaviour is now pinned by the r62 Outline (work-queue.feature:60), withdraw ×5 and retry ×1.
- **w240, 8b68f278**: `tests/scripts/test_workqueue_done.py::test_an_open_proposal_keeps_the_initiative_from_done`, case `("merged", True)` changed to `("merged", False)`. Before, it proved that a `merged` proposal lets an initiative reach done; now it proves the opposite. This is not a loosening. Listed in w240's plan §4 (D1).

Other initiatives' commits in the range (not i55's; each initiative's own branch review read them; I did not read their plans):
- 99896662 (i51/w230): `tests/scripts/test_supervise_answers.py::test_a_question_names_a_term_of_the_glossary_or_a_glossary_proposal_as_a_whole_word_in_any_case` deleted. It proved `names_one` (r162). r162 is retired for r209/r210 and `names_one` was removed.
- 94f0a743 (i63/w236): `supervision_faults_steps.is_failed` now leaves `.shop/work/i2` out of its clean-status `git status` assertion (r218).
- a5d6b59b / cb269262 (i54/w232): `requests_flow_steps.show_prints` now compares only the first line of `work show`'s output, because show now prints more lines after it (r59).
- Formulate commits af49d7ff (supervision r162 scenario rewritten as r209) and 19c0bc4d / 0e9fa09f (r23 and r14 deprecated). These are formulate rounds, not work-items.

## Allowances

- w239: 3-implement and 5-implement both say "none". The commits change no test outside plan §4. Holds.
- w240: 3-implement and 4-implement both say "none". The only changed test is plan §4's `merged` case. Holds.

## Cannot verify

- Nothing that fails the review. Every check the role asks for has a run in the brief.
- The suite shows **3 xpassed**, but `-rfEx` does not name them (`X` is not in `-r`). I cannot tell which expected-failure scenarios now pass. Observation 3.

## Findings

### 1. Important, fix now (the i55 initiative's capability-proposals; no work-item). The lines i55 applied are dropped from its proposals, so they are never built

- **Where**:
  - spec/capabilities/requests.md:58-67 (r50–r58)
  - spec/capabilities/work-queue.md:28 (r47)
  - spec/capabilities/supervision.md:34, :81, :122 (r185, r186, r184)
  - `.shop/work/i55/requests.md` frontmatter (`adds: [requests#r64@0.29]`, `removes: [requests#r14@0.29]`)
  - scripts/workqueue_list.py:73-74 and :65
  - scripts/work:35-43
  - features/requests.feature:239 (@r34), :411 (@r39), :428 (@r41), :443 (@r43), :459 (@r13)
- **What is wrong**:
  - Commit deda9fa6 ("spec: requests (i55) … adds requests#r50@0.29 … r58, supervision#r184@0.29, r185, r186, work-queue#r47@0.29; removes requests#r13@0.29, r34, r39, r41, r43") applied these lines to the spec.
  - The requests proposal was then redrafted (13-integrate, round 2). It now names only r64 and r14. The work-queue proposal names only r62 and r23, and the supervision proposal only r212, r213 and the four it removes.
  - No feature file has a scenario tagged r50–r58, r47, r184, r185 or r186, and no i55 work-item accepts them.
  - **r50 is contradicted in the code**: "When `work list` is run, `work` shall print each request with its status and whose turn it is". But `listing` prints `request <name> <status>` with no turn (workqueue_list.py:74), and its JSON gives `{"request", "status"}` with no turn (:65).
  - **The retired r13 behaviour is still there**: `work show` with no target prints every request with its status and turn (scripts/work:35-43, and the text form after it). No live line asks for that now.
  - **Scenarios of retired ids are still live**: the @r13, @r34, @r39, @r41 and @r43 scenarios are neither deprecated nor re-tagged to r50, r55, r56, r57 and r58. The @r39, @r41 and @r43 ones run as w212's expected failures under the retired ids (see the XFAIL lines in the suite output).
- **Why it matters**:
  - Lines the person's delegation approved (q21's lines 1–9, among them "line 1 replaces requests r13") end with nothing building them.
  - `work list` gives a wrong answer against r50.
  - The feature files pin retired requirement ids.
  - Once the supervision proposal settles, i55's done condition (r62/r213) will hold, and the initiative will close with these lines unbuilt.
  - This is the fault named in i55's own source (observation 2026-10-27-redraft-overwrites-other-proposal), now hitting i55's own proposals.
- **Fix**: put the lost ids back on i55's proposals, by hand repair or by the integrate path:
  - requests: adds r50–r58, removes r13, r34, r39, r41, r43
  - work-queue: adds r47
  - supervision: adds r184, r185, r186, removes r149
  
  Then let the formulate rounds tag or deprecate the scenarios and draft the work-items. The cross-repository lines r52, r53, r56, r57 and r58 can be accepted by w212's successor and held there, as r39, r41 and r43 are now. Alternatively, retire those lines through integrating-a-proposal.

### 2. Minor, observation (w239). An observation with no `date:` line is listed with the date "None"

- **Where**: scripts/workqueue_list.py:52-54 and :78 (JSON: `"date": null` at :67).
- **What**: `uncited` gives `None` when an observation has no `date:` line, and `listing` prints `observation <id> None`. r64 says "with its date". Every observation in the scenarios has a date, and the code was moved unchanged from workqueue_status.py.
- **Fix**: print the observation without a date, or refuse a record that has none.
- **Reproduction**: from reading the code, not a run. The regex `(?m)^date: (\S+)` falls back to `None` (:52-54).

### 3. Minor, drop (w240). The `with_state` step regex lost its space

- **Where**: tests/scenarios/work_queue_status_steps.py (`with_state`, about line 45 in the new file).
- **What**: `whose work-items? (?P<items>.+)$` became `whose work-items?(?P<items>.+)$`. The step still works; it just also accepts text glued to "work-item". Neither the plan nor the report mentions it.
- **Fix**: restore the space.

### 4. Minor, observation (w240). vulture: unused `notes` in a file w240 touched

- **Where**: tests/scenarios/work_queue_status_steps.py:100.
- **What**: the hit was already there before w240 (it was at line 77 at the base); w240's added Givens moved it. Nobody has cleared it.
- **Fix**: drop the parameter, or use it.

### 5. Minor, observation (no i55 work-item). Deprecated scenarios whose replacement is green are still in the feature files

- **supervision r163** (`features deprecated`: "for: r209 and r210 | no scenario has that title"): r209 and r210 were built by w230 (i51, green, i51 done).
- **supervision r28** (for removal): r218 was built by w236 (i63, green).
- **work-queue r34 and r35** (for removal): r60 and r61 come from i54, which is done.
- These belong to other initiatives' work-items; each should be retired with its binding.

### 6. Minor, observation (no work-item: the range on `main`). The range holds commits that belong to no i55 work-item

- Almost every commit in the range other than w239's and w240's is marked `none`. They are other initiatives' workflow commits (transitions, notes, round merges, spec applies, formulate rounds, hand repairs) and their code commits. The code commits, with the work-item each sits between the transitions of:
  - a807b5b7 (w228)
  - 99896662 (w230)
  - afc4aa72 (w231)
  - a5d6b59b, cb269262 (w232)
  - 4e206ec4 (w233)
  - ed25c279, ab71c3fc (w235)
  - d8f57cc8, 94f0a743 (w236)
  - a9cb7536, fd8364d1 (w237)
- Each of these initiatives had its own branch review. Because `main` is the initiative branch, every initiative's review range takes in every other initiative's commits.
- **Fix**: give the brief each commit's work-item across all initiatives, or start the range at each initiative's own commits.

## Shape (CLAUDE.md)

- **Size limit (300 lines)**: met. `tools size` prints nothing. The touched files: workqueue_list.py 129 lines, workqueue_done.py 78, test_workqueue_done.py 28, work_queue_status_steps.py about 183.
- **Module map, `scripts/workqueue_list.py`** ("`work list` and `work show <target>`: the queue listed, an initiative or a work-item shown, the record of raised requests"): met in concern. The row does not say that the listing now includes uncited observations (w239), or that `show` shows a request (w232). The module docstring (workqueue_list.py:1, "capability work-queue, r34-r39") still cites the retired r34 and r35 and does not name requests r64. `show`'s docstring (:118, "an initiative or a work-item") leaves out requests. Observation; it is complete when the row and docstrings name r64 and the request target.
- **Module map, `scripts/workqueue_status.py`** (`work status`): met. `uncited` left it and the `report` parameter is gone (workqueue_status.py, `status` and `open_text`).
- **Module map, `scripts/workqueue_done.py`** (an initiative done): met. `CLOSED_PROPOSAL = ("formulated", "withdrawn")` (:13); the docstring cites r62 and r47.
- **Module map, `tests/scenarios/`** (one `<capability>_*_steps.py` module a concern): the done condition's proposal Givens went into `work_queue_status_steps.py`, a status-steps module, as the plan says (D3, following the existing proposal Givens there). Observation only.
- **Reachability**:
  - `runs_status` is removed with its only scenario.
  - `work status` is still reached, by work-queue.feature's deprecated status scenarios and by `open_text` (the SessionStart hook).
  - The code `work show` runs with no target (scripts/work:35-43) is reached only by the @r13 scenario, whose line is retired (finding 1).
- **Code no line asks for (i55's commits)**: none.
  - The `observations` JSON key and text lines serve r64.
  - Dropping observations from `work status` follows from r14's retirement.
  - `CLOSED_PROPOSAL` serves r62 and r47.

## Coupling

- **i55's code** (workqueue_list.py, workqueue_status.py, workqueue_done.py) uses only the standard library and the repository's own modules. It has no coupling to another project.
- **pytest-bdd and pytest** (the suite):
  - The suite warns `PytestRemovedIn10Warning: Passing nodeid to _register_fixture is deprecated` from pytest_bdd/compat.py:28. pytest-bdd relies on a private pytest API, so the suite breaks on pytest 10 unless pytest-bdd follows.
  - What would make it stable: pin pytest below 10 together with the pytest-bdd version, or upgrade both together.
- **git**, in code outside i55's commits:
  - supervise_faults.py reads `git status --porcelain` paths with `line[3:].strip('"')`. Porcelain quotes unusual paths with C-style escapes, which this does not undo. It relies on paths needing no escapes; true for `.shop/work` names today.
  - stub_claude.py's `git_retry` matches the stderr text `index.lock`, which is a git message and not a contract. It is test-only, and a mismatch only means no retry.
- **Claude Code hooks** (hooks.json UserPromptSubmit, i60): uses the published `CLAUDE_PLUGIN_ROOT` and stdout-as-context contract. Nothing beyond it.

## Observations

1. Observation with no date lists `None` (finding 2). Reproduction: read workqueue_list.py:52-54 and :78; not run.
2. Scenario tags r200 and above, and `@deprecated`, are not registered marks. tests/scenarios/conftest.py:40 registers `r1`–`r199` only. The suite warns `PytestUnknownMarkWarning: Unknown pytest.mark.r209` (and r210, r211, r214, r215, r216, r218, deprecated), 32 times each, so `--strict-markers` would fail. Reproduction: the warnings summary of the suite run at 3d02f4a1.
3. 3 xpassed in the whole suite at 3d02f4a1 are unnamed (`-rfEx` has no `X`). A test that would show them: the same command with `-rX`. Not run.
4. `work show <request>` and `work list` disagree on whose turn (finding 1). Reproduction: read scripts/work:35-43 against workqueue_list.py:73-74; not run. A test that would show it: an @r50 scenario, "work list prints q1 with open and the upstream's turn". Not run.
