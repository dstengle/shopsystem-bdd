# w120 research notes

Work-item: w120, accepts work-queue#r15. Accepted scenarios: 2 (8 example rows as tests).
Tools: `tools check` run; `tools tests-of` refused, no map (`tools map` not run: it runs the suite); `tools refs` not run; callers by search. Scratch: `.shop/scratch/w120-1-research/` (git-ignored, so `git status --porcelain` stays clean).

## 1. Why each scenario is red today

None is red. All 8 collected tests pass.
- Command: `python3 -m pytest -q "<node id>"` for each of the 8 node ids of `tests/scenarios/test_work_queue.py` (run, 8 passed).
- The work-item's real defect is not a scenario: `tools check tests/scenarios/work_queue_answer_steps.py scripts/workqueue_answer.py` (run) exits 1 with `tests/scenarios/work_queue_answer_steps.py:2:1: I001 [*] Import block is un-sorted or un-formatted`. Ruff's diff (run, probe_ruff.py) removes one of the two blank lines between the import block and `BREAKS = {...}` (line 5 of the file). Nothing else in that check.
- `tools check` with no paths said "nothing to check" (no Python file changed since base); the project-wide ruff run was not done.

## 2. What the system answers today

Probe: `.shop/scratch/w120-1-research/probe_answer.py` (run, `python3 -m pytest -q -s -n 0 <path>`). Each case: a fresh fixture repo in scratch, `scripts/work --root <repo> answer ...` of this checkout. Results (rc, stderr, files changed):

Scenario Givens and Whens:
- Newline in an awaiting-answer item: rc 1, `an answer has a line break in it; an answer is one line`, no files changed, no traceback.
- VT, FF, CR, NEL, LS, PS in an awaiting-answer item: same refusal, no file changed. (Matches the 7 Outline rows.)
- Two lines to a `ready` item: same one-line refusal, not the "not awaiting-answer" one; no file changed.

Nearest cases:
- A: one line to a `ready` item: rc 1, `w1 is not awaiting-answer ...`, nothing changed.
- B: `text\n` (break at the end), awaiting: refused, nothing changed.
- C: `\n` alone: refused, nothing changed.
- D: empty answer `""`, awaiting: rc 0, `w1 ready`, two files changed; a bullet `- <date>: ` is written. (See defect 6a.)
- E: a tab `a\tb`: accepted, `w1 ready`.
- F: U+001C (file separator): accepted, `w1 ready` (defect 6b).
- G: CRLF `a\r\nb`: refused (CR), nothing changed.
- H: break answer to missing `w9`: the one-line refusal comes first, nothing changed.
- I: one-line answer to missing `w9`: `there is no work-item w9 under .shop/work`, nothing changed.
- J: awaiting-answer file, log.jsonl with no move into awaiting-answer, one-line answer: `log.jsonl gives no transition of w1 to awaiting-answer ...`, nothing changed.
- K: same as J with a break answer: one-line refusal, nothing changed.
- L: a second answer to the same item after a good one: first `w1 ready`; second refused as not awaiting-answer; the commit count went 2 to 2 (no new commit).
- M: no log.jsonl at all, one-line answer: refused as J; nothing changed.
- Refusal then `work show`: `i1/w1 awaiting-answer`, file untouched.

Code read (read): `scripts/workqueue_answer.py:27-28` checks LINE_BREAKS before `workqueue.find` (line 29) and the awaiting check (line 31). So the order of refusals is the one the scenario pins.

## 3. Old assumptions

Requirement r15 adds a refusal; it changes no form that existing code writes. One row for a reader that assumes multi-line answers:

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_brief.py:answer_lines | joins each answer's continuation lines into one `Answer:` line (`" ".join(l.strip() ...)`) | nothing to change: `work answer` now writes one line, so the join is a no-op for its output; it still reads hand-written multi-line answers | tests/scenarios/supervision_answers_steps.py:briefs_hold_answers, one-line bullets only (by search; no map) | search for `answer_lines` and `## Answers` |
| scripts/supervise.py:held / questions | reads `## Answers` bullets with their continuation lines, pairing answer n with question n | unchanged; a one-line answer is one bullet | none found by search (the held reader is run by supervision tests with one-line answers, see row above) | search for `held(` |

Callers of `workqueue_answer.answer`: `scripts/work:41` only (search).

## 4. Tests the requirements make impossible to keep

`tools tests-of` not available (no map), so by search. Searched `tests/` and `features/` for `work answer` and `## Answers`: the only tests of `work answer` are the r13, r14 and r15 scenarios in `features/work-queue.feature` and their steps. They use one-line answers ("Use the first reading") or the r15 refusal. The r15 scenarios themselves pass (run). Verified sound: `tests/scenarios/test_work_queue.py` (r13, r14, r15 scenarios) and `tests/scenarios/supervision_answers_steps.py`. Found none that can no longer pass. Note: the two accepted scenarios and test_work_queue.py import of `work_queue_answer_steps` are unchanged by a fix.

## 5. A step the work-item skips

The work-item adds no path. The one-line check is the step itself (r15). Its only effect: a refusal of break answers before the item is found and before its status is read, and before any write. Shown by probe H (missing item with a break answer: refused as one line, nothing changed) and the scenario-1 outlines (run). Nothing else in the path to skip. 

## 6. Defects

Each is a probe result, not a judgement on the plan.

### 6a. An empty answer is written as an empty bullet
Command: probe test `test_nearest_cases`, case D: `work answer w1 ""` on an awaiting-answer w1.
Came back: `rc 0`, stdout `w1 ready`; files `.shop/work/i1/w1.md` and `log.jsonl` changed; the `## Answers` section gets `- <date>: `. Run.

### 6b. A U+001C (file separator) in an answer is accepted
Command: probe case F: `work answer w1 "a\x1cb"` on awaiting-answer w1.
Came back: `rc 0`, `w1 ready`, the answer written as one bullet. Run.
Not in r15's list of seven breaks. Python's `str.splitlines` (used by the test step `has_answer`, `tests/scenarios/work_queue_answer_steps.py:33`) splits on U+001C, U+001D and U+001E, so a reader using it sees two lines. The step's effect on the test is read, not run.

### 6c. The work-item's own defect: ruff I001
Command: `python3 .../tools check tests/scenarios/work_queue_answer_steps.py` (run).
Came back: `tests/scenarios/work_queue_answer_steps.py:2:1: I001 [*] Import block is un-sorted or un-formatted`, exit 1. Ruff's diff: one blank line too many between imports and `BREAKS` (run).

## 7. The file set

Production and test files the work-item must change:
- `tests/scenarios/work_queue_answer_steps.py`: delete one of the two blank lines after the import block (lines 5-6). The ruff diff shows it (run). Nothing else.

Also on the change's path, edited or not (`wc -l`):
- `scripts/work`: 80 lines, room 220. Not edited.
- `scripts/workqueue.py`: 262 lines, room 38. Not edited.
- `scripts/workqueue_answer.py`: 48 lines, room 252. Not edited (LINE_BREAKS already has the seven breaks).
- `tests/scenarios/test_work_queue.py`: 284 lines, room 16. Not edited; imports the step module with `import *`.
- `tests/scenarios/work_queue_answer_steps.py`: 33 lines, room 267. Edited.

Files that must keep passing and need no edit: the 8 node ids (run, pass) and the probe outputs above.
