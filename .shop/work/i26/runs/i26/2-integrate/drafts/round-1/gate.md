# Gate, integrate round 1 (q3)

Drafts: .shop/scratch/2-integrate/drafts/round-1/spec/capabilities/{requests,supervision}.md

## Behaviour lines added (4, none changed, none removed; no terms, no decisions)

requests
- [r20] **When** the upstream asks a question on a line of a request in its turn, `work` shall write the question in the request.
- [r21] **When** the asker answers a question on a request in its turn, `work` shall write the answer in the request.

supervision
- [r98] **When** a round of the kind `intake` that `work run` started gives a question on a line of a request, `work run` shall write the question in the request.
- [r99] **When** `work run` ends while a request whose asker is this context is in the asker's turn, `work run` shall exit with an error, printing the request with its open questions.

Also drafted (not a Behaviour line): requests `## Not yet`, "Commands for the other parts of a request" narrowed to the asker's revisions and withdrawals of lines.

## Questions

1. requests r20/r21: which command writes a question and which an answer? The note names none. A: new commands (`work question <request> <n> <text>`, `work answer <request> <text>`) in the lines. B (recommended): lines as drafted; commands stay Implementation, named once known.
2. requests r4/r5 conflict with r20/r21 (r4: asker's part written only by `work request`; r5: upstream's part only by `work outcome`/`work resolve`). Change them to add answers (r4) and questions (r5)? Yes (recommended) / no, leaving a contradiction.
3. requests r12: should the commit rule cover the question and answer commands? Yes (recommended) / no.
4. requests: is r16's refusal out of turn the intended refusal for a question in the asker's turn or an answer in the upstream's turn? Yes (recommended), nothing changes / no, a separate refusal line.
5. requests Implementation: add "r20, r21: a question is written under `## Questions`, an answer under `## Answers`, the n-th answering the n-th"? Yes (recommended) / no.
6. supervision r67 vs r98: A (recommended): the intake round gives the question in its result and `work run` writes it; r67 changes to "... that writes each line's line outcome or gives a question on it, and passes the turn with `work turn`." B: both may write it; r67 stays and r98 would write it twice.
7. supervision r98: Implementation line "`work run` writes the question with `work`'s question command (requests r20), in the upstream's turn, before the round's `work turn`"? Yes (recommended) / no.
8. supervision r99, "asker is this context": A (recommended): asker is `internal` or this context's id (q3 is `internal`), with an Implementation line saying so. B: only this context's id.
9. supervision r99, which requests: only those kept in this repository (recommended; line becomes "a request kept in this context whose asker is this context") / also requests this context raised elsewhere.
10. supervision r99 vs r9/r82 (exit successfully when all work-items green / no node awaiting): should r9 and r82 add "and no request whose asker is this context is in the asker's turn"? Yes (recommended; r99 would otherwise contradict them) / no.
11. supervision r99, "open questions": A (recommended): every question with no answer under `## Answers`, with that as an Implementation line. B: only those of the upstream's latest turn.

Cut sentences: 0.
