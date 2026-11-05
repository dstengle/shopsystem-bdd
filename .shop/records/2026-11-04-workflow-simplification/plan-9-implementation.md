# Plan 9 of the workflow simplification: implementation report

This is the report of the two implementer sessions that executed `plan-9-retirement.md` on 2026-11-05, each with
superpowers:executing-plans, one commit per task and no subagents. The first did Tasks 1-8 and stopped at a clean task
boundary because its context was running low; the second did Tasks 9-11. The ledger was
`.superpowers/sdd/plan-9-retirement/progress.md` (git-ignored). The end-of-branch review is left to a separate
reviewer, into `plan-9-review.md`, as the plan's Task 11 says; neither implementer ran one.

All 11 tasks are done. The old workflow is retired and plugin 2.0.0 is released on the branch:
- 271 codified lines of 16 capabilities are retired under design-decision/the-old-workflow-retired (0080): every line
  of the twelve capabilities of the old stages, which keep their files as the record of their ids, and lines of
  batch-measurement, requests, design-model-check and migration-tools;
- `work run` and its supervisor, the queue's commands (`add`, `run`, `retry`, `note`, `status`, `start`,
  `delegate`), `measure initiative`, `model why`, `migrate prompting` and `migrate compacting` are deleted, with ten
  agents and six skills;
- `model check` reads nothing of `.shop/work/` but its `source` ids; live requests are `.shop/requests/q<n>.md`;
- `migrate upgrade` has the 2.0.0 step "the workflow simplified" (migration-tools g24/r24), and this repository was
  upgraded by it; D20's four surviving pieces of work are items b1-b4.

Every decision the plan did not settle was **decided by the implementer, 2026-11-05; revisit**. The commits are on
`workflow-simplification`, from `adfc2101` to this report's commit, and are not pushed.

## Final state

Measured at the end of Task 11 (HEAD `d4a47c73` plus this report), beside the baseline (`19e9fee5`/`f9807bc8`).

