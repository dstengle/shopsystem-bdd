# w183 research notes

Tools: `tools refs` ran (`Scripts:` path). `tools tests-of` has no map (`tools map` not run): every test list below is `by search`. `tools size --limit 300` printed nothing: no file over 300.
Probe: `.shop/scratch/w183-1-research/probe_rounds.py`, run `python3 -m pytest -q -s -n 0 <path>` (xdist hides prints).

## 1. Why each accepted scenario is red today

Run: `python3 -m pytest -q "tests/scenarios/test_supervision.py::<name>"` (node ids from `--collect-only`).

- r111 `test_an_initiative_that_a_workitems_transition_leaves_able_to_be_done_is_set_done_before_work_run_ends`: undefined Given `i1 is started and its work-item w1 is ready` (feature line 877). Code: see 2 and 3.
- r114 `..._the_proposals_adds_changes_and_removes_are_written_from_the_change_list_the_round_applied`: undefined Given `i1's capability-proposal p1 is awaiting-answer, its adds naming thing#r4 and thing#r5, ... given by its gate round, and its Answers section with "No."` (line 987). Also undefined by search: `the apply round for p1 gives DONE with a change list that adds thing#r4 and changes thing#r2 on thing`. Code: `scripts/supervise_rounds.py` `Rounds.run_round` never reads an apply round's `changes` (only the integrate branch calls `supervise_change.entries`); `move` writes no `adds/changes/removes`.
- r83 deprecated `..._the_proposal_is_formulated_deprecated`: PASSES today (1 passed). Retired by w183.
- r83 `..._ends_without_giving_a_question_the_proposal_is_formulated`: undefined Given `the formulate round for p1 gives DONE with no question` (line 1258). Code: passes in substance today (`AFTER["approved"]` always goes to formulated).
- r112 `..._gives_questions_each_is_written_under_the_proposals__questions`: undefined Given `the formulate round for p1 gives DONE with the questions "Are returns counted?" and "Is a loan one book or many?"` (line 1267). Code: `supervise_rounds.py:103` `asked = ... if kind == "gate" else None`, so a formulate round's questions are dropped.
- r113 `..._gives_a_question_the_proposal_is_awaitinganswer`: undefined Given `the apply round for p1 ends, and the formulate round for p1 gives DONE with the question "Are returns counted?"` (line 1275). Code: `supervise_rounds.py:16` `AFTER["approved"] = ("formulate", "formulated")`, no question check.
- r115 Outline, 4 examples: undefined Given `the gate round for p1 <ending>, and every worker gives DONE` (line 1311; each example's text differs: BLOCKED / ends in an error / ends at its turn limit / no result file). Code: `supervise_rounds.py` `run_round` raises `Refused`; `supervise.py:200-206` `pull_through` calls `self.rounds()` before `self.pull(MOVABLE)`, so nothing else of the initiative moves; `supervise_all.py:66` catches it per initiative.

Stand-in keys needed by the new Givens (read: `tests/scripts/stub_claude.py:186-253`): the gate, apply and formulate sessions all carry `agent=initiative-round`; `plan["initiative-round"]` covers all three, `plan["round:formulate"]`, `plan["round:apply"]` override per kind, `fields` merges into result JSON (so `changes` works). No stub change needed.

## 2. What the system answers today

Probes (run, `python3 -m pytest -q -s -n 0 .shop/scratch/w183-1-research/probe_rounds.py`; the real `scripts/work run i1` against a scratch git repo with the stand-in claude):

- P1 formulate round gives a question (p1 awaiting-answer, answered "One place.", plan `round:formulate` questions ["Are returns counted?"]): rc 0. p1 `approved -> formulated` (log, by work run). p1 `## Questions` holds only the old "Is a shelf one place or a list?"; "Are returns counted?" is not written. Then w1 drafted -> green in the same run.
- P2 gate BLOCKED with question, p1 and w1 drafted: rc 1, stderr `the gate round of p1 (.shop/work/i1/runs/p1/1-gate) gave the outcome BLOCKED, and p1 keeps its status drafted`. p1 stays drafted; w1 stays drafted (no transition, no worker). Log has only the gate's push/start/end lines.
- P3 w1 `done` (review is its last stage), q2 `delivered` naming i1, all workers DONE: rc 0, stdout `w1 green`. i1 stays `started`. Branch review ran. `measure initiative` was refused by the stand-in's session transcript (`session.json ... no usage with input and output tokens`), so the measurement r105 needs is missing. Deviation: the scenario's w1 is `ready`; I used `done` to avoid a merge. Inconclusive for the done path; read in 3.
- Scenario run (not probe) of the deprecated r83 test: passes.
- read: `workqueue_done._holds` (`workqueue_done.py`) checks work-items and delivered requests only, not the measurement or analysis (r105 says both).

Nearest cases not run (read): the formulate round's questions when the proposal has no `## Answers` (`due()` waits for answers); an apply round that gives `changes` with an unknown capability (read: nothing reads it).

## 3. Old assumptions

Places still assuming the old form (read unless marked):

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_rounds.py:16 `AFTER` | `approved` -> formulate, always to `formulated`; `awaiting-answer` -> apply, `approved` | r113: a formulate question gives `awaiting-answer`; r116 says an answered formulate question gives a formulate round, but `AFTER` gives an apply round for any `awaiting-answer` | test_supervision r83 deprecated (run, passes), r71, r80 (by search) | read, `tools refs` |
| scripts/supervise_rounds.py:103 `asked` | questions only for kind `gate` | r112 needs formulate questions written | gate scenarios r69, r85 (by search) | read |
| scripts/supervise_rounds.py:105 `move(name, before, after, asked)` for apply | apply's move writes no lists | r114 writes adds/changes/removes from the applied list | none (by search: no apply-with-changes test exists) | read |
| scripts/supervise_change.py:38 `write_proposals` | the only writer of a proposal's `adds/changes/removes` (integrate) | r114: apply rewrites them | integrate scenarios (by search: supervision_integrate_steps.py proposals_written) | `tools refs write_proposals`: 0 (see defect D2) and search |
| scripts/supervise_draft.py:43 | drafts work-items only for `formulated` | a formulate round with a question now parks the proposal awaiting-answer, not drafted | proposal drafting scenarios (by search) | read |
| scripts/supervise.py:113 `move` calls `workqueue.move` | a work run's move never runs the done check | r111: a move that leaves i1 able to be done must make it done | none (by search: no test of i1 done via work run passes today) | read |
| scripts/workqueue.py:242 `moved_to` | the done check, used by the work-queue commands only | r111 needs it on the run's path | work-queue withdraw/resolve scenarios (by search) | read, `tools refs moved_to` (2 refs, 1 production) |
| scripts/supervise.py:200 `pull_through` | a Refused from `rounds()` stops draft and pull | r115: the other nodes go through their transitions before the exit | r86-r88 scenarios (by search, not run) | read, probe P2 |
| scripts/workqueue.py:19 `PROPOSAL_STATUSES` | `awaiting-answer` is in `STATUSES`, so `approved -> awaiting-answer` is allowed | no change needed | none | read |

## 4. Tests the requirements make impossible to keep

`tools tests-of` has no map: all by search.

- test_supervision.py, `..._the_proposal_is_formulated_deprecated` (feature line 1245): passes today. Retired by w183 (its `## Retires` names it); removed with the feature scenario.
- Searched the stand-in plans that set `initiative-round` questions for all three kinds (supervision_rounds_steps.py:42-49, supervision_all_steps.py:84-87). A formulate round in those scenarios would now stop at awaiting-answer; I found no scenario where that round is reached with a question, so none breaks.
- r71 `..._a_formulate_round_is_started_for_the_proposal` and r80 `..._is_approved` (by search): formulate with no question still ends `formulated`; they keep passing.
- r86-r88 (by search): assert a round's proposal keeps its status; they do not assert the other nodes stay put; no change.
- Scenarios with a gate BLOCKED and a drafted work-item: none found by search, so r115 breaks no test.
- Verified sound (read): no test asserts `i1` stays `started` after a green work-item, except through the r109/r111 scenarios that are red today.

## 5. A step the work-item skips

- The done check: `supervise.move` calls `workqueue.move` (no done check), while the work-queue path calls `workqueue.moved_to` (done check, and `initiative.md` in the commit). read. Effects only the skipped step produces: write `status: done` to `initiative.md`, and add it to the commit. Existing way not run in a probe.
- The pull after a round's refusal: `pull_through` skips `draft()`, `pull()` and branch review when `rounds()` raises (P2). read and probe P2.

## 6. Defects

D1 a formulate round's questions are dropped and the proposal goes `formulated`.
- Repro: `python3 -m pytest -q -s -n 0 .shop/scratch/w183-1-research/probe_rounds.py::test_formulate_round_gives_question_on_approved_proposal` (run).
- Came back: p1 `formulated`; `## Questions` holds only "Is a shelf one place or a list?"; log `approved -> formulated by work run`.
- Requirements r112, r113 are accepted by w183; this is their red case, reported as a defect too.

D2 (tool) `tools refs becomes` said 0 references; `scripts/workqueue.py:245` calls `workqueue_done.becomes(...)`. Found by search. `tools refs write_proposals` said 0 for the same kind of reason, though `write_proposals` is called in `supervise_rounds.py:108` (found by search).

## 7. The file set

Production:
- scripts/supervise_rounds.py (134): `AFTER` and `due()` for a formulate question (r113, r116 reading); `asked` for formulate (r112); write apply's lists (r114).
- scripts/supervise.py (260): `pull_through` runs `pull` after a refused round, then re-raises (r115); done check after moves (r111), or the call in `move`.
- scripts/supervise_change.py (52): a writer for a proposal's lists, used on apply (r114).
- scripts/workqueue_done.py (67): if the done check is reused from `supervise` (r111).
- scripts/workqueue.py (290): only if `moved_to` is reused from the run (room 10 lines, so keep it out).
- scripts/supervise_draft.py (81): read only, no change (formulated check).

Tests and features:
- features/supervision.feature (1468, not Python): remove the `@r83 @deprecated` scenario at line 1245 (Retires).
- tests/scenarios/supervision_rounds_steps.py (263, room 37): new Givens for r112, r113, r83 no question, r114, and the gate-by-ending Givens for r115 would push it over the room; put them in a new module (e.g. `tests/scenarios/supervision_proposal_rounds_steps.py`) and add a row in CLAUDE.md's module map.
- tests/scenarios/test_supervision.py (259, room 41): no change needed for the new steps (imports the step modules); the deprecated test goes away with its scenario (scenarios() binds by feature).
- tests/scenarios/supervision_then_workers.py (279, room 21): no change; `w1 is green` is in test_supervision.py.
- tests/scripts/stub_claude.py (270): no change needed (read: plan keys sufficient).

Modules on the path, unedited, with line counts (room under 300): supervise_worker.py 251 (49); supervise_pool.py 143 (157); supervise_all.py 83 (217); supervise_draft.py 81 (219); supervise_analysis.py 74 (226); workqueue_request.py 183 (117); workqueue.py 290 (10); workqueue_done.py 67 (233); supervise_change.py 52 (248); supervise.py 260 (40); supervise_rounds.py 134 (166).

Open readings (the planner decides; both given):
- Q1: `AFTER["awaiting-answer"] = apply` treats every `awaiting-answer` as a gate or formulate question alike. Reading A: a formulate question's answers give a formulate round (r116), so `AFTER` must know the round that asked. Reading B: they give an apply round, as today's `due()` does. The status alone does not say which.
- Q2: r111's done check after a run move: reading A, in `supervise.move` via `moved_to`; reading B, once after `pull` in `pull_through`. r105 also needs the measurement, which `workqueue_done` does not check (not in w183's accepted set).
