# Branch review of i24-requests-and-the-context-loop

**Verdict: DONE_WITH_CONCERNS.** The suite is green and every work-item's check passes. Five Important findings are triaged fix now; three of them were reproduced on HEAD. No finding is Critical.

1. Delegated answers fail on any node with two or more open questions (w147).
2. A `proposed` initiative that fulfils no request is left invalid (w151).
3. `model check` rejects statuses the glossary gives (w131 and w146).
4. `measure initiative` has refusals that no line asks for (w133).
5. `work retry` back to green skips r23's done check (w130).

## Range

`f890f2f..4dec501` (385 commits, 96 files outside `.shop/`). Work-items: w121 (withdrawn; its commits 3593951 and 82ad81f are merged), w122–w135, w136 (withdrawn, no commits), w137–w155.

Attribution: each implementation commit falls inside its work-item's `ready -> claimed` .. `claimed -> done` window. Where windows overlap, the commit just before the item's `claimed -> done` is taken as that item's: 4e5c8de w129, d23a6a4 w131, 7b769e8 w130, 2a2c0de w140, 395fd37 w137, 470de51 w139, 7999ff2 w153, c79de72 w151, 8f54c17 w134.

The `spec:` and `features:` commits belong to no work-item. These are 474bc25, 67112f7, 1778e8a, 43b147f, fbcae98, 8c569b9, d5bee28, 131d474, c0ba438, d2c54ff, 28047f5, d154a59, 8e2efaf, 75b000e, 948112b, e840075, 5d4cc75, aa3a579, 26175cd, a67f7d6 and a6ccc6a. They are the capability-proposals' integrate and formulate rounds, made by the coordinator under the person's delegation, and touch only `spec/` and `features/`. Minor, observation.

## Suite

`Suite: 840 passed, 0 failed at 4dec501 in 19 s` (pytest's own line: `840 passed, 1 skipped, 356 warnings, 56 subtests passed in 18.21s`).

- It runs in parallel: `pytest.ini` has `addopts = -n auto`.
- The steps do not drive the entry points in-process: they use `subprocess.run` (`tests/scenarios/conftest.py:34`).
- It runs under 60 s, so this is no finding.

## Checks

**Work-item checks.** `python3 -m pytest -q -n auto --work-item <w>` was run for each green work-item at HEAD. All pass:

| Work-items | Result |
|---|---|
| w122 | 146 passed |
| w123 | 154 passed |
| w124 | 146 passed |
| w125 | 145 passed |
| w126 | 152 passed |
| w127 | 149 passed |
| w128 | 148 passed |
| w129 | 144 passed |
| w130 | 147 passed |
| w131 | 160 passed |
| w132 | 157 passed |
| w133 | 145 passed |
| w134 | 147 passed |
| w135 | 144 passed |
| w137, w138, w139 | 146 passed each |
| w140 | 152 passed |
| w141 (guarantees) | 142 passed |
| w142, w143, w144, w145 (guarantees) | 142 passed each |
| w146 | 144 passed |
| w147 | 145 passed |
| w148 | 155 passed |
| w149 | 145 passed |
| w150 | 144 passed |
| w151 | 144 passed |
| w152 | 143 passed |
| w153 | 146 passed |
| w154 | 145 passed |
| w155 | 144 passed |

Each run also has 1 skipped and 56 subtests passed.

**w125's named check** (w121's open question: r65 under xdist): `tests/scripts/test_work_items.py::test_a_guarantees_work_item_left_with_no_test_exits_successfully_under_xdist` runs `pytest -n 2 --work-item w1` on a guarantees-only consumer and asserts exit 0. It passes in the suite. `scripts/work_items.py:123-131` decides r65 in `pytest_sessionfinish` from the work-item and the spec, so the result is the same on the controller and on each worker. **w121's question is resolved by w125.**

**`tools check --base f890f2f`** (Minor, observation): exits 1. Every hit is on a line this branch added.

- `== ruff ==`: 7 errors.
  - I001 at `scripts/measure_build.py:3` (w133, e713679)
  - I001 at `scripts/supervise_analysis.py:4` (w153, 7999ff2)
  - I001 at `scripts/workqueue.py:239` (w130, 7b769e8)
  - I001 at `tests/scenarios/test_design_model_check.py:7` (w131, d23a6a4)
  - I001 at `tests/scenarios/test_work_queue.py:7` (w123, w130, w148)
  - FURB167 at `tests/scenarios/design_model_check_requests.py:132` (w132, 1303b55)
  - FURB167 at `tests/scripts/stub_claude.py:182` (w154, 2739c54)
  - The fix: `ruff check --fix`.
