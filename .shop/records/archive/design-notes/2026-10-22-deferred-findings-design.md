# The 0.22.0 review's deferred findings (0.23.0, part 1)

Source: review-finding/2026-10-22-0-22-0-final-review (I2-I8, M1-M3), observation/2026-10-22-deferred-from-0-22-0.
The person approved this scope on 2026-10-22 and delegated the drafting decisions to the coordinator's recommendations
("work independently" to the release gate); every reading below is the coordinator's and is listed on the release gate.

## work-queue

- `work withdraw <work-item>` transitions a work-item to `withdrawn`, from any status but `claimed` and `green`
  (decision 0039's lifecycle row: "any but claimed, green → withdrawn | the person, `work withdraw`"). It is a
  transition like any other: written, logged and committed as `work retry`'s is (r4, r5, r9).
- `work retry` returns a `failed` work-item to the status that `log.jsonl` gives it in the transition into
  `failed`, as its status before. This settles r8's "the status it had before the failed stage": when the fault was the
  push after a transition's commit, the work-item returns to the status that transition made, not the one before it.

## supervision

- A fault decides the work-item's status whatever the worker's outcome: when a worker's outcome and a fault both
  apply to one stage, `work run` transitions the work-item to `failed`, and the outcome's transition (r3, r5) is not
  made.
- r10's "change nothing" is about a run that cannot start: when `work run` cannot do what it was asked, it changes
  nothing; a fault met during a stage is not that case, and is recorded as r39 and r41 say.
- r4's merge condition names r43: the work-item's scenarios pass and the whole suite passes but for the failures r43
  counts as expected.
- r5's "the tests" are the work-item's scenarios or the whole suite.
- r45 covers a worker's session that exits with an error code, or whose output holds no JSON result, as well as one
  that ends in an error or at its turn limit.
- The branch review is not a worker's stage (no work-item owns it), but it is kept as a stage is: when the branch
  reviewer's session ends, `work run` copies its directory into `.shop/work/<initiative>/runs/branch-review/<k>/`
  and commits it on the initiative branch.
- When the branch reviewer starts or ends, `work run` appends a line to `log.jsonl` as it does for a worker.
- `work run` starts no branch review when the initiative branch's head is the commit the last kept branch review
  read.
- When the push verification before the branch review fails, `work run` exits with an error, saying why, and starts
  no branch review.
- When no work-item can make a transition and a work-item is `failed`, `work run` exits with an error, printing each
  work-item's status and each fault.

## Glossary

- **fault**: a failure outside a worker's work that stops a stage: a push or git command failing, a worker changing
  a file under `.shop/work/` outside its stage directory, or a worker's session ending in an error, at its turn limit
  or without a result `work run` can read. Not: crash.
- **remote**: the remote `work run` pushes the initiative branch to: the branch's upstream remote, else `origin`.
  r35 and r38's "the repository's remote" is this.
- **work-item branch**: the branch an implementer commits a work-item's work on, from the initiative branch's head,
  merged into the initiative branch and deleted when the work-item is green.
- **failed** is reworded to use **fault**, and its committed work is "kept, and pushed when the remote takes it"
  (not "kept and pushed": the push may be the fault).
- **worker** stays "for one stage of one work-item": the branch reviewer is not a worker.

## Implementation only (no line)

- The `push verified` and merge-time `suite` lines in `log.jsonl`, and `work retry`'s and `work withdraw`'s printing
  of `<work-item> <status>`, are Implementation of supervision and work-queue.
- A failed commit of a fault's transition is reported as r10 says, not as a traceback.
