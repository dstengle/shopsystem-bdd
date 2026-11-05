# Plan 9 (retirement and the 2.0 step): implementation report — PARTIAL

**Status: partial.** Tasks 1-8 are done, committed, and ticked in `plan-9-retirement.md`. Tasks 9, 10 and 11 are
not started. The implementer stopped at this clean task boundary because its context was running low. **Next: Task 9**
(`migrate upgrade` 2.0.0 and the version).

Every decision below that the plan does not settle was **decided by the implementer, 2026-11-05; revisit**.

## State at the end of Task 8 (HEAD `02c7ca90`), beside the baseline (`19e9fee5`/`f9807bc8`)

| figure | baseline | now | the plan's end target |
|---|---|---|---|
| suite | 1582 passed, 1 skipped | **1248 passed, 1 skipped**, no failure, no xfail | no failure; 1 skipped |
| ceiling list | `test_e2e_codified`, `test_supervision` flaky | **empty** | both gone |
| `model check` | 53 / 16 / 19 / 0 | **0 violations, 16 warnings, 0 unresolved, 0 file problems** | 0/16/0/0 |
| `model logic` | 11 (6 L5, 5 L6) | **4 findings: 4 L5** (U4 twice, U7, U8) | only U4, U7, U8 L5 (4) |
| `model lexicon --check` | 401, 0 problems | **401 terms, 0 problems** | 402 after Task 9 (`queued`) |
| decisions | 78 {28, 48, 2}; in force {4, 15, 9} | **82 {accepted 29, superseded 51, rejected 2}; in force {check 5, requirement 13, judgement 11}** | the same |
| `decisions --check` | 4 hold | **5 hold** (0018, 0048, 0076, 0082, 0083) | 5 hold |
| `model restates` | 581: 513 restated, 68 dropped | **581: 140 restated, 441 dropped, 0 pending, 0 missing** | 140 / 441 / 0 / 0 |
| `features generate --check` | exit 0 | exit 0; `supervision.feature` and `work-queue.feature` removed | the same |
| `vocab --check`, `bindings --unbound` | clean | clean | clean |
| `tools size --limit 300`, `tools check` | silent, clean | silent, clean | the same |
| unbuilt | `{} 0 []` | `{} 0 []` | the same |
| `ls agents` / `ls skills` | 13 / 11 | **3 / 5** | 3 / 5 |
| plugin version | 1.0.0 | 1.0.0 | 2.0.0 (Task 9) |

## The commits

| task | commit | what was done | collection diff (removed / added) |
|---|---|---|---|
| 1 | `adfc2101` | `scripts/shop_files.py` (`Refused`, `frontmatter`, `context_path`, `read`, `git`, `committed`, `append`, `LINE_BREAKS`) and `scripts/transcripts.py` (the transcript readers) out of `workqueue`/`measure_read`; `measure_cost.KINDS`/`duration`; `request_text.requests`; `spec_read.is_guarantees`; `workqueue_request`→`request_moves`, `workqueue_lines`→`request_lines` (and their tests); `test_kept_modules.py` | 13 / 15 (the renamed files' ids, and 2 new tests) |
| 2 | `b63d286b` | the helper `plan-9-retire.py.txt` (D10); D11 in `model_restates`; ten guarantees capabilities retired; 0080 (supersedes 0065); `spec/index.md`'s "Retired in 2.0.0" table; `test_spec_retired.py` | 82 / 25 (the ten capabilities' parametrised ids of `test_spec_guarantees`, three tests moved) |
| 3 | `4796db0c` | supervision retired; `supervise*.py` (22), `stub_claude`, the supervise/e2e/worker tests, `tests/scenarios/supervision_*`, ten agents, six skills deleted; `features generate` removes a retired service capability's feature (D4); `work_items.py` keeps only the unbuilt mark (D14); `test_agents.py` rewritten to 0083 (supersedes 0053); README's top sections rewritten for 2.0; `test_retirement.py` | 177 / 9 (supervision 80 scenarios, test_supervise_* 63, e2e 1, worker 3, `--work-item` 16, old test_agents 12, batch_git 1, a skill test 1) |
| 4 | `ea901055` | work-queue, requests r3/r4/r10-r13, migration-tools r22/r23 retired; `workqueue*.py` (7), `migrate_session.py`, `migrate_prompt.py` deleted; `request_view.py`, `shop_frozen.py`; `work` cut to D9; hooks.json without `prompting` and PreCompact; `work_queue_handlers.py` trimmed | 64 / 4 (work-queue 26, requests 6, migration-tools 2, deleted test files 20, hooks params 4, backlog_moves 4, backlog_items 1, work_items 1) |
| 5 | `554104fd` | design-model-check's 23 lines retired; D16's rules out of `model.lp` with their dead derivations; `w_uncited_obs` with `cited/1`; `model_work` reads only the frozen sources; `model why` gone; 0027/0036/0047 re-pointed; unused handlers removed | 38 / 3 (design-model-check 23 scenarios, 15 model tests named in the ledger) |
| 6 | `a1a8d953` | live requests in `.shop/requests/` (`REQUESTS`, `FROZEN`, `next_number`); every reader, writer and fixture moved | 0 / 2 |
| 7 | `7cc211c6` | batch-measurement r1-r17 retired; `measure_build.py`, `measure_read.py`, `test_measure_runs.py`, `batch_measurement_transcripts.py` deleted; `measure initiative` gone; 0018 a check; `test_measure_show_old.py` | 20 / 1 (17 scenarios, test_measure_runs 2, the allowance test 1) |
| 8 | `02c7ca90` | the glossary (D19), `spec/index.md` (where it stands, purpose, constraints, composition, where things live), `docs/capability-format.md`, README's 2.0.0 section, the module-map sweep; 0081, 0082 (supersedes 0006) | 0 / 1 |

