# research of w184 (supervision r110, r117, r19)

Method: no coverage map (`tools tests-of` says "no map"; `tools map` not run, it is a whole-suite run). Function uses by `tools refs`; tests by search and by run. Scripts: `python3 /home/vscode/shopsystem-bdd/scripts/tools`. `tools size --limit 300`: no file over 300.

## 1. Why each accepted scenario is red today

Run: `python3 -m pytest -q "tests/scenarios/test_supervision.py::<node>"` (4 node ids from `--collect-only`). Result: 1 passed, 3 failed.

- **r19, "a limit of 80 turns"** (features/supervision.feature:405). Run: AssertionError at tests/scenarios/supervision_then_workers.py:218 (`max_turns`): argv has `--max-turns 40`. Missing: scripts/supervise_worker.py:54 `MAX_TURNS = {"research": 40}` must be 80; the flag is passed at :222. The two earlier Thens (file set, accepted scenario) passed in the run.
- **r19, "a limit of 40 turns (deprecated)"** (feature:393). Run: passes. It must be retired with the change (see 4).
- **r117, "gives no question"** (feature:1453). Run: `StepDefinitionNotFoundError` for Given "the gate round's result gives no question, and every round ends" (feature:1456). Missing step: tests/scenarios/supervision_rounds_steps.py (steps at :42 and :47 need a question). The Then "p1's ## Questions holds one question, asking for the approval of p1's lines as drafted" matches the step at supervision_rounds_steps.py:52, whose `gate_question()` unpacks four quoted strings: it would crash with ValueError (read, not run). Code: scripts/supervise_rounds.py:103 `asked = [...]` is `[]` for a gate with no question; scripts/supervise.py:111-118 `move()` writes nothing for `[]`. Missing: an approval question in `run_round` (supervise_rounds.py:103-105).
- **r110, "next branch review before exit"** (feature:1461). Run: `StepDefinitionNotFoundError` for Given "every worker gives DONE, the first branch reviewer's result lists two findings ... and the second lists nothing to fix now" (feature:1465). Existing step supervision_proposal_steps.py:44 has no "first"/"second" and gives one result per agent (tests/scripts/stub_claude.py:184-190, `plan.get(short)`, read). Also undefined (read, not run): Then "one work-item was drafted in i1 for the two findings, and it is green" (feature:1467; the step at supervision_proposal_steps.py:76 has ", part of p1, naming ..." instead), and Then "after that work-item turned green a second session of bdd-branch-reviewer was started, before `work run` exited" (feature:1468; the step at supervision_then_workers.py:268 says "after {name} was green", and asserts exactly one review, so it cannot be reused). Missing in code: scripts/supervise.py:207-213 `pull_through` runs one branch review per run; after the fix is pulled (:211) nothing re-checks.

## 2. What the system answers today

