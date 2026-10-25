# w177 research notes

How counts were made: no coverage map exists (`tools tests-of` and `untested` answer "no map"; `tools map` runs the whole suite, which I was told not to run), so every test list below is **by search**. `tools refs` returns 0 for callers in `scripts/work` (no `.py` suffix, so not read), so the callers are **by search**. Scripts run from `/home/vscode/shopsystem-bdd/scripts` (Scripts:); the code under study is this worktree's `scripts/work`. Probes are in `.shop/scratch/w177-1-research/` (not ignored by git: see the end).

## 1. Why each accepted scenario is red today

Run: `python3 -m pytest -q -rfE --tb=short <node id>` for the eight node ids in `tests/scenarios/test_requests.py` (run, xdist on).

- r5 "the asker answering a question leaves the request's questions and line outcomes as they were and writes no resolution" (features/requests.feature:97): FAILS, `StepDefinitionNotFoundError` on Given `q1 holds the upstream's question "Which queue?" on line 1` (line 100). Missing: the Given in `tests/scenarios/requests_write_steps.py` (its `write_request` in `tests/scenarios/requests_steps.py:32` writes only `## Outcomes` and `## Resolution`), and the code: `scripts/workqueue_request.py` has no writer of `## Questions`.
- r20 "the upstream asking a question on a line in its turn writes the question in the request" (:115): FAILS, undefined When `the upstream asks the question "Which queue?" on line 1 of q1` (line 118). Missing: that When in `requests_write_steps.py`; and in code, no command: `scripts/work` argparse has no question subcommand (`work question` → "invalid choice"), and `workqueue_request.py` has no question writer.
- r21 "the asker answering a question in its turn writes the answer in the request" (:122): FAILS, undefined Given `q1 holds the upstream's question ...` (line 125). Behind it, also undefined and not yet reached: When `the asker answers that question with "..."` (:126) and Then `q1 holds the answer "..." to the question "..."` (:127). Code: no answer writer; `scripts/work answer` is the work-item command (`workqueue_answer.py`) and refuses `q1` (probe 2).
- r4 "outcome writing a line outcome leaves the request's lines and answers as the asker wrote them" (:79): FAILS, undefined Given with question and answer (line 82). Not yet reached: Then `q1's answers are as they were` (:85), undefined.
- r12 "a change to a request commits the request on the current branch" (:217): FAILS, undefined When `the upstream asks the question "Which queue?" on line 1 of q1` (line 221). The commit side already exists (`workqueue_request._change` → `workqueue.committed`).
- Deprecated, retired by the Retires list: r4 (:71), r5 (:88), r12 (:207) PASS today.
- Thens `q1 holds the question ...`, `q1 holds the answer ...`, `q1's questions are as they were`, `q1's answers are as they were`: not defined (read: grep of tests for "holds", "questions are as they were", "answers are as they were" finds none).

## 2. What the system answers today

Probes (`run`), file `.shop/scratch/w177-1-research/probe_requests.py` and `probe_turn.py`, `python3 -m pytest -q -n0 -s <path>`. Repos are git repos made under the scratch directory, with `spec/index.md` for `bounded-context/ex.com/prod/ctx`.

1. `test_baseline_outcome_and_turn` (the r4/r5/r15/r16/r12 Givens and Whens that exist):
   - `work request "Show the queue" --from ctx-a --lines <2 EARS lines> --source o1` → rc 0, prints `q1`; commit `work request: q1`.
   - `work outcome q1 2 accepted` (upstream turn) → rc 0; `## Outcomes` = `2. accepted`; Lines untouched; commit `work outcome: q1`.
   - `work turn q1` → rc 0; `status: awaiting-asker`, `turn: asker`; commit `work turn: q1`.
   - `work outcome q1 1 accepted` (asker turn) → rc 1, "q1 is in the asker's turn; the upstream writes a line outcome only in its own turn", nothing changes.
2. `test_no_question_or_answer_command`:
   - `work question q1 1 "Which queue?"` → rc 2, argparse "invalid choice: 'question'".
   - `work answer q1 "The work queue"` → rc 1, "q1 is not awaiting-answer; work answer answers only an awaiting-answer work-item or capability-proposal". The name is taken by the work-item command.
3. `test_hand_written_questions_survive_commands` (the nearest case of r4/r5/r21 scenarios: the store already holds a question and an answer, written by hand in the form `model` accepts):
   - `work outcome q1 2 accepted` (upstream turn) → rc 0; `## Questions` and `## Answers` left exactly as written.
   - `work turn q1` → rc 0; Questions and Answers left as written.
   - `work outcome q1 1 accepted` (asker turn) → rc 1, refused.
   - `git status --porcelain` clean after.
