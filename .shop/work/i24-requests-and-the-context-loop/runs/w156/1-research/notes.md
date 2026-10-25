# w156 research notes

Scripts: `<Scripts>` = /home/vscode/shopsystem-bdd/scripts. No map exists (`tools tests-of` says "no map: make one with tools map"; not made). Every test list below is `by search`. `tools refs answers` gives 0 refs (a method name is not resolved). Probes: `.shop/scratch/1-research/probe_delegation.py`, `probe_more.py` (run with `-n0 -s`; each case in its own scratch repo; stand-in claude).

## 1. Why each scenario is red today

Neither is red. Both pass today (`run`):
- `python3 -m pytest -q "tests/scenarios/test_supervision.py::test_under_a_delegation_each_question_..._that_reply[Please get everything delivered....-answers it-...]"` → 1 passed
- same, `[Answer only the questions on the queue's tests...-leaves it for the person-...]` → 1 passed
- `python3 -m pytest -q "tests/scenarios/test_supervision.py::test_an_answer_given_by_a_session_started_under_a_delegation_is_written_naming_that_delegation"` → 1 passed

The gap is not in these scenarios: each has one node with one question, so `answers()` commits each node before the next session starts. Their Givens cannot show two questions on one node (see 6, F1).

## 2. What the system answers today (probes, all `run`)

Commands: `python3 -m pytest -n0 -s -q .shop/scratch/1-research/probe_delegation.py -k <case>` and `probe_more.py`.

