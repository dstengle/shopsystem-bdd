# w113 research notes

Scripts: plugin 0.24.0 `tools`. `tools refs` ran: 0 refs for `workqueue_answer.answer` (tests reach `work` by subprocess). `tools tests-of`: no map (`tools: no map: make one with tools map`), so tests are found `by search`. Probes: `probe_answer.py`, `probe_pairs.py` in scratch, run with `-n 0` (xdist hides prints). Scratch is ignored: `git status --porcelain` is clean.

Accepted scenarios (features/work-queue.feature): the deprecated newline one (l.214), the line-break Outline (l.223, 7 examples), the two-lines-to-ready one (l.241). All tagged @r15.

## 1. Why each scenario is red today

Run: `python3 -m pytest -q <node id>` for the 9 node ids: deprecated, 7 Outline examples, ready (one run). Result: 8 failed, 1 passed.

- **Deprecated newline scenario**: PASSES today (run). Its When is `work_queue_answer_steps.py:7`, and the LF check at `scripts/workqueue_answer.py:29` refuses it.
- **Outline, 7 examples**: 7 FAIL with `StepDefinitionNotFoundError: When "...with an answer of two lines broken by <line break>"`, Line 226 (run). Missing: a When step with a `{line break}` parameter in `tests/scenarios/work_queue_answer_steps.py`, mapping `a newline` and `U+000B`, `U+000C`, `U+000D`, `U+0085`, `U+2028`, `U+2029` to their characters. Behind it, once the step exists, 5 of 7 examples would still fail their Then: `work answer` exits 0 for VT, FF, NEL, LS, PS (run, probe 1). CR and LF are refused today at `scripts/workqueue_answer.py:29` (`if "\n" in text or "\r" in text`) (run). The "a newline" and CR examples would pass once the step exists.
- **Two lines to a ready work-item** (`test_an_answer_of_two_lines_..._first`): FAILS with `StepDefinitionNotFoundError` for `broken by a newline`, Line 244 (run). Behind it, the code runs the awaiting-answer check first: `workqueue_answer.py:26-27` refuses "w1 is not awaiting-answer", which lacks "an answer is one line" (run, probe 2). The one-line check at line 29 is reached only after `asked_from` (line 28). So the order must change in `answer()`.

## 2. What the system answers today