4. `test_edge_cases` (the scenario's own data empty, the line absent, the value odd):
   - `work request "Empty" ... --lines <empty file>` → rc 0; request with empty `## Lines`. Then `work turn q1` → rc 0, `status: refused`, `turn: asker`.
   - `work outcome q2 5 accepted` on a two-line request → rc 0; `## Outcomes` holds `5. accepted`.
   - `work outcome q2 1 banana` → rc 0; the word is written.
   - `work request ... --delegation ""` → rc 0; `delegation: ""` in the frontmatter.
5. `probe_turn.py::test_turn_run_out_of_turn`: `work turn q1` run while the turn is the upstream's → rc 0; status `awaiting-asker`, turn `asker`. The turn passed to the asker with no outcome written. Then `work outcome q1 1 accepted` → refused (asker's turn).

Read (not run): `workqueue_request.outcome` checks only `turn == asker`, so the upstream check is the field, not the side that runs it. No command takes a side argument (read of `scripts/work` and `workqueue_request.py`), so "the asker answers in its turn" can only be checked by the field.

## 3. Old assumptions

Requirements r4, r5, r12 (their new forms), r20, r21 change what writes a request's parts. The table lists places that rely on the old form, where the old form is: `work` writes the upstream's part only through `outcome` and `resolve`; the asker's part only through `request`; `turn` writes status and turn only.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_request.py:outcome | writes `## Outcomes` only; refuses only when `turn == asker` (no side argument) | r16: a question and an answer need the same turn test, on the field, with no side given | tests/scenarios/test_requests.py (r15, r16, r4 deprecated); tests/scenarios/supervision_intake_steps.py (via `work outcome` in an intake round) | by search |
| scripts/workqueue_request.py:turn | rewrites status and turn; passes the turn whoever runs it (probe 5) | r7/r16: out-of-turn `turn` is a reading question, see Defects D4 | tests/scenarios/test_requests.py (r7, r17, r18, r8, r9); supervision_intake_steps.py | by search |
| scripts/workqueue_request.py:request (template) | writes `## Lines`, `## Outcomes`, `## Resolution` only | the new writers must add `## Questions` and `## Answers`, and `model` already accepts them (scripts/model_requests.py SECTIONS) | tests/scenarios/requests_write_steps.py (all `request` scenarios); tests/scenarios/requests_steps.py:write_request | by search |
| scripts/workqueue_request.py:_numbered / _with_entries | one entry per number, a second write to a number replaces the first | r20 keys a question by line; r21 answers the n-th question by its n: two questions on one line would overwrite | none (no test writes two entries to one number) | by search |
| scripts/workqueue_request.py:_change → workqueue.committed | commits the file only, on the current branch; resets on failure | r12: question and answer writers must go through it; today only four commands do | tests/scenarios/work_queue_git_steps.py (r12 scenarios, via the four commands) | by search |
| scripts/workqueue_request.py:accepted_lines | reads `## Outcomes` and `## Lines` only | unaffected by Questions/Answers | tests/scenarios/supervision_rounds_steps.py:120, supervision_integrate_steps.py:52 (requests with Outcomes) | by search |
| scripts/model_requests.py:request_form | accepts Questions and Answers already | none needed | none (no test has a request with Questions) | by search |
| scripts/supervise_intake.py:brief (lines 60-62) | tells the intake session to write `outcome <n> question` and to put the question's text in its result's `questions`; nothing writes that text to the request | r20: an upstream question is written by `work` in `## Questions`; this route bypasses it | none (tests/scenarios/supervision_intake_steps.py has no `question`) | by search |
| scripts/work: answer (workqueue_answer.py) | answers work-items only; `work answer q1` refuses | a request answer under the same word is a name clash for the planner | tests/scenarios/work_queue_answer_steps.py (work-item answers) | by search |

## 4. Tests the requirements make impossible to keep

By search (no coverage map). Searched tests for `work outcome|turn|resolve|request|answer`, `Outcomes|Questions|Answers|## Resolution`, `requests/q` and the request step modules.

- tests/scenarios/test_requests.py: three scenarios pass today and are retired by the Retires list (r4 :71, r5 :88, r12 :207). They still pass on the new requirements too, so they are removed, not made impossible. Verified by run (section 1).
- tests/scenarios/requests_write_steps.py, requests_steps.py, requests_show_steps.py, work_queue_git_steps.py: their Thens (`lines are as they were`, `gives line n`, `has no resolution`, `is as it was`) hold under the new forms: none can no longer pass. Read.
- tests/scenarios/supervision_intake_steps.py:21-39: drives `work outcome` with accepted/refused and `work turn`. Unchanged by w177. Read.
- tests/scenarios/supervision_rounds_steps.py:120, supervision_integrate_steps.py:52, design_model_check_requests.py: requests with `## Outcomes` and `## Resolution`. Unchanged. Read.
- No test asserts that a request has no Questions or Answers section, or that a turn command writes nothing. none.

