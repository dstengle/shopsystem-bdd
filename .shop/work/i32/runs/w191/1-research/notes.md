# w191 research notes

Scope: supervision#r118, supervision#r119 (two scenarios, features/supervision.feature:1458-1474).
Checkout: HEAD 0764d6ca, `git status --porcelain` empty. Ignored: `.shop/scratch/`, `__pycache__/`.
Tools: `tools map` never made (no map), so `tests-of` and `untested` were not run; every list below says `search`
or `refs`. `refs` undercounts: `refs asked_by_reviewer` gives 1, search gives 4 (see part 3).
Session env sets PYTEST_ADDOPTS `--work-item w191`: plain pytest runs of other files are refused (r56), and
`-p no:work_items` is refused too. So scenarios outside w191's accepts were not run.
Probe file: `.shop/scratch/w191-1-research/probe_answers.py` (fixtures under its `fx/`).

## 1. Why each scenario is red today

Neither is red. Both pass on this checkout.

- `python3 -m pytest -q -p no:cacheprovider -n 0 "tests/scenarios/test_supervision.py::test_under_a_delegation_an_answer_to_a_reviewers_question_that_asks_for_a_change_makes_the_workitem_ready_again"`: 1 passed. run
- same for `..._that_accepts_the_workitem_as_it_is_transitions_the_workitem_to_done`: 1 passed. run
- `python3 -m pytest -q -p work_items --work-item w191 -n 0 tests/scenarios/test_supervision.py -k delegation`: 2 passed, 201 deselected. run
- The behaviour is there: `scripts/supervise_answers.py:80-86` (reviewer move through `workqueue_answer.reviewer_status`), `:117-122` (verdict read from the session), `:83` (`self.verdicts[name]`). Steps: `tests/scenarios/supervision_delegation_steps.py:67-80`, stand-in verdict `change`/`accept`. read
- Findings file of branch review 1 (`.shop/work/i32/runs/branch-review/1/findings.md`) says the same: w190 is green with both scenarios. read

So the brief's premise ("red") does not hold. The work-item's real content is the findings (part 6, D1, D2).

## 2. What the system answers today

Probe A, the real entry point: `python3 <worktree>/scripts/work answer w1 "<text>" [flag]`, run in fixtures
(a reviewer's question: log `done -> awaiting-answer`; a drafter's question: log `researched -> awaiting-answer`).

| case | command | came back | run |
|---|---|---|---|
| reviewer, change | `answer w1 "No, remove the old reader." --change` | rc 0, `w1 ready`, Answers written, log `awaiting-answer -> ready` by `work answer`, git clean | run |
| reviewer, accept | `... "Yes, keep it as it is." --accept` | rc 0, `w1 done` | run |
| reviewer, neither | `... "Yes."` | rc 1, "the answer must say whether it asks for a change (--change) or accepts the work-item as it is (--accept)"; file and log unchanged | run |
| reviewer, both | `... "Yes." --change --accept` | rc 1, refused, unchanged | run |
| drafter, accept flag | `... "Use the short name." --accept` | rc 0, `w1 researched`: the flag is ignored | run |
| drafter, plain | `... "Use the short name."` | rc 0, `w1 researched` | run |

Probe B, a direct call of `supervise_answers.Answers.answers` (a subclass with stubbed `delegation`, `held`, `section`,
`commit`, `push`, `uncommitted`, `move`; not `work run`): w1 awaiting-answer, asked by its reviewer, its one question
already answered by an earlier committed run. Came back: `KeyError 'w1'`, no move. run
(`python3 -m pytest -q -s -p no:cacheprovider -n 0 .shop/scratch/w191-1-research/probe_answers.py::test_keyerror_direct_call`,
output `KEYERR-PROBE raised KeyError 'w1' | calls: []`.)

