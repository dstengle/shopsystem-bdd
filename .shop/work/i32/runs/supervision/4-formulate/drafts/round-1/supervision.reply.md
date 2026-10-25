## Coverage

| id | line | scenario |
|---|---|---|
| r118 | "**Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item with an answer that asks for a change, `work run` shall transition the work-item to `ready`." | under a delegation, an answer to a reviewer's question that asks for a change returns the work-item to ready |
| r119 | "**Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item with an answer that accepts the work-item as it is, `work run` shall transition the work-item to `done`." | under a delegation, an answer to a reviewer's question that accepts the work-item as it is transitions the work-item to done |

## Questions

None. Neither line admits two readings.

## Cases no line mentions

- How `work run` tells whether a session's answer asks for a change or accepts the work-item. No line says what in the session's result marks this. The scenarios state the kind of answer in a Given.
- A session's answer to a reviewer's question that neither asks for a change nor accepts the work-item as it is, or that does both.
- A work-item with more than one reviewer's question, where one answer asks for a change and another accepts the work-item. No line says which transition wins, or whether `work run` waits until every question has an answer.
- A reviewer's question that the session leaves for the person (r77). No line says the work-item then stays `awaiting-answer`. The r77 outline shows this only for a question that is not a reviewer's.
- After the transition to `done`, r2 starts the reviewer again, and it could ask the same question again. No line stops that loop.

## Drafts

- /tmp/work-run-i32-_6c6pt8f/supervision-4-formulate/.shop/scratch/4-formulate/drafts/round-1/supervision.feature
