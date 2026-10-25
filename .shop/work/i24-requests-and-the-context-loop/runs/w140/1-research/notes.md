# Notes of w140: work answer on a capability-proposal

Map: none (`tools tests-of`: "no map"), so tests are found by search and pytest collection. `tools refs workqueue_answer`: 0 references (tests reach `work` by subprocess). Probes run with `-n 0` (xdist hides prints). Scratch `.shop/scratch/w140-1-research/` is ignored; `git status --porcelain` clean.

Note: `pytest.ini` has `-n auto`, and `scripts/work_items.py` deselects every scenario that w140 does not accept (10 of 63 collected in test_work_queue.py).

## 1. Why each scenario is red today

Command: `python3 -m pytest -q -n 0 -p no:cacheprovider tests/scenarios/test_work_queue.py -rfE --tb=short` (run): 10 collected, 8 passed, 2 failed.

- r9 outline, row `answer p1` (`[answer-...capability-proposal p1 is awaiting-answer...]`): FAILED, `StepDefinitionNotFoundError: Given "an initiative i1 under .shop/work/ whose capability-proposal p1 is awaiting-answer"`, features line 236. Missing: no step matches "whose capability-proposal {name} is {status}". `with_items` (tests/scenarios/test_work_queue.py:69-71) needs "whose work-item".
- r24 scenario (`test_answer_on_an_awaitinganswer_capabilityproposal_...`): FAILED, same missing Given, features line 260.
- Behind the missing Given, read: once it exists, the When refuses at scripts/workqueue_answer.py:33 (`asked_from`, no log line for p1), as probe a shows, and the Then `has under ## Answers` would fail on rc 1.
- Behind it, read: the commit (`workqueue.rels_of`, workqueue.py:211) names `log.jsonl`, which the scenario does not make; `git add` of a missing path would refuse. Not reached by a probe, since `asked_from` refuses first.
- r9 deprecated outline (4 rows) and r9 outline work-item rows (4 rows): PASS today (run).

## 2. What the system answers today

Probe: `.shop/scratch/w140-1-research/probe_answer_proposal.py`, run `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w140-1-research/probe_answer_proposal.py`: 6 passed (run). Entry point `scripts/work --root <repo> answer p1 "Use the first reading"`, in scratch repos.

