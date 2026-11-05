# Plan 6 of the workflow simplification: implementation report

This is the report of the one implementer agent that executed `plan-6-decision-tiers.md` on 2026-11-05. It used
superpowers:executing-plans, with one commit per task and no subagents.

All 5 tasks are done. The `decision-tiers` capability is built, and all 6 of its requirements are out of `unbuilt:`.
Each decision now carries `tier:` and `enforced_by:`. `model check` reads them and gives `w_untiered`, `v_d6`, `v_d7`
and `v_d8`. `model decisions --check` checks the index, then runs each `check` decision's tests, one pytest run a
decision, and writes nothing. The 73 decisions are sorted: 27 are in force, and 27 of the old process's are superseded
by 0074. The new decisions 0075 and 0076 bring the total to 75. The `check` decisions a capability rests on are now
part of the readiness bar. `model decisions --check` is one of the review's checks, and the batch's subagents read the
`judgement` decisions. The commits are on `workflow-simplification`, from `b7161178` to this report's commit, and are
not pushed. No baseline got worse.

## Final state

| Check | Result |
|---|---|
| Suite (`python3 -m pytest -q`) | **1393 passed**, 1 skipped, **8 xfailed**, **135 subtests** passed (29 s). The start was 1356 passed and 14 xfailed. The 37 new passes are 6 decision-tiers scenarios and 31 script tests: tiers 7, decisions 10, decision checks 6, readiness decisions 7 and the skill 1. The subtests are unchanged. |
| Timing run (`python3 -m pytest -m timing -n 0 -q`) | `2 passed, 1402 deselected` (5.6 s). The second is `test_the_decisions_run_side_by_side` (Deviation 2). |
| Unbuilt ids | `False 9 []`: decision-tiers is absent, 9 ids remain, no problems |
| `model check` | 53 violations, 16 warnings, 19 unresolved references, 0 file problems (at baseline) |
| `model logic` | `11 findings: 6 L5, 5 L6` |
| `model lexicon --check` | `401 terms, 0 problems` |
| `model decisions --check` (live) | index current; four `holds` lines (0006, 0048, 0053, 0076); `4 check decisions: 4 hold, 0 failing`; exit 0; **2.9 s** wall |
| `features generate --check` | exit 0 |
| `features vocab --check` | `every step has one handler` |
| `features bindings --unbound` | `every binding names a scenario` |
| `tools size --limit 300` | silent. `model_work.py` is 280 (266 + 14, limit 285), `scripts/model` 218 (≤ 230), `model_report.py` 192 (≤ 205), `readiness_bar.py` 151 (≤ 160), and in `batch_brief.py` (233) only `CHECKS` changed. The new files: `model_decisions.py` 130, `decision_tiers_handlers.py` 155, `test_model_tiers.py` 105, `test_model_decisions.py` 175, `test_decision_checks.py` 62, `test_readiness_decisions.py` 109. |
| `tools check $(git diff --name-only 95178ceb...HEAD -- '*.py')` | ruff and vulture clean; import-linter states no contracts |
| Smoke run (Task 5, Step 3) | The first `ready b1` exited 1 with `design-decision c (check) fails: tests/test_c.py::test_c: exit 1`. `decisions --check` exited 1 with `failing  spec/decisions/c.md (design-decision/ex.com/prod/ctx/c): …: exit 1` and pytest's tail. `status --porcelain` showed only `?? spec/decisions/index.md`, with no `.pytest_cache` or `__pycache__`. After `test_c` was made to pass, `ready b1` readied it. The plan's shell has no `bc`, so a second item, b2, was timed through Python: the failing `ready` took **0.51 s** and the passing `ready` **0.41 s**. |

## Commits