- `== vulture ==`: `tests/scenarios/work_queue_status_steps.py:77` has an unused variable `notes` (w123, 2305b9e).
- `== import-linter ==`: "the project states no import contracts". This is not `missing`; there is nothing to read.

**`tools size --limit 300`**: prints nothing. No tracked Python file is over 300 lines.

**`features deprecated`**: three deprecated scenarios are left.

- work-queue @r1 "add with --part-of, --under and --accepts writes a drafted work-item with the fields given (deprecated)": already there at Base.
- migration-tools @r15 "`migrate run` on a repository with <change> refuses …": already there at Base.
- work-queue @r9 "`work <command>` commits the change it makes to a work-item on the current branch (deprecated)": deprecated on this branch by 28047f5, but its replacement's work-item, w140 (accepts work-queue#r9), is green. See Finding M1.

**`features bindings`**: "every binding names a scenario".

**Dry-run and real modes**: none on this branch. `git push --dry-run` is a verification step, not a mode of an operation the system offers. `migrate status` and `migrate upgrade` both take their steps from one `pending()` (`scripts/migrate_upgrade.py:47-50`), and the branch changed only the hook's text. No randomized test is needed.

## Removed and weakened tests

None. What I searched: every removed line under `tests/` and `conftest.py` in `git diff f890f2f HEAD`, plus added `skip`/`xfail`. The removed lines account for themselves:

- `supervision_tests_steps.py`: the Given "i1's work-item w1 is ready, accepting other#r1" was generalised into a regex Given. Its only user, the deprecated r56 scenario, is retired by w121's Retires.
- `batch_measurement_then_steps.py::gives_sessions` now asserts every column of the table, and the token columns still go through `NUMBERS`. This is stronger, not weaker.
- `batch_measurement_given_steps.py::directory_holds` / `store_transcript`: Givens only.
- The scenarios removed from `features/` are only the deprecated ones the work-items' Retires list: w122 batch-measurement @r43, w124 migration-tools @r24, w121 supervision @r56, w131 design-model-check @r19. Their bindings are `scenarios()` calls, which are unchanged.

## Allowances

- **w121, `tests/scenarios/test_supervision.py::run_work` (setup)**: holds. 82ad81f only filters `PYTHONPATH` in the environment; no assert, expected value or parametrize case changes.
- **w130, `tests/scenarios/work_queue_status_steps.py::with_state` (setup)**: holds. 7b769e8 only writes extra work-items from the Given's text; no assert changes. The function was first committed after Base (2305b9e).
- Every other report gives "none". I checked those against the diff above.

## Cannot verify

- **F-obs-1** (`supervise_all.py` thread crash): checked by reading only. I know of no input today that raises a non-`Refused` exception in a thread.
- **F-obs-3** (PreCompact hook in a worker session): checked by reading. A compaction inside a worker could not be triggered cheaply. The SessionStart half is shown by this very session, which started with `work status`'s text, w121's stale question included.

## Findings

### F1. Important, w147 (3f97115), fix now: delegated answers on a node with two or more open questions

**Where:** `scripts/supervise_answers.py:69-80` (with `scripts/supervise_faults.py:92-112`).

**What is wrong:**

- `answers()` writes the first answer into `w1.md` with `self.section` and does not commit it.
- `ask()` then starts the next question's session. When that session ends, `worker()` → `checkout_changes()` (r28) sees `w1.md` changed in the main checkout and not committed by work run.
- work run puts it back, reverting the answer, and raises a Fault blaming the answering session. `keep_round` commits the record, and the run exits 1.
- The next run does the same. A node with two or more open questions is never answered under a delegation.

**Why it matters:** gate rounds give several questions per proposal (r68, r85), so r77 fails in its main case. The answer is lost and the run stops every time.

**Reproduced:** `python3 -m pytest -n0 -s <probe>`, using the supervision steps and the r78 Givens plus a second bullet under w1's `## Questions`. What came back:

- `EXIT 1`
- `work: the session answering w1's question faulted: while its answerer worked, .shop/work/i1/w1.md changed in the repository's own checkout and not committed; work run put it back`
- `w1.md` has both questions and no `## Answers`.
- The last commit is `work: w1 answer round 2-answer faulted`.

**Fix:** make the node file work run's own while it writes answers. Either commit each answer as it is written, or write all of a node's answers after its sessions have ended. Add an r77 examples row with two questions on one node.

### F2. Important, w151 (c79de72), fix now: a `proposed` initiative that fulfils no request

**Where:** `scripts/supervise_rounds.py:113-124` with `scripts/supervise_brief.py:66-70`.

**What is wrong:**