- a. Scenario data (p1 awaiting-answer, no log.jsonl): rc 1, `work: log.jsonl gives no transition of p1 to awaiting-answer; work answer has no status to return it to`. File and tree unchanged (run).
- b. Nearest: log.jsonl holds only w9's line: same refusal (run).
- c. Nearest: log.jsonl gives p1 drafted -> awaiting-answer: rc 0, `p1 drafted`; p1.md becomes `status: drafted`; `## Answers` gets `- 2026-10-25: Use the first reading`; log line appended; commit `work answer: p1 awaiting-answer -> drafted` holds p1.md and log.jsonl (run). See D1.
- d. Nearest: answer with LF, no log: rc 1, `an answer is one line`, nothing changed (run). The line check runs first for a proposal.
- e. Nearest: p1 `approved`: rc 1, `p1 is not awaiting-answer; work answer answers only an awaiting-answer work-item` (run).
- f. Control: work-item w1 awaiting-answer, asked from claimed: rc 0, `w1 ready`, Answers written, commit holds w1.md and log.jsonl (run).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_answer.py:asked_from (15-21) | returns the status to go back to, from log.jsonl's move into awaiting-answer; refuses with no such move | a proposal has no status to return to; r24 writes the answer only, so this must not run for a proposal | 15 answer tests (work-item rows, r13, r14, r15 rows) by search, proposals: none | search (collection `-k answer`), probe a |
| scripts/workqueue_answer.py:answer, `workqueue.move` (line 46) | writes the status back to the asking status and appends a log line | proposal path must not call it; probe c shows it sets p1 to drafted | the same work-item answer tests; proposals: none | read, probe c |
| scripts/workqueue_answer.py:answer, `rels_of` (line 47) | commits the file and initiative log.jsonl, always | r9: log.jsonl only if the change made a line; a proposal with no log would fail the commit | work-item answer tests; proposals: none | read |
| scripts/workqueue.py:rels_of (211-213) | always returns [file, log.jsonl] | r9 "if it made one"; also used by retry (206) and withdraw (234) | retry and withdraw tests by search (test_work_queue.py work-item rows) | search |
| scripts/workqueue_answer.py:answer refusal text (32) | "answers only an awaiting-answer work-item" | names work-items only; reads wrong for a proposal | none (no test asserts the text) | search (grep "answers only" in tests: none) |
| scripts/workqueue.py:find (216-221) | globs `*/<name>.md`, kind-blind | finds p1.md; keeps working | answer tests incl. probes b, c (run) | probe |
| scripts/workqueue.py:agrees (179-192) | status from the file, refused when log.jsonl's last move disagrees | applies to a proposal too (r6); keep | work-item tests; proposals: none | read |
| scripts/workqueue.py:STATUSES, move (15-16, 137-160) | only work-item lifecycle statuses; proposal statuses (approved, formulated) refused | proposal path must not reach move | work-item answer tests; proposals: none | read |
| scripts/model_work.py:11 STATUSES["capability-proposal"] | {drafted, approved, merged, formulated, withdrawn}; no awaiting-answer | an awaiting-answer proposal (r24's input) fails the model's status check | none (grep tests for awaiting-answer: no model test) | read, grep |
| scripts/work:109 help text; README.md:141 | "answer the question of an awaiting-answer work-item" | docs only | none | search |
| scripts/workqueue_status.py:parts (45-48) | open questions for both kinds: Questions past Answers | works for an answered proposal; no change | status scenarios with p1 approved (by search) | read |

## 4. Tests the requirements make impossible to keep

Tests that execute `answer()`: 17 by search (`pytest --whole-suite --collect-only -k answer`). Run: 15 passed, 2 failed (the red targets of part 1). The 15 assert work-item behaviour that r24 keeps: status return, Answers, log line, one-line refusal (run, `--whole-suite -k answer`).

- Checked, sound: the 7-row line-break outline (`test_answer_with_a_line_break_in_it_is_refused_and_nothing_changes`) still passes if the line check stays first (probe d).
- Checked, sound: the r9 deprecated and r9 rows hold file and "nothing under .shop/work/ differs"; both hold whether or not log.jsonl is in the commit (read of work_queue_git_steps.py:48-71).
- Checked, sound: tests/scripts/test_work_withdraw.py (asserts HEAD unchanged on a refused withdraw; no log assertion) (read).
- Checked by search: no test asserts a proposal is refused by `work answer`, or that a proposal's status is returned. `grep "answers only|not awaiting-answer|asked_from|rels_of|committed\("` over tests/: no such assertion.
- Result: none impossible to keep. The two red targets need their Given (part 1).

## 5. A step the work-item skips

Answering a capability-proposal skips the steps the work-item way takes in `answer()`:

- `asked_from` (workqueue_answer.py:33): the return status and the refusal "log.jsonl gives no transition". Its own effect is the refusal, which probe a shows for the proposal as it stands (run). Dropping it lets a proposal be answered with no log, which the scenario needs.
- `workqueue.move` (workqueue_answer.py:46): its effects are the status write, the log line (time, before, after, by), the STATUSES check, and the file restore when the log cannot be written (r7). Probe c shows the status write and the log line on a proposal (run). The restore: read (workqueue.py:155-160).
- `agrees` (workqueue.py:179): kept on the proposal path by the current order (read); r6 refusal on a file/log disagreement.
- The commit of log.jsonl (`rels_of`): the work-item way commits it; the proposal path commits its own file only (r9, read).
- The line check (r15): kept by the proposal path, shown by probe d (run).

## 6. Defects

### D1. `work answer` on a capability-proposal returns its status to the asking status

Reproduction: probe c, `probe_answer_proposal.py::test_c_proposal_logged_into_awaiting_answer_from_drafted`. Setup: p1 `status: awaiting-answer`, log.jsonl `{"work-item": "p1", "before": "drafted", "after": "awaiting-answer", ...}`. Command `scripts/work --root <repo> answer p1 "Use the first reading"`. Returned `rc 0`, stdout `p1 drafted`. p1.md now `status: drafted` with `## Answers` `- 2026-10-25: Use the first reading`. A log line appended and commit `work answer: p1 awaiting-answer -> drafted` (p1.md and log.jsonl). r24 says only the answer is written, so the status should stay `awaiting-answer`.

## 7. The file set

Must change:
- `scripts/workqueue_answer.py` (48 lines, room 252): `answer()` takes a capability-proposal: no `asked_from`, no `move`, commit its own file. Work-item path unchanged.
- `tests/scenarios/work_queue_answer_steps.py` (32 lines, room 268): add the Given "an initiative {ident} under .shop/work/ whose capability-proposal {name} is {status}", writing p1.md with no log line. Star-imported by test_work_queue.py:21.

May change, not needed for these scenarios:
- `scripts/workqueue.py` (279 lines, room 21): `rels_of` "if it made one" in general (r9).
- `scripts/work` (147 lines, room 153): help text line 109.
- `README.md:141`: docs line.
- `scripts/model_work.py` (219 lines, room 81): awaiting-answer for capability-proposal (old assumption, part 3).

Not changed: `tests/scenarios/test_work_queue.py` (287 lines, room 13): the Given would crowd it; put it in the answer steps module.

Modules on the change's path, edited or not (line count, room):
- `scripts/work`: 147, room 153
- `scripts/workqueue.py`: 279, room 21
- `scripts/workqueue_answer.py`: 48, room 252
- `scripts/model.py`: 139, room 161 (loaded by workqueue for frontmatter)
- `scripts/model_parse.py`: 271, room 29 (read by model)
- `tests/scenarios/test_work_queue.py`: 287, room 13
- `tests/scenarios/work_queue_answer_steps.py`: 32, room 268

Room is 300 less the count (CLAUDE.md size limit). `tools size` not run.
