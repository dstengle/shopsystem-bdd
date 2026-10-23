# Research of w100: work-queue r15

Scope: the one accepted scenario, `features/work-queue.feature`: "answer with a newline in it is refused, and nothing changes" (@r15). The work-item's body also lists fixes outside its `accepts:` (retirements, put-back, a noqa, a gate for other items). Not researched here.

No `tools map` exists, so `tests-of` and `untested` have no map: counts below are `by search` or `refs`. Probe files: `.shop/scratch/w100-1-research/` (probe_answer_newline.py, probe_answer_separators.py).

## 1. Why the scenario is red today

- Command: `python3 -m pytest -q -s "tests/scenarios/test_work_queue.py::test_answer_with_a_newline_in_it_is_refused_and_nothing_changes"` (run). Result: `StepDefinitionNotFoundError: Step definition is not found: When "the session runs \`work answer w1\` with an answer of two lines"`. Line 233.
- Missing step: no When matches "the session runs `work answer w1` with an answer of two lines". The existing `run_work_newline` (tests/scenarios/test_work_queue.py:177) needs "with a newline and `{extra}` in the {option} value".
- Then "work exits with an error, saying that an answer is one line" has no step either: "it exits with an error" (test_work_queue.py:214) is exact, and "work says that {reason}" (:267) starts with other words (read; pytest-bdd stops at the When, so not reached by run).
- Given "an initiative i1 under .shop/work/ whose work-item w1 is awaiting-answer" matches `with_items` (test_work_queue.py:66) (read).
- And "... are as they were" matches `both_as_they_were` (test_work_queue.py:260) (read).
- Code behind: none missing. `scripts/workqueue_answer.py:29-30` refuses a newline (run, see section 2).
- Fix lives in step definitions: a When and a Then for r15. The new steps must set `context["before"]` as `run_work` does (test_work_queue.py:172).

## 2. What the system answers today