- `round()` moves the initiative to `started` and commits that, makes the round's worktree and branch, and then `worker()` → `verify_push` logs a line.
- `brief()` → `integrate_lines()` → `path_of(root, "")` then raises `Refused("there is no request  under .shop/work/requests")`. Note the empty id and the double space.
- `Refused` is not caught by `except (Fault, GitFailed)`, so `keep_round` never runs.

**Why it matters:** the initiative is `started` although no round started (r10: change nothing), the branch `round/i1-1-integrate` is left, and `log.jsonl` is left uncommitted. Every later `work run` is refused under r46.

**Reproduced:** a probe with i1 `proposed`, dated 2026-10-20, with no `fulfils`, then `work run i1` twice. What came back:

- `EXIT 1`, `work: there is no request  under .shop/work/requests`
- `STATUS  M .shop/work/i1/log.jsonl`
- `BRANCHES * main  round/i1-1-integrate`
- `LOG work: i1 proposed -> started`
- The initiative is `status: started`.
- The second run gives `SECOND EXIT 1`, `work: .shop/work/i1/log.jsonl under .shop/work is not committed; commit it before work run starts`.

This is the same failure as observation 2026-10-25-integrate-round-without-request, which i24 met itself (dd7ac50 committed the line by hand).

**Fix:** check that the request can be read, in `due()` or `check()`, before anything moves, and refuse as r10 requires. What `work run` does for such an initiative needs a supervision line first (through integrating-a-proposal).

### F3. Important, w131 (d23a6a4) and w146 (bbca36c), fix now: `model check` rejects statuses the glossary gives

**Where:** `scripts/model_work.py:11` and `:14`.

**What is wrong:** `STATUSES` gives a capability-proposal no `awaiting-answer` and a request no `withdrawn`. Both are in term/status (`spec/index.md:128`, changed on this branch). `model check` therefore reports each as a file problem (design-model-check r27: "a status … not in its kind's lifecycle"), on data work run itself writes (r69, w146/w152).

**Reproduced:** a probe using `tests.scenarios.conftest.World`, with `proposal(status="awaiting-answer")` and a request with `status: withdrawn`. `model check` gave:

- `file: .shop/work/i1/p1.md: status 'awaiting-answer' is not one of approved, drafted, formulated, merged, withdrawn`
- `file: .shop/work/requests/q1.md: status 'withdrawn' is not one of accepted, awaiting-asker, awaiting-upstream, delivered, open, refused`

**Fix:** add both statuses, and add a design-model-check r27 examples row for each.

### F4. Important, w133 (e713679), fix now: refusals no line asks for

**Where:** `scripts/measure_read.py:55-66`.

**What is wrong:** `measure initiative` refuses in three cases, and no batch-measurement Behaviour line asks for any of them:

- `fulfils` is not one id;
- the request is not there;
- the request has no asker.

r63 and r64 only say what to give.

**Why it matters:** behaviour reaches code only through a line. work run's r75 → `analyse()` then reports "refused, so there is no analysis".