Every removed id belongs to a deleted file, a scenario of a retired line, or a test named in the ledger (each task
compared `ids-before-<n>.txt` and `ids-after-<n>.txt` under `/home/vscode/.claude/jobs/7e9ba079/tmp/p9/`).

## Rulings so far (decided by the implementer; revisit)

1. Task 1: `test_kept_modules` has a second test, that every allowance is still needed; `request_moves` was allowed
   `workqueue_done` until Task 4. The suite's count was one above the plan's because of it.
2. Task 1: `workqueue.py` re-exported `request_text.requests` for the old code until Task 4.
3. Task 2: the helper accepts a capability with no id (formulation) when no id is asked, writing the notice and D3's
   sections.
4. Task 2: `spec/index.md`'s Testing bullets on 0065 and role-boundaries name 0080 and the guarantees left.
5. Task 2: `test_spec_retired` was written after the helper ran; its failure on the old files was not watched. The
   restates test's failure was watched (state `missing`, not `pending` as the plan guessed: the target is codified).
6. Task 3: **D4 narrowed.** A service capability with no group *and ids in `retired:`* has no feature file.
   feature-file-tools r17's example is a codified capability with no group and `retired: []` that must still be
   written.
7. Task 3: supervision's handlers were the registry handlers of six keys that other features use. They are kept as
   `tests/scenarios/world_fallbacks.py`: the Given records nothing, as supervision's recorded nothing they read, and a
   Then or When that no feature's handler takes fails, naming the step. No `supervision_*` module survives.
8. Task 3: README's intro, requires, layout, workflow, scripts and agents sections were rewritten in Task 3, not
   Task 8, so that the grep test passes at that commit. `## work run` was removed.
9. Task 3: raising-a-request's step 5 and its `work run` example line were changed in Task 3 (the plan put step 5 in
   Task 4).
10. Task 3: `test_an_initiative_is_still_measured_until_plan_9` was replaced by `test_an_initiative_measurement_is_still_read`,
    with the line it tests. The conftest's `EXPECTED` was emptied, because its 5 L6 went with supervision.
    `test_bound` drops the removed features. `work_items.spec_root` looks for `spec/capabilities/`, not `.shop/work/`.
11. Task 4: `work_queue_handlers.py` was trimmed by dropping each handler that left `vocab --check` clean, but the
    ThenExitsErr and ThenPrints `` `work` `` handlers stay. Dropping them would have swapped their checks for
    world_run's weaker fallback.
12. Task 4: `work answer` loses `--change` and `--accept`, and the test of their refusal on an item goes with them.
    `work show` with no target prints what `work list` prints. The uncited observations count both the frozen
    sources and the live requests' sources.