| Task | Commit | What was done | Verification |
|---|---|---|---|
| 1 | `b7161178` | `model_decisions.py`, minimal: `TIERS`, `split`, `test_file`, and `wrong`, the D2 file problems. `read_decisions` → `read_tier` (`tier/2`, `enforced_test/2`, `enforced_req/2`, a requirement entry `want`ed). `model.lp`: `v_d6`, `v_d7`, `v_d8`, `w_untiered` (D3, D4). The index's `tier` column (D12). The contract's text. `decision_tiers_handlers.py` (`decision`, `field`, `GivenK_A design-decision`, the local `GivenK_C design-decision`, `GivenR supersedes`). `test_decision_tiers.py` binds with `bind_all`. `unbuilt: [r4, r5]`. The `untiered` definition fixed (D3), with one Implementation bullet. The module map's handlers row. | 7 tests failed first, then passed. With the model tests, 63 passed. decision-tiers ran `4 passed, 2 xfailed`, and design-model-check passed as before. Mutations, each reverted: `v_d8` without `status(New, "accepted")` failed `test_v_d8_…`; `w_untiered` without the history clauses failed `test_history_needs_no_tier`; r6 left in `unbuilt:` failed as `XPASS(strict)`. Suite: 1367 passed, 10 xfailed. `model check`: 71 violations, 87 warnings (Deviation 1). |
| 2 | `b59780bc` | D5 in `model_decisions.py`: `Decision`, `decisions`, `Ran`, `run`, `check_tests` (4 workers), `report`, with `TIMEOUT`, `WORKERS` and `TAIL`. `cmd_decisions --check` prints the index line, then the report, and exits 1 on either failing. The r4 and r5 handlers (the local `GivenK test` and `GivenK_C test`, `GivenR enforced by`, `WhenRuns` `` `model decisions --check` ``, and the local Then of `uses`). `unbuilt: []`. The D5 and D6 Implementation bullets, the contract's `decisions` paragraph, and the `model_decisions.py` module-map row. | 11 tests failed first, then passed. With design-model-check's decisions scenarios, 14 passed, and r50-r52 were unchanged. decision-tiers: 6 passed. Mutations, each reverted: dropping `-o addopts=` failed the addopts test. Dropping `-p no:cacheprovider` failed writes-nothing and @r5, on U3. Dropping `-B` together with `PYTHONDONTWRITEBYTECODE` failed the same two (Deviation 4). Treating exit 5 as holding failed the `collects nothing` case. Live: `0 check decisions: 0 hold, 0 failing`, exit 0. Suite: 1379 passed, 8 xfailed. |
| 3 | `727a9f39` | The sort applied to the frontmatter of 71 files, `status:`, `tier:` and `enforced_by:` only. 0074 gains `supersedes:` with the 27 slugs. 0075 and 0076 written. `test_decision_checks.py` (D10, D17, totals, judgement). Index regenerated. | At RED, the size and generate tests passed by design. The tiers test failed with 71 `w_untiered` and 18 `v_d8`, and the totals and judgement tests failed. After the sort all passed, and `model check` was back at 53/16/19/0. Mutations, each reverted: with 0012 set to `accepted`, `w_untiered` fired and the tiers test failed. With 0019 set to `accepted`, `v_d8` fired (Deviation 5). Removing 0076's `enforced_by` gave `v_d6`. A 301-line tracked file failed 0076's test, and `decisions --check` gave `failing  spec/decisions/0076-…: exit 1`. It was taken out with `git rm -f` alone. Suite: 1384 passed. |
| 4 | `e20df824` | `readiness_bar.rested_on`, `decision_reasons` and `_RAN`, with `check` appending the decision reasons (D13). `batch_brief.CHECKS` gains `model decisions --check` (D14). building-a-batch step 4's judgement bullet (D15). `well-formed` (D13). The readiness Implementation bullet. decision-tiers' `## Not yet` is `- None.`. | 8 tests failed first. `…not_run` passed at RED, as a test of absence does. Then all passed. With the bar, batch, brief, skill and decision-check tests and the readiness and batches scenarios, 79 passed. Mutations, each reverted: matching `rests_on` by the full id only failed the short-form case (and every other test using the short form). Dropping the cache failed `test_each_decision_runs_once_a_process`. Suite: 1393 passed. |
| 5 | this commit | This report, the README row, every box of the plan ticked. | Step 2's figures above; the smoke run. |

## The sort as applied

The plan's table was applied with three changes. The final totals are 75 decisions: 27 `accepted`, 46 `superseded` (19
by an accepted decision and 27 by 0074) and 2 `rejected`. The 27 in force are 4 `check`, 15 `requirement` and 8
`judgement`, which are the plan's totals, since one change moves a decision up and another moves one down.

