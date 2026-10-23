# Research of w105: `work answer` refuses every Unicode mandatory line break (work-queue#r15)

Tools: plugin 0.24.0 `scripts/tools`. `tools refs` ran by name (`asked_from`, `ASKED_FROM`, `answer`). `tools tests-of` has NO map ("no map: make one with tools map"); I did not run `tools map` (it runs the whole suite). So every test list below is `by search`, and `tests-of` is unavailable.
Scratch: `.shop/scratch/w105-1-research/` (probe_answer.py). `git status --porcelain` empty at start and end; the scratch dir is ignored, nothing to remove.
Run probes with `-n 0`: pytest.ini adds xdist, which hides printed output otherwise.

Accepted scenarios (features/work-queue.feature, @r15):
- S1 `answer with a newline in it is refused, and nothing changes (deprecated)` (line 213; tagged @r15 @deprecated)
- S2 `answer with a line break in it is refused, and nothing changes` (Outline, line 223; 7 examples)
- S3 `an answer of two lines to a work-item not awaiting-answer is refused as more than one line first` (line 241)

## 1. Why each scenario is red today

Test ids from `python3 -m pytest -q --collect-only tests/scenarios/test_work_queue.py` (9 ids for the 3 scenarios).

- S1: GREEN today. Run: `python3 -m pytest -q "tests/scenarios/test_work_queue.py::test_answer_with_a_newline_in_it_is_refused_and_nothing_changes_deprecated"` -> 1 passed. It passes because workqueue_answer.py:29 refuses LF. Keep it green (see part 4).
- S2, example `a newline`: RED. Run: `... ::test_answer_with_a_line_break_in_it_is_refused_and_nothing_changes[a newline]` -> `StepDefinitionNotFoundError: When "the session runs \`work answer w1\` with an answer of two lines broken by a newline"` (feature line 226).
- S2, `U+000B, the vertical tab` and `U+2029, the paragraph separator`: RED, same error with the `broken by <line break>` text. Run for those two. The other four (U+000C, U+000D, U+0085, U+2028) were not run; `read`: the same undefined step, since no step matches `broken by`.
- S3: RED. Run: `... ::test_an_answer_of_two_lines_to_a_workitem_not_awaitinganswer_is_refused_as_more_than_one_line_first` -> StepDefinitionNotFoundError for "...broken by a newline" (feature line 244).
  - Missing step: tests/scenarios/work_queue_answer_steps.py has only "with an answer of two lines" (exact text, LF).
  - Missing code: even with the step, the code refuses first with the wrong text. workqueue_answer.py:26-27 checks awaiting-answer before the line-break check at :29. Probe `ready_lf` (part 2) shows "w1 is not awaiting-answer", not "an answer is one line".
- Missing behind the S2 steps, all `read`: no step in tests/scenarios/work_queue_answer_steps.py or test_work_queue.py maps "broken by <line break>" to the seven characters.
- Code gap for S2: workqueue_answer.py:29 tests only `"\n" in text or "\r" in text`. It lacks U+000B, U+000C, U+0085, U+2028, U+2029 (probe: they are accepted).

## 2. What the system answers today (probes)

Probe file: `.shop/scratch/w105-1-research/probe_answer.py`. Command: `python3 -m pytest -q -s -n 0 .shop/scratch/w105-1-research/probe_answer.py`. Each case makes a fresh git repo in the scratch dir, one work-item w1 (`status` as shown; log.jsonl with `claimed -> awaiting-answer` unless shown), then runs `python3 <worktree>/scripts/work --root <repo> answer w1 "<text>"`. `run`.