## 5. A step the work-item skips

The question and answer writers are new paths. The existing path (`outcome`) goes through steps the new ones must also take:

- Turn test: `outcome` refuses in the asker's turn (probe 1, `run`). `resolve` has no turn test (by design, r10). The new writers need `question` refused in the asker's turn, and `answer` refused in the upstream's turn (r16). Read: the existing check only refuses on `asker`, so an `answer` written in an upstream turn is not refused by any rule that exists.
- Request lookup: `path_of` refuses an unknown request (`there is no request ... under .shop/work/requests`). Read; `work outcome q9` not run.
- Line existence: `outcome` does not check that line n exists (probe 4, `run`: `5. accepted` written). A question on a missing line would land the same way. (Defect D1.)
- Commit: `_change` → `workqueue.committed`: `git rev-parse` before any write, commit of only the file, reset on a failed commit (read, `workqueue.py:264`). Effect only that step produces: the commit (probe 1, `run`: `work outcome: q1` in the log). A non-git directory: refused before writing (read; not probed, since a probe there would sit inside the worktree's own git repository).
- Answer numbering: `answer` must find the question it answers (r21, "the n-th answering the n-th"); nothing today reads a question. Read.

## 6. Defects

Each is `run` (probe 4 or 5 unless noted).

- D1 — `work outcome q2 5 accepted` on a two-line request → rc 0, writes `5. accepted` to `## Outcomes`. Repro: `work request ... --lines <2 lines> --source o1`, then `work outcome q2 5 accepted`.
- D2 — `work request ... --lines <empty file>` → rc 0, a request with no lines. Then `work turn q1` by the upstream → rc 0, `status: refused` (every line of none is settled, `all()` on nothing). Repro: empty lines file, `work request`, `work turn q1`. Reading of "should refuse" is the plan's; the spec's r1 does not say a request needs a line.
- D3 — `work request ... --delegation ""` → rc 0, `delegation: ""` written. Against r22 (current spec): "If the delegation given to `work request` is empty, then `work request` shall refuse". r22 is not in w177's accepted set; reported because it is wrong today.
- D4 — reading needed: `work turn q1` run while the turn is the upstream's → turn goes to the asker, status `awaiting-asker`, nothing written (probe_turn). r7 literal: "pass the request's turn to the other side", which this does; r16 literal: refuse a command "that writes a part" in the other side's turn; the turn field is arguably part of the request. Both readings given; not judged.
- D5 — reading needed: `work outcome q2 1 banana` → rc 0, writes `1. banana`. The spec's r15 says "with the word it is given"; r17 names accepted, refused, withdrawn, question as the outcomes. Both readings given.

## 7. The file set

Production and tests the work-item must change:

- scripts/workqueue_request.py — add the question writer (turn check, line keyed, `## Questions`) and the answer writer (turn check, n-th answering n-th, `## Answers`), both through `_change`; found by sections 1 and 3.
- scripts/work — add the two subcommands (names not in the spec, see the question in the result), dispatch in `main`; found by `work --help` (probe 2) and section 2.
- tests/scenarios/requests_write_steps.py — the Givens (`holds the upstream's question`, `and the asker's answer ... to it`), the Whens (`the upstream asks the question`, `the asker answers that question with`) and the Thens (`holds the question`, `holds the answer`, `questions are as they were`, `answers are as they were`); found by section 1.
- tests/scenarios/requests_steps.py — `write_request` writes `## Questions` and `## Answers` when given; found by section 1 (its template writes only Outcomes and Resolution).
- features/requests.feature — remove the three deprecated scenarios (:70, :87, :206) per the Retires list; found by the Retires section of the work-item.

Affected, not in the file set unless the plan decides: scripts/supervise_intake.py (brief, lines 60-62: the `question` outcome route, section 3); no test requires its change.

Module path, with lines (`wc -l`) and room to 300:

| file | lines | room | change |
|---|---|---|---|
| scripts/workqueue_request.py | 144 | 156 | edited |
| scripts/work | 151 | 149 | edited |
| tests/scenarios/requests_write_steps.py | 122 | 178 | edited |
| tests/scenarios/requests_steps.py | 108 | 192 | edited |
| features/requests.feature | not Python | — | edited |
| scripts/workqueue.py | 290 | 10 | not edited (committed, read) |
| scripts/model_requests.py | 63 | 237 | not edited (accepts the form) |
| scripts/supervise_intake.py | 112 | 188 | not edited (section 3) |
| tests/scenarios/test_requests.py | 9 | 291 | not edited |

`tools size --limit 300` (run from the plugin's scripts): no file over the limit.

Scratch: `.shop/scratch/w177-1-research/` holds two probes, `repos/` (nested git repos from probes), `lines_*.md`, `plain`-less. It is inside the worktree and not ignored by git as far as I know; I could not delete it from my shell.