| # | plan | applied | evidence |
|---|---|---|---|
| 0071 an-asker-is-told-by-its-registered-asker-id | `requirement`: requests#r42, requests#r57 | **`judgement`** | requests.md has no live r42 or r57: the two are 0.29 ids under `## Dropped` ("not implemented; kept under Not yet"). An entry naming them would be an unresolved reference, and no live line states the decision. It drops (D7). |
| 0036 one-requirement-form | `judgement` (a `check` if a test is found) | **`requirement`**: design-model-check#r31 | No test refuses `#behaviour/r<n>`. r31 ("a work-item whose `accepts` names a reference that is not `<capability>#r<n>`" → error) states the decision: a requirement is written `<capability>#r<n>` and in no other way. It moves up (D7). |
| 0047 references-are-ids | `requirement`: **r30, r32** | `requirement`: design-model-check#r31, #r32, #r33 | r30 is about a scenario's tag naming a requirement its capability lacks, not a frontmatter field, so it is dropped. r31 refuses a frontmatter reference not in id form (`accepts`). r32 refuses a proposal's `adds` that names no id, and r33 refuses an `under` that names nothing, as a path written there would. Together they state "frontmatter names other files by id". |

The other bold entries are confirmed with `model why` and by reading the lines:
- **0018**: batch-measurement r6 and r7 refuse a `garbled` session file and an `unreadable` transcript, naming it.
- **0049**: migration-tools r1, where `migrate run` relocates every old-layout directory and rewrites what names them, in one run.

The plain entries were read too, and each states its decision:
- **0001**: r36 and r38, a capability's id and name, and a feature paired by name.
- **0024**: r4, an id listed as retired is reused.
- **0025**: r47 and r48, clingo.
- **0027**: r36 and r37, type-first ids.
- **0033**: r22-r24, the glossary judged by `model check`.
- **0045**: r42, an old layout refused, naming `scripts/migrate`.
- **0051**: r25, a line that does not parse.
- **0054**: r10 and r11, a requirement untested and a scenario overtagged.
- **0060**: batch-measurement r1.
- **0062**: migration-tools r13 and r14.
- **0075**: decision-tiers r1-r3.

All four `check` decisions hold in `model decisions --check` (0006, 0048, 0053, 0076).

## Deviations

1. **Task 1's `model check` figure: 71 violations, not 72.** Today's accepted → accepted supersessions number 18, not
   19: 0049 supersedes 0032, which is `rejected`. 53 + 18 = 71. Warnings were 87, as planned.
2. **`test_the_decisions_run_side_by_side` is marked `timing`.** It holds a time ceiling (under 2.5 s), and this
   repository runs such tests alone (`pytest.ini`: "holds a time ceiling, so it runs alone"). So the timing run is
   `2 passed`.
3. **Parametrised cases as loops.** `test_v_d8_…` and `test_a_wrong_enforced_by_is_named` loop in the `ModelTest`
   with `reset()`, with no `subTest`, so the subtests stay at 135. `test_a_test_that_does_not_run_is_failing` is a
   pytest function and uses `pytest.mark.parametrize`.
4. **The `-B` mutation.** Dropping `-B` alone leaves the run green, because `PYTHONDONTWRITEBYTECODE=1` (D5) also stops
   bytecode. Dropping both turned the writes-nothing test and @r5's U3 red, and so did dropping `-p no:cacheprovider`
   alone. The two bytecode guards are redundant, and both are kept.
5. **The 0012 mutation.** With 0012 set back to `accepted`, the run gives `w_untiered` and not `v_d8`: its superseder
   0038 is now itself superseded by 0074. The tiers test still fails. To show a live `v_d8`, 0019 was used instead,
   whose superseder 0042 is accepted. That gave one row, and the test failed.
6. **0075's and 0076's `source`** is written in full,
   `record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-design`, as 0074 writes it. The
   plan's short form `record/2026-11-04-…` is unresolved, and `test_the_live_decisions_keep_their_tiers` caught it.
7. **The local Then is keyed `("ThenDoes", "test")`**, acting on `step.term == "use"`. A local key is
   (template, kind), not (template, verb), as the batches' `@local("ThenDoes", "batch")` shows.