Probe 1, `probe_answer.py::test_each_break_in_an_answer_to_an_awaiting_answer_item` (run; `work --root <repo> answer w1 "line one<X>line two"`, w1 awaiting-answer, log says claimed→awaiting-answer):
| break | rc | result |
|---|---|---|
| LF U+000A | 1 | "the answer has a newline in it; an answer is one line"; nothing changed, 1 commit |
| VT U+000B | 0 | lands: `## Answers` gets `- 2026-10-23: line one\x0bline two`; w1 → ready; 2 commits |
| FF U+000C | 0 | lands, as VT |
| CR U+000D | 1 | refused, one-line message; nothing changed |
| NEL U+0085 | 0 | lands |
| LS U+2028 | 0 | lands |
| PS U+2029 | 0 | lands |
| FS U+001C | 0 | lands (not in r15's list) |
| GS U+001D | 0 | lands (not in r15's list) |
| RS U+001E | 0 | lands (not in r15's list) |
| none (space) | 0 | lands, control |

Nearest cases (run):
- `two lines, ready, no log`: rc 1, "w1 is not awaiting-answer; work answer answers only an awaiting-answer work-item"; no change.
- `two lines, awaiting-answer, no log`: rc 1, "log.jsonl gives no transition of w1 to awaiting-answer"; no change. A two-line answer is refused for this reason first.
- `answer w9` (missing item): rc 1, "there is no work-item w9 under .shop/work"; no change.
- Empty answer `""` to awaiting-answer: rc 0, lands as `- 2026-10-23: ` (an empty bullet). Not in r15; reported only.
- Existing `## Answers` followed by `## Notes`: rc 0; the new bullet is appended after the old one, `## Notes` kept (run).
- First attempt, before the probe set git identity: a VT answer was refused by the commit step, `work: git commit failed: Author identity unknown`; w1 left as it was; 1 commit (run).

Probe 2, `probe_pairs.py` (run; `supervise.Run.held`, `questions`, `answer_lines` on a file with two Questions):
- control, two one-line answers: pairs Q1/first, Q2/answer two (correct).
- an answer holding `\x0b- ` (a VT followed by "- "): `held Answers` gives 3 bullets; `answer_lines` pairs Q2 with `answer one` and drops `answer two`. `held` uses `str.splitlines()` (`scripts/supervise.py:170`).

## 3. Old assumptions

Requirement r15 changes "an answer is one line, broken only by LF or CR, and refused after the awaiting-answer check" into "by any of seven Unicode breaks, refused first".

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_answer.py:answer l.29 `"\n" in text or "\r" in text` | refuses LF and CR only; VT, FF, NEL, LS, PS land (run) | must refuse all seven (VT, FF, NEL, LS, PS are the defect); FS/GS/RS: see Questions | deprecated node and Outline "a newline" and CR examples (by search: test_work_queue.py via work_queue_answer_steps.py) | read + probe 1 |
| scripts/workqueue_answer.py:answer l.26-28 (status check, then `asked_from`) before l.29 | a two-line answer to a non-awaiting-answer item is refused as "not awaiting-answer" | the one-line refusal comes first (the ready scenario) | ready node only (red today); none other (by search) | read + probe 2 |
| scripts/workqueue_answer.py:asked_from l.12-18 | refuses with "no transition" before the line check | after the line check (ordering) | by search: test_work_queue.py answer nodes with an awaiting-answer Given | read + probe 2 |
| scripts/workqueue.py:add l.79-83 (`"\n" in title or "\r" in title`, same for --part-of/--under/--accepts) | the same LF/CR-only check, for work add's title and fields | r15 names answers only: unchanged unless the plan extends it (a question) | by search: tests/scenarios/work_queue_add_steps.py, tests/scripts/test_work_add_title.py | read |
| scripts/supervise.py:held l.170 (`.splitlines()` of the section) | splits Answers and Questions bullets at every Unicode break | a VT/FF/NEL/LS/PS in a new answer would start a bullet: impossible after the fix; files already holding one stay split | by search: tests/scenarios/test_supervision.py l.217-220 (`section(text,"Answers").splitlines()`), supervision_answers_steps.py | read + probe 2 |
| scripts/supervise.py:questions l.177-180 and supervise_brief.py:answer_lines l.53-63 | pair the n-th Answers bullet with the n-th Questions bullet, from `held` | a break-holding answer shifts every later pair | by search: features/supervision.feature l.791 scenario (supervision_answers_steps.py, briefs_hold_answers) | read + probe 2 |
| scripts/supervise.py:section l.110-123 | writes worker Questions with `\n` continuation indent; a VT in a question is not checked | r15 names answers only: out of scope, but the same reader splits on it | by search: supervision scenarios that write Questions (supervision_given.py) | read |
| scripts/migrate_upgrade_answers.py (`plan`, l.16) | renames `## Rulings` to `## Answers`, free text left as it is | a 0.24.0 Rulings answer with a VT stays, and is split by `held` | by search: tests/scripts/test_migrate_upgrade_answers.py, tests/scenarios/migration_upgrade_answers_steps.py | read |

## 4. Tests the requirements make impossible to keep

Searched by search (no map) over `tests/` for old-behaviour assertions: `x0b|x0c|x85|u2028|u2029|U\+|splitlines|one line|not awaiting-answer|answer_lines|held(|Rulings`.
- No test asserts that a VT, FF, NEL, LS or PS answer lands. None asserts the order of refusals for a multi-line answer.
- The answer nodes in `tests/scenarios/test_work_queue.py` are the accepted ones (collect-only: 9 nodes with "answer" in the name). The `answer` row of the retry/withdraw table (l.186-190, "Use the first reading") is plain text and keeps passing.
- `tests/scenarios/test_supervision.py:217-220` (`section(text, "Answers").splitlines()`) asserts LF-only answers; it still passes, since its answers hold no break.
- `tests/scenarios/supervision_answers_steps.py` and feature l.791 use plain-text answers; they keep passing.
- `tests/scripts/test_migrate_upgrade_answers.py` tests only the migration's plan on log lines; not affected.
- none that can no longer pass as written.

## 5. A step the work-item skips

The new refusal is a check in `answer()` before `workqueue.committed` (`workqueue_answer.py:44`). The existing way runs these before writing:
- `workqueue.find` (refuses a missing item; run: "there is no work-item w9"),
- `agrees` (refuses a non-awaiting-answer item; run: "w1 is not awaiting-answer"),
- `asked_from` (refuses an awaiting-answer item with no log transition; run: "log.jsonl gives no transition").
If the one-line check is moved above these (the ordering r15 asks), a two-line answer to a ready or log-less item is refused by the line check instead. Refusals only these steps produce, for multi-line answers: "not awaiting-answer" and "no transition" (run).

Effects only `committed` produces (run, probe 1 first attempt): the commit refusal "git commit failed: Author identity unknown"; the files are put back, 1 commit left. Effects only `move` produces: the log line `before: awaiting-answer, after: ready, by: work answer` and the status line (run).

The migration path (`migrate_upgrade_answers.plan`) writes `## Answers` by rename, without any check: read.

## 6. Defects

### D1. Breaks VT, FF, NEL, LS, PS land in an answer
Repro: `work --root <repo> answer w1 "line one<VT>line two"` on a w1 awaiting-answer (log: claimed→awaiting-answer).
Came back: rc 0, `w1 ready`; w1.md `## Answers` `- 2026-10-23: line one\x0bline two`; log last line `awaiting-answer -> ready`. Same for U+000C, U+0085, U+2028, U+2029 (run). r15 says these are refused.

### D2. An answer with a VT and "- " splits into two bullets; the reader pairs the wrong answer
Repro: as D1 with text `first<VT>- second answer` on a w1 with two `## Questions`.
Came back: rc 0; `## Answers` `- 2026-10-23: first\x0b- second answer`. `str.splitlines` gives `['- 2026-10-23: first', '- second answer']`. `supervise.Run.answer_lines` (probe 2) pairs Q2 with `answer one` and drops the second answer (run).

### D3. A two-line answer to a non-awaiting-answer item is refused for the wrong reason
Repro: `work --root <repo> answer w1 "line one\nline two"` with w1 `ready`, no log.
Came back: rc 1, `work: w1 is not awaiting-answer; work answer answers only an awaiting-answer work-item` (run). r15's scenario requires "an answer is one line" first.

Reported, not a defect under r15: an empty answer `""` lands as `- 2026-10-23: `.

## Questions for the plan (both readings)
- FS, GS, RS (U+001C-U+001E): not in r15's list. Python's `str.splitlines` splits on them, so a check written with `splitlines()` would refuse them; a check on the seven listed would let them land. Both readings: (a) the seven only; (b) also these three.
- `work add` (title and fields) keeps the LF/CR-only check: in scope or not?

## 7. The file set

Production:
- `scripts/workqueue_answer.py` (45 lines, room 255): the check for all seven breaks, before `agrees` and `asked_from`. Found: read, probes 1-2.
- `scripts/workqueue.py` (262 lines, room 38): only if the break set is shared with `add`; not needed for the accepted scenarios. Found: read.
- `scripts/work` (80 lines, room 220): no change needed (answer dispatch at l.41; `Refused` exits 1 at l.74-76). Found: read.

Tests:
- `tests/scenarios/work_queue_answer_steps.py` (27 lines, room 273): the When with `broken by {line break}`, mapping the 8 names to their characters. Found: `StepDefinitionNotFoundError` runs.
- `tests/scenarios/test_work_queue.py` (282 lines, room 18): no edit needed; it imports the answer steps (`from .work_queue_answer_steps import *`, l.21). Keeps passing: the deprecated node (run).

Modules on the change's path, unchanged:
- `scripts/supervise.py` (218 lines, room 82): the reader of Answers (`held`), unchanged unless the plan extends the fix to existing files (D2).
- `scripts/supervise_brief.py` (110 lines, room 190): `answer_lines`, reads through `held`.
- `scripts/migrate_upgrade_answers.py` (43 lines, room 257): renames `## Rulings`; writes no check.