Nearest cases, read (not run through `work run`: it needs the stub worker harness):
- the session gives no `verdict` on a reviewer's question: `ask` returns None, the question stays for the person (`supervise_answers.py:119-121`). read
- the session's status is not DONE, or its answer is empty or has a line break: None (`:117-118`, `:123`). read
- the session fails (error, turn limit, no result, or it changed `.shop/work/`): `Refused` is raised and the run stops, after `keep_round` (`:112-115`). read
- the answer for one question is None: later questions are not answered (`:74`). read
- `work run` calls `answers()` on every run (`supervise.py:204`). read

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/workqueue_answer.py:answer` (lines 53-58) | a reviewer's answer's status comes only from the human's `--change`/`--accept`; refuses without one or with both | the session's `verdict` gives the same status (r118, r119); `work answer`'s rule stays for the person | by search: `tests/scenarios/work_queue_answer_steps.py:19-45` (not run here: plugin refusal) | search, refs |
| `scripts/workqueue_answer.py:asked_by_reviewer` (24-28) | last move into awaiting-answer was from `done` | also read by the delegation path: `supervise_answers.py:82, 104, 119` | by search: delegation and work-queue scenarios | refs found 1 (`:55`); search found 4 |
| `scripts/workqueue_answer.py:reviewer_status` (31-33) | `ready` on change, `done` on accept | also called by `supervise_answers.py:83` | by search: the two accepted scenarios | refs found 1 (`:58`); search found 2 |
| `scripts/supervise_answers.py:answers` line 83 `self.verdicts[name]` | the verdict a session gave this run | KeyError when no session ran for this item this run (D1) | by search: the two accepted scenarios (they reach line 83 with a verdict). The KeyError path: none | search, probe B |
| `scripts/supervise_answers.py:answers` lines 77-79 (answer written, committed, then the move in a second commit) | two commits: answer, then move | a stop between them leaves the state D1 needs; `work answer` writes and moves in one commit (`workqueue_answer.py:74-76`) | none | read |
| `scripts/supervise_answers.py:answers` line 80 (`kind == "work-item"`) | a proposal is never moved by this path | none for r118/r119 | by search: delegation scenarios | read |
| `agents/delegation-answerer.md` (20 lines) | no word `verdict` (grep finds only the branch-reviewer and task-reviewer agent texts) | the session must give `verdict` for a reviewer's question; only the brief asks for it (`supervise_answers.py:17`) | none | search |
| `scripts/supervise_answers.py:answers` (the `verdicts` dict, reset at line 68) | per-run | `self.verdicts` is the only source of the verdict; a committed answer carries none | none | read |

## 4. Tests the requirements make impossible to keep

No map, so by search over `tests/` for `asked_by_reviewer`, `reviewer_status`, `verdict`, `awaiting-answer`, answer steps.

- `tests/scenarios/work_queue_answer_steps.py:19-45`: `work answer` refusals (no flag, both flags, the reviewer's rule) and their messages. Kept: the person's rule is unchanged by r118, r119. Not run here (plugin refusal under PYTEST_ADDOPTS); probe A reproduces each refusal. Verified by probe: sound.
- `tests/scenarios/supervision_delegation_steps.py:67-80`: the stand-in verdict. It writes `verdict` in the session's fields. Sound: it matches the accepted scenarios.
- `tests/scenarios/supervision_answers_steps.py:40-47` (`reviewer_asked`): a reviewer's question with its log. Sound.
- Nothing in the tests asserts a behaviour that r118 or r119 change. None can no longer pass. Searched, not run: the rest of `test_work_queue.py`.

## 5. A step the work-item skips

The delegation path does not run `work answer`'s checks: the flag rule (`workqueue_answer.py:55-57`) is replaced by the session's
`verdict` (`supervise_answers.py:119-122`), and a missing verdict leaves the question instead of refusing. read
Effects only that path produces:
- a reviewer's answer written and committed with no status change (`supervise_answers.py:79`), then the move in a second commit: the window of D1. read, and probe B.
- a verdict stays in memory only (`self.verdicts`): the next run cannot move the item (D1). read, and probe B.
- `work answer` refuses an answer with a line break (`workqueue_answer.py:39-40`); the delegation path leaves the question (`supervise_answers.py:123`). read.

## 6. Defects

### D1. `work run` crashes with KeyError on a reviewer's item whose answer is already committed
- Where: `scripts/supervise_answers.py:83`. Source: branch review 1, finding 1 (`findings.md`).
- Reproduction: `python3 -m pytest -q -s -p no:cacheprovider -n 0 .shop/scratch/w191-1-research/probe_answers.py::test_keyerror_direct_call`
  came back `KEYERR-PROBE raised KeyError 'w1' | calls: []`; w1 stays `awaiting-answer` (its file has the one answer).
  Driven directly on `Answers.answers`, not through `work run`. run
- Through `work run`: the findings report rc 1 with the same `KeyError: 'w1'` in the suite's harness. read (findings).
- Every later `work run` reaches it again (`supervise.py:204` calls `answers()` each run; `self.verdicts` is empty each run). read

### D2. `work answer --accept` on a non-reviewer's question is accepted and the flag is ignored
- Reproduction: `python3 <worktree>/scripts/work answer w1 "Use the short name." --accept` on a `researched -> awaiting-answer`
  item: rc 0, `w1 researched`, log `awaiting-answer -> researched` by `work answer`. run (probe A, `drafter_accept`).
- Readings for the plan: refuse a reviewer-only flag on a non-reviewer item, or ignore it as today. Not decided here.

## 7. The file set

Changes the scenarios need: none (both pass).
Changes the findings need (D1, D2, FURB167):
- `scripts/supervise_answers.py` (142 lines): D1 fix at lines 80-86 (`self.verdicts.get(name)`, leave or refuse). Search and probe B.
- `tests/scenarios/supervision_delegation_steps.py` (202 lines): FURB167 at line 171 (`re.M` to `re.MULTILINE`; seen by read); a step for D1's test if one is added. Findings file.
- `scripts/workqueue_answer.py` (77 lines): only if D2 is refused, or the verdict rule is shared with a new reading. Probe A.
Not in the file set: `features/supervision.feature` (a D1 scenario would need a requirement; none of w191's accepts covers it).

Modules on the change's path (edited or not), `wc -l`, room under 300 (`tools size --limit 300` prints nothing):
- `scripts/supervise.py` 265, room 35
- `scripts/supervise_worker.py` 251, room 49
- `scripts/supervise_faults.py` 161, room 139
- `scripts/supervise_brief.py` 167, room 133
- `scripts/workqueue.py` 290, room 10 (`move`, `agrees`: the only mover)
- `scripts/workqueue_request.py` 183, room 117 (`delegation` reads the request)
- `scripts/workqueue_answer.py` 77, room 223
- `tests/scenarios/test_supervision.py` 260, room 40
- `tests/scenarios/supervision_world.py` 173, room 127
- `tests/scenarios/supervision_delegation_steps.py` 202, room 98
- `tests/scenarios/work_queue_answer_steps.py` 70, room 230
