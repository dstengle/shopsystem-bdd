/tmp/work-run-i26-lerbditg/i26-2-integrate/.shop/scratch/2-integrate/drafts/round-1/spec/capabilities/requests.md
/tmp/work-run-i26-lerbditg/i26-2-integrate/.shop/scratch/2-integrate/drafts/round-1/spec/capabilities/supervision.md

## Change list

| change | capability | id | line | note sentence |
|---|---|---|---|---|
| added | requests | r20 | **When** the upstream asks a question on a line of a request in its turn, `work` shall write the question in the request. | "**When** the upstream asks a question on a line of a request in its turn, `work` shall write the question in the request." (q3 line 1) |
| added | requests | r21 | **When** the asker answers a question on a request in its turn, `work` shall write the answer in the request. | "**When** the asker answers a question on a request in its turn, `work` shall write the answer in the request." (q3 line 2) |
| added | supervision | r98 | **When** a round of the kind `intake` that `work run` started gives a question on a line of a request, `work run` shall write the question in the request. | "**When** an intake round that `work run` started gives a question on a line of a request, `work run` shall write the question in the request." (q3 line 3) |
| added | supervision | r99 | **When** `work run` ends while a request whose asker is this context is in the asker's turn, `work run` shall exit with an error, printing the request with its open questions. | "**When** `work run` ends while a request whose asker is this context is in the asker's turn, `work run` shall print the request with its open questions and exit with an error." (q3 line 4) |

Glossary: no term added, changed or removed.

Other drafted change: requests `## Not yet`, the entry "Commands for the other parts of a request" narrowed to the asker's revisions and withdrawals of lines, since r20 and r21 now give the asker's answers and the upstream's questions.

Wording: r98 says "a round of the kind `intake`" because that is how the spec already says "intake round" (r67). r99 keeps one "shall" by putting the print in a participle, the same way r32 does ("exit with an error, printing ...").

Decision files: none.

## Questions

1. requests r20/r21, which command writes a question and which an answer. The note names none. Reading A, a new command for each (e.g. `work question <request> <n> <text>` and `work answer <request> <text>`): the lines would be "**When** `work question <request> <n> <text>` is run in the upstream's turn, `work` shall write `<text>` as a question on line n." and "**When** `work answer <request> <text>` is run in the asker's turn, `work` shall write `<text>` as an answer in the request." Reading B, the command is `work`'s own and stays in Implementation: r20/r21 stay as drafted. (Recommended: B, and add an Implementation line naming the commands once they are known.)
2. requests r4 and r5 conflict with r20/r21. r4 says the asker's part is its lines, written only by `work request`. r5 says the upstream's part is its line outcomes and resolution, written only by `work outcome` or `work resolve`. If yes, change them to: r4 "`work` shall write the asker's part of a request, its lines and its answers, only when `work request` or <the answer command> is run." and r5 "`work` shall write the upstream's part of a request, its line outcomes, its questions and its resolution, only when `work outcome`, <the question command> or `work resolve` is run." If no, r20/r21 contradict r4/r5 as they stand.
3. requests r12 (commit). Does `work` commit the request when a question or an answer is written? If yes, add the question and answer commands to r12: "**When** `work request`, `work outcome`, <the question command>, <the answer command>, `work turn` or `work resolve` changes a request, `work` shall commit the request on the current branch."
4. requests, refusal out of turn. r16 already refuses any command that writes a part in the other side's turn. Is that the intended refusal for a question asked in the asker's turn or an answer given in the upstream's turn? If yes, nothing changes. If no, write a separate refusal line.
5. requests, where the question and answer are kept. The Implementation section already lists `## Questions` and `## Answers`. If yes, add the Implementation line "r20, r21: a question is written under the request's `## Questions` and an answer under its `## Answers`, the n-th answer answering the n-th question."
6. supervision r67 and r98, two readings of who writes the intake round's question. r67 says the intake session "writes each line's line outcome or a question on it". r98 says `work run` writes the question from what the round gives. Reading A, the round gives the question in its result and `work run` writes it: change r67 to "... that writes each line's line outcome or gives a question on it, and passes the turn with `work turn`." Reading B, both the session and `work run` may write it: r67 stays, and r98 would write the question a second time. (Recommended: A.)
7. supervision r98, which command `work run` writes the question with. If it writes through `work`'s question command (requests r20), add the Implementation line "r98: `work run` writes the question with `work`'s question command (requests r20), in the upstream's turn, before the round's `work turn`."
8. supervision r99, what "a request whose asker is this context" covers. Reading A, the request's asker names this context's id or is `internal` (q3 itself has `asker: internal`): the line stays, plus the Implementation line "r99: a request's asker is this context when its `asker` is `internal` or this context's id." Reading B, only a request whose asker is this context's id: write "**When** `work run` ends while a request whose asker names this context's id is in the asker's turn, ...".
9. supervision r99, which requests count. Is it requests kept in this repository only (`.shop/work/requests/`, where this context is also the upstream), or also requests this context raised with other contexts and keeps in their repositories? If only this repository's, write "**When** `work run` ends while a request kept in this context whose asker is this context is in the asker's turn, `work run` shall exit with an error, printing the request with its open questions."
10. supervision r99 conflicts with r9 and r82, which make `work run` exit successfully when every work-item is `green` or `withdrawn` (r9) or no node is `awaiting-answer` or `failed` (r82). If r99 is meant to win, change r9 to "**When** no work-item can make a transition, every work-item is `green` or `withdrawn` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing each work-item's status." and change r82 the same way.
11. supervision r99, what "open questions" means. Reading A, every question on the request that has no answer yet. Reading B, only the questions asked in the upstream's latest turn. If A, the line stays and gets the Implementation line "r99: an open question is one of the request's `## Questions` with no answer under `## Answers`."

## Cut sentences

None. Every accepted line of q3 is a Behaviour line. The request's title ("A request's questions and answers through work") and its Outcomes are request metadata, not sentences to integrate.
