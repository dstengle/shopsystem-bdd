# work-queue, round 1

## Coverage

| id | line | scenario |
|---|---|---|
| r14 (changed) | "When `work answer <work-item> <answer>` is run on an `awaiting-answer` work-item whose question a researcher, a planner or an implementer asked, `work` shall transition it to the status the stage that asked its question started from: `drafted` for a researcher's question, `researched` for a planner's and `ready` for an implementer's." | answer to a researcher's, a planner's or an implementer's question transitions the work-item to the status that stage started from (Scenario Outline, three rows; the old outline is kept as a deprecated scenario with a `Deprecated for:` line pointing at the new title, and its reviewer row is dropped from the new one) |
| r26 (added) | "When `work answer <work-item> <answer>` is run, with the flag saying that the answer asks for a change, on an `awaiting-answer` work-item whose question a reviewer asked, `work` shall transition the work-item to `ready`." | answer that asks for a change, to a reviewer's question, transitions the work-item to ready |
| r27 (added) | "When `work answer <work-item> <answer>` is run, with the flag saying that the answer accepts the work-item as it is, on an `awaiting-answer` work-item whose question a reviewer asked, `work` shall transition the work-item to `done`." | answer that accepts the work-item as it is, to a reviewer's question, transitions the work-item to done |
| r28 (added) | "If `work answer <work-item> <answer>` is run without the flag saying whether the answer asks for a change or accepts the work-item as it is on an `awaiting-answer` work-item whose question a reviewer asked, then `work` shall exit with an error, saying that the answer must say which, and change nothing." | answer to a reviewer's question that says neither whether it asks for a change nor whether it accepts the work-item is refused, and nothing changes |

## Questions

None. Each of the four lines has only one reading.

## Cases no line mentions (no scenario written)

- An answer to a reviewer's question that says both that it asks for a change and that it accepts the work-item as it is.
- An answer to a researcher's, a planner's or an implementer's question that says it asks for a change or accepts the work-item as it is: does the flag get ignored or refused?
- The asks-for-a-change or accepts flag given to `work answer` on a capability-proposal (r24) or through `<initiative>/<name>` (r30).
- An answer to a reviewer's question that has a line break in it and no flag: which refusal comes first, r15's or r28's. (r15's existing scenario gives the one-line refusal first only against "not awaiting-answer".)
- Whether the `## Answers` entry r13 writes for a reviewer's question records which way the answer went.

## Drafts

- /tmp/work-run-i25-3zfrxbbu/work-queue-3-formulate/.shop/scratch/3-formulate/drafts/round-1/work-queue.feature
- /tmp/work-run-i25-3zfrxbbu/work-queue-3-formulate/.shop/scratch/3-formulate/drafts/round-1/work-queue.reply.md
