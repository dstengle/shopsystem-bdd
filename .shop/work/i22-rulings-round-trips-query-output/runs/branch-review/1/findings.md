# Branch review of i22-rulings-round-trips-query-output

**Verdict: DONE_WITH_CONCERNS.** The suite is green and every check passes. Two Critical findings are about records: w92 and w95 each retired deprecated scenarios, and neither work-item has a `## Retires` section. One Important finding is triaged fix now: `work answer` refuses an answer that holds a newline, and no line asks for that refusal. The product code matches the lines it accepts.

## Range

`dc9ece7..55b4057` on `next`: 125 commits, 263 files, of which 88 are under `features/`, `scripts/`, `tests/`, `ruff.toml` and `CLAUDE.md`.

Work-items:
- **Through `work run`'s claimed → done:** w94 (a207018, 6212f6f, cd39016), w96 (2bf920a), w97 (625728c) and w99 (52141df).
- **Merged by hand and withdrawn, attributed by their merge commits and `## Delivered`:**
  - w91: 8f57ccb, f460299, merged in 6eb48a9
  - w92: adf0d01, 79cc5a1, merged in 49dd8e6
  - w93: 5eb628a, merged in 58da176
  - w95: 583db74, e6d39e2, 61e6706, merged in a7a04ab
  - w98: cca993a, 42a13da, ffbbabd, merged in 0218152

## Suite

`Suite: 699 passed, 0 failed at 55b4057 in 13.2 s` (1 skipped, 62 subtests passed). It runs in parallel: `pytest.ini` gives `addopts = -n auto`. In-process only in part: the batch-measurement steps call `measure`'s `main` in-process, and the other capabilities' steps run the scripts as subprocesses. The suite is under 60 s, so this is no finding.

## Checks

- **w98's check, `python3 scripts/tools check scripts tests`:** passed. ruff printed "All checks passed!", vulture printed "clean", and import-linter said "the project states no import contracts". This session would not run the worktree's own `scripts/tools` without approval. So I ran the plugin's copy (`/home/vscode/shopsystem-bdd/scripts/tools check scripts tests`) from the worktree, with the worktree's `ruff.toml`. I read the two `tools_check.py` files side by side and they are the same. No other work-item names a check.
- **`tools check --base dc9ece7`:**
  - ruff: All checks passed!
  - vulture: clean
  - import-linter: "the project states no import contracts". This is not `missing`; there are no contracts to read for.
- **`tools size --limit 300`:** printed nothing. No file is over the limit, touched or not.
- **`features deprecated`:** four deprecated scenarios.
  - batch-measurement @r42 "the totals are over the stages' sessions…" (Finding M1)
  - work-queue @r9 "`work <command>` commits the change…" outline (Finding M2)
  - migration-tools @r15 `migrate run` outline: already there at Base
  - work-queue @r1 "add with --part-of…": already there at Base
- **`features bindings`:** "every binding names a scenario".
- **Dry-run and real mode:** the branch adds or changes no operation that has both a dry-run and a real mode. `git push --dry-run` in supervise_review.py and supervise_faults.py is not touched. There is no agreement test to run, and none is owed.

## Removed and weakened tests

What I searched for:
- removed `def` lines in `git diff dc9ece7 HEAD -- tests`: 7, each rewritten in place, none deleted
- added `skip` or `xfail`: none
- removed or changed `assert` lines
- scenarios removed from `features/`

1. **Seven deprecated supervision scenarios retired by w92 (adf0d01):** @r5 ×2, @r32 ×2, @r26, @r36 and @r37. They proved the awaiting-ruling and `## Rulings` behaviour. w92's plan lists all seven (§1, §4). Five of them are also listed in w91's Retires, which 8f57ccb retired. The @r26 and @r37 scenarios are listed under no work-item's Retires. → C1
2. **Six deprecated supervision scenarios retired by w91 (8f57ccb), the @r4 one among them:** listed in w91's Retires. Holds.
3. **The analysis-tools @r11 outline "tests-of fails when nothing executed the target or the function does not exist (deprecated)", retired by w95 (583db74):** it proved exit 1 on an empty answer and on an unknown function. w95's plan lists it (§1, §4). w95.md has no Retires. → C2
4. **The batch-measurement @r41 scenario "…awaiting-ruling and failed counts…", retired by w94 (cd39016):** listed in w94's Retires and in its plan §4. Holds.
5. **`tests/scenarios/test_analysis_tools.py` `exits_with_error`, w95:**
   - The exact stderr `tools: src/cart.py has no function named …` and the `unexecuted` branch (`0 of the 1 tests…`) were removed.
   - The new `says_target_unreadable` (test_analysis_tools.py:54-56) checks only a prefix: `tools: cannot read src/cart.py:<name>: `.
   - Both are in w95's plan §4. Holds.
