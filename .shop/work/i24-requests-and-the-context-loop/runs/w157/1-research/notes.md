# research of w157 (supervision r77, branch review 1 F1)

Search: no coverage map (`tools tests-of` says "no map"); `tools refs` gave 0 references for `Answers.answers`, so callers and tests are `by search` / `read`. Probes in `.shop/scratch/w157-1-research/` (`probe_answers.py`, `probe_more.py`), run by `python3 -m pytest -q -s -n 0`. Git status clean after the run.

Accepted scenarios: `features/supervision.feature` L971 (Outline, 2 examples) and L988 (two questions).

## 1. Why each scenario is red today

- **Outline, `answers it` / `leaves it for the person`** (L971): `python3 -m pytest -q "<id>"`, both examples: **passed** (run). Green today; not red.
- **Two questions on one work-item** (L988): `python3 -m pytest -q --tb=short "tests/scenarios/test_supervision.py::test_under_a_delegation_a_workitem_with_two_questions_has_each_given_to_a_session_of_its_own_and_both_answers_stay_written_when_the_run_ends"` → **failed**, `StepDefinitionNotFoundError` at L991, the Given `its ## Questions section with "A" and "B", each with no answer`. Step missing: `tests/scenarios/supervision_answers_steps.py` has only the variant with `and its Answers section` (L16); `supervision_delegation_steps.py` L23 takes one question.
- Steps after L991 are also missing (`read`: no pattern matches; pytest-bdd stops at the first):
  - L992 Given `the session given "Q" under the delegation answers "A", the session given "Q2" answers "A2", and every round ends and every worker gives DONE` — no definition (`supervision_delegation_steps.py` L39–52 cover only one question).
  - L994 and L995 Then `"<quoted question>" was given to (a|another) session of its own, ..., <files>, and nothing else` — `given_only` / `question_given` (`supervision_delegation_steps.py` L104–117) match only the names `w1|p1`.
  - L996 Then `w1's answer to "Q" is "A", naming the delegation` — defined (`supervision_delegation_steps.py` L137).
- Behaviour missing, shown by probe (below): even with the steps, the scenario fails at the exit: the first answer is reverted when the second session ends (`supervise_faults.py:checkout_changes` via `supervise_worker.py:185`). Exit 1, no answer written.

## 2. What the system answers today

Probes run through `scripts/work run i1` with the stand-in claude (`tests/scripts/stub_claude.py`), as the scenarios do. Set-up: initiative `i1` fulfils `q1` with the delegation text; `w1` awaiting-answer; `delegation-answerer` plan entry set per probe.

