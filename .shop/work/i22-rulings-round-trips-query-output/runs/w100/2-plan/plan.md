# Plan of w100: branch review 1's fixes

Outcome: QUESTION. The plan below covers everything except the two retirements (M1, M2) and the follow-up to M1 (I2). The work-item says to list those two scenarios under a `## Retires` section, but it has no such section. Without one, the implementer may not run `features retire` (design-decision 0006, agents/bdd-implementer.md), and a reviewer would mark the change Critical.

## 1. What goes green

- **work-queue#r15**: "answer with a newline in it is refused, and nothing changes" (features/work-queue.feature, @r15).
  - Red today because two steps are undefined (notes §1).
    - The When "the session runs `work answer w1` with an answer of two lines" has no definition (StepDefinitionNotFoundError, run).
    - The Then "work exits with an error, saying that an answer is one line" has no definition either (read).
  - The Given and the last And already match `with_items` and `both_as_they_were`.
  - The code already refuses, with these exact words, and changes nothing (scripts/workqueue_answer.py:29-30; probe, notes §2).
- **Retired scenarios**: none, because the work-item has no Retires section. M1 (batch-measurement @r42 deprecated scenario) and M2 (work-queue @r9 deprecated outline) wait on the question.

The work-item's other fixes, from its body (the coordinator's answers, 2026-10-23, under the person's delegation), are taken as rulings:
- **Put-back.** Any exception of an upgrade step puts back every change (migration-tools r15, r20).
- **Duplicate test class.** Remove `AVersionFileThatHoldsNoVersion`.
- **The `# noqa`.** Fix the comment in measure_read.py.

## 2. Where the change lands

- `tests/scenarios/work_queue_answer_steps.py` (13 lines): add the r15 When and Then. The researcher's set.
- `scripts/migrate_upgrade.py`: the `upgrade` put-back catches any exception, not only CalledProcessError and OSError. Added by the work-item's body.
- `tests/scripts/test_migrate_upgrade.py`: remove the class `AVersionFileThatHoldsNoVersion`, and change the module docstring so it no longer names the version-file case. Added by the work-item's body.
- `scripts/measure_read.py`: the `moment` line with the `# noqa: FURB162`. Added by the work-item's body.

These are left out until the question is answered: features/batch-measurement.feature, features/work-queue.feature (the retirements, done with `features retire`) and tests/scenarios/batch_measurement_then_steps.py (I2).

## 3. Decisions

1. **Where the r15 steps go.** They go in work_queue_answer_steps.py, not in test_work_queue.py, which has only 18 lines of room (CLAUDE.md size limit; notes §7).
   - The When runs `work answer w1` with an answer of two lines joined by a newline.
   - It records `context["before"]` the same way `run_work` does, so that `both_as_they_were` can compare.
   - The Then asserts that the command exited with an error and that its stderr says an answer is one line.
   - Rests on work-queue#r15, r7 and design-decision/exits-are-successful-or-errors (the step checks "an error", not a particular exit code).
2. **Which answers count as a newline.** Only the `\n` and `\r` that workqueue_answer.py refuses today. The U+2028 / form-feed case (notes D1) stays as it is. Rests on the work-item's "Change no other behaviour".
3. **What the put-back catches.** Every `Exception` raised while the steps are applied or while the version commit is made. It then resets and cleans as it does now, prints the same "migrate put the repository back as it was; …" message with the error, and exits with an error. Rests on migration-tools r15 and r20 (every change or none) and the work-item's ruling. KeyboardInterrupt and other non-Exception signals are not part of the ruling.
4. **The `Z` replacement in `moment`.** Drop the `.replace("Z", "+00:00")` and its `# noqa`. From Python 3.11, `datetime.fromisoformat` reads a trailing `Z` as UTC, so the function gives the same answer for every input. The work-item allows either option.
5. **Removing the duplicate test class.** Remove `AVersionFileThatHoldsNoVersion` completely, per the work-item's ruling. The migration-tools r30 outline (`status`, `upgrade`) and the r31 hook scenario keep covering these cases.

## 4. Tests the decisions break

- `tests/scripts/test_migrate_upgrade.py::AVersionFileThatHoldsNoVersion`: removed by decision 5 (all three tests). The r30 and r31 scenarios must still pass afterwards, for both `status` and `upgrade`, and for the hook.
- The other decisions break nothing:
  - The r15 steps only add code. No test asserts that `work answer` accepts a newline (notes §4).
  - Decision 3: by search, no test expects an exception other than CalledProcessError or OSError to escape `migrate upgrade`. The only "Traceback" checks are `assertNotIn` (test_migrate_upgrade.py, test_migrate_upgrade_ids.py).
  - Decision 4: same answer for every input. Any test of `moment` with a `Z` time stays green on 3.11.

## 5. Open cases

- **The empty version file.** The removed class also checked a `.shop/plugin-version` that holds nothing ("nothing" in the message). The r30 and r31 scenarios use only "next". Once the class is gone, no test covers the empty-file case. The implementer says so in the report.
- **D1 (notes §6).** `work answer` accepts U+2028 and form feed, and `supervise.held` then splits that one answer into two bullets. This is not part of r15 as written and is left for a later line. The implementer leaves it alone.
- **D2.** For an item with no log line, the log check comes before the newline check, so that error message shadows the newline one. This is outside the scenario, which has the log line.
