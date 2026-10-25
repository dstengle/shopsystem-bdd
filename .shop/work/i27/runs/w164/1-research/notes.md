# notes: research of w164 (supervision r91-r97, r66)

Method: no coverage map (`tools tests-of` says none; `tools map` runs the whole suite, not run), so every test list here is `by search`. Names: `tools refs`. Accepted scenarios run by node id in `tests/scenarios/test_supervision.py` (`-n 0` not needed; xdist on). Probes: `.shop/scratch/w164-1-research/probe_w164.py`, run with `python3 -m pytest -q -s -n 0 -p no:cacheprovider <path>`. Probe repos are under the ignored `.shop/scratch/`.

## 1. Why each accepted scenario is red today

Command for all: `python3 -m pytest -q --tb=short <node id>` (9 ids). Result: 8 failed, 1 passed (r66).

- r94 `test_an_initiative_with_no_workitem_gets_no_branch_review...`: run. Undefined step `Given i1 is started, its capability-proposal p1 is awaiting-answer, ... and i1 has no work-item` (feature line 569). Also undefined: `the initiative branch holds a commit of notes.txt that no kept branch review has read`. Code behind it: `supervise.py:pull_through` (all() over no items is true, so branch_review runs) and `supervise_review.py:branch_review`/`unread` (no guard for an initiative with no work-item). Probe c1/c2 shows the review starts (section 2).
- r95 `test_work_run_started_with_no_initiative_runs_the_integrate_apply_and_formulate_rounds...`: run. Undefined step at line 846 `an initiative i2 under .shop/work/ whose capability-proposal p2 is awaiting-answer, ..., and its Answers section with "One book."`. Also undefined: the i3 variant (847), `every round ends, each round of the kind integrate, apply or formulate ending only after long enough...` (848), `a round of the kind integrate was started for i1, and a round of the kind apply for each of p2 and p3` (850), `no round of the kind integrate, apply or formulate was started before every other round of those kinds had ended` (851). Code: `supervise_all.py:run_all` runs each initiative's `pull_through` in its own thread; the only limit is `Semaphore(limit)` in `supervise_worker.py:worker` (line 182) and `supervise_review.py:branch_review` (line 63). `self.lock` (RLock) guards only git steps, not the session. Nothing serialises integrate/apply/formulate across initiatives (`supervise_rounds.py:round`, line 61-63).
- r97 `test_an_initiative_with_no_workitem_is_not_measured`: run. Undefined step at line 987 (same as r94's Given). Also undefined: `` `work run` ran no `measure initiative` on i1 `` (line 989; only the "after the branch review was kept" form exists, `supervision_analysis_steps.py:61`). Code: `supervise.py:pull_through` line 205-211 calls `self.analyse()` after `lists_nothing(kept)`; `supervise_analysis.py:analyse` (line 36).
- r66 `test_work_run_started_with_no_initiative_takes_every_initiative...`: PASSED. Givens and Thens all defined (`supervision_all_steps.py`). It pins gate rounds side by side and one session per initiative; it does not pin the r95 serialisation (gate is not an r95 kind). Consistent with r66 as changed.
- r93 `test_a_started_initiative_with_neither_a_capabilityproposal_nor_a_workitem...`: run. Undefined step at line 1084 `i1 is started, has neither a capability-proposal nor a work-item, and fulfils the request q1, whose lines 1 and 3 ...`. Code: `supervise_rounds.py:due` (line 33) returns an integrate only for `status == "proposed"`.
- r96 `test_an_integrate_round_that_ends_done_without_a_change_list...`: run. Undefined step at 1092 (same "has neither" Given). Also undefined: `the integrate round for i1 gives DONE with no change list` (1093), `` `work run` names the integrate round of i1 `` (1095). Code: `supervise_rounds.py:round` (line 77-87) has no change-list check for kind `integrate`.
- r91 `test_the_drafts_of_an_integrate_round_that_ending_are_kept...[gives DONE with a change list naming thing]` and `[ends at its turn limit]`: both run. Undefined step at 1122 `the integrate round for i1 writes spec/capabilities/thing.md under its drafts path and <ending>`. Also undefined: `every other round ends` (1123), `the initiative branch has a commit of the integrate round's drafts, its spec/capabilities/thing.md as the round wrote it` (1125). Code: `supervise_rounds.py:round` (merge only on DONE, line 67-69; `keep_round` on non-DONE commits only the stage dir, line 96-105); `supervise_worker.py:keep_named` (226-238) copies single-path result fields only, flattened to the basename.
- r92 `test_an_integrate_rounds_change_list_gives_one_drafted_capabilityproposal...`: run. Undefined step at 1136 `the integrate round for i1 gives DONE with a change list that adds thing#r4 ...`. Also undefined: `every other round ends` (1137), `the commit that wrote i1's capability-proposals wrote two, ...` (1139). Code: no code writes a capability-proposal (`grep` over `scripts/workqueue*.py` and `supervise*.py` finds only readers; `supervise_draft.py:draft_proposals` reads `formulated` ones).

## 2. What the system answers today (probes, run)

Command: `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w164-1-research/probe_w164.py` (7 cases; each builds its repo, bare remote, stand-in claude of `tests/scripts/stub_claude.py`; runs `scripts/work run i1`). Note: a session under a `work run` worker refuses ("a worker starts no delivery"), so the probe clears `SHOPSYSTEM_WORK_RUN_WORKER` from its environment. Probe fixtures lack `spec/index.md` and a session usage block, so `measure initiative` is refused in them; the refusal itself shows that it was started.

- c1 (r94, r97 shape: `started`, p1 `awaiting-answer` with its question, no work-item, a notes.txt commit). run. Exit 0. A `bdd-branch-reviewer` session STARTED (`branch review 1 of i1` committed). Stderr: `` `measure initiative i1` was refused ... spec/index.md ... is missing `` — so measure was started with no work-item.
- c2 (same, no notes.txt; only the proposal's commit after base). run. Same: reviewer started, measure started. So the review starts on any commit after the base, not only on the unread notes commit.
- c3 (r96, r84: `proposed`, fulfils q1, integrate DONE, result has no change list). run. Exit 0, no error. Log: `work: i1 proposed -> started` and the round commit. No "change list" check. Integrate round's stage dir committed; reviewer started afterwards (no work-items).
- c4 (r92: same, result.json `"changes": [{"op":"adds","id":"thing#r2",...}]`). run. Exit 0. Result file holds the change list; no capability-proposal file written (`git ls-tree HEAD .shop/work/i1/` shows only initiative.md, log.jsonl, p1 absent, runs).
- c5 (r91 turn-limit: integrate writes `spec/capabilities/thing.md` in its worktree, `error_max_turns`). run. Exit 1: "the integrate round of i1 (.shop/work/i1/runs/i1/1-integrate) faulted, and i1 keeps its status started ... error_max_turns, 26 turns". The round's stage dir and log committed (`work: i1 integrate round 1-integrate faulted`). `spec/capabilities/thing.md` at HEAD unchanged; the drafted text is in no commit.
- c6 (r91 DONE: same write, status DONE). run. Exit 0. Drafted `thing.md` NOT on the initiative branch (HEAD still the base text). The stand-in's written file is not a committed change and `keep_named` copies nothing (no result field names it).
- c7 (r93: `started`, fulfils q1, no proposal, no work-item). run. Exit 0, no `initiative-round` session started; log shows nothing. Gap.
- Read (not run): `supervise_rounds.py:round` logs `before: proposed` in `start_initiative` for any integrate, so a started initiative given one would log a wrong transition (read).
- Read (not run): rounds of different initiatives are not serialised (section 1, r95). Not probed: needs two initiatives with apply/formulate rounds; the scenario's Givens are undefined.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| supervise_rounds.py:due (line 33) | integrate only when `status == proposed` and fulfils | r93: also `started` with no proposal and no work-item | by search: `supervision_rounds_steps.py` "fulfils the request" givens; none for `started` | tools refs due; read |
| supervise_rounds.py:round, start_initiative (52-54, 89-94) | writes `started`, logs `before: proposed`, commits, for any integrate | r93 path must not log `proposed -> started`; r84 stays for `proposed` | by search: rounds scenarios "i1's transition to started" (`supervision_rounds_steps.py:174`) | read; probe c3 |
| supervise_rounds.py:round, DONE branch (77-87) | any DONE for integrate is accepted, no change list read | r96: DONE without change list is an error naming the round; r92: change list read | none (no test covers a DONE integrate without change list; by search) | read; probe c3 |
| supervise_rounds.py:round, merge and keep (61-81, 96-105) | drafts merged only on DONE; non-DONE keeps stage dir and log only | r91: drafts kept in both endings | by search: `test_the_drafts_of...` (red) | read; probe c5, c6 |
| supervise_worker.py:keep_named (226-238) | copies a result field's single path, renamed to its basename | r91/r92: a drafts tree (spec/... path) must keep its path, and a change list, not a path | none (by search: no scenario names a result path field for an integrate) | read |
| supervise_brief.py:integrate_lines (66-70) | gives request and accepted lines only; no drafts path, no change-list form | r91 needs a drafts path; r92 needs the result's change-list shape | by search: supervision_intake/rounds briefs assert `# integrate of` only | read |
| agents/initiative-round.md (lines 27-32) | integrate replies with gate.md text and paths; result fields not named | r92: result must carry a change list the code reads | none (agent file, not run by tests; the stand-in writes fields) | read |
| supervise.py:pull_through (205-211) | `all(...)` over `items()`; empty list is true, so branch review and analyse run | r94, r97: no work-item means no review, no measure | by search: no scenario with a started initiative of no work-item (none found) | read; probe c1 |
| supervise_review.py:branch_review (39), unread (19-33) | reviews any commit since base not read by a review | r94: no review without work-item, whatever the branch holds | by search: supervision_review_steps "no session of bdd-branch-reviewer" (work-items present) | read; probe c2 |
| supervise_analysis.py:analyse (36) via supervise.py:211 | runs `measure initiative` after a kept review that lists nothing | r97: not for an initiative with no work-item | by search: supervision_analysis_steps (work-items present) | read; probe c1 |
| supervise_all.py:run_all (45-54) and supervise_rounds.py:round | initiatives in threads; only the session semaphore limits sessions | r95: integrate/apply/formulate rounds one at a time across initiatives | none (r95 red; by search no test) | read |
| supervise_draft.py:draft_proposals (36-56) | reads formulated proposals written by hand; no code writes one | r92: work run must write `drafted` proposals from the change list | by search: supervision_proposal_steps (fixtures write proposals by hand) | read; tools refs (no writer) |
| scripts/workqueue_done.py mark (used by start_initiative) | writes an initiative's status | r92/r93 reuse it only for proposed → started | by search: rounds scenarios | read |

## 4. Tests the requirements make impossible to keep

No map, so `by search`. Searched `tests/scenarios/*.py` and `features/supervision.feature` for the old behaviour: a started initiative with no work-item (`no work-item` appears in `supervision.feature` 569, 987, 790 and fixtures in `work-queue.feature`), and a branch review or measure without work-items.
- `supervision.feature` line 790 table row "no work-item | not expected": in a `--work-item` test-selection table, not a run without items. Read only the grep line; not changed by r91–r97. Not verified in full.
- `supervision_rounds_steps.py:137` `no_integrate_started`, used by the "fulfils no request" and "q9" scenarios: those initiatives are `proposed`, so r93 does not change them. Sound.
- `supervision_all_steps.py` `idle_i1` (stuck work-item) and `ended_initiatives`: each has a work-item or is done/abandoned; r93/r94/r97 do not reach them. Sound.
- `supervision_all_steps.py` `i2_with_proposal` (started, proposal drafted, no work-item): r93 needs neither, so not reached; but r94/r97 apply: with no work-item and a commit after base, the r66 scenario would now get no review and no measure. The r66 scenario asserts only gate rounds and session overlap, so it stays sound.
- `supervision_analysis_steps.py:61` and `supervision_review_steps.py:94`: all have work-items. Sound.
- r66 scenario: passes today; its assertions hold under r66 as changed. Sound.
- None found that asserts r96's old "DONE integrate is fine" behaviour (none exists).

## 5. A step the work-item skips

- Proposed-to-started (r84, existing path): `start_initiative` does `workqueue_done.mark`, logs `proposed -> started`, and commits with a push (`supervise_rounds.py:89-94`). The r93 path (already `started`) gives no round through `start_initiative`, so the status write, the log line and its commit are skipped. Probe c3 shows the existing effects: the status commit, the log line `before: proposed`, the push. Effects of that step only: the status write, the log line, the commit. Read for the r93 path.
- Non-DONE round (existing path): the round branch `round/<name>-<label>` is never merged nor deleted (`supervise_rounds.py:77-81`), so its commits, the drafts with them, are left as a stray branch. Read; probe c5 shows no drafts in any commit.
- Change list to proposals (r92, new path): no existing step writes a capability-proposal. `workqueue.add` (used by `draft_proposals`) is the nearest existing writer; it is for work-items. Read: nothing in the code tells what a proposal writer must check (requirement ids exist in `spec/`); no step for that exists.

## 6. Defects (probes run)

Each has its reproduction in section 2; commands: `probe_w164.py` cases named.
- D1 (c1, c2): a review and a measure start for an initiative with no work-item. Stderr: `measure initiative i1 was refused ...`; log: `branch review 1 of i1`.
- D2 (c3): integrate DONE with no change list accepted, exit 0, `proposed -> started` committed; r96 wants an error naming the round.
- D3 (c4): change list in the result is ignored; no capability-proposal written, exit 0.
- D4 (c6): drafts written in an integrate round DONE do not reach the initiative branch (HEAD keeps the base `thing.md`).
- D5 (c5): on turn limit the round's drafts are lost too; the faulted round keeps only its stage dir and log.
- D6 (c7): started initiative with its request's accepted lines gets no integrate round, exit 0 (r93).

## 7. The file set

Production (to change):
- scripts/supervise_rounds.py (105 lines, room 195): `due` for `started` with neither (r93); change-list read, refusal and proposal hand-off in `round` (r92, r96); drafts kept on both endings (r91); the integrate's no-DONE merge.
- scripts/supervise.py (247 lines, room 53): `pull_through` guard so no-work-item initiatives get no review and no measure (r94, r97); `pull_through` runs `rounds()` in its order (r95 serialisation hook).
- scripts/supervise_review.py (82, room 218): `branch_review` guard for no work-item (r94) if placed here rather than in `pull_through`.
- scripts/supervise_all.py (66, room 234): a shared lock across initiatives for integrate/apply/formulate sessions (r95); `run_all` threads already exist.
- scripts/supervise_worker.py (247, room 53): `keep_named` keeps a drafts tree's paths (r91); `worker`'s slot shared with the round lock (r95).
- scripts/supervise_brief.py (129, room 171): `integrate_lines` names the drafts path and the change-list shape (r91, r92).
- NEW module, suggested `scripts/supervise_change.py` (a new concern: the change list to capability-proposals, r92): a row in CLAUDE.md's module map is needed.
- agents/initiative-round.md (60 lines, not Python): integrate result gives a change list field (r92) — read only.
- skills/integrating-a-proposal/SKILL.md (78 lines): says the change list is the round's reply (read).

Tests (to change or add, for the accepted scenarios' steps):
- tests/scenarios/supervision_rounds_steps.py (258 lines; over 300 limit? no, room 42): new Givens/Thens for r91, r92, r93, r96 ("has neither", "gives DONE with no change list", "writes ... under its drafts path", "gives DONE with a change list that ...", "every other round ends", the integrate-round commit Thens).
- tests/scenarios/supervision_all_steps.py (136, room 164): Givens for i2/i3 with awaiting-answer and Answers; "every round ends, each round ... ending only after long enough"; "no round of the kind integrate, apply or formulate ...".
- tests/scenarios/supervision_analysis_steps.py (77, room 223): "`work run` ran no `measure initiative` on i1" (r97).
- tests/scenarios/supervision_review_steps.py (96, room 204): "notes.txt that no kept branch review has read" Given (r94).
- tests/scenarios/supervision_given.py (250, room 50): the "i1 is started, its capability-proposal p1 ..., and i1 has no work-item" Given (r94, r97).
- tests/scenarios/supervision_world.py (173): helper for a change-list result if shared.

Modules on the path, edited or not (line counts by `wc -l`, room under 300):
- scripts/supervise.py 247 (53); scripts/supervise_rounds.py 105 (195); scripts/supervise_review.py 82 (218); scripts/supervise_analysis.py 74 (226); scripts/supervise_all.py 66 (234); scripts/supervise_worker.py 247 (53); scripts/supervise_brief.py 129 (171); scripts/supervise_draft.py 81 (219); scripts/supervise_pool.py 143 (157); scripts/supervise_intake.py 112 (188); scripts/workqueue_done.py 67 (233); scripts/workqueue_request.py 142 (158).
- All under the 300 limit (CLAUDE.md), none over; `tools size` not run.
