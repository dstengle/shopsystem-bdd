# Branch review 9 of i32: Reviewers' answers and questions as the loop reads them

**Verdict: DONE.**
- No finding is triaged fix now, and none is Critical.
- Every check that i32's work-items name was run and passes.
- Reviews 1 to 8 ended DONE_WITH_CONCERNS because review#r31 could not be checked on a real batch. It can be now. i33's and i34's branch reviews were run by this agent and measured in this range (`51925236`, `6064c949`), and they follow r31 (see Cannot verify).
- Since branch review 8 (`7b81607b`), none of i32's agent, script or test files has changed in a way that touches its scenarios. The new code is i33's w194 (`919e4510`, `6ef3162b`) and i34's w195 (`f682b013`, with its formulate round `e8f5572a`).

## Range and work-items

- **Range:** `d3d3839d..b774a91b` (202 commits).
- **w189** (review#r31): `ee81efd0`, at `agents/bdd-branch-reviewer.md:74,76`.
- **w190** (supervision#r118, r119): `6622133a`, `31c86e3c`.
- **w191** (the fix of branch review 1): `32b5f1fa`.
- **Commits that belong to no i32 work-item:**
  - Carried from reviews 1 to 8: i31's w185 and w193, i33's w192, i33's and i34's rounds, records and queue moves.
  - New since `7b81607b` (30 commits):
    - `919e4510` and `6ef3162b`: i33's w194 (supervision r121, r120 steps, r75, r105). It retires the deprecated @r75 PARTIAL scenario.
    - `f682b013`: i34's w195 (supervision r122), in `scripts/work_items.py`.
    - `eb30678a` and `e8f5572a`: i34's apply and formulate of r122.
    - The rest touch `.shop/` only. They are queue moves for w194 and w195, branch review 8 of i32, branch review 1 of i33 and of i34, and i33's and i34's measurements and moves to done.

## Suite

`Suite: 922 passed, 0 failed at b774a91b in 24.86 s`. The time is pytest's figure, and the wall time was 25.16 s. There were also 1 skipped and 56 subtests passed. The command was `python3 -m pytest -q -p no:cacheprovider --tb=line`.

- **Parallel:** yes, with `-n auto` from `pytest.ini`.
- **In-process:** no. The steps run `scripts/work` as a subprocess. The suite takes under 60 s, so this is no finding.
- **Since review 8:** the 8 failures of i33's w194 now pass, and so do i34's r122 rows.

## Checks

- **w189:** `pytest -n 0 tests/scripts/test_agents.py tests/scripts/test_supervise_answers.py` gives 9 passed and 18 subtests passed. The plan's other check, `measure` on a later batch, is verified (see Cannot verify).
- **w190:** `pytest -n 0 --work-item w190` gives 146 passed, 1 skipped and 56 subtests passed. The plan also asks for the whole suite, which passes (see Suite).
- **w191:** `pytest -n 0 --work-item w191` gives 146 passed, 1 skipped and 56 subtests passed. `test_supervise_answers.py` passes (it is part of w189's 9).
- **`tools check --base d3d3839d`:**
  - **ruff:** 20 errors. None is on a line an i32 work-item wrote, except the carried RUF100.
    - 12 are in committed run records under `.shop/work/i32/runs/` and `.shop/work/i33/runs/` (finding 3).
    - 2 are RUF100 at `tests/scripts/test_supervise_answers.py:9,10` (finding 2).
    - 3 are I001 at `tests/scenarios/test_supervision.py:14` and FURB167 at `tests/scripts/stub_claude.py:189,190` (finding 9).
    - 1 is I001 at `scripts/workqueue.py:248` (finding 10).
    - 2 are new:
      - I001 at `scripts/supervise_analysis.py:4`;
      - RUF100 at `tests/scenarios/supervision_proposal_steps.py:118`.
      - Both lines are unchanged from `7b81607b`. They show now because w194 and w195 touched those files (finding 12).
  - **vulture:** clean.
  - **import-linter:** `missing`, with the message "the project states no import contracts". I checked the module map myself (see Shape).
- **`tools size --limit 300`:** prints nothing.
- **`features deprecated`:** 7 deprecated scenarios. Review 8 had 8, and the @r75 PARTIAL scenario is gone, retired by w194.
  - These stay although their replacements' work-items are green (finding 11, widened):
    - work-queue @r23 (w192 green);
    - supervision @r75 "when every work-item is green or withdrawn …" (w194 green);
    - supervision @r105 (w194 green).
  - Carried, none of them i32's: migration-tools @r15, supervision @r102, work-queue @r1 and @r9.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real:** `work run` has no dry-run mode of any operation, so no agreement test applies.

## Removed and weakened tests

None in i32's work-items.

- **Searched:**
  - the removed lines of `git diff d3d3839d HEAD -- tests features`, as in reviews 1 to 8;
  - since review 8, the removed lines of `git diff 7b81607b HEAD -- tests features`, and the added lines for `skip`, `xfail` and `parametrize`.
- **Since review 8, none of them i32's:**
  - **The @r75 PARTIAL scenario and its step `reviewer_partial` were removed** (w194, `919e4510`).
    - It proved that a PARTIAL review with no question is not measured.
    - It is listed under w194's `## Retires`, which the person's delegated answer of 2026-10-25 put there.
    - It was removed with its binding. This holds.
  - **`started_with_items` is now parametrized.** Its old text still matches, and it writes the same files.
  - **`counted_as` was moved verbatim into `check_counted`.**
  - **`session_answers` now skips `asked_by_the_log` when a log already exists.**
    - This is a Given, and no assertion changed.
    - It is used by @r78 and @r120 only. i32's @r118 and @r119 use a different Given (`…, an answer that asks for a change, …`), and they still pass.

## Allowances

- **i32:** none is claimed. The reports of w189, w190 and w191 give none, and the commits agree.

## Cannot verify

None.

- **review#r31 on a real batch: now verified.**
  - w189's plan names `measure` of a later initiative as the check.
  - i33 and i34 were each measured in this range (`51925236`, `6064c949`).
  - Their kept branch reviews (`.shop/work/i33/runs/branch-review/1/result.json` and `.shop/work/i34/runs/branch-review/1/result.json`) each give `DONE` with `questions: []`. Their findings triage nothing as fix now, so this is what r31 asks.
  - i32's own reviews 2 to 8 also gave `questions: []` while marking their unverified checks `DONE_WITH_CONCERNS`. So no unverified check and no non-fix-now Critical reached `questions`, which is the defect D1 that w189 removed.
- **Whether a real `delegation-answerer` session gives `verdict` is not a check any i32 work-item names.** w190's checks are its scenarios and the whole suite, and both pass. Reviews 1 to 8 listed it here, but it is a dependence on the agent, so it is now under Coupling.

## Findings

### 1. Minor, no work-item (`3e1cb8bb`), observation (carried): i31's status was edited by hand
- **Reproduction:** `git show 3e1cb8bb`.

### 2. Minor, w191, observation (carried): RUF100 in the new test
- **Where:** `tests/scripts/test_supervise_answers.py:9,10`.
- **Fix:** drop `E402` from the `noqa`.

### 3. Minor, no work-item, observation (carried): `tools check` lints committed run records
- **Where:** 12 ruff errors under `.shop/work/*/runs/`.
- **Fix:** exclude `.shop/` from `tools check`.

### 4. Minor, w191, observation (carried): an answered but unmoved reviewer's item waits with no question shown
- **Where:** `scripts/supervise_answers.py:85-88`, unchanged.
- **Reproduction:** review 2's probe.

### 5. Minor, w190, observation (carried): with several reviewer questions on one item, the last verdict wins
- **Where:** `scripts/supervise_answers.py:124`, unchanged.

### 6. Important, no i32 work-item, observation (carried): other initiatives' work lands in i32's range
- **What:** since review 8, i33's w194 and i34's w195 code is in the range, as are i33's and i34's moves to done.
- **Why it matters:** each of those commits started i32's branch review again, which is how this is review 9.
- **Fix:** a line on how one initiative's branch review treats another's commits, through integrating-a-proposal.
- **Reproduction:** `git log --oneline 7b81607b..HEAD -- scripts tests features` lists `919e4510`, `6ef3162b`, `e8f5572a` and `f682b013`.

### 9. Minor, w185 (i31), observation (carried): ruff hits in files w185 touched
- **Where:** `tests/scenarios/test_supervision.py:14` and `tests/scripts/stub_claude.py:189,190`.

### 10. Minor, w192 (i33), observation (carried): a ruff hit that was already there, in a file w192 touched
- **Where:** `scripts/workqueue.py:248`.

### 11. Minor, w192 and w194 (i33), observation (carried, widened): deprecated scenarios stay while their replacements' work-items are green
- **Where:**
  - `features/work-queue.feature` @r23 (w192 green);
  - `features/supervision.feature` @r75 "when every work-item is green or withdrawn …" and @r105 (w194 green).
- **Why it matters:** they still pass, so nothing is broken. They stay as dead weight until some work-item retires them. i33's own branch review (F1) says the same.
- **Fix:** i33 retires them with `features retire`, in a work-item that lists them under `## Retires`.
- **Reproduction:** `features deprecated`, then `grep status .shop/work/i33/w192.md .shop/work/i33/w194.md` gives `green` twice.

### 12. Minor, w194 (i33) and w195 (i34), observation (new): ruff hits that were already there, in files they touched
- **Where:**
  - `scripts/supervise_analysis.py:4`: I001 on the import block whose comment explains the order;
  - `tests/scenarios/supervision_proposal_steps.py:118`: RUF100 on `# noqa: E731`.
- **Origin:** both lines are the same at `7b81607b` (`git show 7b81607b:<path>`).
- **Fix:** for the I001, a `noqa: I001` that gives the reason. For the RUF100, drop the `noqa`.
- **Reproduction:** `tools check --base d3d3839d`.

### 13. Minor, no i32 work-item (supervision#r121, i33), observation (new): a review that "fails" now closes the initiative
- **What:**
  - review#r6 says a check the branch reviewer cannot verify fails the review, and the agent text says DONE_WITH_CONCERNS "goes to the person".
  - Under i32's review#r31, such a review's `questions` is empty.
  - Under i33's supervision#r121 (`scripts/supervise_analysis.py:19-26`), a kept review with no question lists nothing to fix now, whatever its status. So `work run` measures the initiative and sets it done, and nothing routes the concern to the person.
  - w189's plan, decision 2, relied on `lists_nothing` requiring `DONE`, and that no longer holds.
- **Why it matters:** an unverified check or a Critical finding that is not fix now reaches the person only through `findings.md` and the measurement. This follows the lines as written, so it is no wrong answer.
- **Fix:** if the person wants the status to stop the close, a line through integrating-a-proposal, for example in r121 or r75.
- **Reproduction:**
  - The r121 Outline (`features/supervision.feature:1046-1060`) passes in the suite, and its PARTIAL, BLOCKED and NEEDS_CONTEXT rows are each measured.
  - `lists_nothing` (`scripts/supervise_analysis.py:26`) returns `not data.get("questions")` whatever the status, so `{"status": "DONE_WITH_CONCERNS", "questions": []}` is measured too.

### Checked, no finding
- **i32's files since review 8:**
  - `agents/bdd-branch-reviewer.md`, `scripts/supervise_answers.py`, `scripts/workqueue_answer.py` and `tests/scripts/test_supervise_answers.py` are unchanged.
  - `tests/scenarios/supervision_delegation_steps.py` gained w194's r120 Then and the conditional in `session_answers`. Neither is reached by @r118 or @r119 (see Removed and weakened tests).
- **Risk: w195's `proposals()` (`scripts/work_items.py:71-85`) marks i32's scenarios xfail in a whole-suite run.**
  - i32's proposals (`.shop/work/i32/review.md` and `supervision.md`) are `formulated`, so they are excluded.
  - The whole suite has 0 xfailed at HEAD, and the i32 work-item runs pass.
- **Risk: w194's `any(s == "green" …)` guard (`scripts/supervise.py:222`) stops i32 being measured.** i32 has three green work-items, so the guard holds.
- **Code that no line asks for in i32:** none, as in review 8.

## Shape

- **Size, 300 lines:** met. `tools size` prints nothing.
- **Module map, i32's rows:** met and unchanged:
  - `supervise_answers.py`;
  - `workqueue_answer.py:31`;
  - `tests/scenarios/supervision_delegation_steps.py`;
  - `tests/scripts/test_supervise_answers.py`.
- **Unreached code or steps:** none. vulture is clean, and every binding names a scenario.
- **Observation (carried):** `asked_by_reviewer` is read three times for one question (`supervise_answers.py:82,106,121`). The refactor is complete when `grep -c asked_by_reviewer scripts/supervise_answers.py` gives 1.

## Coupling

- **Claude CLI / delegation-answerer:**
  - r118 and r119 rely on a `verdict` result field that only the brief names (`scripts/supervise_answers.py:17-18`). `agents/delegation-answerer.md` does not name it.
  - No real reviewer's question has yet been answered under a delegation in this range. The delegation-answerer sessions in i33's and i34's logs answered proposals' questions.
  - If a real session leaves `verdict` out, the question is left for the person (`supervise_answers.py:122`), which is safe.
  - Naming `verdict` in `agents/delegation-answerer.md` would make this stable.
- **`tests/scripts/stub_claude.py`:** mirrors the CLI's result JSON, so a change in the CLI's fields would show only on a real run.
- **pytest-bdd, ruff, vulture:** used through their public CLI or API only.

## Observations

- i31's status was hand-edited: `git show 3e1cb8bb` (finding 1).
- RUF100 at `test_supervise_answers.py:9,10`: `tools check --base d3d3839d` (finding 2).
- 12 ruff errors under `.shop/work/*/runs/`: `tools check` (finding 3).
- An answered but unmoved reviewer's item waits silently: review 2's probe gives rc 3 and `w1 awaiting-answer` (finding 4).
- The last verdict wins: `supervise_answers.py:124` (finding 5).
- Other initiatives' code is in i32's range: `git log --oneline 7b81607b..HEAD -- scripts tests features` (finding 6).
- I001 at `test_supervision.py:14` and FURB167 at `stub_claude.py:189,190`: `tools check` (finding 9).
- I001 at `scripts/workqueue.py:248`: `tools check` (finding 10).
- Deprecated @r23, @r75 and @r105 remain with w192 and w194 green: `features deprecated` (finding 11).
- I001 at `supervise_analysis.py:4` and RUF100 at `supervision_proposal_steps.py:118`: `tools check` (finding 12).
- A DONE_WITH_CONCERNS review with no question closes the initiative: the r121 Outline at `features/supervision.feature:1046` and `supervise_analysis.py:26` (finding 13).
- `agents/delegation-answerer.md` does not name `verdict`: `grep -n verdict agents/delegation-answerer.md` gives nothing (Coupling).