- **control** (one question, one node, stand-in answers): EXIT 0, w1 `green`; `## Answers` holds `- 2026-10-25: The delegation covers it.` then `  by: work run, under the delegation "..."`. Exit 0 is the pipeline after it; `measure initiative` stderr line is a stub artefact (stub session.json has no usage), not a finding.
- **two questions, one node**: EXIT 1; stderr `work: the session answering w1's question faulted: while its answerer worked, .shop/work/i1/w1.md changed in the repository's own checkout and not committed; work run put it back`. Two answerer sessions started, then the answer for question 1 is reverted; w1.md has no `## Answers`; last commit `work: w1 answer round 2-answer faulted`. (Also in `probe_more` second run: same fault again; commits pile up; nothing kept.)
- **request gives no delegation**: EXIT 3, no answerer session, question left. Correct (`delegation()` returns None).
- **answer of two lines** (stand-in answers `first line\nsecond line`): EXIT 3, session given, nothing written, question left, no refusal printed. `work answer` refuses such a line (`workqueue_answer.py:27-28`); this path silently leaves it (`supervise_answers.py:103`).
- **first question answered by the person, second open**: EXIT 0, only the open question gets a session (`READS` shows `scripts/queue.py` only), `## Answers` keeps the person's `Earlier answer.` and adds the delegation line; w1 green.
- **awaiting-answer work-item with no `## Questions` at all**, under delegation: EXIT 0; no session; `answers()` moves it on (`supervise_answers.py:76-78`, `open_questions == []`) and the pipeline runs to `green`; no answer written. See 6, D2.
- **no log line of w1's move to awaiting-answer** (`log.jsonl` removed): EXIT 1, stderr `work: log.jsonl gives no transition of w1 to awaiting-answer; work answer has no status to return it to`. The answer IS written in w1.md, uncommitted; the answerer's stage dir and `log.jsonl` uncommitted. Second run: EXIT 1, `... are not committed; commit them before work run starts` (r46). See 6, D3.
- Not probed (`read`): a question raised by a worker later in the same run. `supervise.py:201` calls `self.answers()` once, at the start of `pull_through`, so such a question waits for the next run (supervision observation F-obs-2 in the review). Not in w156's accepted scope, but within r77's "each question of the initiative".

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/supervise_answers.py:Answers.answers` l.74 | writes each answer with `self.section`, uncommitted, then starts the next question's session | each question's session starts after its answer is kept: the write must be committed (or deferred) before the next `ask` | the two accepted scenario tests (one question per node only); two-question case: none | search (`tools tests-of` has no map); probe two questions |
| `scripts/supervise_faults.py:checkout_changes` l.92-113, called in `supervise_worker.py:worker` l.185 | puts back any uncommitted change to `.shop/work/` in the main checkout at each worker's end (r28) | a session of the same run can see its own pending answer as "changed": the answer is lost and the run stops (F1) | every worker test (not counted by map); the answer path: none for two questions | read chain l.74 → l.83-99 → worker l.185; probe |
| `scripts/supervise_brief.py:answer_lines` l.72-82 | labels every `## Answers` bullet "Answers the person gave" in later worker briefs (r57) | delegation answers are given by work run, not the person; the label is false for them | none (`grep "Answers the person gave"` in `tests/`: no hit) | search |
| `scripts/supervise_rounds.py` l.30-36 (r70 ready check: Answers count ≥ Questions) | a proposal's apply round starts once `## Answers` has as many bullets as `## Questions` | delegation answers count too, so apply starts with no person's answer. Intended by r77 or not: the requirement does not say (both readings: a person's answer only, or any answer) | not checked (no map) | read |
| `scripts/supervise_answers.py:answers` l.76-78 (work-item with no open question → `move` to asked-from status) | moves an awaiting-answer work-item with no open question back to its asked-from status, writes nothing | none of r77/r78 covers zero questions; this makes a transition with no answer | none (probe only) | read; probe no_questions |
| `scripts/supervise.py:pull_through` l.201 (`self.answers()` once) | answers only what is open at the run's start | a question raised within the run waits for the next run (F-obs-2) | the two accepted scenario tests (state set before the run) | read; review F-obs-2 |
| `scripts/supervise.py:questions` l.186-188; `scripts/workqueue_status.py` l.47 | open questions = Questions past the count of Answers | delegation answers count the same: compatible | not checked | read |
| `scripts/workqueue_answer.py:answer` `write()` l.37-46 | person's answer inserted before the next `## ` heading | the `  by:` continuation line sits in the bullet: compatible (checked on probe output) | by search: test_work_queue answer scenarios (not counted) | read; probe output |

## 4. Tests the requirements make impossible to keep

None. Searched `tests/` for `delegation`, `delegation-answerer`, `answers()`, `open_questions`, `Answers the person gave`: hits only in `tests/scenarios/supervision_delegation_steps.py` (its Givens set the stand-in's answer and check the brief and the `by:` line), `tests/scenarios/test_supervision.py` (the r77/r78 bindings), `tests/scenarios/supervision_answers_steps.py` (person's answers, r57 scenarios). The two accepted tests pass and stay sound for their cases; a fix for F1 keeps them passing (they never have two questions on one node). No test asserts the old `"the person gave"` wording (see 3). `tests/scripts/` has no test of `supervise_answers.py`.

## 5. A step the work-item skips

`workqueue_answer.answer` (what `work answer` does) checks the work-item is `awaiting-answer` at write time, refuses a line break, takes the asked-from status from the log (refusing if none) and writes through `workqueue.committed`, so the answer is one commit. `answers()` does none of the commit: it writes with `self.section` and commits only at the node's end.
- Effect only this path produces: a `work run` is refused for the answer's own session (two questions, F1). Probe: `run`.
- Effect only this path produces: an uncommitted answer left when the asked-from status is unknown (refused after the write). Probe: `run`, no log line.
- Line-break refusal: `work answer` refuses (`workqueue_answer.py:27-28`, read); this path leaves the question silently (probe "answer of two lines", `run`).
- The answering session's stage dir and `log.jsonl` are not committed on the refusal path that stops the run (probe no-log, `run`; r90 covers only the error outcome, which is in `features/supervision.feature` and not in w156).

## 6. Defects

**D1. Two open questions on one node: the first answer is reverted and the run exits 1 (w156's r77, F1).** Reproduction: `python3 -m pytest -n0 -s -q .shop/scratch/1-research/probe_delegation.py -k two_questions`. Came back: EXIT 1; stderr `work: the session answering w1's question faulted: while its answerer worked, .shop/work/i1/w1.md changed in the repository's own checkout and not committed; work run put it back`; w1.md has both questions, no `## Answers`. Same with the control (one question) → EXIT 0.

**D2. An awaiting-answer work-item with no question is moved on with no answer, under a delegation.** `python3 -m pytest -n0 -s -q .shop/scratch/1-research/probe_delegation.py -k no_questions` → EXIT 0; w1 `green`; no session and no `## Answers`; `log.jsonl` shows the move. (Probe's stand-in plan is the same as the control.)

**D3. An answer written with no commit, and the run refused on the next start.** `python3 -m pytest -n0 -s -q .shop/scratch/1-research/probe_more.py -k no_log` → run 1 EXIT 1 (`log.jsonl gives no transition of w1 to awaiting-answer`), w1.md holds the answer uncommitted; run 2 EXIT 1 `... not committed; commit them before work run starts`.

**D4 (read, not run). The answerer can read any file of its worktree.** `agents/delegation-answerer.md` (20 lines) tells it to read only the brief's files, but `supervise_worker.py` TOOLS `"answer"` (l.42) gives `Read, Glob, Grep` with no path limit. "given ... nothing else" (r77) rests on the agent's text and the brief. The frontmatter also lists `Write`, which `tools()` strips from `--allowedTools` (l.121).

## 7. The file set

Must change (for the fix to F1 and for two-question rows; the accepted scenarios' steps stay as they are):
- `scripts/supervise_answers.py` (121 lines; room 179): `answers()` commits or defers each answer before the next `ask` (D1); zero-question branch (D2) if in scope; the answer path's line-break and refusal behaviour (5), if in scope.
- `features/supervision.feature` (1099 lines; not a Python file, no size limit): a two-question-on-one-node example for r77 (the review's fix), with its own tags.
- `tests/scenarios/supervision_delegation_steps.py` (147 lines; room 153): a Given for two open questions on one node (the existing Givens take one question; `supervision_answers_steps.py:17-19` has a two-question Given for person's answers, not reused).
- `tests/scenarios/test_supervision.py` (252 lines; room 48): binds features via `scenarios()`; changes only if a new step module is imported.

Modules on the change's path, edited or not (`wc -l`; room = 300 − lines):
- `scripts/supervise.py` 247 (room 53): `pull_through` l.201 (F-obs-2 if in scope).
- `scripts/supervise_faults.py` 161 (room 139): `checkout_changes` l.92-113 (the cause of D1; read only).
- `scripts/supervise_worker.py` 247 (room 53): `worker` l.165-214, `TOOLS["answer"]` l.42 (D4; read only).
- `scripts/supervise_brief.py` 129 (room 171): `answer_lines` l.72-82 (the wording in 3).
- `scripts/supervise_rounds.py` 97 (room 203): r70 ready check l.30-36 (read only).
- `scripts/workqueue_answer.py` 53 (room 247): read only; the writer whose checks the answer path does not repeat.
- `scripts/workqueue.py`: on the path (`move`, `committed`) — not counted in this run.
- `agents/delegation-answerer.md` 20 lines (not Python; D4).
- Not counted: `tools size --limit 300` (CLAUDE.md) — checked by line counts above only.
