# supervision r98: formulate round 1

## Coverage

| id | line | scenario |
|---|---|---|
| r98 | "**When** `work run` starts an implementer for a work-item that an answer to the question of a work-item's reviewer returned to `ready`, `work run` shall give the implementer the reviewer's findings and the answer." | none: returned as a question (below) |

## Questions

- r98: "**When** `work run` starts an implementer for a work-item that an answer to the question of a work-item's reviewer returned to `ready`, `work run` shall give the implementer the reviewer's findings and the answer."
  - Reading 1: answering a reviewer's question puts the work-item back to `ready`, so r98 applies every time a reviewer's question is answered. That contradicts work-queue r14, which sends a work-item to `done` when its question came from a reviewer. Under this reading r14 has to change with r98, and the scenario's Given is `work answer` on a reviewer's question.
  - Reading 2: work-queue r14 stands, so the answer puts the work-item back to `done` and the reviewer runs again. Under this reading r98 applies only when the work-item gets to `ready` some other way after a reviewer's question was answered. No line names such a route, so no scenario can reach the line's condition through `work answer`.
  - Smaller point, which can be settled with the main one: "the reviewer's findings" could mean the findings of the review that asked the question, or every review of the work-item so far. "the answer" could mean only the answer to that question, or every answer the work-item has (as r57 gives).

## Cases no line mentions

- A work-item whose reviewer asked more than one question over several reviews before it got back to `ready`: which findings and answers the implementer gets.
- A reviewer that asked its question without writing a findings file (for example an outcome other than `DONE`): what "the reviewer's findings" is then.
- How r98 and r57 relate for the implementer's brief: whether the answer is written twice or once.
- An answer given under a request's delegation (an answer naming the delegation) and not by the person: whether r98 treats it the same way.

## Drafts

None written. r98 is the only line to formulate, and it is returned as a question. No other file is under /tmp/work-run-i25-3zfrxbbu/supervision-3-formulate/.shop/scratch/3-formulate/drafts/round-1/.
This reply: /tmp/work-run-i25-3zfrxbbu/supervision-3-formulate/.shop/scratch/3-formulate/drafts/round-1/supervision.reply.md