| figure | baseline | end | the plan's target |
|---|---|---|---|
| suite (`python3 -m pytest -q`) | 1582 passed, 1 skipped, 135 subtests (30.5 s); 1583 ids | **1260 passed, 1 skipped**, 77 subtests, no failure, no xfail (23.9 s, 24.4 s, 24.8 s in three runs; no flaky failure); 1261 ids | no failure; 1 skipped; the count falls by the removed ids |
| collection diff over the plan | | 394 ids removed, 72 added (1583 − 394 + 72 = 1261) | each removed id accounted for |
| ceiling list | `test_e2e_codified`, `test_supervision` flaky | **empty** | both gone |
| timing (`-m timing -n 0`) | 4 passed (6.4 s) | **4 passed** (3.0 s) | 4 passed |
| `model check` | 53 / 16 / 19 / 0 | **0 violations, 16 warnings, 0 unresolved, 0 file problems** | 0/16/0/0 |
| `model logic` | 11 (6 L5, 5 L6) | **4 findings, 4 L5**: U4 "obliges `work` to commit a transition in every state", U4 "… to push a commit in every state", U7 "obliges a worker to change a file in every state", U8 "obliges a tool to print in every state" | U4 ×2, U7, U8 |
| `model lexicon --check` | 401, 0 problems | **402 terms, 0 problems** (`queued`) | 402 |
| decisions | 78 {28, 48, 2}; in force {check 4, requirement 15, judgement 9} | **82 {accepted 29, superseded 51, rejected 2}; in force {check 5, requirement 13, judgement 11}** | the same |
| `model decisions --check` | 4 hold | **5 hold, 0 failing** (0018, 0048, 0076, 0082, 0083); index current | 5 hold |
| `model restates` | 581: 513 restated, 68 dropped | **581: 140 restated, 441 dropped, 0 pending, 0 missing** | 140 / 441 / 0 / 0 |
| `features generate --check` | exit 0 | exit 0; `supervision.feature` and `work-queue.feature` gone | the same |
| `vocab --check`, `bindings --unbound` | clean | clean | clean |
| `tools size --limit 300` | silent | silent | silent |
| `tools check` (every Python file changed since `19e9fee5`) | clean | ruff and vulture clean; no import contracts | clean |
| unbuilt | `{} 0 []` | `{} 0 []` | the same |
| `ls agents` / `ls skills` | 13 / 11 | **3** (`architecture-reviewer`, `pr-reviewer`, `trial-runner`) / **5** (`analyzing-a-batch`, `building-a-batch`, `raising-a-request`, `shaping-items`, `taking-in-a-request`) | 3 / 5 |
| plugin version | 1.0.0 | **2.0.0**; `.shop/plugin-version` 2.0.0; `migrate status` lists no pending step | 2.0.0 |
| names table (plan-8 Q2) | 0 rows | **4 item rows** (7 lines), 0.07 s | 4 rows, under 0.2 s |
| `git log --oneline 19e9fee5..HEAD` | | 16 commits before this report (the plan's, Tasks 1-9, the partial report, the upgrade and four `work idea`) | |

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
| 9 | `656edf06` | `scripts/migrate_upgrade_simplified.py` (D13: `plan(root) -> Changes`, `FROZEN_TEXT`) and its step in `STEPS`; `apply` makes a move's destination directory; plugin.json 2.0.0 and D22's description; migration-tools: the `release` value `1.0.0`, `queued`, r14's and r19's givens at `2.0.0` (P10), g24/r24, the Implementation bullet; `migration_old.TARGET = "2.0.0"`; the `queued` check, r24's rename and index checks in the handlers; `work_queue_world.matches` reads a backticked path; README's 2.0.0 section and CLAUDE.md's row; `test_migrate_upgrade_simplified.py` (11 tests) | 0 / 12 (11 step tests, `@r24`) |
| 10 | `f298479d`, `95f08cb4`, `e23b54cd`, `5608a6b9`, `d4a47c73` | `migrate upgrade` on this repository (one commit by migrate: `.shop/plugin-version`, `.shop/work/FROZEN.md`, q14 renamed to `.shop/requests/q14.md`); D20's four items `work idea` b1-b4, each committing itself | 0 / 0 |
| 11 | this report's | the verification, the smoke run, this report, the records index, the plan's boxes ticked (Task 10's among them) | 0 / 0 |

Every removed id belongs to a deleted file, a scenario of a retired line, or a test named in the ledger. Each task
compared `ids-before-<n>.txt` and `ids-after-<n>.txt` under `/home/vscode/.claude/jobs/7e9ba079/tmp/p9/`, and every
task's gate ran before its commit with the figures in the ledger.

### Task 9 in detail

- The tests were written first, with the spec's g24/r24 and `TARGET = "2.0.0"`. Run before the module existed:
  `test_migrate_upgrade_simplified.py` failed on its import, and `@r24` failed on "`migrate` writes
  `.shop/work/FROZEN.md`" (no step pending, nothing changed). `@r14` and `@r19` passed, through `migration_old.plugin()`'s
  copy at `TARGET`.
- After the module, the step in `STEPS` and plugin.json at 2.0.0: three failures, each found and fixed at its cause.
  A test's `Path / "…%d" % n` precedence. `@r24`'s write step went to the work-queue world's shared
  `ThenDoes write` handler, which matched no backticked path, so `matches` now reads one as that file.
  `work request --from <q2's asker>` is refused by requests r32 (ruling 22).
- The gate: 1260 passed, 1 skipped. Its first run failed `test_the_module_map_is_whole` only because the new module
  was still untracked when the suite ran (the gate's `git add -N` comes after it); the re-run was green.
  `model lexicon --check` 402 terms; `model check` 0/16/0/0; `migrate status` gave `1.0.0`, `2.0.0` and
  `pending upgrade step 2.0.0 "the workflow simplified": …`.

### Task 10 in detail

- Counted before: 12 open initiatives and 28 internal requests not closed; q14 the only open request of a peer.
- `python3 scripts/migrate upgrade` exited 0 and printed `upgraded to 2.0.0: the workflow simplified`, then 12
  `open initiative` notes (i39, i45, i47, i49, i52, i53, i55, i56, i58, i59, i60, i61), 30 `the lines of proposal …
  were never applied` notes (i45-i61's drafted proposals), `moved request q14 to .shop/requests/` and 28
  `internal request` notes (q17-q47). 72 lines in all.
- Its commit `f298479d` holds `M .shop/plugin-version`, `R100 .shop/work/requests/q14.md → .shop/requests/q14.md` and
  `A .shop/work/FROZEN.md`, and nothing else: no deletion, and `spec/decisions/index.md` unchanged because it was
  already current. `migrate status` then listed no step; `model check` gave 0/16/0/0, so q14 brings no violation.
- D20's items, each `work idea "<title>" --note "from <source> of the frozen queue (.shop/work/…)"`:
  b1 "Requests between repositories over GitHub issues" (i39 w212, deferred: it needs a design session with the
  person), b2 "Request lines into an upstream in the downstream's own terms" (q17), b3 "Every command answers in JSON
  and exits 0 but on a crash" (q25), b4 "Requirement quality: fewer question cycles from better lines" (q26).
- The names table: 4 item rows (7 lines with its sentence and header), 0.070-0.077 s in three runs. Under 50 rows,
  so no narrowing.
- The gate: every figure as the Intended baselines; `git status --porcelain` empty; collection unchanged.

## The smoke run

On a clone of this worktree at `/home/vscode/.claude/jobs/7e9ba079/tmp/p9/smoke`, checked out at `19e9fee5` (a real
1.0 repository: `.shop/plugin-version` 1.0.0, 64 initiative directories, 47 requests; the plan's "66 initiatives and
49 requests" counted other entries: `.shop/work/requests/` also holds `log.jsonl` and `runs/`), this branch's
`scripts/migrate upgrade` was run by its absolute path.

- **First run: exit 1, 0.37 s.** The clone has no git identity (this worktree's is repository-local), so the commit
  failed with "Author identity unknown". migrate printed "migrate put the repository back as it was" and the tree was
  as before: HEAD `19e9fee5`, `git status --porcelain` empty. That is r15's all-or-nothing, seen on a real repository.
- **Second run, with a local `user.name`/`user.email` in the clone: exit 0, 0.23 s wall.** One commit
  `migrate upgrade: 1.0.0 to 2.0.0`; `git diff --diff-filter=D HEAD~1` empty; the diff is the same three entries as
  Task 10's; `.shop/plugin-version` 2.0.0. Its output is byte-identical to Task 10's (12 / 30 / 28 / 1 notes).

## Deviations, each with its reason

All decided by the implementer; revisit. 1-21 are the first implementer's (Tasks 1-8), 22-27 the second's.

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
22. Task 9: `test_the_upgraded_repository_is_on_the_new_workflow` raises its new request `--from internal`, not
    `--from <q2's asker>` as the plan wrote. Requests r32 refuses a request raised as another asker ("this repository
    raises requests only as itself"). The test still shows q5 numbered above the frozen q1-q4.
23. Task 9: one test beyond the plan's list, `test_a_request_whose_frontmatter_does_not_read_refuses`, for D13's
    second refusal. A request "does not read" when its frontmatter gives no `status` or no `asker`; the refusal names
    the file and changes nothing.
24. Task 9: `migrate_upgrade.apply` makes a move's destination directory, because `git mv` refuses a missing one and
    `.shop/requests/` is new. A step's internal request whose asker is this context's own `bounded-context/<path>` is
    named as an `internal request` (D8 leaves both unmoved).
25. Task 9: r24's given block gives the old decisions index as a line of text, not a table row, since a table row
    beside text in a given block is a file problem (v15m). The handlers' index check branches on whether the given
    holds a ledger; r24's rename check compares the moved request byte for byte with the given file.
26. Task 9: `work_queue_world.matches` reads a noun phrase that is a backticked path as that file, so the shared
    `ThenDoes write` handler takes "`migrate` writes `.shop/work/FROZEN.md`" rather than a second `write` handler
    (which `vocab --check` would refuse as a duplicate claim).
27. Task 10: the task has no commit step of its own (migrate and `work idea` commit themselves); its boxes are ticked
    in Task 11's commit.

## D1-D23

| # | Kept or changed |
|---|---|
| D1 | Kept. Everything is on `workflow-simplification`; nothing was pushed. |
| D2 | Kept. 271 lines; restates 140 / 441 as the planner measured. |
| D3 | Kept, with deviation 3 (formulation, which had no id). |
| D4 | **Changed** (deviation 6): only a service capability with no group *and ids in `retired:`* loses its feature. |
| D5 | Kept, with deviations 14 and 18: a frozen kind's reference, and a frozen request's, is history, never resolved. |
| D6 | Kept. `shop_frozen.sources`, `cited/1`; `w_uncited_obs` stays 16. |
| D7 | Kept. |
| D8 | Kept (Task 9). q14 is the one request it moved here. |
| D9 | Kept, with deviation 12. |
| D10 | Kept, with deviation 3. The helper is committed once (Task 2) and was not edited after. |
| D11 | Kept. |
| D12 | Kept. 3 agents, 5 skills. |
| D13 | Kept, with deviations 23 and 24. `FROZEN_TEXT` is D13's text exactly. |
| D14 | Kept. |
| D15 | Kept. |
| D16 | Kept, with deviation 16 (`foreign`/v18d narrowed to request ids). |
| D17 | Kept, with deviation 25. r24 is D17's sentence; it parses with `queued`, and lexicon is 402. |
| D18 | Kept: 0080, 0081, 0082, 0083; 0018, 0027, 0036, 0047 re-pointed in frontmatter only. |
| D19 | Kept, with deviation 21. |
| D20 | Kept: b1-b4. Left out as planned: q41 (plan-5 S6's quiet git), q45 and q46 (plans 2-8 built them), q14 (moved; to be resolved by the person, below), and the other internal requests, each about `work run`, its rounds, gates, proposals or delegations. |
| D21 | Kept. |
| D22 | Kept. plugin.json 2.0.0 with D22's description; README's `## 2.0.0` names the step. |
| D23 | Kept. `test_a_0_29_repository_reaches_2_0_in_one_commit` (0.29.0 → 2.0.0 in one commit). |

## The "Every item left for plan 9" table

| # | settled by / state |
|---|---|
| 1 | settled, Task 5 (`554104fd`): frozen history is not resolved |
| 2 | **open**: `_LineParser`'s swap waits for a Python 3.12 floor (this machine is 3.11.15) |
| 3 | settled, Task 3 (`4796db0c`) |
| 4 | settled, Task 3 (`4796db0c`) |
| 5 | settled, Task 8 (`02c7ca90`) |
| 6 | settled, Tasks 3-5, 7 (`4796db0c`, `ea901055`, `554104fd`, `7cc211c6`) |
| 7 | settled, Task 8 (`02c7ca90`, 0082) |
| 8 | settled, Task 8 (`02c7ca90`, 0081) |
| 9 | settled, Task 3 (`4796db0c`, 0083) |
| 10 | settled, Task 5 (`554104fd`) |
| 11 | settled, Task 9 (`656edf06`): the step rewrites `spec/decisions/index.md` |
| 12 | settled, Task 2 (`b63d286b`, 0080) |
| 13 | **open** as planned: r52 against decision-tiers r5, ruled by `spec/universal.md`'s precedence |
| 14 | settled, Tasks 3, 7, 8 |
| 15 | kept as history (D22) |
| 16 | settled, Task 3 (`4796db0c`) |
| 17 | settled, Task 8 (`02c7ca90`) |
| 18 | settled, Task 4 (`ea901055`) |
| 19 | measured, Task 10: 4 rows, 0.07 s. **Open** only in that no narrowing is needed below about 50 rows |
| 20 | kept (D15) |
| 21 | **open** as planned: no `conversation` line expands `q<n>` or `r<n>` |
| 22 | settled, Tasks 9-10 (`656edf06`, `f298479d`, b1-b4 `95f08cb4`..`d4a47c73`) |
| 23 | settled, Tasks 2-5, 7 |
| 24 | settled, Task 9 (`656edf06`) |
| 25 | settled, Task 9 (`656edf06`): the chained upgrade is tested (D23) |
| 26 | **open** as planned: the old kinds and retired capabilities' Terms stay in the lexicon |
| 27 | **open** as planned: `docs/design-model/` v5 still describes initiatives; a v6 is a design session's work |

## Open problems

- The open rows: 2 (Python 3.12 floor), 13 (r52 and decision-tiers r5), 21 (the names table expands no `q<n>`/`r<n>`),
  26 (unused old terms in the lexicon), 27 (design model v5); 19 needs nothing until the backlog nears 50 rows.
- **q14** (`product/missingmass.io/subscriptions-viewer`, accepted, turn upstream) now lives in `.shop/requests/`.
  Its fulfilment, "requests go through one shared tool", is what `work request` already is. It is to be resolved with
  `work resolve` by the person, since a resolution names a requirement and version for the person to confirm; it was
  not resolved here.
- The requests D20 left out stay frozen, named in the upgrade's notes: q41 (settled by plan-5 S6's quiet git), q45 and
  q46 (built by plans 2-8), and the 25 other internal requests, each about `work run` and its machinery.
- **Found in the smoke run:** `migrate upgrade` in a repository with no git identity fails at its commit. It puts
  everything back, as it should, but the message is git's ("Author identity unknown"), not a refusal before the step
  that names the missing identity. Every step has this; it is not new in 2.0.0.
- **Found in Task 9:** a scenario Then whose noun phrase is a backticked path (`` `migrate` writes `x` ``) is matched by
  the work-queue world's shared `ThenDoes write`; a capability with its own notion of "write" would have to chain
  through `local`.
- The 12 open initiatives' and 30 unapplied proposals' content is frozen and named in the upgrade commit's message;
  only D20's four were entered as items. Anything else still wanted is the person's to shape.
- The end-of-branch review has not run.

## Files

- New: `scripts/shop_files.py`, `scripts/transcripts.py`, `scripts/request_view.py`, `scripts/shop_frozen.py`,
  `scripts/migrate_upgrade_simplified.py`; renamed `scripts/request_moves.py`, `scripts/request_lines.py`;
  `tests/scenarios/world_fallbacks.py`; tests `test_kept_modules.py`, `test_spec_retired.py`, `test_retirement.py`,
  `test_measure_show_old.py`, `test_migrate_upgrade_simplified.py` and the renamed request tests.
- Decisions: `spec/decisions/0080-the-old-workflow-retired.md`, `0081-the-2-0-layout.md`,
  `0082-feature-files-written-by-features-generate.md`, `0083-the-2-0-agents.md`; 0018, 0027, 0036, 0047
  re-pointed.
- Deleted: `scripts/supervise*.py` (22), `scripts/workqueue*.py` (7), `migrate_session.py`, `migrate_prompt.py`,
  `measure_build.py`, `measure_read.py`, `stub_claude`, their tests, `tests/scenarios/supervision_*`,
  `features/supervision.feature`, `features/work-queue.feature`, ten agents and six skills.
- Changed: sixteen capability files under `spec/capabilities/` (twelve retired whole), `spec/index.md`,
  `spec/decisions/index.md`, `features/*.feature` (generated), `scripts/work`, `scripts/model*`, `model.lp`,
  `scripts/migrate_upgrade.py`, `hooks/hooks.json`, `.claude-plugin/plugin.json`, `README.md`, `CLAUDE.md`,
  `docs/capability-format.md`.
- This repository: `.shop/plugin-version` 2.0.0, `.shop/work/FROZEN.md`, `.shop/requests/q14.md`,
  `.shop/backlog/b1.md`-`b4.md`.
- Records: `plan-9-retire.py.txt` (Task 2), this report.