**Fix:** write the refusal line first, through integrating-a-proposal, with its scenario, or remove the refusals. (w133's task review found this. It was accepted as-is under the delegation, but the rule triages it fix now.)

### F5. Important, w130 (7b769e8), fix now: `work retry` back to green skips the done check

**Where:** `scripts/workqueue.py:202-215`.

**What is wrong:** `work retry` can return a work-item to `green`. This happens after `Faults.fail` moved it green → failed when the push of a green move failed (`supervise_faults.py:79-90`). retry does not run `workqueue_done.becomes`/`mark`, so the initiative stays `started` although r23's condition now holds.

**Why it matters:** the coordinator's answer to w130 (Reading B) names `work retry` as one of the commands r23 means. No later command makes the condition true, because it already holds. This is a wrong answer.

**Fix:** do in `retry` what `withdraw` does (`workqueue.py:239-247`), with initiative.md in the commit, and add an r23 examples row for retry.

### M1. Minor, w140, observation: the deprecated work-queue @r9 scenario is still there

**Where:** `features/work-queue.feature` (the @r9 deprecated scenario).

**What is wrong:** the scenario was deprecated by 28047f5. Its replacement is accepted by w140, which is green, but w140 has no `## Retires` (it was drafted with `work add` before r73's drafting existed).

**Fix:** a work-item that retires it with its binding.

### M2. Minor, observation: lint and dead code

The `tools check` hits above. Repro: `python3 <Scripts>/tools check --base f890f2f`. Also `scripts/model_facts.py:32` `CONTEXT_PATH =rf"…"` and `scripts/workqueue_request.py:136` `after =edit(…)` (w132, w149), whitespace that ruff's selected rules do not flag.

## Shape

- **Size limit (CLAUDE.md):** met. `tools size --limit 300` prints nothing.
- **Module map:** every new module has a row (supervise_all, supervise_answers, supervise_analysis, supervise_intake, supervise_draft, model_requests, migrate_session, workqueue_status, workqueue_note, workqueue_start, workqueue_done, workqueue_request). Two rows no longer say what their module does (Minor, observation):
  - The `scripts/supervise*.py` row says `supervise_rounds.py` holds "a capability-proposal's apply and formulate rounds". It also runs the gate (w146) and integrate (w151) rounds.
  - The `workqueue_done.py` row says "the rewrite `work withdraw` and `work resolve` commit". `mark` also writes `started` for work run's integrate round (w151, `supervise_rounds.py:147-152`).
  - Check that would show this complete: each row names every caller of its module's public functions.
- **Step modules:** "one `<capability>_*_steps.py` module a concern" is met by every new step module but `tests/scenarios/design_model_check_requests.py` (w131). That module follows its siblings `design_model_check_reading.py` and `_then.py`, which were already off-pattern at Base.
- **Code no scenario reaches:** vulture finds only `notes` (above). `features bindings` is clean.
- **The repository's own `model check`** (Minor, observation): it reports v16a for i24 itself (dated 2026-10-24, fulfils no request). This is the rule this branch adds, and what F2 tripped over. It also reports v_d1 for nine done initiatives (i1, i3, i8–i11, i13, i16, i17). There is no `.shop/work/requests/`, so these come from the part rule (`model.lp:242`), which the branch did not change. Repro: `python3 <Scripts>/model check`.

## Coupling

- **Claude Code transcripts** (`scripts/measure_read.py`): counts compactions from `type: system, subtype: compact_boundary` rows and tool uses from `tool_use` content blocks. Both are an internal, unpublished format. If either is renamed, the figure becomes 0 silently, because r47 refuses only an unknown shape, not an unknown subtype. What would make it stable: a fixture test on a recorded real transcript, and/or counting the `compacted` lines the branch's own PreCompact hook writes to the ledger, which go through the published hook API.
- **`claude -p --output-format json`**: `subtype` values (`error_max_turns`, `error_during_execution`) and `num_turns` are part of the SDK's documented result. They are relied on correctly.
- **pytest-bdd internals** (`scripts/work_items.py:71-76`): reads `item.function.__scenario__`, `.feature.filename` and `.tags`. These are private. A pytest-bdd upgrade breaks them, which `tests/scripts/test_work_items.py` would show. What would make it stable: pin pytest-bdd's major version where the plugin declares its dependencies.
- **Claude Code hooks** (`hooks/hooks.json` PreCompact, `${CLAUDE_PLUGIN_ROOT}`): these are published. See F-obs-3 for how they meet work run's own workers.

## Observations

- **F-obs-1. Important, w134 (8f54c17):** `scripts/supervise_all.py:45-49` catches only `Refused` in an initiative's thread. Another exception is printed by `threading.excepthook`, and `run_all` can exit 0 under r82. Checked by reading; no known input triggers it today (observation 2026-10-25-thread-crash-exits-zero).
- **F-obs-2. Important, w147:** the answer pass runs once, at the start of `pull_through` (`scripts/supervise.py:201`). A question raised later in the same run goes to the person with exit 3, against r77, until the next run (observation 2026-10-25-answer-pass-once-a-run).
- **F-obs-3. Important, w124 (c8c7e34, 63bdb23):**
  - Neither hook checks `SHOPSYSTEM_WORK_RUN_WORKER` (`scripts/migrate_session.py`, `scripts/migrate_upgrade.py:168`), and work run's workers load this plugin.
  - Every worker is told `work status`, stale questions included. This session's start shows it.
  - A worker session that compacts would append to `.shop/work/<initiative>/ledger.md` and commit it on the worker's branch. That is a change under `.shop/work/` outside its stage directory, which fails the work-item (r6, r34).
  - Fix: both hooks say and do nothing under a worker. This needs a migration-tools line.
- **F-obs-4. Minor, w153:** `scripts/supervise_analysis.py:58-66` copies `analysis.md` when the session's result is readable but not DONE (from w153's open cases).
- **F-obs-5. Minor, w148:** a `--lines` path that is a directory is refused as "does not exist" (`scripts/workqueue_request.py:73-74`; from w148's open cases).
- **F-obs-6. Minor, supervision r74 (`scripts/supervise_draft.py:58-81`):** one fix work-item is drafted under the capability-proposal of the first work-item named, with that work-item's `under` and `accepts`. This review's fix-now findings span supervision (F1, F2), design-model-check (F3), batch-measurement (F4) and work-queue (F5). One drafted work-item cannot accept the lines of all of them.