| case | status (log) | answer | rc | stdout / stderr | files changed; commits |
|---|---|---|---|---|---|
| baseline | awaiting-answer (log) | `plain answer` | 0 | `w1 ready` | w1.md, log.jsonl; 1 -> 2 |
| lf | awaiting-answer | `line one\nline two` | 1 | `work: the answer has a newline in it; an answer is one line` | none; 1 -> 1 |
| cr | awaiting-answer | `line one\rline two` | 1 | same message | none |
| vt | awaiting-answer | `line one\x0bline two` | 0 | `w1 ready` | w1.md, log.jsonl; 1 -> 2; file gets `- 2026-10-23: line one<VT>line two` |
| ff | awaiting-answer | `line one\x0cline two` | 0 | `w1 ready` | as vt |
| nel | awaiting-answer | `line one\x85line two` | 0 | `w1 ready` | as vt |
| ls | awaiting-answer | `line one line two` | 0 | `w1 ready` | as vt |
| ps | awaiting-answer | `line one line two` | 0 | `w1 ready` | as vt |
| trailing_lf | awaiting-answer | `plain\n` | 1 | `an answer is one line` message | none |
| ready_lf | ready (no log) | `line one\nline two` | 1 | `w1 is not awaiting-answer; work answer answers only an awaiting-answer work-item` | none |
| ready_vt | ready | `line one\x0bline two` | 1 | same `not awaiting-answer` | none |
| ready_plain | ready | `plain answer` | 1 | same | none |
| awaiting_no_log_lf | awaiting-answer (no log.jsonl) | `line one\nline two` | 1 | `log.jsonl gives no transition of w1 to awaiting-answer; ...` | none |

All cases above: `run`. Reading (`read`): workqueue_answer.py:28 `asked_from` runs before the line-break check at :29, which is why awaiting_no_log_lf refuses on the log, not the line break.

Scenario Givens and Whens against today's code:
- S2 awaiting-answer, LF/CR: refused as the scenario wants (lf, cr). Other five separators: accepted and written (defect D1).
- S3 ready, two lines: refused, but for the wrong reason (ready_lf, defect D2).

Nearest cases not in the scenarios:
- A two-line answer to an awaiting-answer work-item with no log line: refused on the log, not "one line" (awaiting_no_log_lf).
- Existing `## Answers` section: `read` only (workqueue_answer.py:35-41 inserts after the last bullet of the section); not probed.

## 3. Old assumptions

