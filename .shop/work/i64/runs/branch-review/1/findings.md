# Branch review of i64

**Verdict: DONE.** No finding is Critical and none is triaged fix now. Every check has a result from a run in the brief, all at `b95f4ce3`. There are five Minor observations; one of them is about how much of the range is other initiatives' work.

## Range and work-items

- Range: `86582d02..b95f4ce3` on `main`, 133 commits.
- i64 has one work-item, **w242** (supervision#r221@0.29, `green`). Its commits are `6b8591215`..`b95f4ce3`, the ones marked `w242` in the brief. Its one code commit is `4fa77b43` "supervision r221: a sent-back glossary-proposal gets a new integrate round". The implementers' reports name `79b36ae5` and `5960964a`; those are the same change before `work run` rebased it, as the stage review checked.
- i64's own non-work-item commits are its integrate, gate, apply and formulate rounds and its notes: `5f0ec7e3`..`c571078f`, `a4b69ec8` (spec r221) and `2fb83d16` (r221 scenario formulated).
- Every other commit in the range belongs to other initiatives that work on `main` at the same time: i55 (w239, w240, w241, w243, w244, requests-deda9fa6) and i62 (w245). Finding 5 covers them.

## Suite

`Suite: 1090 passed, 0 failed at b95f4ce in 37.69 s`. The run also gives 1 skipped, 25 xfailed, 12 xpassed and 56 subtests passed.
- **Parallel:** yes (`-n auto`).
- **In-process:** no. The step definitions run the entry points as subprocesses, for example `[sys.executable, scripts/work …]` (migration_session_steps.py:88) and `scripts/model` (design_model_check_reading.py:130).
- The suite runs under 60 s, so neither of these is a finding.
- **Dry-run versus real mode:** the system has no operation with both modes. The only `--dry-run` is a `git push --dry-run` probe (supervise_review.py:55, supervise_faults.py:71), so no randomized agreement test is owed.

## Checks

All of these ran at `b95f4ce3`.

- **w242's scenarios** (`pytest -q -n auto -p work_items --work-item w242`): exit 0, 184 passed, 1 skipped, 56 subtests passed, in 6.63 s. The r221 scenario passes. It is not in the suite run's XFAIL list.
- **tools check:** exit 1.
  - **ruff:** 15 errors. None is on a line w242 changed.
    - `.shop/work/i55/runs/requests-deda9fa6/1-formulate/splice.py` (5): a scratch script that an i55 formulate round committed.
    - `scripts/supervise_merge.py:127` PLC0206 and `tests/scripts/test_supervise_merge_rerun.py:11,12,13,52`: from w245 (i62), in this range.
    - `tests/scenarios/supervision_proposal_steps.py:102,146` RUF100, `supervision_reintegrate_steps.py:13` F401, `:174` FURB167: in files w242 touched, but on lines that were already there (w242's hunks are :125-133/:142-143 and :30-32/:69-72).
    - `tests/scenarios/test_supervision.py:14` I001: the import block that i62's `supervision_rerun_steps` import joined.
  - **vulture:** `tests/scenarios/work_queue_status_steps.py:100` unused `notes`. The line is outside this range's hunk of that file (:19-47), so it was already there.
  - **import-linter:** the project states no import contracts.
- **tools size:** exit 0, no output. No tracked Python file is over the limit, the files w242 touched included.
- **features deprecated:** exit 0. It lists 23 deprecated scenarios. One names a replacement that does not exist: "under a delegation, each question … that <reply>" is deprecated `for: r209 and r210`, and `no scenario has that title`. This range did not touch that scenario (finding 4).
- **features bindings:** exit 0, "every binding names a scenario".

## Removed and weakened tests

I searched the change for deleted test or step functions, dropped parametrize cases, removed, loosened or changed asserts and expected values, added skip/xfail, rewritten assertions and removed scenarios.

- **w242:** none.
  - `integrate_after_apply` (supervision_reintegrate_steps.py:69-73) now takes `name` and passes it to `position(repo, node, …)` and `rounds(repo, kind, name)`. Both helpers default to `p1` (supervision_rounds_steps.py:150, :231), so the `p1` case asserts exactly what it did before.
  - `apply_applies_nothing` takes `name`, and its plan entry is unchanged.
  - The answers regex of `glossary_proposal_answered` was widened from `[^,]+?` to `.+?`. It matches more step lines and asserts nothing less.
  - The plan's §4 lists none, which agrees with this.
- **Other initiatives, in this range:**
  - `tests/scripts/test_workqueue_done.py:19`: the case `("merged", True)` now expects `False` (commit 8b68f27, w240, i55). It proved that a `merged` proposal let an initiative be done. w240's plan §4 lists it, so it holds.
  - Two deprecated work-queue r23 scenarios were removed (w240, Retires). The deprecated supervision r9 and r105 scenarios were removed (w241, Retires); in the net diff they appear as being replaced by r212 and r213.
  - The requests r39, r41 and r43 scenarios were retitled and re-tagged in place as r56, r57 and r58, without being deprecated first (formulate commit 627b4a7, i55). See finding 4.

## Allowances

All three w242 implement reports give `## Tests changed under an allowance` as none. The 4-implement report says "none (not checked in detail …)". No row is claimed, so none is to verify, and the step changes above alter no `assert`, no expected value and no case.

## Cannot verify

None. Every check this review gives has a result from a run in the brief.

## Findings

### 1. Minor, w242, observation: a glossary-proposal is sent back to integration with its apply round's questions still open
`scripts/supervise_rounds.py:59`
- **What is wrong:** the new r221 check routes a glossary-proposal at `awaiting-answer` to `integrate` whenever `sent_back`. It does not first ask whether its questions all have an answer. The capability-proposal path does ask, at :55-56, before `route` reaches its r150 check at :70.
- **Why it matters:** an apply round that gives both questions and `unheld_answers` would start an integrate round before the person answers those questions. The plan's §5 leaves this case unchosen, and no Behaviour line names it, so this is hardening.
- **Fix:** guard the check with `len(self.held(name, "Answers")) >= len(self.held(name, "Questions"))` when the status is `awaiting-answer`, as :55-56 does.
- **Test that would show it (not run):** a scenario where g1's apply round gives one question and `unheld_answers`, and that asserts no integrate round for g1 is started.

### 2. Minor, w242, observation: an integrate brief for an initiative that fulfils no request is built without request lines
`scripts/supervise_brief.py:135-136`
- **What is wrong:** this file is outside w242's file set (the 3-implement report names it). The docstring at :130-132 still says the brief gives "the request the initiative fulfils".
- **Why it matters:** an integrate round started for a proposal of an initiative with no `fulfils` used to be refused ("there is no request under .shop/work/requests"). Now it gets a brief without the `Request:` and accepted-lines lines. The r221 scenario needs this, because its i1 fulfils nothing, so it serves a line and is not code no line asks for.
- **Operator precedence (risk named, verified by reading):** the conditional expression covers the whole list, `(… + […]) if ident else []`, and `accepted_lines` is not evaluated when `ident` is empty. It is correct.
- **Fix:** one sentence in the docstring for the case with no request.

### 3. Minor, w242, observation: ruff findings already in files w242 touched
`tests/scenarios/supervision_proposal_steps.py:102,146` (RUF100), `tests/scenarios/supervision_reintegrate_steps.py:13` (F401), `:174` (FURB167). These come from the `tools check` run above, on lines w242 did not change. **Fix:** `ruff --fix` in the work that next touches these files.

### 4. Minor, no i64 work-item, observation: feature-file records
- **Requests r39, r41, r43 (formulate commit 627b4a7, i55):** these scenarios were removed without being deprecated. Each was retitled in place as r56, r57 or r58, so no scenario is left for r39, r41 or r43. The replacements are xfail, accepted by requests-deda9fa6 and w212.
- **The r209/r210 deprecation:** "under a delegation, each question … that <reply> (deprecated)" names `r209 and r210` as its replacement, and `features deprecated` says no scenario has that title. This was already the case before this range.
- **Fix:** the replacement line should give the replacement scenario's title. For the requests scenarios, the formulate round should deprecate rather than rewrite in place. Both belong to i55's and i62's reviews.

### 5. Minor, no work-item, observation: the range holds commits of other initiatives
- **What is wrong:** `Base..HEAD` on `main` takes in i55's and i62's commits, and the brief marks them `none`. That includes code commits of their work-items:
  - fce410f, 8b68f27, aff8ddf, 153518e (i55: w239, w240, w241)
  - b274fa5, 83e3b8e, 5887978 (i62: w245)
  - the requests, supervision and work-queue formulate and spec commits
- **Why it matters:**
  - None of these commits is i64's, and none is reviewed here beyond what is noted above.
  - i55's code was reviewed in "branch review 1/2 of i55" (583f706, 212ee99).
  - w245's commits are on `main` while w245 is `awaiting-answer` (4208f8d, 7b95194), and they bring the ruff findings above in `supervise_merge.py` and `test_supervise_merge_rerun.py`.
- **Fix:** the branch-review brief should attribute commits to their work-items across initiatives, or leave other initiatives' commits out of the range. i62's own branch review should cover w245.

## Shape

- **Size limit:** met. `tools size` printed nothing.
- **Module map rows w242 touched:**
  - `scripts/supervise*.py` (rounds, brief): met. The r221 routing sits in `supervise_rounds.py` beside r149/r150, and the brief change sits in `supervise_brief.py`. The plan suggested `supervise_glossary.py` as the home of the glossary routing; w242 left it unchanged, and the check sits in the caller, as the plan allowed.
  - `tests/scenarios/` (one `<capability>_*_steps.py` module a concern): met. The steps were widened in their existing modules, `supervision_proposal_steps.py` and `supervision_reintegrate_steps.py`.
- **Unreachable code and steps:** none found from w242. Widening the steps to `[pg]1` keeps the `p1` scenarios bound, and the w242 scenario run passes.

## Coupling

The project depends on pytest, pytest-bdd and pytest-xdist; w242 adds no new reliance on them.
- The suite warns that `pytest_bdd/compat.py:28` passes `nodeid` to `_register_fixture` (`PytestRemovedIn10Warning`). That is pytest-bdd's coupling to pytest internals, and it would break under pytest 10.
- **What would make it stable:** pin pytest below 10, or move to a pytest-bdd release that passes `node`.
- This is not new in this range.

## Observations

- `supervise_rounds.py:59` sends a glossary-proposal with an open apply question to integration. Reproduction: by reading :55-56 against :59. The test that would show it is not run (finding 1).
- `supervise_brief.py:130-132`: the docstring does not cover the brief with no request. Reproduction: by reading :135-136, which the r221 scenario drives and which passes in the w242 run (finding 2).
- Ruff findings already in files w242 touched. Reproduction: `tools check --base 86582d02` at b95f4ce3, exit 1, the lines listed in finding 3.
- Scenarios removed without deprecation and a dangling deprecation. Reproduction: the brief's change (features/requests.feature @r39→@r56, @r41→@r57, @r43→@r58) and `features deprecated` ("no scenario has that title") (finding 4).
- Other initiatives' commits in the range, w245's merged while it is `awaiting-answer`. Reproduction: the brief's Commits list (finding 5).