- P1 `probe_answers.py::test_two_questions` (w1 with Q1 "Does scripts/log.py own the log?" and Q2 "Is a title given twice in features/books.feature one book or two?", stub answers "Yes." to each). **run.** Exit 1. stderr: `work: the session answering w1's question faulted: while its answerer worked, .shop/work/i1/w1.md changed in the repository's own checkout and not committed; work run put it back`. Two answer sessions started (`1-answer`, `2-answer`); `w1.md` ends with no `## Answers`. Log/commit: `work: w1 answer round 2-answer faulted`. Status `awaiting-answer` (the run's `keep_round` commit).
- P2 `probe_answers.py::test_one_question_control` (one question). **run.** Exit 0, `w1` green, `## Answers` = `2026-10-25: Yes.` with `by: work run, under the delegation "..."`. The answer is in the commit `work: w1 done -> green`. stderr also says `measure initiative i1 was refused ... session.json is not a session.json of a shape measure knows`: the stub's `session.json` has no usage figures (stub artefact, `read` that it is the stub).
- P3 `probe_more.py::test_two_questions_none_covered` (delegation-answerer gives DONE with no answer). **run.** Exit 3; both questions unanswered; `w1` awaiting-answer; no fault. Commit `work: w1 awaiting-answer -> awaiting-answer` (from `supervise_answers.py:80`).
- P4 `probe_more.py::test_first_question_already_answered` (Q1 has committed answer "Yes, earlier.", Q2 open). **run.** One answer session (for Q2 only), no fault, `w1` green, both answers kept in `## Answers`.
- Nearest cases not probed (read): an answering session that ends at its turn limit or in error (r89, r90 scenarios, `supervise_answers.py:ask` L96–99: keep_round then Refused) — read only.

## 3. Old assumptions

The answers path writes the answer into the main checkout's work-item file and leaves it uncommitted; the next session's end assumes that the main checkout's `.shop/work/` holds only work run's own, committed, changes.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/supervise_answers.py:answers` L74–75 | `section()` writes each answer, no commit; next question's session starts with the file dirty | each answer must survive the next session's end: commit it at once, or keep it out of the check | r77 outline (run, both examples), r77 two-questions (step missing, not run), r78, r89, r90 (by search, not run) | read + probe P1 |
| `scripts/supervise_answers.py:answers` L80 | `commit(name, before, before)` only when the item is not moved (questions left) | the commit of a partly answered item comes after the sessions, too late for the next one | r77 outline `leaves it` (run), probe P3 | read + probe P3 |
| `scripts/supervise_answers.py:ask` L96–99 | a fault in the session: `keep_round`, then `Refused`; answers already written stay uncommitted | the fault must name the session, not the answers work run wrote | r89, r90 (by search, not run) | read |
| `scripts/supervise_faults.py:checkout_changes` L92–113 | every path under `.shop/work/` that differs from HEAD, other than run dirs and the own log, is put back and is a fault | an answer work run wrote is not a worker's change; this check must not revert it, and must still catch a worker's | r28 scenario (`features/supervision.feature` L576; by search, not run); every worker session | read + probe P1 |
| `scripts/supervise_worker.py:worker` L185 | calls `checkout_changes()` at every session's end, the answering session's too | the answering session's end is where the first answer is lost | every worker and answer scenario (by search) | read + probe P1 |
| `scripts/supervise.py:section` L118–131 | writes the bullet into the working file; `held()` reads the working file | answers in the working file are read by the next question's own check; the r57 brief reads them too | r57 `briefs_hold_answers` (`supervision_answers_steps.py` L24, by search, not run) | read |
| `scripts/supervise.py:commit` L96–107 | commits the item file, its run dirs and log.jsonl; then pushes | an answer commit made per answer would also push per answer (r38) | r38 push scenarios (by search, not run) | read |
| `scripts/supervise_answers.py:open_questions` L57–58 | n-th open question is the question after the answers; read once per item | unchanged by r77; the appended answer keeps the n-th rule | P4 (run) | read + probe P4 |

## 4. Tests the requirements make impossible to keep

Search (no map). Tests the change can break:
- `tests/scenarios/test_supervision.py` r28 scenario (`features/supervision.feature` L576): asserts that an uncommitted `.shop/work/` change at a worker's end is a fault and is put back. It must stay true for workers. A fix that exempts all answering-session changes would break it; an exemption limited to work run's own answers would not. Not run (by search); read as sound against the fix shape.
- Any test that counts the commits or pushes of an answered item (r38, r7): a per-answer commit adds commits and pushes. None found by search that asserts a count under delegation; not run.
- r89/r90 scenarios: they assert no answer on a cut-short session and the committed stage directory. A per-answer commit must not commit the failed session's record early. Read: consistent.
- No existing test asserts the uncommitted-answer state; the only delegation tests are the five in `supervision_delegation_steps.py` and `supervision_answers_steps.py`, and the outline passes today (run).

## 5. A step the work-item skips

The existing way writes a work-item's section and commits it in one move: `supervise.py:move` L109–116 (`section` then `commit`, which pushes, `supervise.py:commit` L96–107). The answers path writes the section and leaves the commit to later (`supervise_answers.py:answers` L74–81). Effects only the commit produces:
- the answer is in HEAD, so `checkout_changes` (`supervise_faults.py` L105–112) does not revert it (`read`, and P1 shows the revert without it);
- the push of the initiative branch (r38) after each answer (`read`);
- the commit on the initiative branch of the answered item's file, with the message `work: <name> <before> -> <after>` (`read`; P2 shows that a moved item's commit carries its answer).
- A failed push at `supervise_answers.py:81` (`self.push()`) raises `Fault`, which `answers()` does not catch; `pull_through` (`supervise.py` L200–214) has only a `finally`, so it reaches the caller (`read`, not run).

## 6. Defects

### D1. Two questions on one work-item under a delegation: the first answer is lost and the run exits 1

Reproduce (run, P1):
```
python3 -m pytest -q -s -n 0 .shop/scratch/w157-1-research/probe_answers.py::test_two_questions
```
Came back: `RETURNCODE 1`; `STDERR work: the session answering w1's question faulted: while its answerer worked, .shop/work/i1/w1.md changed in the repository's own checkout and not committed; work run put it back`. Two answer sessions started, `1-answer` and `2-answer`. `w1.md` ends with no `## Answers`; `LOG` shows `work: w1 answer round 2-answer faulted`. The same run with one question (P2) exits 0 and writes the answer. Matches branch review 1 F1 (`.shop/work/i24-requests-and-the-context-loop/runs/branch-review/1/findings.md` §F1), confirmed by the run.

### D2 (candidate, not judged): a refused `measure initiative` exits 0

P2 and P4 print `work run: measure initiative i1 was refused ...` and exit 0. Caveat: the stub writes a `session.json` without usage, so the refusal may be the stub's. Left to the plan.

## 7. The file set

Production (must change for the scenarios; each `read`, the probe in brackets):
- `scripts/supervise_answers.py` (121 lines, room 179): `answers()` commits, or otherwise keeps out of the check, each answer before the next session starts [P1, L74–81].
- `scripts/supervise_faults.py` (161, room 139): only if the fix exempts work run's own answers from `checkout_changes` rather than committing them [P1, L92–113]. The worker-facing check must keep r28.

Tests (must change for the scenario to pass):
- `tests/scenarios/supervision_delegation_steps.py` (147, room 153): add the Given for the two-question item, the Given with two sessions' answers, and the Then for a quoted question's session (two patterns; `given_only` takes a question, not a name) [pytest-bdd undefined-step output].
- `tests/scenarios/supervision_answers_steps.py` (52, room 248): alternative home for the two-question Given (`each with no answer`).
- `tests/scripts/stub_claude.py` (260, room 40): its plan answers per agent only (`fields`, L243); the scenario needs a different answer per question (`the session given Q answers A`), so the stub must pick the answer by the brief's `Question:` line.

Modules on the change's path (edited or not), with line counts (`wc -l`) and room to 300:
- `scripts/supervise.py` (247, room 53): `run`, `pull_through` (L190–216), `move`, `section`, `commit` — unchanged unless `commit` is called per answer.
- `scripts/supervise_worker.py` (247, room 53): `worker` L165–214 with `checkout_changes` at L185 — read, unchanged.
- `scripts/supervise_brief.py` (129, room 171): the r57 brief reads answers from the working file — read, unchanged.
- `scripts/workqueue.py` (286, room 14): `move`, `agrees` — unchanged.
- `scripts/workqueue_answer.py` (53, room 247): `asked_from` used when an item moves — unchanged.
- `scripts/workqueue_request.py` (142, room 158): `field`, `path_of` read the delegation — unchanged.
- `tests/scenarios/test_supervision.py` (252, room 48): binds `features/supervision.feature` by `scenarios()` — unchanged.
- `tests/scenarios/supervision_given.py` (250, room 50): `repository`, `work_items` Givens — unchanged.
- `tests/scenarios/supervision_world.py` (173, room 127): `item_text`, `section`, `starts` — unchanged.
