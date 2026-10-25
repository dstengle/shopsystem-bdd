# Research of w147: answers under a request's delegation

Work-item: `.shop/work/i24-requests-and-the-context-loop/w147.md`, under `supervision`, accepts r77 and r78, blocked_by w126 (green).
Tools: `tools refs` ran on `answer` only (name-based). `tools tests-of` and `untested` have no map (`tools: no map`); `tools map` not run (it writes outside my scratch). Test lists below are `by search`. `tools size --limit 300` printed nothing (no tracked Python file over 300).

## 1. Why each scenario is red today

Command for both: `python3 -m pytest -q "<node id>"` (run, node ids from `--collect-only`). Each fails at its first Given, so the later steps were not reached.

- r77, outline, example "answers it" (`test_supervision.py::test_under_a_delegation_..._that_reply[Please get everything ...-answers it-...]`): `StepDefinitionNotFoundError` for Given `i1 fulfils the request q1, which gives the delegation "..."` (feature line 943). Missing too (by search, no step matches): `each session given a question under the delegation <reply>` (946), the Thens at 948-949 (`... was given to a session of its own, given the question, the delegation "...", <files>, and nothing else`) and `<after>` (950). Code: no delegation is read anywhere in `scripts/` (search `delegat`: none). `supervise.py` `Run.run()` has no answer pass; `pull(MOVABLE)` skips `awaiting-answer`, so no session is started for w1 or p1.
- r77, example "leaves it for the person": same first failure (Given at 943), same missing steps.
- r78 (`test_an_answer_given_by_..._naming_that_delegation`): `StepDefinitionNotFoundError` for Given at line 960. Missing: `the session answering under the delegation answers "...", and every worker gives DONE` (962) and the Then `w1's answer to "..." is "...", naming the delegation "..."` (964). Code: `scripts/workqueue_answer.py:answer` writes `- <date>: <text>` with no `by` (line 42-45), so nothing names a delegation. Nothing in `supervise*.py` writes an answer.

## 2. What the system answers today

Probe: `python3 -m pytest -q -s -n 0 .shop/scratch/w147-1-research/probe_delegation.py` (run). Scratch repos with an initiative `i1` fulfilling `q1`, and `w1` `awaiting-answer` with `## Questions` "Which module owns the log?". `SHOPSYSTEM_WORK_CLAUDE=/bin/false`, so any started worker would fault. `SHOPSYSTEM_WORK_RUN_WORKER` removed from the env (my own shell is a worker, so `work run` refuses otherwise; first probe run showed it).