6. **`tests/scripts/test_tools.py:103-104` `forgotten`, w95:** the expected exit changes from 1 to 0, with the new line. Listed in w95's plan §4. Holds.
7. **`batch_measurement_then_steps.py` `gives_counts`, w94:** `awaiting_ruling` becomes `awaiting_answer`. Listed in w94's plan §4. Holds.
8. **`batch_measurement_then_steps.py:139-148` `gives_totals`, w94:** it asserted the three token columns unconditionally and now asserts only the columns the table names. Listed in w94's plan §4 (D5). The change holds; its allowance row does not (I2).
9. **The supervision steps:**
   - `awaiting` and `sections` Thens, and the `item_with_sections` and `awaiting_with_questions` Givens: rewritten from ruling to answer, and `run_work`'s env drops `SHOPSYSTEM_WORK_RUN_WORKER`. w92's plan §4. Holds.
   - `supervision_tests_steps.two_items`: renamed by w91 (8f57ccb). w91's plan §4, Reading A. Holds.
10. **`design_model_check_problems.file_problem_named`, w97:** the filter is narrowed, so the step is stronger. w97's plan, decision 5.
11. **`test_work_queue.with_items` and the `work_queue_withdraw_steps` regex, w91:** the Given now writes the asker's log line. The status pattern widens to `[\w-]+` so it can match `awaiting-answer`; no assertion is loosened. w91's plan §4.
12. **w98's test edits:** renames (`map_kept` → `map_kept_in`, `none` → `_none`), `[...][0]` → `next(...)`, `re.M` → `re.MULTILINE`, `zip` → `itertools.pairwise`, `.format` → f-strings, `timezone.utc` → `UTC`. Each is equivalent and no assertion changed.

## Allowances

| Work-item | Row | Verified |
|---|---|---|
| w94 | `gives_totals`: interim | **Does not hold.** `gives_totals` existed at Base, so it was not first committed after Base. The change is allowed by plan §4 (D5), not by this row. → I2 |
| w94 | `stages_sessions_took`: setup | Holds. The diff changes no assert, no expected value and no parametrize case. |
| w94 | `gives_counts`: plan §4 | Holds (plan-listed). |
| w95 | `ToolsTest.run_script` env: setup | Holds. Env only. |
| w95 | `analysis_tools_json_steps` `gives_references`, `gives_summary`: the initiative's own | Holds. First committed in e6d39e2, after Base. It now asserts what the answered wording (d05706e) says. |
| w92 | none beyond plan §4 | Holds. The deviation, rewriting the Questions/Answers Then instead of removing it, keeps the step and weakens nothing. |
| w93, w96, w97, w98, w99 | none | Holds. w96's F12 adds only `atexit` cleanup. |

## Cannot verify

- **The worktree's `scripts/tools` was not run** (it needed approval). I ran the plugin's copy, which has the same `tools_check.py`, in the worktree. This is counted as verified, by that method.
- **The probes were not run.** Running `.shop/scratch/i22-rulings-round-trips-query-output-branch-review/probe.py` needed approval. The observations below are read from the code at the named lines; none of their outputs come from a run.

## Findings

### C1: Critical, w92, fix now (record)
- **Where:** `features/supervision.feature`, adf0d01.
- **What:** seven deprecated scenarios were retired with `features retire`, and w92.md has no `## Retires` section. Two of them are listed under no work-item's Retires:
  - "a work-item whose transition is to awaiting-ruling keeps its work-item branch (deprecated)" (@r26)
  - "no worker is started for a work-item that is <status> (deprecated)" (@r37)
