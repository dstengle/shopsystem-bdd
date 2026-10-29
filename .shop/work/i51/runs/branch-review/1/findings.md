# Branch review of i51 (supervision r209, r210; r162, r163 retired)

**Verdict: DONE_WITH_CONCERNS.** Nothing is triaged fix now. w230's code does what r209 and r210 ask. The suite passes at the head, and every removed test is listed in the plan. One finding is Critical under the review's rules: w230 removed the @r162 scenario from `features/supervision.feature`, but w230 has no `## Retires` section. The removal is accepted only by a delegated answer in `## Answers`. The scenario asserted a retired requirement and can no longer pass, so this is triaged observation, not fix now. Because it is Critical, the review goes to the person. `tools check` exits 1, but none of its errors is on a line this branch changed.

## Range and work-items

- Range: `3c43389a5a12ce6f84d8556d2d86945c5fd901aa..eadc07902810f1f79cb7ad2cba621fbf1635c787` on `main`.
- Work-items of i51: **w230** (`under: supervision`, accepts supervision#r209 and #r210), now `green`. Its commits are 67f24af1 to eadc0790; the implementation commit is `998966626` (`051b2b9d` before the merge).
- The initiative branch is `main`, which other initiatives share. The range therefore also holds the work of i45, i47 to i50 and i52 to i59. Every commit outside w230 is marked `none` (see Finding 3).

## Suite

- `Suite: 1066 passed, 0 failed at eadc0790 in 33.22 s` (plus 1 skipped, 11 xfailed, 3 xpassed and 56 subtests passed). The run was `python3 -m pytest -q -n auto -rfEx -p work_items --work-item w230 --whole-suite`, exit 0.
- The 11 xfails are all w212's `test_requests.py` scenarios ("accepted by w212, neither green nor withdrawn"), which r43 counts as expected.
- **Parallel:** yes (`-n auto`, pytest-xdist).
- **In-process:** no. `tests/scenarios/test_supervision.py:79` runs `scripts/work` through `subprocess.run`, and the step in `test_work_queue.py:179` also starts a process. Only some steps (`test_work_queue.py:193-204`) drive the library in-process.
- The suite takes under 60 s, so the lack of in-process steps is not a finding.
- **Dry-run and real mode:** the system has no dry-run mode of one of its own operations. The only `--dry-run` is `git push --dry-run`, used as a probe (`supervise_faults.py:71`, `supervise_review.py:55`). No agreement test applies.

## Checks

All of these ran at `eadc0790`.

- **w230's scenarios:** `python3 -m pytest -q -n auto -p work_items --work-item w230` gave 184 passed, 1 skipped, 56 subtests passed in 7.05 s, exit 0.
- **`tools check --base 3c43389a`:** exit 1.
  - **ruff:** 16 errors.
    - 11 are in scratch scripts that other initiatives committed under `.shop/`: `.shop/work/i50/runs/supervision/{2-apply,3-formulate}/splice.py` (SIM115) and `.shop/work/i59/runs/i59/1-integrate/cmp.py` (I001, SIM115, C402, FURB167).
    - `tests/scenarios/supervision_integrate_steps.py:87` RUF059.
    - `tests/scenarios/supervision_proposal_steps.py:102,137` RUF100.
    - `tests/scripts/test_supervise_answers.py:9,10` RUF100.
    - The branch touched all three test files, but none of these lines is in the change's hunks. The hunks are at `supervision_integrate_steps.py:19-27`, `supervision_proposal_steps.py:6-9,184-195` and `test_supervise_answers.py:54-71`, so the errors predate the branch.
  - **vulture:** `tests/scripts/test_supervise_answers.py:36,51` unused `args`. These were there before the branch; w230 only deleted the file's last test.
  - **import-linter:** "the project states no import contracts". The output does not say `missing`, so there was nothing to read for myself.
- **`tools size`:** prints nothing, exit 0. No file is over 300 lines, and none the branch touched.
- **`features deprecated`:** exit 0. It lists 15 deprecated scenarios. All but one are "deprecated for removal". The exception is the r163 outline in `features/supervision.feature`: "for: r209 and r210 | no scenario has that title" (see Finding 2).
- **`features bindings`:** "every binding names a scenario", exit 0.

## Removed and weakened tests

What I searched the change for: deleted `def test_`; removed `Scenario`, `Scenario Outline` and `Examples` rows; removed or loosened `assert` lines; added `skip` or `xfail`; step patterns whose assertion changed; and renamed tests.

1. **Deleted: `tests/scripts/test_supervise_answers.py::test_a_question_names_a_term_of_the_glossary_or_a_glossary_proposal_as_a_whole_word_in_any_case`** (w230).
   - It proved that `supervise_glossary.names_one` matches a glossary term or a glossary-proposal name as a whole word, in any case, and does not match partial words. That is r162's rule.
   - It is listed in plan §4 "Tests the decisions break": yes.
2. **Removed: the @r162 Scenario Outline** "under a delegation, a question of the initiative that names <named> is left for the person and given to no session", both examples (w230). It was at `features/supervision.feature:1334` at the time of the merge.
   - It proved that a work-item's question naming the term "ledger" or the glossary-proposal g1 went to no session and stayed unanswered.
   - It is listed in plan §4: yes (decision D2).
   - Within the range it was first deprecated by the formulate commit `af49d7ff` and then removed by `998966626`. This removal is Finding 1.
3. **Widened, not weakened** (w230, `tests/scenarios/supervision_delegation_steps.py`):
   - `glossary_proposal_awaiting` (l.29-34) takes an optional `## Questions` and writes the same file without one.
   - `two_unanswered` (l.70-75) takes `w\d+` instead of only w1.
   - `question_unanswered` (l.131-134) takes `w1|g1` and makes the same assertion. The w1 form is still used at `features/supervision.feature:1402`.
4. **Not removed:** the @r93 scenario is only deprecated, for removal (`6ce69452`, i49). The @r163 outline is only deprecated, for r209 and r210 (`af49d7ff`). Their steps and Examples rows are unchanged.

## Allowances

Both implementer reports (3-implement and 4-implement) give `## Tests changed under an allowance: none`. There are no rows to verify.

## Cannot verify

Every run the review needs is in the brief, so none is missing. Two claims rest on runs the brief does not give, and I took them only as claims:

- 3-implement's red runs ("4 failed (undefined steps) … r210 2 failed on the Then"). The change landed as one commit, so nothing in the range shows them. The code path is consistent with the claim: before the change, `names_one` at `supervise_answers.py:75` kept w2's questions from every session.
- w230's first whole-suite failure, `test_work_run_that_cannot_do_what_it_was_asked…[not a git repository]`. The coordinator's answer says it was a fixture race. The brief's run at `eadc0790` shows it passing, but a single pass does not show that a race is gone (see Observation 4).

## Findings

### 1. Critical, w230, observation: `features/supervision.feature:1334` (at merge): a scenario was removed with no `## Retires` entry

- **What is wrong.** Commit `998966626` removes the @r162 @deprecated outline. `.shop/work/i51/w230.md` has no `## Retires` section. The retirement exists only as the 2026-10-29 answer in `## Answers`, given by the coordinator under the person's delegation ("Retires: the @r162 deprecated outline … its removal stands").
- **Why it matters.** A change under `features/` is allowed only when it removes a deprecated scenario that the work-item lists under Retires. That rule keeps retiring a scenario with r73 and r123, not with the implementer.
- **Why it is not fix now.** No answer is wrong and no data was lost. The outline asserted r162, which is in the capability's `retired:` list. It could not pass under r210, and r4's whole-suite gate would otherwise have stopped w230. The binding is `scenarios("supervision.feature")`, which binds the whole file, so no binding was left dangling (`features bindings` is clean).
- **Fix.** The person rules on it. Either write the ruling under a `## Retires` section of w230, which accepts the removal as made, or restore the outline and retire it through r123. Review 5 already raised this as Critical, and review 6 accepted the delegated answer.

### 2. Important, none (i51's formulate commit `af49d7ff`), observation: `features/supervision.feature:1317`: `Deprecated for: r209 and r210` names no scenario

- **What is wrong.** r73 drafts `## Retires` from a `Deprecated for:` line that names a scenario. r123 retires a deprecated scenario once its replacement's work-item is green. Both need that line to name a replacement scenario, but this line gives requirement ids. `features deprecated` says so: "for: r209 and r210 | no scenario has that title".
- **Why it matters.**
  - This is why w230 was drafted with no `## Retires` for the r162 outline (the root of Finding 1).
  - The r163 outline's replacement, w230, is now `green`. r123 should draft a work-item to retire it, but it cannot find the replacement through this line, so the r163 outline may stay deprecated indefinitely.
- **Fix.** Write the line with the titles of the r209 and r210 scenarios, or raise a request for r73 and r123 to read a `Deprecated for:` line that names requirement ids.
- **Test that would show it (not run):** a scenario where a deprecated scenario's `Deprecated for:` line names the requirement ids of a work-item that turns green, and `work run` drafts the retiring work-item.

### 3. Minor, none, observation: commits that belong to no work-item

- **What is wrong.** Every commit in the range except w230's 13 is marked `none`.
- **What they are.** Almost all are workflow bookkeeping (`work note`, `outcome`, `turn`, `answer`, status moves, intake, integrate, gate, apply and formulate merges), and they span other initiatives because the initiative branch is `main`. The ones that change code, features or spec outside i51 are:
  - `a807b5b7` (r173 code in `supervise_glossary.py` and `supervise_rounds.py`). It sits between `w228 ready -> claimed` and `w228 claimed -> done` (i50), and i50's branch review 1 (`a746612b`) followed it.
  - `e4e58445` (r173 scenario) and `6ce69452` (r180 scenario, r93 deprecated): formulate commits of i50 and i49.
  - `a3da368c` and `d27c27d3` (spec-consistency, i45).
- **i51's own commits outside w230:** `2c74c3a6` (spec r209, r210 replacing r162, r163), `af49d7ff` (formulate) and `73758cad` "i51 hand repair: supervision back to approved … empty glossary-proposal withdrawn". The hand repair is a change by hand to the workflow's state, outside any round.
- **Why it matters.** `Base..HEAD` on a shared `main` is not i51's branch. A review of this range sees other initiatives' code that this review cannot attribute.
- **Fix.** Give an initiative its own branch, or have the branch review's commit list attribute each commit to its initiative and work-item.

### 4. Minor, w230, observation: `CLAUDE.md:37`: stale module-map row for `scripts/supervise_glossary.py`

- **What is wrong.** The row still says the module gives "the questions under a delegation that name a term or a glossary-proposal, left for the person (supervision r162)". w230 deleted `names_one`, `terms_of` and `proposals_of` (`supervise_glossary.py`, diff at l.82-99). The row also does not name r173's `approval_question` (`supervise_glossary.py:45-54`, i50).
- **Fix.** Reword the row: the terms of glossary-proposals not approved, withheld from an apply round (spec-integration r55), and the approval question of a glossary gate with no question (supervision r173).
- **Reproduction.** Read `CLAUDE.md:37`. `grep -rn names_one scripts tests` finds nothing (review 6).

### 5. Minor, w230, drop: `scripts/supervise_answers.py:1`: stale docstring id

The docstring still opens with "(capability supervision r77, r78)". r77 is retired; this predates the branch. Polish only.

## Behaviour against the capability

- **r209:** `Answers.asking` (`scripts/supervise_answers.py:51-58`) lists only `work-item` and `capability-proposal` files that are awaiting-answer. A glossary-proposal's question therefore reaches no session, whatever its words.
- **r210:** `Answers.answers` (l.70-80) gives every open question to `self.ask`, with no test of its words.
- **r173 (i50, in range):** `Rounds` (`supervise_rounds.py:999-1002`) writes `approval_question` for a glossary-proposal whose gate gave no question, and r117's question otherwise.
- Nothing contradicts a Behaviour line or the Purpose.
- **Code no line asks for:** none. w230 only removes the mechanism of the retired r162.

## Shape

- **Size limit (CLAUDE.md "Size limit"):** met. `tools size` prints nothing.
- **Module map, rows the branch touched:**
  - `scripts/supervise_answers.py` ("answers under a request's delegation"): met.
  - `scripts/supervise_glossary.py`: not met, the row is stale (Finding 4).
  - `scripts/supervise*.py` (rounds): met for r173's gate question.
  - `tests/scenarios/`, one `<capability>_*_steps.py` module a concern: met. The delegation steps are in `supervision_delegation_steps.py`, the glossary gate steps in `supervision_proposal_steps.py` and the integrate steps in `supervision_integrate_steps.py`.
  - `tests/scripts/` (tests no scenario drives): met.
- **Unreached code:** none left by w230. `terms_in` is still used by `withheld` (review 6). Every step w230 widened is still reached: the w1 form of `question_unanswered` at `features/supervision.feature:1402`, and `glossary_proposal_awaiting` without a question by r210 and r163.

## Coupling

- **pytest-bdd on pytest's private API:** the suite run shows 299+299 `PytestRemovedIn10Warning` from `pytest_bdd/compat.py:28` (`_register_fixture` with nodeid) and `_pytest/fixtures.py:1986` (`FixtureDef` with baseid). This is pytest-bdd relying on more than pytest publishes, and the whole scenario suite rests on it. The suite would break on pytest 10. To make it stable, pin `pytest<10` or move to a pytest-bdd release that passes `node`.
- **Tags as marks:** the tags `@deprecated`, `@r209` and `@r210` become unregistered pytest marks (`PytestUnknownMarkWarning`). That works today, but it would fail under `--strict-markers`. To make it stable, register the marks in the conftest.
- **The `claude` CLI:** the scenarios stand in for it (`SHOPSYSTEM_WORK_CLAUDE`, `STUB_CLAUDE_PLAN`), and the stand-in's results carry the CLI's result fields (`subtype: error_max_turns`, `num_turns`, `supervision_delegation_steps.py:128`). The code depends on those fields as the CLI emits them, so a change in the CLI's result JSON would go unseen by the suite. That predates the branch. A contract test against a recorded real result would make it stable.
- The branch adds no new external dependency.

## Observations

1. Finding 1: the r162 removal is recorded only in w230's `## Answers`. Reproduction: `.shop/work/i51/w230.md` has the headings `## Questions` and `## Answers` and no `## Retires`.
2. Finding 2: the r163 outline's `Deprecated for:` names no scenario. Reproduction: `features deprecated` at eadc0790 prints "… that <reply> (deprecated) | for: r209 and r210 | no scenario has that title".
3. Finding 3: commits with no work-item. Reproduction: the brief's `## Commits` marks every commit except w230's 13 as `none`, including `73758cad` (i51 hand repair).
4. Fixture race: `tests/scenarios/supervision_given.py:72` `shutil.rmtree(repo / ".git")` races git's automatic maintenance (`FileNotFoundError: 'maintenance.lock'`). Reproduction: w230's first whole-suite run in `.shop/work/i51/w230.md:136-164` (1 failed); it passed at eadc0790. The coordinator raised it as its own request. Test that would show it fixed (not run): repeat that scenario under `-n auto` with `gc.auto`/`maintenance.auto` on, or remove `.git` with `ignore_errors` after `git maintenance` has stopped.
5. Finding 4: stale `CLAUDE.md:37` row. Reproduction: read the row; `grep -rn names_one scripts tests` is empty.
6. `tools check` exits 1 on errors that predate the branch, or that sit in scratch scripts committed under `.shop/`. Reproduction: the brief's `tools check` output. Fix: exclude `.shop/` from ruff, and clear RUF100, RUF059 and the vulture `args` in the three test files.