- `work run i1`, request with `delegation: "Please get everything ..."` in its frontmatter: exit 3, stdout `w1 awaiting-answer` and `  - Which module owns the log?`, no session, no commit. Same as the no-delegation request (exit 3, same output). Delegation ignored.
- `work answer w1 "The queue module."` on the same repo: exit 0, prints `w1 researched`; w1.md gets `## Answers` / `- 2026-10-25: The queue module.`; commit `work answer: w1 awaiting-answer -> researched`. No `by`, the status returns to the asking stage (`workqueue_answer.asked_from`).
- Nearest cases not probed: a request with a `## Delegation` section (model's `request_form` refuses any `##` section outside `Lines, Outcomes, Questions, Answers, Resolution` — `scripts/model_requests.py` SECTIONS, read); a request file whose delegation is a block scalar (read: `model_facts.unread` only reports it). A request with two questions and one answered: read only.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_answer.py:answer (24-52) | writes `- <date>: <text>`, moves to the asking status, logs `by="work answer"` | r78 needs an answer given under a delegation to name it (`by`); the line format has no place for it | tests/scenarios/work_queue_answer_steps.py:35-41 asserts the exact `- <date>: <text>` line (by search) | refs answer; read |
| scripts/supervise.py:Run.run (the sequence rounds, draft, pull) | no pass that answers questions; `pull(MOVABLE)` skips awaiting-answer | r77 needs a pass that, for each unanswered question of an initiative whose request gives a delegation, starts one session | none, no test drives an answer session (by search for `delegat`: none) | read |
| scripts/supervise.py:held / questions (lines 170-184) | counts `## Answers` bullets against `## Questions` (r32) | a session's answer must be a bullet in the same position, or a question stays open | tests/scenarios/supervision_answers_steps.py, test_supervision.py:220-229 (by search) | read |
| scripts/supervise_rounds.py:due (lines 25-35) | an awaiting-answer proposal is due when Answers ≥ Questions | a delegation answer counts as answered and starts apply (r70); a "leaves it" answer must not | tests/scenarios/supervision_rounds_steps.py (by search) | read |
| scripts/supervise_brief.py:answer_lines (58-67) | writes each answer into a brief as `  Answer: <text>`, dropping the leading `- ` | a delegation answer reaches later briefs with its `by` text, or the brief strips it | tests/scenarios/supervision_answers_steps.py:briefs_hold_answers (by search) | refs answer; read |
| scripts/model_requests.py:request_form (SECTIONS, 43-63) | refuses any `##` section not in SECTIONS; frontmatter keys unchecked | where the delegation is written is not given by any requirement; a section would be refused by `model` | none (by search: no test of `delegation`) | read |
| scripts/workqueue_request.py:request (60-78) | writes id, kind, asker, origin, status, turn and sections; takes no delegation | nothing writes a delegation; the Givens write it directly | none found (by search) | read |
| scripts/workqueue.py:requests (113-120) | reads name, status, turn, source of each request | not a delegation reader | none (by search) | read |

Requirement gap (not a conflict): spec/capabilities/requests.md has no line that says how a request gives a delegation (search `delegat` in spec/: only supervision.md, spec-integration.md and decisions). The plan needs one.

## 4. Tests the requirements make impossible to keep

By search (no map). Read and found sound:
- tests/scenarios/supervision_answers_steps.py and test_supervision.py:220-229 (`sections` step): assert `Answers == ["- " + answer]`. Fixture-written, so a change to the person's line format breaks them only if the code writes the format. Passes today (not run).
- tests/scenarios/work_queue_answer_steps.py:35-41: exact `- <date>: <text>`. Keeps passing if a person's `work answer` keeps the format, so a delegation's `by` must be a separate form, not a change to this one. Passes today (not run).
- tests/scenarios/supervision_rounds_steps.py: apply and formulate rounds after answers. Not affected unless due() changes.
No test is impossible to keep by the requirements, as far as the search shows. Not run: the list is by search.

## 5. A step the work-item skips

- The path that starts an answer session must go through the same verifications as any worker: r35 (verify push before a worker starts) and r46 (`.shop/work/` uncommitted check in `check()`, supervise.py). Read in supervise.py `check` and spec r35/r46. A session started outside `worker()` would skip both. Not probed.
- A person's `work answer` writes and commits through `workqueue.committed` and moves through `workqueue.move(by="work answer")`. A delegated answer written by work run must go through `self.move` and `self.commit` (which push, r38), or the answer is not pushed. Read: supervise.py move/commit; not checked: whether `workqueue.committed` pushes (not read).
- r77 says the session is given "the question, the delegation, and the files it names, and nothing else". The mandatory brief lines (r11 plugin dir, r17 never change directory, r25 worktree and scripts, r44 result file first) would be in that brief too. Conflict: the requirement's "nothing else" against r11/r17/r25/r44. Both readings: (a) the answer session's brief holds only the question, the delegation and the two files, plus the worker's required lines; (b) it holds nothing beyond those lines. Not decided here.

## 6. Defects

None found by probe. `work run` with an awaiting-answer item and no answer: exit 3, prints the question (probe above, run). `work answer` on a work-item moves it back to its asking status (probe, run).

## 7. The file set

Production (must change for r77, r78):
- scripts/supervise.py: `Run.run` gets an answer pass before `pull`; `MOVABLE` stays. 234 lines, room 66.
- scripts/workqueue_answer.py: writing a delegation answer with its `by` (a form separate from the person's). 53 lines, room 247.
- scripts/supervise_brief.py: `answer_lines` shows the `by` text beside the answer. 115 lines, room 185.
- scripts/supervise_rounds.py: `due()` counts the answers as they are (no change expected; read). 74 lines, room 226.
- new module (the answer sessions, a concern not in the module map): e.g. scripts/supervise_answers.py. CLAUDE.md requires a module map row. Size: new.
- scripts/model_requests.py: only if the request's delegation is written as a `## Delegation` section (then SECTIONS gets it). 63 lines, room 237.
- scripts/workqueue_request.py: only if `work request` takes a delegation. 131 lines, room 169.
- scripts/workqueue.py is on the path only if `requests` reads the delegation: 286 lines, room 14 (tight).

Tests (new steps for the two scenarios, and the Given that writes the delegation):
- tests/scenarios/: a new module for the r77/r78 steps (e.g. supervision_delegation_steps.py, new). test_supervision.py (249 lines, room 51) imports step modules; add an import there if it lists them. Not checked how it registers modules (read: test_supervision.py not read in full).
- tests/scenarios/supervision_given.py (250 lines, room 50) and supervision_then_workers.py (279 lines, room 21) are on the path for the stand-in's plan (`fields` for the answer); changes there would be tight.
- tests/scripts/stub_claude.py (258 lines, room 42): the stand-in's `fields` writes the answer; no change expected.

Path modules, unchanged: scripts/supervise_pool.py (142, room 158; pull is defined by the Pool class, not read), scripts/supervise_worker.py (238, room 62; `worker()` used for the session, read by name), scripts/work (entry, dispatch only).

Sizes from `wc -l` (or `tools size`, which printed nothing over 300).
