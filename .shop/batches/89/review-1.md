---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-89/review-1
kind: review
batch: batch-89
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/112
head: 7bf0cdbf3dc3a79925d3790d099785d0b382b865
range: 8056c8d665660d043949296a0fa51eb63b63eccf..7bf0cdbf3dc3a79925d3790d099785d0b382b865
result: clean
---

# batch-89 review 1

## Verdict

All three items are built and every run in `## Runs` exits 0. There is nothing to fix now, and two observations are recorded.

- **b583 (drafting#r65):** `add_line_to` (scripts/backlog_lines.py:91-94) now puts a line with no `--in` into the item's existing group of the same title. It opens a new group only when the item has none of that title. The scenario handler checks that the committed item holds one group of work-queue with both lines. In `tests/scripts/test_backlog_reword.py`, the `--retires` line now gets a `--group` of its own. That keeps the test's subject (removing a line, its group and the id it retires), and its assertions are just as strict, so the test is not weakened.
- **b569 (consistency#r43):** the new world row is a test that can fail. r1's response request is made by the decisions service, and r3 is triggered on the person's request. If the chain followed r1's request to r3 anyway, r2's Then would be entailed and `spec logic` would report an L8.
- **b584 (chore):** the commit touches only `tests/scripts/test_cpu_budget.py`, and the test is marked `budget`.

The batch follows the module map: a new row was added for `tests/scenarios/drafting_handlers_group.py` and the `scripts/backlog_lines.py` row was updated. No judgement decision is contradicted, and the change is well under the size limit.

## Findings

### f1 Minor observation: b569 adds no code; the behaviour was already there from b545
- item: b569
- where: scripts/spec_entail_chain.py:89
Commit 8cf0711df is titled "spec logic follows a response's request to no line of a different requester", but it changes only tests/scenarios/design_model_check_worlds_chain.py, tests/scenarios/requested.py and the item's model and vocabulary lines. I checked whether a chain could reach a line of a different requester. It cannot. `_premise` rewrites a chained line's trigger `ev(Q,req,<key>,D,X)` to `evC(Q,k-1,Ereq,D,X,S), covers(<key>,Ereq)`, so the requester `D` must unify with the doer of the forced request. That code came with b545 and `covers` (lines 46-50) does not need to compare requesters. The line is met and the new row does test it. This is recorded so the item's history is clear: b569 contributed a scenario and its words, not a change to the entailment check.

### f2 Minor observation: r65's scenario handler does not model the requirement group r3
- item: b583
- where: tests/scenarios/drafting_handlers_group.py:313
The Given "the requirement group r3 does not have the group title g1" and the Then "does not keep the requirement group r3" are both handled as "the committed item holds exactly one group, titled with the item's title". That check does fail if the old behaviour comes back (a second group with the same title), so it guards the line. But r3 itself is never made or looked for. A more faithful Then would also check that no group's title differs from g1.