8. **Small additions to D5's interfaces:**
   - `Ran` gains `timeout`, the seconds for the "timed out after <n> s" line;
   - `run` also drops `PYTEST_ADDOPTS` from the environment, so that the person's own environment cannot deselect a
     named test;
   - the D2 problems live in `model_decisions.wrong()`, to keep `model_work.py` at 280.
9. **The smoke run's times** were taken with Python on a second item, because the shell has no `bc`.

## D1-D18

| # | Kept or changed |
|---|---|
| D1 | Kept: built on `workflow-simplification`, not pushed. |
| D2 | Kept. The problem texts: `tier '<t>' is not one of check, requirement, judgement`; `enforced_by <e>: a test, on a requirement decision`; `enforced_by <e>: not a file of this repository`; `enforced_by <e>: a requirement, on a check decision`; `a judgement decision gives no enforced_by`. |
| D3 | Kept, and the `untiered` definition fixed in place. |
| D4 | Kept. `v_d8(Old, New)`. 0073 → 0033 is silent (0073 is now superseded). |
| D5 | Kept, with `Ran.timeout` and `PYTEST_ADDOPTS` dropped (Deviation 8). |
| D6 | Kept: r52 is unchanged, and one Implementation bullet says so. |
| D7 | Applied, with three rows changed (the sort above). |
| D8 | Kept: 27 decisions superseded by 0074. |
| D9 | Kept (0075), with the source in full (Deviation 6). |
| D10 | Kept: 0076 and the two tests in `test_decision_checks.py`. |
| D11 | Kept: only frontmatter is written, and no `## Decision` section is edited. |
| D12 | Kept: the `tier` column after `status`. |
| D13 | Kept. |
| D14 | Kept. |
| D15 | Kept. |
| D16 | Kept, with the Then keyed by kind (Deviation 7). |
| D17 | Kept, and it also refuses an unresolved reference naming `spec/decisions/`. |
| D18 | Kept: no `--json`. |

## Open problems for plans 7-9

- **design-model-check r52 against decision-tiers r5 (D6).** r52 says `--check` exits successfully on a current index.
  In a repository with a failing `check` decision it now exits 1. This is left for the person: retire and replace r52,
  or let r5 stand as the unwanted-behaviour exception.
- **Plan 9's retirement of the old capabilities.** It may supersede 0053 (the v3 agents, in force while
  role-boundaries holds) and narrow 0065.
- **Plan 7's knob changes** are to be recorded as decisions, each with its figures (design goal 8).
- **0060 is superseded** when plan 7 builds `measure batch`.
- **`model decisions --check` has no `--json`** (D18).
- **0071 is `judgement`** until requests gives the registered asker id a live line. That line would raise it to
  `requirement`.
- **The bar runs a check decision's tests on the root checkout.** An item whose own lines would change those tests
  (none can today, since lines change no code) would be checked against the tests as they are.
- **The end-of-branch review** of `bfca3e3b..HEAD` against the Review Focus and the sort is not done. It is for a
  separate reviewer, into `plan-6-review.md`.

## Files

- New:
  - `scripts/model_decisions.py`;
  - `tests/scenarios/decision_tiers_handlers.py`;
  - `tests/scripts/test_model_tiers.py`, `test_model_decisions.py`, `test_decision_checks.py` and
    `test_readiness_decisions.py`;
  - `spec/decisions/0075-decisions-carry-their-tier.md` and `0076-python-files-stay-at-300-lines.md`;
  - this report.
- Changed:
  - `scripts/model_work.py`, `model.lp`, `model_report.py`, `scripts/model`, `readiness_bar.py` and `batch_brief.py`;
  - `tests/scenarios/test_decision_tiers.py` and `tests/scripts/test_skill_building_a_batch.py`;
  - `skills/building-a-batch/SKILL.md`;
  - `spec/capabilities/decision-tiers.md` and `readiness.md`, and `spec/index.md` (`well-formed`);
  - the frontmatter of 71 files in `spec/decisions/`, and `spec/decisions/index.md`;
  - `CLAUDE.md`, `.shop/records/README.md` and the plan.
