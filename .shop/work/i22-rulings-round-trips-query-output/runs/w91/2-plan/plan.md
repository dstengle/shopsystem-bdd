# Plan of w91: `work answer`, and the status awaiting-answer

Accepts work-queue#r9, #r13, #r14. Rests on decisions 0039 (work-item-lifecycle-as-run), 0063 (a-ruling-returns-to-the-asking-stage), 0064 (answers-not-rulings), work-retry-reads-the-log. The work-item has no `Retires` section and no `## Rulings`/`## Answers`.

One question is open (see the result's `questions`): whether this work-item renames `awaiting-ruling` in `work run` (supervise) now. The plan below gives what both readings share, and what each one adds.

## 1. What goes green

- **work-queue#r9**, "`work <command>` commits the change it makes to a work-item on the current branch": the `answer` example is red. Its Given fails with a ValueError at test_work_queue.py:70, because `with_items` cannot read the clause "its question asked by an implementer". There is also no `work answer` subcommand: argparse rejects it with exit 2. The add, retry and withdraw examples pass today and must keep passing.
- **work-queue#r13**, "answer on an awaiting-answer work-item writes the answer with the date under the work-item's Answers": red. Its Then (feature line 213) has no step definition, and `work answer` does not exist.
- **work-queue#r14**, "answer on an awaiting-answer work-item transitions it to the status the asking stage started from" (researcher, planner, implementer, reviewer): all 4 examples are red in the same Given (test_work_queue.py:70). The transition also does not exist, and `awaiting-answer` is in neither status set.
- **Deprecated**: the r9 outline "`work <command>` commits … (deprecated)" passes today and must keep passing. This work-item retires no scenario (it has no Retires section).

## 2. Where the change lands

Under both readings:
- `scripts/work`: a new `answer` subcommand that takes the work-item id and the answer text, set up the way `withdraw` is.
- `scripts/workqueue_answer.py` (new): the answer path. It checks that the status is `awaiting-answer`, checks r6 agreement, finds the asker's start status from the log, writes the dated answer under `## Answers`, then makes the transition and writes the log line through `workqueue.committed`. It is a new module because workqueue.py has only 45 lines of room, and because the answer path is a new concern (CLAUDE.md).
- `scripts/workqueue.py`: the status set gains `awaiting-answer`. Any shared helper the answer module needs is exposed here only if that fits in the room left.
- `scripts/model_work.py`: the work-item status set gains `awaiting-answer`.
- `CLAUDE.md`: a module-map row for `scripts/workqueue_answer.py` (CLAUDE.md requires one for each new module).
- `tests/scenarios/test_work_queue.py`: `with_items` stops treating a trailing ", its question asked by …" clause as a work-item. It has 23 lines of room, so the new steps go in a new module, imported the way the other work_queue_*_steps modules are.
- `tests/scenarios/work_queue_answer_steps.py` (new): the Given with the asker clause, which writes w1 as `awaiting-answer` plus its log.jsonl line into `awaiting-answer` from the asker's start status. It also holds the r13 Then, which reads the `## Answers` section for the text and today's date.

Reading A only (rename in `work run` now): `scripts/supervise.py` (lines 156, 237, 245; `questions()` reads `## Answers`), `scripts/supervise_merge.py` (lines 88, 106), and the supervision tests in part 4. `awaiting-ruling` leaves both status sets.

Reading B only (`work run` keeps the old name until w92): both status sets keep `awaiting-ruling` next to `awaiting-answer`, and no supervise file changes.

Out of the set under both readings: `scripts/measure_build.py`, `scripts/measure_show.py` and `scripts/measure`. The measure rename is batch-measurement#r41, which belongs to w94. The researcher listed them; I removed them.

## 3. Decisions

1. **The asker is read from the log.** `work answer` takes the `before` of the work-item's last log.jsonl line, which must be its transition into `awaiting-answer`. It returns the work-item to that status, with one mapping: `claimed` returns to `ready`. Researcher, planner and reviewer questions leave from `drafted`, `researched` and `done`. An implementer's question leaves from `claimed`, and the implementer's stage starts at `ready` (0039: ready → claimed by the implementer). This rests on work-queue#r14, decision 0063 and design-decision/work-retry-reads-the-log (r8 reads `before` the same way). Nothing is added to the work-item's file.
2. **No asker means a refusal.** If there is no log line into `awaiting-answer`, or its `before` is none of `drafted`, `researched`, `claimed`, `done`, `work answer` refuses and changes nothing. This rests on work-queue#r7, since the r14 transition cannot be made.
3. **Status and agreement are checked before any write.** `work answer` on a work-item that is not `awaiting-answer` is refused before anything is written (work-queue Implementation, r7). The r6 agreement check runs before any write too (work-queue#r6).
4. **One commit.** The answer and the transition land in one commit holding the work-item's file and its log line, made through `workqueue.committed` (work-queue#r9). The section is written before the log line, as the Implementation note says ("the log line last"). A failure restores the file, as `move` and `committed` already do.
5. **Each new answer is added to the end of `## Answers`.** If the work-item has no such section, it is created at the end of the file (work-queue#r13, decision 0064 for the heading). `work answer` does not import supervise: the section writer lives in the new module.
6. **Test data for r13.** The r13 Given ("w1 is awaiting-answer", no asker) is still matched by `with_items`, so it writes no log line. Under decision 2 that would be refused. So for an `awaiting-answer` item, `with_items` also writes a log line into `awaiting-answer` from `researched`. This only makes the Given consistent with the lifecycle (0039) and asserts nothing the scenario does not say.
7. **The supervise rename is a QUESTION** (see the result's `questions`). It touches the status `work run` writes and the section `questions()` reads.

## 4. Tests the decisions break

Under both readings:
- tests/scenarios/test_work_queue.py `with_items`: red today for the r9 answer example and for r14. It is changed as in part 2 so that it no longer takes the asker clause as a work-item, and it writes the log line of decision 6. The scenarios that already use it are unchanged: none of them has an awaiting status.
- tests/scripts/test_work_withdraw.py, test_work_items.py, test_work_add_title.py: unaffected. The researcher found by search that none of them names an awaiting status or Rulings, and add, retry and withdraw do not change.
- The batch-measurement tests: unaffected, because measure is not changed.

Reading A only. These break, and the replacements belong to w92:
- test_supervision.py:108-110: the step that asserts `awaiting-ruling`. It would be rewritten to assert `awaiting-answer`. The deprecated supervision scenarios that use it (feature lines 86, 111, 139, 228-234, 250-251, 518, 696) then go red, and w91 has no Retires section to retire them.
- test_supervision.py:200-205, supervision_given.py:114-117 and supervision_faults_steps.py:125-129: they write `## Rulings` and `awaiting-ruling`. They would be rewritten to write `## Answers` and `awaiting-answer`. The deprecated scenario at supervision.feature:672-675 goes red.
- supervision_tests_steps.py:98-101: its data would be renamed to `awaiting-answer`. It runs under both names.

Reading B: no supervision test breaks.

## 5. Open cases (for the implementer to name, not to choose)

- The date format under `## Answers`, and the shape of the answer line: whether it is a bullet, and where the date goes relative to the text.
- What `work answer` prints on success: whether it prints `<work-item> <status>` the way retry and withdraw do. The scenarios do not say.
- An answer that is empty or only whitespace.
- A work-item that already has a `## Answers` section, possibly not the last section.
- The commit message: the shape `withdraw` uses would be "work answer: w1 awaiting-answer -> ready".
