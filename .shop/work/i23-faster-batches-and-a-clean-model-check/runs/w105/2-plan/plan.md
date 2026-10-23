# Plan of w105: `work answer` refuses every Unicode mandatory line break (work-queue#r15)

## 1. What goes green

work-queue#r15, scenarios in features/work-queue.feature:

- **answer with a line break in it is refused, and nothing changes** (Scenario Outline, 7 examples). Red today: the When step "the session runs `work answer w1` with an answer of two lines broken by <line break>" has no step definition (StepDefinitionNotFoundError, run by the researcher). Behind it, `answer` in scripts/workqueue_answer.py tests only LF and CR, so VT, FF, NEL, U+2028 and U+2029 are accepted, written under `## Answers` and committed (defect D1, probed).
- **an answer of two lines to a work-item not awaiting-answer is refused as more than one line first**. Red today: the same undefined step ("broken by a newline"); behind it, `answer` checks the awaiting-answer status (and the log) before the line break, so a ready w1 gets "is not awaiting-answer" instead of "an answer is one line" (defect D2, probed).
- **answer with a newline in it is refused, and nothing changes (deprecated)**: tagged `@r15 @deprecated`, green today and kept green (decision 4). The work-item has no `Retires` section, so it retires nothing.

## 2. Where the change lands

The researcher's set, unchanged:

- `scripts/workqueue_answer.py`: `answer` refuses an answer holding any of the seven mandatory line breaks, as its first check, before it finds the work-item, reads its status or its log; the refusal says that an answer is one line. Module docstring names r15 among its requirements.
- `tests/scenarios/work_queue_answer_steps.py`: one parsed When step for "the session runs `work answer w1` with an answer of two lines broken by {line break}", mapping each of the seven example names ("a newline", "U+000B, the vertical tab", ... "U+2029, the paragraph separator") to its character, taking the snapshot and running `work answer` as the existing two-lines step does.

Not changed (on the path, read by the researcher): `scripts/work`, `scripts/workqueue.py`, `tests/scenarios/test_work_queue.py` (already imports the steps module with `*`), `scripts/supervise.py`, `scripts/supervise_brief.py`, the feature file.

## 3. Decisions

1. **The seven breaks are exactly r15's list**: U+000A, U+000B, U+000C, U+000D, U+0085, U+2028, U+2029, and no others. U+001C–U+001E (which Python's line splitting also breaks on) are not refused; r15 names its list. Rests on work-queue#r15.
2. **The one-line check comes first of every refusal in `answer`**: before `workqueue.find`, the awaiting-answer status check and `asked_from`'s log check. Rests on the person's ruling pinned in the scenario "an answer of two lines to a work-item not awaiting-answer is refused as more than one line first" ("of several reasons to refuse an answer, the one-line refusal comes first"), and on work-queue#r7 (nothing changes). So a two-line answer to an unknown work-item, or to an awaiting-answer one with no log line, is also refused as more than one line.
3. **The refusal's text says "an answer is one line"** and no longer names only "a newline" (it covers all seven breaks); the wording around it is the implementer's, so long as it contains "an answer is one line" and no traceback. Rests on work-queue#r15 ("saying that an answer is one line") and r7.
4. **The deprecated scenario stays bound and green**: its step "with an answer of two lines" (LF) and its Then step are kept as they are; retiring it is not this work-item's (no `Retires` section). The researcher's question on whether it counts as acceptance changes nothing the narrator observes and needs no answer here. Rests on work-queue#r15.
5. **The break set lives in workqueue_answer.py**, not in workqueue.py (room 38 lines there; `work add`'s title check is not r15's and stays as it is). Rests on work-queue#r15 (answers only).

## 4. Tests the decisions break

None. Verified from the notes (part 4) and by reading the steps module:
- `test_answer_with_a_newline_in_it_is_refused_and_nothing_changes_deprecated`: LF is still refused with a message containing "an answer is one line"; still passes.
- `answer_of_two_lines` and `refuses_multiline_answer` in work_queue_answer_steps.py: unchanged, still pass; the Then step only checks the non-zero exit and "an answer is one line" in stderr, so decision 3 keeps it.
- No test asserts that VT/FF/NEL/LS/PS is accepted, nor the "not awaiting-answer" refusal for an answer with a break (researcher's grep), so decision 2 breaks none.
- tests/scripts/test_work_add_title.py is about `work add`, untouched by decision 5.

## 5. Open cases

For the implementer to name in the report, not to choose:
- An answer with a line break only at its end (e.g. a trailing LF from a shell): refused today and under the plan; no scenario says whether a trailing break should be stripped.
- U+001C–U+001E (file, group, record separators): accepted under r15's list, yet `held` in supervise.py splits the Answers section on them, so such an answer could fold into two lines when read back.
- CR LF as one break: refused like any other; no scenario distinguishes it.
- An empty answer or one of only a line break: no scenario.
- `work add` titles still accept VT, FF, NEL, U+2028, U+2029 (workqueue.py:79-83); not r15's.