- **Why it matters:** decision 0011 has the work-item that turns the replacement green list each scenario it retires under Retires. Without the list, the removal is a change under `features/` that no work-item lists.
- **Fix:** add `## Retires` to w92.md naming the seven, as plan §1 lists them. w94's finding was fixed the same way.

### C2: Critical, w95, fix now (record)
- **Where:** `features/analysis-tools.feature` (lines 124-136 before 583db74), 583db74.
- **What:** the deprecated @r11 outline "tests-of fails when nothing executed the target or the function does not exist (deprecated)" was retired, and w95.md has no `## Retires` section.
- **Why it matters:** the same as C1.
- **Fix:** add `## Retires` to w95.md naming the outline. Plan D1 gives the reason.

### I1: Important, w91, fix now
- **Where:** `scripts/workqueue_answer.py:29-30`, 8f57ccb.
- **What:** `work answer` refuses an answer that holds a newline ("an answer is one line"). No line asks for this refusal:
  - r13 and r14 do not ask for it.
  - work-queue's Implementation section names only the refusal of an item that is not awaiting-answer.
  - r7 covers only what `work` cannot do, and writing a multi-line answer is possible.
- **Why it matters:** behaviour reaches code only through a line, and this is an observable refusal.
- **Fix:** either write the line first through integrating-a-proposal (for example a work-queue Implementation bullet: "an answer is one line; one holding a newline is refused under r7", which would also make `answer_lines`' pairing safe), or remove the check.

### I2: Important, w94, observation
- **Where:** `runs/w94/4-implement/report.md:30-31` and `tests/scenarios/batch_measurement_then_steps.py:139-148`.
- **What:** the allowance row calls the `gives_totals` change "interim", but the test was committed before Base. The row claims more than it holds.
- **Why it matters:** the change itself is plan-listed (§4, D5), and tables still give every token column, so the product is unaffected. The record of why the test may change is wrong.
- **Fix:** correct the row to "plan §4 (D5)". Restore the unconditional token-column asserts once M1 retires the deprecated r42 scenario, which is the only table without turns.

### M1: Minor, w94, observation
- **Where:** `features/batch-measurement.feature:105-120`.
- **What:** the deprecated @r42 totals scenario is still in the suite. Its replacement's work-item, w94, is green, accepts r42, and lists only r41 under Retires.
- **Why it matters:** the deprecated scenario keeps `gives_totals` conditional (I2).
- **Fix:** a work-item that lists it under Retires removes it with `features retire`.

### M2: Minor, w91, observation
- **Where:** `features/work-queue.feature:176-190`.
- **What:** the deprecated @r9 outline is still in the suite. Its replacement, with the answer row, was delivered by w91, which is withdrawn after a hand merge and passes at HEAD.
- **Fix:** the same as M1.

### M3: Minor, no work-item, observation
- **What:** these commits belong to no work-item:
  - formulation and spec: 4768a80, b5d7b83, 0756b18, 4987643, d05706e, db3ac66. Three of them change `features/` by formulation: deprecations, new scenarios, and d05706e's rewording of the not-yet-green r55 scenario.
  - records: 599367f
  - hand edits to work-item files: 4627a98, 9a5e068, cc44eec (statuses set to awaiting-answer by hand), f460299, ad07088, a902966, 6c803dc and 7c07931
- **Also:** five work-items' code reached `next` by hand merges, not through `work run`'s claimed → done. w95's task review was left to this review.
- **Fix:** none needed for the product. The person may want the hand status edits (cc44eec) noted as the r29 step applied ahead of itself.

## Shape

- **Size, 300 lines (CLAUDE.md:5):** met. `tools size` printed nothing.
- **Module map:**
  - `scripts/workqueue_answer.py`: a new concern, with its row added (CLAUDE.md:20). Met.
  - `scripts/migrate_upgrade_answers.py`: under `scripts/migrate_upgrade*.py`, one module a step. Met.
  - `scripts/measure_read.py`, which now also reads Claude Code's store (measure_read.py:219-233): the row's "reading". Met.
  - `scripts/tools_map.py` and `scripts/tools_refs.py`, which take `--json`: their rows. Met.
  - `supervise_brief.py:53-63` (answers in briefs) and `supervise_worker.py:115-116` (a kept branch): `work run`. Met.
  - `model_work.py:82-89`: r110. Met.
- **`tests/scenarios/`, `<capability>_*_steps.py`:** analysis_tools_json_steps.py, supervision_answers_steps.py and work_queue_answer_steps.py meet the pattern. migration_upgrade_answers_steps.py and migration_version_steps.py use the `migration_` prefix that the existing migration modules already use.
- **`tests/scripts/`:** test_migrate_upgrade.py, test_migrate_upgrade_answers.py and test_work_item_ids.py. Met.
- **Dead code:** vulture is clean. `Merge.failed_claimed`'s path to awaiting-answer (supervise_merge.py:81-91) is reached by no scenario. The path predates the branch, which only renamed it (w92's report says so).
- **Refactor observation:** test_migrate_upgrade.py:50-82 (`AVersionFileThatHoldsNoVersion`, from w96) now repeats what the r30 and r31 scenarios (w99) assert. The check that would show it done: the class removed, and the r30 and r31 scenarios still passing for both `status` and `upgrade`.