The old form: an answer's line breaks are LF and CR only, and the status check comes before the break check.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_answer.py:answer, line 29 | refuses `\n` and `\r` only | must refuse all seven (LF, VT, FF, CR, NEL, LS, PS) with "an answer is one line" | test_answer_with_a_newline_in_it_is_refused_and_nothing_changes_deprecated (by search; run: passes) | read; probe vt/ff/nel/ls/ps |
| scripts/workqueue_answer.py:answer, lines 26-27 | awaiting-answer check first | the line-break refusal comes first (S3) | none (by search: no test asserts "not awaiting-answer" for an answer with a break) | read; probe ready_lf |
| scripts/supervise.py:held, line 199 | `section.splitlines()` splits the Answers section on the seven breaks plus U+001C–U+001E; continuation lines fold into the bullet | `work answer` will write no seven-break answers; U+001C–U+001E still split (not in r15's list) | none (by search: tests/scenarios/supervision_answers_steps.py, supervision_faults_steps.py, supervision_given.py use plain answers) | read |
| scripts/supervise_brief.py:55-62 (answer pairs for the worker) | pairs the n-th Answers bullet with the n-th Questions bullet | one bullet per answer holds once seven-break answers are refused | none (by search; plain answers only) | read |
| scripts/workqueue.py:79-83, `add` title and field check | refuses `\n` and `\r` only | not changed by r15 (r15 is about answers); same gap, a title may hold VT, LS | tests/scripts/test_work_add_title.py (by search; LF/CR title only) | read |

## 4. Tests the requirements make impossible to keep

`tests-of` unavailable (no map). By search:
- test_answer_with_a_newline_in_it_is_refused_and_nothing_changes_deprecated (test_work_queue.py): passes now; still passes after the change, since LF is still refused with the same text. Verified by run.
- work_queue_answer_steps.py `answer_of_two_lines` (LF text "line one\nline two") and `refuses_multiline_answer`: still pass after the change.
- No test asserts that VT/FF/NEL/LS/PS is accepted (grep for `x0b|x0c|u2028|u2029|x85`: none in tests/).
- No test asserts "is not awaiting-answer" for a two-line answer (grep: none).
- Result: none can no longer pass as it is. Sound: the two tests above, and test_work_add_title.py (r1/r7, unaffected).

## 5. A step the work-item skips

- Only `work answer` writes a `## Answers` section: grep `## Answers` and `workqueue_answer` finds only workqueue_answer.py:35-41; migrate_upgrade_answers.py renames the heading only (`read`). So no other path skips the check.
- Moving the break check before the status check is the requirement's ruling (S3), not a skipped step. Effects only the `answer` status check produced (the "not awaiting-answer" refusal) now come second for two-line answers: `read`, probe ready_lf shows the refusal as it stands.
- Nothing else: none.

## 6. Defects

D1: `work answer` accepts a VT, FF, NEL, LS or PS, and writes it into the work-item.
- Command: `python3 <wt>/scripts/work --root <repo> answer w1 "line one\x0bline two"` (and the same with \x0c, \x85,  ,  ) on an awaiting-answer w1.
- Came back: `w1 ready`, rc 0; w1.md gains `- 2026-10-23: line one<VT>line two`; log.jsonl gains a line; one commit added. Probe cases vt, ff, nel, ls, ps. `run`.
- Expected by r15: refused, "an answer is one line", nothing changed.

D2: a two-line answer to a work-item not awaiting-answer gets the "not awaiting-answer" refusal, not the one-line refusal.
- Command: `work answer w1 "line one\nline two"` on a ready w1.
- Came back: `work: w1 is not awaiting-answer; ...`, rc 1, no change. Probe ready_lf. `run`.
- Expected by S3: "an answer is one line" first.
- Same with an awaiting-answer w1 that has no log line: refused on the log (awaiting_no_log_lf). `run`.

## 7. The file set

Must change:
- scripts/workqueue_answer.py (45 lines; room 255): `answer()` moves the line-break check before `asked_from` and the status check; the check tests the seven breaks, not `\n`/`\r`. Found by: read (lines 26-29), probes D1, D2.
- tests/scenarios/work_queue_answer_steps.py (27 lines; room 273): add the When steps "the session runs `work answer w1` with an answer of two lines broken by <line break>" (the seven example names mapped to their characters) and "...broken by a newline". Found by: search for "broken by" (none), run (StepDefinitionNotFoundError).

On the change's path, not changed:
- scripts/work (80 lines; room 220): `cmd_answer` calls `workqueue_answer.answer`; no change needed.
- scripts/workqueue.py (262 lines; room 38): `find`, `agrees`, `logged`, `move`, `committed`, `rels_of`, `read` used by answer(). Optional home for a shared break set (room 38 only); not required.
- tests/scenarios/test_work_queue.py (282 lines; room 18): imports work_queue_answer_steps via `*`; no change needed for the new steps.
- scripts/supervise.py (263 lines; room 37): reads Answers; not changed (part 3).
- scripts/supervise_brief.py (110 lines; room 190): not changed (part 3).
- features/work-queue.feature: Gherkin, no size limit; not changed.

Size: `tools size --limit 300` printed nothing (no tracked Python file over 300 lines).

## Questions for the plan (both readings given, not decided)

- S1 is listed as accepted, though tagged `@deprecated`. Reading A: it is accepted and must stay green (it does). Reading B: the model reads a `@deprecated` scenario as not counting as acceptance (features/design-model-check.feature:490), so r15's accepting scenarios are S2 and S3 only.
- S3 needs the break check before the status check; the ruling is in the scenario's Pins line (feature line 242). Only the scenario text fixes the order; r15's text does not.
