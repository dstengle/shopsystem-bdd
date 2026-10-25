# w152 research notes

Work-item w152 (supervision r69): when the gate round `work run` started for a capability-proposal ends, the proposal is `awaiting-answer`.
Accepted scenario: `features/supervision.feature:857`. Scenario tests run with `--work-item w152` from the environment (PYTEST_ADDOPTS), so only this scenario collects; `tools tests-of` has no map (`tools: no map`), so test lists below are `by search`.

## 1. Why the scenario is red today

Command (`run`): `python3 -m pytest -q "tests/scenarios/test_supervision.py::test_when_the_gate_round_work_run_started_for_a_capabilityproposal_ends_the_proposal_is_awaitinganswer"`

Result (`run`): `StepDefinitionNotFoundError: Step definition is not found: Given "the gate round gives the question "Is a title given twice one book or two?" on p1, and every round ends"`, feature line 860. The run stops at the Given; no When or Then runs.

What is missing (`read`):
- A step binding for the wording `the gate round gives the question "<q>" on p1, and every round ends`. No file binds it.
- Nearest binding: `tests/scenarios/supervision_rounds_steps.py:42` `gate_result`, regex `the gate round's result gives the question (?P<text>.+), and every round ends$`. It differs in "'s result" and in the trailing " on p1", so it does not match. It also calls `gate_question`, which unpacks four quoted strings (question, two readings, mark), so a bare question would fail there too.
- Two readings, for the plan: (a) add a binding in `supervision_rounds_steps.py` that sets `plan["initiative-round"] = {"status": "DONE", "questions": [text]}` with no readings; (b) reword feature line 860 to the existing `gate_result` wording with readings. The feature line is spec-owned; I do not choose.
- The rest of the scenario's steps exist: `a round of the kind gate was started for p1` (`supervision_rounds_steps.py:64`), `p1 is awaiting-answer` (`test_supervision.py:129`), `every round ends` (`supervision_rounds_steps.py:76`).
- Code behind the Then, `read`: `supervise_rounds.py:round` runs the gate worker, then `self.move(name, before, after, asked)` with `AFTER["drafted"] = ("gate", "awaiting-answer")` (`supervise_rounds.py:12`, `:65`). `supervise.py:move` (`:106`) calls `workqueue.move`, then writes each question with `section`. So the code path for r69 exists. The probe below shows it working with the scenario's own question.

## 2. What the system answers today

Probe files, in `.shop/scratch/w152-1-research/`:
- `probe_gate.py`: the case builder and runner. Its first run failed on the git identity of the `work` commit (environment, not a finding). Not used for results.
- `probe_gate_run.py`: five cases, with the identity set. Run: `python3 -m pytest -q -s -o addopts= .shop/scratch/w152-1-research/probe_gate_run.py` (`run`).
- `probe_gate_fault.py`: two faulted-round cases. Run: `python3 -m pytest -q -s -o addopts= .shop/scratch/w152-1-research/probe_gate_fault.py` (`run`).

Each case: a repository in scratch with spec/index.md, `.shop/work/i1/initiative.md` started, and `p1.md` drafted (`adds: [thing#r1]`). Entry point: `python3 scripts/work run i1` with the stand-in claude (`tests/scripts/stub_claude.py`) and the plan's gate result. Repository git identity set.