13. Task 4: `measure_read` used `shop_files` until its deletion. The migration-tools PreCompact bullet and the
    requests delegation bullets were removed from Implementation.
14. Task 5: a reference of a frozen kind (initiative, work-item, the proposals) is never resolved.
15. Task 5: a 0.29 id that only a decision's `source` names is looked up by its form. 0072's six ids were resolved
    before only because the frozen proposals named them.
16. Task 5: `foreign`/v18d are narrowed to request ids. `cited/1` qualifies short ids without making `foreign`
    facts. `shop_frozen` reads frontmatter through `model_parse`: `shop_files`' loader of `scripts/model` made an
    import cycle.
17. Task 5: the reference-form tests were re-pointed from proposals' `adds` to a decision's `enforced_by`/`source`.
    The range tests were deleted, because no live field expands a range. Handlers whose (template, term) no step uses
    were removed, measured by a key scan rather than by `vocab --check`.
18. Task 6: a `request/<this context>/q<n>` whose file is only in the frozen `.shop/work/requests/` is history, not
    unresolved (decisions 0069, 0071 and 0073 cite q9, q14 and q30).
19. Task 7: "the newest `*-i<n>-*.md`" was read as the newest record named `-i<n>` (`2026-11-02-i64.md`).
    `batch_measurement_world.py` was cut to the run of `measure`.
20. Task 8: `test_the_module_map_is_whole` failed at first. `scripts/features`, `migrate` and `model` were named only
    by `*.py` globs, and their rows now name the scripts. A `<placeholder>` in a row is read as `*`.
21. Task 8: D19's `work run` gloss was joined into one sentence, because v_t7 refuses two.
    `docs/capability-format.md`'s procedures were reworded, and its example glossary was kept as an illustration.

## The "Every item left for plan 9" table, so far

| # | settled by / state |
|---|---|
| 1 | settled, Task 5 (`554104fd`): frozen history is not resolved |
| 2 | open (Python 3.12 floor) |
| 3 | settled, Task 3 (`4796db0c`) |
| 4 | settled, Task 3 |
| 5 | settled, Task 8 (`02c7ca90`) |
| 6 | settled, Tasks 3-5, 7 |
| 7 | settled, Task 8 (0082) |
| 8 | settled, Task 8 (0081) |
| 9 | settled, Task 3 (0083) |
| 10 | settled, Task 5 |
| 11 | **Task 9** |
| 12 | settled, Task 2 (0080) |
| 13 | open (as planned) |
| 14 | settled, Tasks 3, 7, 8 |
| 15 | kept as history |
| 16 | settled, Task 3 |
| 17 | settled, Task 8 (the `measure_batch_*` rows name `parents` and the driver) |
| 18 | settled, Task 4 |
| 19 | **Task 10** |
| 20 | kept (D15) |
| 21 | open (as planned) |
| 22 | **Tasks 9-10** |
| 23 | settled, Tasks 2-5, 7 |
| 24 | **Task 9** |
| 25 | **Task 9** |
| 26 | open (as planned) |
| 27 | open (as planned) |

## What Task 9 needs

- `request_text.REQUESTS` (`.shop/requests`) and `request_text.FROZEN` (`.shop/work/requests`) exist (Task 6).
  `request_text.requests(root)` reads only `REQUESTS`. `shop_files.context_path` and `model_report.render_decisions`
  exist.
- `tests/scenarios/migration_old.py`'s `TARGET` is still `"1.0.0"`, and `plugin.json` is `1.0.0`. migration-tools
  has r22 and r23 retired. D17's g24/r24 and the `queued` condition are not yet written. r14 and r19 still give
  `"1.0.0"`.
- The gate script is `/home/vscode/.claude/jobs/7e9ba079/tmp/p9/gate.sh [base]`. The tick script is `tick.py <task>`.
  Removing a function and its decorators: `dropfn.py`. Handler keys no step uses: `unused.py`.
- The ledger is `.superpowers/sdd/plan-9-retirement/progress.md` (git-ignored). Its `Task <n>: complete` lines mark
  Tasks 1-8.
- The final whole-branch review (executing-plans) has not run yet. Task 11's report replaces this file.
