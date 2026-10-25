# research of w178

Tools: `python3 /home/vscode/shopsystem-bdd/scripts/tools` (the brief's Scripts line). `refs` used for names. `tests-of` and `untested`: no map, `tools map` not run, so test lists are `by search`. `size`: no file over 300.
Accepts supervision r100, r101, r9, r67, r82. Retires the three @deprecated scenarios (r9, r67, r82).
Probe files: `.shop/scratch/w178-1-research/` (probe_r101.py, probe_r101b.py, probe_outcome.py; git-ignored, left for `work run`).

## 1. Why each scenario is red today

Command for all: `python3 -m pytest -q -n 0 --tb=short "<node id>"` on tests/scenarios/test_supervision.py (node ids from `--collect-only -k supervision`). Result: 6 failed, 4 passed.

- r9 new (supervision.feature:217, test_when_every_workitem..._in_the_askers_turn_...): fails at Given line 220 "a request q2 whose asker is this context, awaiting-upstream, its turn the upstream's": StepDefinitionNotFoundError. Missing: a Given writing a request with asker `internal` in `.shop/work/requests/`. Code: none needed for exit 0 (supervise.py:230-232 already returns 0 when all green/withdrawn). Rest of scenario not reached (Then steps line 222-223 exist: test_supervision.py:193, :103).
- r82 new (supervision.feature:1282): same Given, line 1287. Code: supervise_all.py:84 returns 0 with no node waiting; the Given is the only red cause.
- r101 (supervision.feature:226): fails at Given line 229 "a request q2 kept in this context whose asker is this context, awaiting-asker, its turn the asker's, with the question ... and no answer": undefined. Also undefined by read: Then line 231 "`work run` prints q2 with the question "..."" (no pattern in tests/scenarios matches `prints <name> with the question`; test_supervision.py:184 needs "with <status> and the question"). Code: `it exits with an error` (test_supervision.py:108) would fail: supervise.py:191-197 (`run`) and :230-232 (`show`) never read requests, so exit is 0 for green items.
- r67 new outline (supervision.feature:887, [open] and [awaiting-upstream]): fails at Given line 891 "the intake round writes a line outcome for q1's line 1, gives a question on q1's line 2 and passes the turn with `work turn`": undefined (supervision_intake_steps.py:21 defines only the all-lines variant). By read, Then line 893 "an `initiative-round` session of the kind intake was started, given q1, its brief asking ..." does not match intake_started (supervision_intake_steps.py:28, exact text); Then line 894 "q1's line 1 has a line outcome, and q1's turn is its asker's" is undefined. Code: the brief already asks for the question form (supervise_intake.py:59-70), so the brief wording is met once the steps exist.
- r100 (supervision.feature:901): fails at Given line 905 "the intake round writes a line outcome for q1's line 1, gives the question "Which unit is the limit in?" on q1's line 2 and passes the turn with `work turn`": undefined. Then line 907 "q1 holds the question ... on its line 2": undefined (by read). Code: supervise_intake.py:86-101 (`take`) never reads the round's `questions`; scripts/work has no question command (see probe 3).
- Deprecated, retired (pass today): test_when_every_workitem..._deprecated, test_a_request..._deprecated[open], [awaiting-upstream], test_work_run_started_with_no_initiative..._deprecated: 4 passed.

## 2. What the system answers today

Probes run with `python3 -m pytest -q -s -n 0 -p no:warnings <file>`; each repository built under the scratch directory. The worker env var SHOPSYSTEM_WORK_RUN_WORKER is stripped (inherited it refused the run, rc 1, "started by a worker of another `work run`").

Probe 1, `work run` with no initiative, one request `q2` (asker internal, status awaiting-asker, turn asker, one question under ## Questions), no initiatives. Command: `python3 scripts/work run` (probe_r101.py::test_run_with_asker_turn_request_no_initiative). Came back: rc=0, stdout empty, stderr empty. Run. Shows the r82 new and r101 cases: the request is not named and the exit is success.

Probe 2, `work run i1`, w1 awaiting-answer with `## Questions` "Which module owns the log?", same request in asker's turn (probe_r101b.py). Came back: rc=3, stdout `w1 awaiting-answer` and `  - Which module owns the log?`; the request is not printed. Run.

Probe 3, `work` request commands (probe_r101.py::test_work_question_command_and_outcome_word, probe_outcome.py). Came back:
- `work question q1 2 "Which unit?"`: rc=2, "invalid choice: 'question'" (no such command; the subcommand list is add, show, withdraw, run, retry, answer, note, status, request, outcome, turn, resolve, start).
- `work outcome q1 1 accepted`, then `work outcome q1 2 question`, then `work turn q1` (request open, upstream's turn): each rc=0; q1 status becomes `awaiting-asker`, turn `asker`.
- `work outcome q1 2 bogus`: rc=0, lands `2. bogus`.
- `work outcome q1 9 accepted` on a two-line request: rc=0, lands `9. accepted` under ## Outcomes.

Read (not run): r101 nearest cases (asker in the upstream's turn; no `## Answers` section at all) — the same code path, no probe.

Read: the intake round's line outcome `question` path (supervise_intake.py:60-62) ends the round with `work turn`, which sets `awaiting-asker` (workqueue_request.py:109-121, probe 3 confirms), and nothing writes the question text anywhere in the request.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise.py:Run.show (219-232) | exit 0 when every work-item is green or withdrawn; nothing else decides | r9 and r101: also no request whose asker is this context is in the asker's turn; else error naming it | by search: test_supervision.py r9, r9 deprecated, r32, r52, r101 scenarios | refs (`show`, 1 production ref, supervise.py:197); read |
| scripts/supervise.py:Run.run (191-197) | checks, pushes, pulls, shows; no request read | r101: every end of a run checks the requests kept here | by search: all test_supervision.py scenarios that call `work run` | read |
| scripts/supervise_all.py:run_all (27-84), exit at 82-84 | exit 1 on refused or failed, 3 on awaiting-answer, else 0 | r82 and r101: a request in the asker's turn makes it not 0 and prints it | by search: test_supervision.py no-initiative scenarios (r81, r82, r82 deprecated) | read |
| scripts/supervise_intake.py:Intake.take (86-101) | on DONE merges the round branch and keeps the directory; `questions` in the result is never read | r100: writes each question of the result into the request, on its line | by search: test_supervision.py r67 deprecated, r67 (the intake Givens) | read |
| scripts/supervise_intake.py:brief (50-71) | tells the round to write line outcome `question` and give the text in `questions` | requests r5, r20 put a question under `## Questions`, not in Outcomes; r100 writes it; the brief's pass of the turn (62) sets the turn before work run writes | by search: supervision_intake_steps.py:intake_started (28-32) | read |
| scripts/workqueue_request.py:outcome (100-106) | writes any word for any line number; refuses only in the asker's turn | `question` as a line outcome is the state requests r17, r18 test (features/requests.feature:160, :165); a line number that is absent lands (defect D1) | by search: requests_steps (r15, r17, r18 scenarios) | probe 3 |
| scripts/workqueue_request.py:turn (109-122) | any Outcomes word outside accepted, refused, withdrawn sets awaiting-asker | the only effect that turns a question into awaiting-asker; r101 reads the same status | by search: requests r17, r18 scenarios | probe 3, read |
| scripts/workqueue.py:requests (113-120) | yields (name, status, turn, source); no asker | r101 and r9/r82 need each request's asker; callers take a 4-tuple | by search: supervise_intake.py:due, supervise_all.py:unfulfilled, workqueue_status and measure_read callers | refs (`requests`: 8 refs, 1 production file outside supervise) |
| scripts/workqueue_done.py:condition (35) | asker in (internal, context path without prefix) | r101 "this context's id": same rule, if it is this form | by search: work-queue.feature delivered scenarios | read |
| scripts/measure_read.py:asker check (71) | asker == internal or "bounded-context/" + context path | a second reading of "this context's id" (prefixed form); differs from workqueue_done.py:35 | by search: batch-measurement scenarios | read |

## 4. Tests the requirements make impossible to keep

`tests-of` unavailable (no map), so `by search` throughout.

- The four deprecated scenarios (test_supervision.py: r9 deprecated, r67 deprecated [open] and [awaiting-upstream], r82 deprecated): retired by this work-item. Today they pass. Under the change: r9 deprecated and r82 deprecated still pass (no asker-turn request); r67 deprecated still passes because its Then steps do not assert the exit, though its request is left in the asker's turn (see C3).
- Searched for any test expecting exit 0 with a request in the asker's turn: `awaiting-asker` and `turn: asker` appear in tests/scenarios only in requests and batch-measurement steps and in the new r101 Given; none runs `work run`. So no test of the old exit is broken.
- Verified sound: test_supervision.py:103 exits_successfully (asserts rc 0) for r9 new and r82 new, which have no asker-turn request.
- Verified sound: supervision_intake_steps.py:28-32 intake_started (checks "# intake of q1", "Kind: intake" and the request in the brief): the brief already has them (supervise_intake.py:58).
- Verified sound: supervision_intake_steps.py:35-40 lines_have_outcomes (asserts turn asker): no change needed.
- Requests scenarios r15, r17, r18 (features/requests.feature:106-167): unaffected unless `outcome` is changed to refuse a word or a line number (see D1, D2).

## 5. A step the work-item skips

- The question write in the existing way is `work`'s request command (requests r20, r12), which commits on the current branch through workqueue.committed (workqueue.py:264-280) and is refused in the other side's turn (workqueue_request.py:103-104, read). The intake round passes its own turn (brief line 62) before the session ends. So a question write made by `work run` after the merge is in the asker's turn: refused by that step's own rule (requests r16) unless the write happens before the turn (C1). Read.
- Effect only `turn` produces: status `awaiting-asker` and turn `asker` (probe 3). The intake's question path would reach this through the `outcome question` word, not through `## Questions`. Probe 3.
- Lock and push: Intake.take holds the run lock only around the merge (supervise_intake.py:87-89); keep() commits and pushes the stage directory and log (supervise_intake.py:103-112). A question write would be a second commit on the checkout with no lock and no push unless added. Read.

## 6. Defects

D1. `work outcome` writes a line number the request does not have.
Commands (probe_outcome.py::test_outcome_line_that_does_not_exist): a request with two lines, `work outcome q1 9 accepted`. Came back: rc=0; `## Outcomes` holds `9. accepted`. Run. Reading: requests r15 names "line n" and no refusal; shown as a defect on the brief's definition (something landing that should be refused), reading-dependent.

D2. `work outcome` writes any word.
Commands (probe_r101.py::test_work_question_command_and_outcome_word): `work outcome q1 2 bogus`. Came back: rc=0; `2. bogus` written. Run. Reading-dependent: requests r17 implies other words exist; the intake brief names three.

## 7. The file set

Production:
- scripts/supervise.py (248 lines, room 52): run and show check open requests in the asker's turn (r101, r9).
- scripts/supervise_all.py (84, room 216): run_all exit and print of the request (r82, r101).
- scripts/supervise_intake.py (112, room 188): take writes each result question into the request (r100).
- scripts/workqueue_request.py (144, room 156): new question writer and open-question and asker-turn readers (r100, r101).
- scripts/work (151, room 149): new `question` subcommand (requests r20; probe 3).
- scripts/workqueue.py (290, room 10): only if requests() must yield asker; prefer a reader in workqueue_request.py.
Tests and features:
- tests/scenarios/test_supervision.py (258, room 42): import the new steps module.
- tests/scenarios/supervision_intake_steps.py (80, room 220): Givens for the question variants, or a new module.
- tests/scenarios/supervision_request_steps.py (new): Givens for asker-turn requests; Then for the printed question.
- features/supervision.feature (1338 lines): remove the three @deprecated scenarios (207-214, 872-886, 1270-1279), per Retires.

Path modules, edited or not (line count, room under 300):
- scripts/supervise_worker.py (247, room 53): base class Workers, WORKER, git.
- scripts/supervise_pool.py (143, room 157): read_delivery, pull, which Run's show follows.
- scripts/supervise_faults.py (161, room 139): Fault, fault_of.
- scripts/workqueue_status.py (170, room 130): open_names, the initiatives run_all takes.
- scripts/workqueue_done.py (67, room 233): asker rule at line 35 (reference only).
- scripts/measure_read.py (213, room 87): second asker rule at line 71 (reference only).
- tests/scenarios/supervision_world.py (173, room 127): helpers the new steps use.
- tests/scenarios/test_supervision.py (258, room 42): listed above.

No file is over 300 (`tools size --limit 300` printed nothing).

## Conflicts for the plan (both readings given)

C1. r100 timing. Supervision spec note (supervision.md:152): write the question "before the round's `work turn`". Intake brief (supervise_intake.py:62) has the round pass the turn itself, and work run only sees the result after the session. Reading A: the round writes its question itself with a new `work question` (the brief and the stage change). Reading B: work run writes the result's questions after the merge, which needs the turn still the upstream's (the brief's turn step removed).
C2. Question as line outcome or as `## Questions`. Requests r5, r20 and requests.feature:160, :165 (line outcome `question` as a state). Reading A: keep the `question` outcome as the marker and write the text under `## Questions`. Reading B: drop the marker, `turn` then sees only unsettled lines.
C3. Intake of an `internal` asker. The intake round passes the turn to the asker; the asker is internal (this context), so r101 would exit with an error in the same run. The r67 and r100 scenarios do not assert the exit. Reading A: intended; Reading B: r101 excludes requests the round just passed.
C4. "This context's id". workqueue_done.py:35 compares with the bare context path; measure_read.py:71 with "bounded-context/" + path. Reading A: one form (pick it). Reading B: accept both.
C5. The exit code of r101 when a work-item is awaiting-answer (show returns 3). r101 says "an error"; reading A: 3; Reading B: 1.

Summary of outcome: research done; no question for the person is needed (conflicts above go to the plan).
