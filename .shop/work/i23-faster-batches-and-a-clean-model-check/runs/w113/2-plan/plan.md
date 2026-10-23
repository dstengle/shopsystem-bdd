# Plan of w113: work answer refuses every Unicode mandatory line break

Work-item accepts work-queue#r15. Planned from `runs/w113/1-research/notes.md`.

## 1. What goes green

work-queue#r15, in `features/work-queue.feature`:

- **Scenario Outline "answer with a line break in it is refused, and nothing changes"** (7 examples). Red today: all 7 fail with `StepDefinitionNotFoundError` on the When "with an answer of two lines broken by <line break>"; `tests/scenarios/work_queue_answer_steps.py` has no such step. Once the step exists, "a newline" and U+000D would pass (LF and CR are refused today at `scripts/workqueue_answer.py` line 29). The other 5 would still fail their Then: `work answer` exits 0 for U+000B, U+000C, U+0085, U+2028 and U+2029, and the answer lands, with w1 moved to ready (notes: probe 1, D1).
- **Scenario "an answer of two lines to a work-item not awaiting-answer is refused as more than one line first"**. Red today: the same missing When step. Behind that, `answer()` checks the status (`agrees`) and the log (`asked_from`) before the line check, so a ready w1 is refused with "w1 is not awaiting-answer" instead of "an answer is one line" (notes: probe 2, D3).

Retired: "answer with a newline in it is refused, and nothing changes (deprecated)" (@r15). It passes today. The work-item's `## Retires` lists it under delivery#r17, so it is removed with `features retire` (design-decision/held-scenarios). Its own When step goes with it (see 2).

## 2. Where the change lands

- `scripts/workqueue_answer.py`: the one-line check covers exactly the seven code points r15 lists. It moves to the start of `answer()`, ahead of `workqueue.find`, `agrees` and `asked_from`. The refusal still says that an answer is one line.
- `tests/scenarios/work_queue_answer_steps.py`: a new When step, "with an answer of two lines broken by {line break}". It maps the eight Example names ("a newline" and the seven `U+XXXX, ...` names) to their characters and runs `work answer w1` with "line one", the break and "line two". The deprecated scenario's step, "with an answer of two lines" with nothing after it, is removed, because no scenario uses it after the retire.
- `features/work-queue.feature`: only the deprecated scenario is removed, by `features retire`. This is the one exception design-decision 0006 allows. Nothing else in the file is edited.

The researcher's set, plus the feature file for the retire. Left out: `scripts/workqueue.py`, because decision D3 keeps `work add`'s check as it is. `scripts/work` needs no change: it already dispatches the answer and turns `Refused` into exit 1. `tests/scenarios/test_work_queue.py` binds the feature by `scenarios()` and imports the answer steps, so it needs no edit.

## 3. Decisions

- **D1. The break set is the seven code points r15 lists: U+000A, U+000B, U+000C, U+000D, U+0085, U+2028 and U+2029.** The researcher asked about FS, GS and RS (U+001C-U+001E). They are not refused, so an answer holding one still lands. This rests on work-queue#r15, which names the set exactly as "Unicode's mandatory line breaks" and lists its members. FS, GS and RS are not in that list, and they are not mandatory breaks in Unicode's line-breaking classes either. So the check tests membership in the seven. It does not use `str.splitlines`, which would refuse three code points r15 does not name. The reader-side risk this leaves (`supervise.held` splits on FS, GS and RS) is in part 5.
- **D2. The one-line check runs first in `answer()`, before any other reason to refuse**, including a missing work-item, a work-item not awaiting-answer and a log with no transition. It rests on work-queue#r15 and on the person's ruling the accepted scenario pins: "of several reasons to refuse an answer, the one-line refusal comes first". Nothing is read or written before the check, so "change nothing" (r15, r7) holds.
- **D3. `work add`'s LF/CR check on the title and on `--part-of`, `--under` and `--accepts` (`scripts/workqueue.py` add) stays out of scope and unchanged.** r15 names only the answer given to `work answer`, and this work-item accepts only r15. The researcher's second question is settled by that.
- **D4. The refusal's wording is open as long as it says that an answer is one line** (work-queue#r15). Today's text, "the answer has a newline in it", would be wrong for a VT or a U+2028. The implementer words it to fit every break in the set, for example by naming the kind of break or just saying "line break".

## 4. Tests the decisions break

None. Checked against notes part 4, a search of `tests/` with no coverage map:
- No test asserts that a VT, FF, NEL, LS or PS answer lands, and none asserts the order of refusals for a multi-line answer.
- `tests/scenarios/test_supervision.py` lines 217-220, `tests/scenarios/supervision_answers_steps.py` and `tests/scripts/test_migrate_upgrade_answers.py` use answers with no break in them, so D1 and D2 do not touch them.
- In `test_work_queue.py`, the `answer` row of the retry/withdraw table is plain text and keeps passing.
- `work add`'s tests (`work_queue_add_steps.py`, `tests/scripts/test_work_add_title.py`) are untouched under D3.
- The only test that goes is the deprecated scenario's node, removed by the retire (part 1). That is a retirement, not a break.

## 5. Open cases

- An answer holding FS, GS or RS lands under D1. `supervise.held` (`str.splitlines`) would then split it into two bullets and shift the question/answer pairs (the same failure as notes D2). No scenario covers this. The implementer names it in the report and does not change `supervise.py` here.
- Answers already on file from before this fix that hold a VT, FF, NEL, LS or PS, and 0.24.0 `## Rulings` text renamed by `migrate_upgrade_answers`, still split under `held`. No scenario covers this. Name it, don't fix it.
- An empty answer (`""`) lands as an empty bullet. r15 says nothing about it. Name it.
- A break at the very start or end of the answer, such as a trailing LF from a shell, is refused under D1 like any other. The scenarios only show a break between two lines. Name it if it matters.
