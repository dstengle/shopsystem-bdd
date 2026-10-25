## Coverage

This covers the lines this round changes or adds. Every other line of spec/capabilities/supervision.md keeps the scenario it already has in features/supervision.feature.

| id | line | scenario |
|---|---|---|
| r67 | "**When** a request of which this context is the upstream is `open` or `awaiting-upstream`, `work run` shall start an `initiative-round` session of the kind `intake`, given the request, that writes each line's line outcome or a question on it and passes the turn with `work turn`." | Scenario Outline: a request this context is the upstream of that is <status> is given to an intake round that writes each line's line outcome or a question on it (Examples: open, awaiting-upstream) |
| r100 | "**When** a round of the kind `intake` that `work run` started gives a question on a line of a request, `work run` shall write the question in the request." | a question an intake round gives on a line of a request is written in the request |
| r9 | "**When** no work-item can make a transition, every work-item is `green` or `withdrawn` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing each work-item's status." | when every work-item is green or withdrawn and no request whose asker is this context is in the asker's turn, `work run` exits successfully, printing each work-item's status |
| r101 | "**When** `work run` ends while a request kept in this context whose asker is this context is in the asker's turn, `work run` shall exit with an error, printing the request with its open questions." | when `work run` ends while a request whose asker is this context is in the asker's turn, it exits with an error, printing the request with its open questions |
| r82 | "**When** `work run` was started with no initiative, no node of an initiative it took can make a transition and none is `awaiting-answer` or `failed` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing the status of each initiative it took." | `work run` started with no initiative, ending with no node awaiting-answer or failed and no request whose asker is this context in the asker's turn, exits successfully, printing the status of each initiative it took |

The titles of r9, r67 and r82 change, because each line now has a new condition. The old scenarios for these lines become deprecated scenarios.

## Questions

None. No line in this round has two readings that would change a scenario. Two places come close; they are listed under the cases below.

## Cases no line mentions

- A request whose asker is this context, kept in another context's repository: r9 and r82 say "a request whose asker is this context" without "kept in this context", but r101 says "kept in this context". So no line says whether such a request stops r9's or r82's successful exit. The drafts use a request kept in this context.
- A request whose turn is the asker's but whose status is `accepted`, `delivered`, `refused` or `withdrawn`: no line says whether it counts as "in the asker's turn" for r9, r82 and r101. The drafts use only `awaiting-asker` (in the asker's turn) and `awaiting-upstream` (not in it).
- A context that is both the asker and the upstream of a request: once the intake round passes the turn (r67), the request is in the asker's turn, so under r101 that same `work run` would exit with an error. No line says whether this is intended.
- r67 says the intake round "writes" a question on a line, and r100 says `work run` writes the question the round gives. No line says which of the two puts it in the request. Only the Implementation section settles it (`work run` writes it). The r67 draft checks the round's brief and the line outcome; the question in the request is checked only in r100's scenario.
- When r101 and r32 or r52 hold at the same time (a request in the asker's turn and a work-item that is `awaiting-answer` or `failed`), no line says whether the output prints both the request and the work-items' statuses.
- A request in the asker's turn with no open question: r101 prints "the request with its open questions", and no line says what is printed when there are none.

## Drafts

- /tmp/work-run-i26-oc_xbi0g/supervision-3-formulate/.shop/scratch/3-formulate/drafts/round-1/supervision.feature
- /tmp/work-run-i26-oc_xbi0g/supervision-3-formulate/.shop/scratch/3-formulate/drafts/round-1/supervision.reply.md