| case | plan's initiative-round result | exit | stdout | p1 status (after) | p1 ## Questions | round starts | probe |
|---|---|---|---|---|---|---|---|
| one question (the scenario's own) | DONE, `questions: [one]` | 0 | empty | awaiting-answer | `- Is a title…?` | 1 | run |
| two questions | DONE, `[First?, Second?]` | 0 | empty | awaiting-answer | both | 1 | run |
| no questions | DONE, no `questions` | 3 | `w1 awaiting-answer` (see D1) | formulated (passed through apply and formulate) | none | 3 | run |
| object question | DONE, `[{"ask":…}]` | 0 | empty | awaiting-answer | `- {"ask": "x", ...}` (json text) | 1 | run |
| PARTIAL with a question | PARTIAL, `[Is it?]` | 0 | empty | awaiting-answer | `- Is it?` | 1 | run |
| no result file | `result: none` | 1 | none; stderr: round faulted, p1 keeps drafted | drafted | none | 1 | run |
| not-JSON result | `result: not-json` | 1 | none; stderr: result file not JSON, p1 keeps drafted | drafted | none | 1 | run |

Nearest cases, each run in the one-question repository:
- Second `work run i1` after awaiting-answer: no new gate round (round starts stay at 1), exit 1, stdout empty (`run`). Nothing is started for the proposal; `due()` finds Answers 0 < Questions 1.
- Gate with zero questions: `due()` (`supervise_rounds.py:31-32`) treats 0 >= 0 as all answered, so apply and formulate run at once (`run`, D1).
- Scenario's own data empty: the `## Questions` written by `section` as one bullet; the scenario's Then (`p1 is awaiting-answer`) passes on the file's status (`read`).
- Pass-through of the outcome check: rounds never call `outcome()` (see part 5).

Note: the `measure initiative i1 was refused` line in stderr (cases one, two, object, PARTIAL) comes from the stand-in's session.json having no usage figures; a stub artifact, not a finding. It appears because no work-item exists, so `all()` is vacuously true (`run`).

## 3. Old assumptions

Requirement r69 makes a capability-proposal rest in `awaiting-answer` after a real run. Places that assume a proposal is never awaiting-answer, or that only work-items wait on the person:

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/model_work.py:11` STATUSES["capability-proposal"] | lists drafted, approved, merged, formulated, withdrawn: no awaiting-answer | `model check` reports the proposal (run: `status 'awaiting-answer' is not one of approved, drafted, formulated, merged, withdrawn`, D3). Needs awaiting-answer added | none by search: no test asserts awaiting-answer is invalid for a proposal | run of `model check` on the probe repo; grep "capability-proposal" in model_work.py |
| `scripts/supervise.py:run` lines 210-220 | prints and computes exit from `self.items()`, which yields work-items only (`workqueue.py:105-110`) | a waiting proposal is neither printed nor counted: exit 0, empty stdout (run, D2) | none by search for the proposal case; the r81 outline row `capability-proposal p1 \| awaiting-answer` (feature 1041) would exercise it, not run here | run (one question case); read of `items()` |
| `scripts/supervise.py:187-190` run's answers, rounds, draft order | answers() runs before rounds(), once per run | a proposal reaches awaiting-answer during the run, so the next run's answers() picks its questions (r77-r78) | by search: `supervision_delegation_steps.py` builds p1 awaiting-answer by hand | read |
| `scripts/supervise_answers.py:53-58` | takes work-items and capability-proposals that are awaiting-answer | now reached by real runs, not only by hand-written fixtures | by search: `supervision_delegation_steps.py` (hand-written p1) | grep "awaiting-answer" |
| `scripts/supervise_rounds.py:31-32` `due()` | awaiting-answer proposal is due for apply when Answers >= Questions, zero included | with no question the apply round starts with no answer from the person (D1) | none: no test gives a gate zero questions | run (no-questions case) |
| `scripts/supervise_rounds.py:64` gate question text | non-string questions are json.dumps-ed | a gate that gives objects is written as JSON text (run, object case) | none by search | read + run |
| `scripts/workqueue_status.py:47` | reads questions past answers for awaiting-answer items | a proposal's gate questions now appear here after a real run | by search: work-queue status scenarios use hand-written work-items | read |

## 4. Tests the requirements make impossible to keep

`tools tests-of` has no map, so this list is `by search`. Search: tests asserting that a proposal is never awaiting-answer, or that the gate round leaves a proposal drafted: none found (grep for `awaiting-answer` and `capability-proposal` in `tests/`). Scenarios that build a proposal awaiting-answer by hand (`supervision_rounds_steps.py:17`, `supervision_delegation_steps.py:23`, `work_queue_answer_steps.py:19`) set it directly and do not depend on the gate's transition. The r85 scenario that writes gate questions to `## Questions` (feature 1014) is not collected under this `--work-item w152` environment, so it was not run; its binding (`gate_result`) is in the same state as the r69 Given.
Result: none of the existing tests can no longer pass because of r69. The accepted scenario fails only at its own undefined step.

## 5. A step the work-item skips

The gate path goes through `round()` and `move()`, not `stage()`. Steps the work-items' stage path has that the round path does not:
- `outcome(agent, data, failure)` (`supervise_worker.py`; called at `supervise.py` `stage`, line 164): maps a non-DONE result to a question for work-items (r5). `round()` does not call it. Effect (run): a PARTIAL gate result with questions goes to awaiting-answer, exit 0 (D4). Only a worker failure (`failure`) stops a round (run: no result, not-JSON, D-probes above).
- Check that the round's questions are a list (`supervise_worker.py:207`): run in the not-JSON-questions case? Not probed; `read`: the string/list check applies to the round's worker too.
- `move()` writes the status (`workqueue.move`) and then the questions by `section()`, not in one write. Read: a failure between the two leaves awaiting-answer with no `## Questions`; no probe.

## 6. Defects

D1. A gate that gives no question moves the proposal through apply and formulate with no answer from the person.
- Reproduction (run, `probe_gate_run.py::test_no_questions`): plan `{"initiative-round": {"status": "DONE"}}`; `work run i1`.
- Came back: exit 3; p1 log: drafted→awaiting-answer, apply start/end, awaiting-answer→approved, formulate start/end, approved→formulated; stdout `w1 awaiting-answer` (the drafted w1 created by formulate fails its tests).
- Reading to decide: spec r70 "every question has an answer" is vacuously true with none. Both readings are for the plan.

D2. `work run i1` with only a proposal awaiting-answer exits 0 and prints nothing.
- Reproduction (run, `probe_gate_run.py::test_one_question_as_scenario_gives_it`): `work run i1` with the scenario's gate result.
- Came back: exit 0, stdout empty, p1 awaiting-answer with its question. The run prints statuses only of work-items (`supervise.py:210-214`) and counts only work-items for exit (`:218-220`). The stderr `measure initiative` line is the stub artifact in part 2.
- Reading: spec r32 and r9/r82 speak of work-items and of a no-initiative run; r81 (no-initiative run) says a `capability-proposal` awaiting-answer is an error. Whether `work run i1` should exit 3 and print the proposal is for the plan.

D3. `model check` flags a proposal that `work run` itself made awaiting-answer.
- Reproduction (run): `python3 /home/vscode/shopsystem-bdd/scripts/model --root .shop/scratch/w152-1-research/gate-runs/one_question/repo check` (after the one-question case).
- Came back: `file: .shop/work/i1/p1.md: status 'awaiting-answer' is not one of approved, drafted, formulated, merged, withdrawn`; `2 violations, 0 warnings, 1 file problems`. Note: the Scripts path is the plugin's main checkout, not this worktree; `model_work.py` there may differ from the worktree's line 11.

D4. (reading) A round's PARTIAL result with questions is taken as the gate.
- Reproduction (run, `probe_gate_run.py::test_partial_gate`): plan `{"initiative-round": {"status": "PARTIAL", "questions": ["Is it?"]}}`.
- Came back: exit 0, p1 awaiting-answer, `- Is it?` written. For work-items the same outcome makes the item awaiting-answer by r5 with no fault. Whether a PARTIAL gate should be a fault (r45 covers error and no-JSON only) is for the plan.

## 7. The file set

Required for the accepted scenario to pass (one of the two readings in part 1):
- `tests/scenarios/supervision_rounds_steps.py` (123 lines; room 177): add the binding for `the gate round gives the question "<q>" on p1, and every round ends`, questions only, no readings.
- OR `features/supervision.feature` line 860 (feature file, not a limited Python file): reword to the existing `gate_result` wording. Alternative to the step above; not both.

Changes the findings above suggest (not needed for this scenario; the plan decides):
- `scripts/model_work.py` (219 lines; room 81): add awaiting-answer to the capability-proposal STATUSES (D3). Found by: model check run; read of line 11.
- `scripts/supervise.py` (236 lines; room 64): print and exit over capability-proposals awaiting-answer (D2). Found by: run; read of `items()`.
- `scripts/supervise_rounds.py` (76 lines; room 224): zero-question guard in `due()` (D1), and the PARTIAL check if chosen (D4). Found by: run; read of lines 27-34.

Modules on the change's path, edited or not, with line counts (`wc -l`) and room under 300 (CLAUDE.md gives the 300-line limit):
- `scripts/work` (entry): not measured; read only.
- `scripts/supervise.py` 236 (room 64)
- `scripts/supervise_rounds.py` 76 (room 224)
- `scripts/supervise_worker.py` 242 (room 58)
- `scripts/supervise_answers.py` 120 (room 180)
- `scripts/workqueue.py` 286 (room 14)
- `scripts/model_work.py` 219 (room 81)
- `scripts/workqueue_status.py` 170 (room 130)
- `tests/scenarios/supervision_rounds_steps.py` 123 (room 177)
- `tests/scenarios/supervision_given.py` 250 (room 50)
- `tests/scenarios/test_supervision.py` 250 (room 50)
- `tests/scenarios/supervision_world.py` 173 (room 127)
