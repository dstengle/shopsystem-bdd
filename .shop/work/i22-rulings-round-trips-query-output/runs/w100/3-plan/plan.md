# Plan of w100: branch review 1's fixes

This plan replaces the plan in runs/w100/2-plan, which stopped on the Retires question. The work-item now has a `## Retires` section, and its Answers say to use Reading A (2026-10-23). So the plan now also covers M1, M2 and I2.

## 1. What goes green

- **work-queue#r15**: "answer with a newline in it is refused, and nothing changes" (features/work-queue.feature, @r15).
  - Why it is red today: two steps have no definition (notes §1).
    - The When "the session runs `work answer w1` with an answer of two lines" (the run gives StepDefinitionNotFoundError).
    - The Then "work exits with an error, saying that an answer is one line" (read).
  - The Given already matches `with_items` and the last And already matches `both_as_they_were`.
  - The code already refuses with exactly these words and changes nothing (scripts/workqueue_answer.py:29-30; probe, notes §2).
- **Retired** (work-item `## Retires`):
  - batch-measurement @r42: "the totals are over the stages' sessions, an unended stage included, and span the first transition to the last (deprecated)".
  - work-queue @r9: "`work <command>` commits the change it makes to a work-item on the current branch (deprecated)".
  - Both have green replacements in the same feature files (w94, w91). Both files are bound by `scenarios()` (test_batch_measurement.py:14, test_work_queue.py:28), so retiring a block drops that test with it, and no binding needs to change.

Rulings from the work-item body (the coordinator, under the person's delegation, 2026-10-23):
- I2: `gives_totals` is strict again.
- The upgrade put-back catches every exception.
- The duplicate test class goes.
- The `# noqa` in measure_read.py is fixed.

## 2. Where the change lands

- `tests/scenarios/work_queue_answer_steps.py`: add the r15 When and Then. This is the researcher's set.
- `features/batch-measurement.feature`: retire the deprecated @r42 block, with `features retire` (M1, Retires).
- `features/work-queue.feature`: retire the deprecated @r9 outline, with `features retire` (M2, Retires).
- `tests/scenarios/batch_measurement_then_steps.py`: `gives_totals` asserts every token column (I2, answer A).
- `scripts/migrate_upgrade.py`: the `upgrade` put-back catches any exception (work-item body).
- `tests/scripts/test_migrate_upgrade.py`: remove the class `AVersionFileThatHoldsNoVersion`, and update the module docstring so it no longer names that case (work-item body).
- `scripts/measure_read.py`: change the `moment` line that has the `# noqa: FURB162` (work-item body).

## 3. Decisions

1. **The r15 steps go in work_queue_answer_steps.py.** test_work_queue.py has only 18 lines of room (CLAUDE.md size limit; notes §7).
   - The When runs `work answer w1` with an answer of two lines joined by a newline. It records `context["before"]` the way `run_work` does.
   - The Then asserts an error exit and that stderr says an answer is one line.
   - Rests on: work-queue#r15, and design-decision/exits-are-successful-or-errors (the step checks for "an error", not a particular exit code).
2. **What counts as a newline.** Only the `\n` and `\r` that the code refuses today. The U+2028 and form-feed defect (notes D1) is left as it is. Rests on the work-item's "Change no other behaviour".
3. **Retiring.**
   - Each retirement uses `features retire` with the exact deprecated title, never a hand edit. Rests on decision 0006 and the work-item's Retires section.
   - Retire only those two blocks. Their non-deprecated replacements with the same @r42 and @r9 titles stay.
4. **Strict `gives_totals`.**
   - Every column of the totals is asserted against the table, with none skipped when the table lacks it: stages, sessions, turns, round trips, output, new input and cache-read tokens, cost and time.
   - A table without a column is then a failure, not a pass.
   - This is how it was before w94. Rests on the I2 ruling and batch-measurement#r42.
   - The only remaining user is the live @r42 scenario (lines 134-136), which gives every column.
5. **The put-back.**
   - It catches every `Exception` raised while the steps are applied or the version commit is made.
   - It then resets and cleans as it does now, prints the same "migrate put the repository back as it was; …" message with the error, and exits with an error.
   - KeyboardInterrupt and other non-Exception signals are not part of the ruling.
   - Rests on migration-tools r15 and r20 (every change or none) and the ruling.
6. **`moment`.** Drop the `.replace("Z", "+00:00")` and its `# noqa`. On Python 3.11, `fromisoformat` reads a trailing `Z` as UTC, so the result is the same for every input. The ruling allows dropping it.
7. **The duplicate class.** Remove `AVersionFileThatHoldsNoVersion` completely (ruling). The r30 outline (`status`, `upgrade`) and the r31 hook scenario still cover these cases.

## 4. Tests the decisions break

- `tests/scripts/test_migrate_upgrade.py::AVersionFileThatHoldsNoVersion`: removed by decision 7, all three of its tests. The r30 and r31 scenarios must stay green for `status`, `upgrade` and the hook.
- The deprecated @r42 scenario and the deprecated @r9 outline (all three examples) in test_batch_measurement.py and test_work_queue.py: removed by decision 3, because their blocks are retired. Their replacements stay green.
- Decision 4 breaks nothing that stays. The only other user of the step was the deprecated @r42 scenario, whose table has no turns or round trips, and it is retired in the same change. Checked by searching features/ for "the measurement gives the totals": two uses, lines 118 and 134.
- The other decisions break nothing:
  - The r15 steps only add code, and no test asserts that a newline is accepted (notes §4).
  - Decision 5: by search, no test expects any other exception to escape `migrate upgrade`.
  - Decision 6 gives the same result for every input.

## 5. Open cases

- **A step only the retired scenario used.** `transcript_inside` in tests/scenarios/batch_measurement_given_steps.py:142 matches only the deprecated @r42 scenario (by search of features/), so the retirement leaves it unused. Similarly, `stages_sessions_took` still defaults turns and round trips when the table lacks those columns. The ruling does not name either one. The implementer reports both and says whether `tools check` (vulture) flags the unused step, and does not widen the file set without saying why.
- **The empty version file.** The removed class was the only test of an empty `.shop/plugin-version`. The r30 and r31 scenarios use only "next". The implementer says so in the report.
- **D1.** U+2028 and form feed in an answer are accepted, and then split into two bullets (notes §6). This is outside r15 as written.
- **D2.** For an item with no log line, the log check's message shadows the newline message. This is outside the scenario.