Probe commands (run, `python3 -m pytest -q -s -n 0 .shop/scratch/w100-1-research/probe_answer_newline.py`, each case in its own git repo under the scratch directory, running the worktree's `scripts/work answer w1 <answer>`):

| case | answer | state | result |
|---|---|---|---|
| two_lines (the scenario's Given and When) | `line one\nline two` | awaiting-answer, log ok | rc 1; stderr `work: the answer has a newline in it; an answer is one line`; files unchanged; HEAD unchanged; `status --porcelain` empty |
| trailing_nl | `one\n` | same | same refusal |
| cr | `a\rb` | same | same refusal |
| inject | `x\nstatus: ready` | same | same refusal |
| no_log | `one\ntwo` | awaiting-answer, no log line | rc 1; `log.jsonl gives no transition of w1 to awaiting-answer` (the log check runs before the newline check) |
| drafted | `one\ntwo` | drafted, log says awaiting-answer | rc 1; refused for status not matching log; newline check not reached |

Reading: the refusal in the scenario already happens today, with the scenario's wording and no change to files or git. The refusal order (awaiting check, then log, then newline) is read from `workqueue_answer.py:26-30`, and the probe confirms it.

Control (run, probe_answer_separators.py `plain`): `Use the first reading` is written as `- <date>: Use the first reading` under `## Answers`, rc 0.

Nearest cases the scenarios do not give: all six above. The ` `, `\x0c` cases are in section 6.

## 3. Old assumptions

The r15 line does not replace an old form. It adds a refusal to `work answer`. The old assumption it leans on is "an answer is one bullet line": that holds today only for `\n` and `\r`.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_answer.py:answer (lines 29-35, 41) | refuses `\n` and `\r` only; writes one bullet with the date | the refusal the line asks for, already there | r15 scenario (red, step missing) | read; probe |
| scripts/supervise.py:held (193-204) | splits the Answers section with `str.splitlines()`, so ` `, `\x0c` and other separators start a new bullet when they start a line | answer text with those separators is not refused, so one answer becomes two bullets (section 6) | by search: test_supervision.py:sections (212-218) asserts one bullet per answer; none executes the separator case | read; probe |
| scripts/supervise.py:questions (206-209) | open questions are those past `len(held(Answers))` | an extra answer bullet shifts which questions are open (section 6) | none (by search: no test names a separator) | read |
| scripts/supervise_brief.py:answer_lines (53-62) | zips Questions with Answers and joins continuation lines with spaces | with the separator defect, the second half of an answer is dropped from the brief (section 6) | by search: tests/scenarios/supervision_answers_steps.py:briefs_hold_answers | probe (`brief_pairs`) |
| scripts/migrate_upgrade_answers.py:plan (renames `## Rulings`, leaves free text) | a pre-0.25 Rulings text may hold several lines; it is kept as is, so continuation bullets stay | r15 does not reach migrated text; `held` must keep reading continuation lines | tests/scripts/test_migrate_upgrade_answers.py (plan, lines 28-43) | search: grep `## Answers` in scripts |
| scripts/workqueue.py:add (79-83) | the same `\n`/`\r` set for title and fields | same rule; no answer path | by search: tests/scripts/test_work_add_title.py:44 | read |

## 4. Tests the requirement makes impossible to keep

None. r15 only adds a refusal, and no test asserts that `work answer` accepts a newline. Checked:
- `tests/scenarios/test_work_queue.py`: collected 35; the run deselected 34 (the cause, read: pytest.ini `-m "not fixture"` and the work_items plugin, not verified). So the r13 and r14 answer scenarios did not run here. Read: their steps (`has_answer`, work_queue_answer_steps.py) assert a one-line answer, which r15 keeps.
- `tests/scenarios/test_supervision.py:sections` and `supervision_answers_steps.py` (by search): build one-line answers; sound under r15.
- `tests/scripts/test_migrate_upgrade_answers.py` (by search): unaffected.

## 5. A step the work-item skips

None. The refusal sits before the write and before `workqueue.committed` (read, `workqueue_answer.py:29-44`), so no step of the existing path is skipped. The only effect of the refusal is the exit and the message, both shown in section 2.

## 6. Defects

### D1: `work answer` accepts ` ` and `\x0c`, and the reader splits the answer into two bullets

Reproduction (run, `python3 -m pytest -q -s -n 0 .shop/scratch/w100-1-research/probe_answer_separators.py`). The work-item has `## Questions` with `- Which reading?` and log.jsonl's awaiting-answer line.

- `work answer w1 "one<U+2028>- two"`: rc 0. `## Answers` gets `- 2026-10-23: one<U+2028>- two`. HEAD moved. `supervise.Run.held(Answers)` returns `[['- 2026-10-23: one'], ['- two']]`: two bullets for one question. `Briefs.answer_lines` gives only `Answer: 2026-10-23: one`; "two" is lost from the brief.
- `work answer w1 "one<FF>- two"`: same result.
- Control: `work answer w1 "Use the first reading"`: one bullet, the brief pairs it.

Cause: `workqueue_answer.py:29` checks `\n` and `\r` only; `supervise.py:199` splits with `splitlines()`. Effect on questions: `questions()` (supervise.py:209) counts Answers bullets, so an extra bullet marks the next question answered.

### D2: a newline refusal in `answer` is shadowed by the log check

`work answer w1 "one\ntwo"` on an awaiting-answer item with no log line says `log.jsonl gives no transition of w1 ...` and never the newline message (probe `no_log`). Not wrong by itself: the log is read first. Recorded for the plan's wording only.

## 7. The file set

Changes for the scenario to pass:
- tests/scenarios/work_queue_answer_steps.py: new When (`the session runs \`work answer w1\` with an answer of two lines`, makes argv with `\n` in the answer, sets `context["before"]`) and new Then ("work exits with an error, saying that an answer is one line"). Found by the run (section 1).

Changes that the defect D1 would need (not needed for the scenario): scripts/workqueue_answer.py:29 (check for ` `, `\x0c` and other `str.splitlines()` separators) or scripts/supervise.py:199 (split on `\n` only). Left to the plan.

Nothing else must change: the code refuses already (probe), and no passing test asserts otherwise (section 4).

Modules on the change's path, with lines (`wc -l`) and room under 300 (`tools size --limit 300` printed nothing, so none is over):
- scripts/work: 80 lines, room 220
- scripts/workqueue_answer.py: 45 lines, room 255
- scripts/workqueue.py: 262 lines, room 38
- scripts/supervise.py: 263 lines, room 37 (reader on the D1 path)
- scripts/supervise_brief.py: 110 lines, room 190 (D1 path)
- tests/scenarios/test_work_queue.py: 282 lines, room 18 (imports the steps; unchanged if the new steps go in work_queue_answer_steps.py)
- tests/scenarios/work_queue_answer_steps.py: 13 lines, room 287 (file to change)