Probe `.shop/scratch/w184-1-research/probe_due.py` (run: `python3 -m pytest -q -s -n 0 -p no:warnings .shop/scratch/w184-1-research/probe_due.py`, against the checkout's scripts/, a repository in tmp_path). Calls `supervise.Run(root,"i1").due()`:
- proposal `awaiting-answer`, its `## Questions` empty: `('p1', 'apply', 'approved')`. Run.
- proposal `awaiting-answer`, one unanswered question: `None`. Run.
- proposal `drafted`: `('p1', 'gate', 'awaiting-answer')`. Run.

The r117 case end to end (gate DONE with no question) is read: `run_round` gives `asked=[]` (supervise_rounds.py:103), `move` writes no question (supervise.py:114), so the proposal is `awaiting-answer` with zero questions and the next `due()` starts apply. See defect D1.

Nearest cases: r19 80-turn Givens (file set and accepted scenario) run and pass. No other probe made; the rest is read.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| supervise_rounds.py:43-44 `due` | an `awaiting-answer` proposal with 0 questions and 0 answers counts as answered (0 >= 0), so apply starts | r117: a gate with no question now gives one question, so the proposal waits for an answer; a zero-question awaiting-answer proposal must not reach apply | none (no test holds an awaiting-answer proposal with no question; all `awaiting-answer` fixtures in tests/ carry a question) | run (probe_due.py), search (`awaiting-answer` in tests/) |
| supervise_rounds.py:103-105 `run_round` and supervise.py:111-118 `move` | a gate with no question writes no question | r117: writes one approval question under `## Questions` | scenarios with "every round ends" over a drafted proposal: feature:1232, :1392 (Then on the brief only) | search |
| supervise.py:207-213 `pull_through` | one branch review per run; `lists_nothing(kept)` judges the first review only | r110: a review of the fix follows, and analysis waits on the last review | the fix path: feature:1028 (via supervision_proposal_steps.py:44) | search |
| supervise_draft.py:58-81 `fix_work_item` | one fix per review, deduplicated by the findings path | r110: each re-review gets its own findings path, so a repeated finding is drafted again | feature:1028 | search |
| supervise_worker.py:54 `MAX_TURNS` | research gets 40 turns | r19: 80 | the 80-turn scenario (fails) and the 40-turn one (passes) | refs (1 use, supervise_worker.py:222), search (tests) |

## 4. Tests the requirements make impossible to keep

No coverage map, so by search.
- features/supervision.feature:393-403, the 40-turn scenario. Passes today; asserts `--max-turns 40`. Impossible after r19. Retire it with `python3 <Scripts>/features retire "a researcher is given the work-item's file set and accepted scenarios, and a limit of 40 turns (deprecated)"`. Its binding is generated from the feature (test_supervision.py has no per-scenario binding; search for "40 turns" in tests: none).
- feature:1028, the findings-to-fix scenario (supervision_proposal_steps.py:44-83). Read, not run. The stub gives every `bdd-branch-reviewer` session the same two findings (one result per agent). Every worker is DONE, so the fix turns green. Under a re-review after the fix, a second review lists the same findings and a second fix is drafted, and `fix_drafted` (proposal_steps.py:79, asserts exactly one) fails, or the loop does not end. This depends on question Q1.
- feature:1387-1395 (r104) and feature:1232-1235 (r68): gate with "every round ends" and no question. Assert on the brief only; under r117 the proposal waits, the assertions still hold. Kept (read).
- feature:557, :591, :1034-1050 (branch review, measure): single review, unaffected by a loop after a fix. Kept (read).
- Sound: the 80-turn scenario fails only on the turn count; the researcher's file set and accepted scenario Thens pass (run).

## 5. A step the work-item skips

- r117: the approval question goes through `move()` as the gate's questions do (commit, push, `## Questions` written in the same move). No step skipped (read).
- r110: a re-review must go through `branch_review()`, which verifies the push before the review (supervise_review.py:41-45) and pushes the commit after (:78). A loop that calls only `pull()` skips both. Read.
- r110: `fix_work_item` is followed by `self.push()` (supervise.py:210) before the pull, so the fix's commits reach the remote before its review. Read.

## 6. Defects

### D1. A gate with no question leads to an apply round with no answer
Reproduce: `python3 -m pytest -q -s -n 0 -p no:warnings .shop/scratch/w184-1-research/probe_due.py::test_awaiting_answer_with_no_question`
Came back: `awaiting-answer, no question: due() = ('p1', 'apply', 'approved')`. Run.
Chain (read): gate DONE with `questions: []` → `asked=[]` (supervise_rounds.py:103) → `move(...)` writes no question (supervise.py:111-118) → status `awaiting-answer` → `due()` says apply (supervise_rounds.py:43-44, 0 >= 0). The proposal is approved unasked. This is the case r117 names.

## 7. The file set

Edits:
- scripts/supervise_worker.py (251 lines, room 49): `MAX_TURNS` research 40 → 80 (:53-54). Read, search.
- scripts/supervise_rounds.py (134, room 166): a gate with no question writes one approval question (:103-105); decide the `due()` guard for zero questions (:43-44). Read, run.
- scripts/supervise.py (260, room 40): re-run branch review after a fix goes green, until the review lists nothing or no fix is drafted (:207-213). Read.
- tests/scenarios/supervision_rounds_steps.py (263, room 37): Given "the gate round's result gives no question, and every round ends"; the Then at :52 must accept the approval question. Run.
- tests/scenarios/supervision_proposal_steps.py (116, room 184): Given for the first and second reviewer; Then "one work-item ... and it is green". Read.
- tests/scenarios/supervision_then_workers.py (279, room 21): Then "after that work-item turned green a second session of bdd-branch-reviewer was started, before `work run` exited". Read.
- tests/scripts/stub_claude.py (270): a per-session result for `bdd-branch-reviewer` (today one result per agent, :184-190). Read.
- features/supervision.feature (1468): retire the 40-turn scenario (feature:393-403) with `features retire`. Read.

Read, on the change's path, unedited:
- scripts/supervise_draft.py (81, room 219): `fix_work_item` used per review; dedup by findings path. Read.
- scripts/supervise_review.py (82, room 218): `branch_review` and `unread`; re-review needs no change. Read.
- scripts/supervise_analysis.py (74, room 226): `lists_nothing` reads the review it is given. Read.
- scripts/supervise_brief.py: findings lines for a fixed work-item (`findings_lines`, :88); unchanged. Search.

Not edited, checked: no tracked Python file over 300 lines (`tools size --limit 300` printed nothing).

## Questions for the person

- Q1. A re-review after a fix lists findings again. Reading (a): draft a fix for each review and loop until a review lists nothing or no fix is drafted. Reading (b): one re-review per run, then exit (the next `work run` takes it on). The r110 text does not say which.