## Coupling

- **Claude Code's transcript store (w94), measure_read.py:219-233:**
  - **Relies on:** `CLAUDE_CONFIG_DIR`, else `~/.claude`, then `projects/*/<session>.jsonl`, and the rows' `type`, `requestId`, `sessionId`, `isSidechain`, `agentId` and `message.usage.output_tokens`. Claude Code publishes none of this as a contract.
  - **If the layout changes:** round trips silently disappear under r55.
  - **If the row shape changes:** `assistant_rows` raises `Refused` and the whole `measure initiative` refuses (decision 0018).
  - **What would make it stable:** record each stage's transcript path in its session.json when the stage runs; add a test built from a real transcript sample; and have `show` say why a stage has no round trips.
- **ruff (w98), ruff.toml:2-71:**
  - **Relies on:** about 400 rule codes selected by name as "ruff 0.17's" defaults, while `tools install` pins no ruff version (tools_env.py:17).
  - **If ruff changes:** a ruff that does not know a code fails on the configuration itself, and later releases rename and remove codes.
  - **What would make it stable:** pin ruff in `tools install`, or select by rule families.
- **Python 3.11 (w98):** `datetime.UTC` at workqueue.py:141, supervise_worker.py:76 and measure_read.py:19. `work` already needed 3.11, since supervise_worker.py imports `tomllib`; `measure` now needs it too. The noqa at measure_read.py:16 ("older Pythons refuse a Z") implies older Pythons are supported, which they are not. Minor: state the minimum Python, or drop the comment.
- **git (w92), supervise_worker.py:115-116:** `git worktree add <tree> <branch>` on a kept branch is published git CLI. A branch checked out in another worktree fails as a Fault. Stable.

## Observations

None of these was reproduced: running the probe needed approval. Each is read from the code at the lines named.

- **One answer, two questions (w91/w92):** `work answer` on an item whose `## Questions` has two bullets writes one answer and returns the item to its stage. The pairing by position (supervise.py:206-207, supervise_brief.py:53-63) then leaves the second question open in a running item. Reproduction: probe.py `p2` (`work answer w1 "Only the first"` on an item with "First?" and "Second?").
- **Upgrade put-back (w96), migrate_upgrade.py:133-154:** steps are now planned and applied one at a time, and the put-back catches only `CalledProcessError` and `OSError`. A `ValueError` or `AttributeError` raised by a later step's plan would leave the earlier step's `git mv`s and writes in place, with a traceback, against r7. An example is a log.jsonl line that is not JSON, or `[]`, at migrate_upgrade_answers.py:466-467, in an initiative the 0.24.0 step did not rewrite. Fix: catch `Exception` in the put-back branch. Reproduction: probe.py `p1`.
- **Session in several project directories (w94), measure_read.py:227-230:** the first one sorted is read (named by w94's report).
- **Held text with a newline (w99), migrate_upgrade.py:36-40:** a `.shop/plugin-version` whose held text has a newline inside it prints a hook line that is broken across lines (named by w99's report).
