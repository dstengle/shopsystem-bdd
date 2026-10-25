---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/supervision
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i26
status: awaiting-answer
argues: [supervision]
adds: [supervision#r98, supervision#r99]
changes: []
removes: []
date: 2026-10-25
---

# supervision

The drafts of this proposal are in .shop/work/i26/runs/i26/2-integrate.

## Questions
- Which command writes a question and which an answer? Lines (added):
  [requests#r20] **When** the upstream asks a question on a line of a request in its turn, `work` shall write the question in the request.
  [requests#r21] **When** the asker answers a question on a request in its turn, `work` shall write the answer in the request.
  The note names no command. A: put new commands in the lines (`work question <request> <n> <text>`, `work answer <request> <text>`). B (recommended): lines as drafted; commands stay Implementation, named once known.
- requests r4 and r5 contradict r20/r21. Changed lines: r4 was "`work` shall write the asker's part of a request, its lines, only when `work request` is run."; r5 was "`work` shall write the upstream's part of a request, its line outcomes and its resolution, only when `work outcome` or `work resolve` is run." Change r4 to add the asker's answers and r5 to add the upstream's questions? Yes (recommended) / no, leaving a contradiction.
- requests r12 ("**When** `work request`, `work outcome`, `work turn` or `work resolve` changes a request, `work` shall commit the request on the current branch."): should the commit rule cover the question and answer commands (a changed line)? Yes (recommended) / no.
- requests r16 ("**If** a side runs a command other than `work resolve` that writes a part of a request in the other side's turn, **then** `work` shall refuse ... and change nothing."): is it the intended refusal for a question in the asker's turn or an answer in the upstream's turn? Yes (recommended), nothing changes / no, a separate refusal line.
- requests Implementation: add "r20, r21: a question is written under `## Questions`, an answer under `## Answers`, the n-th answering the n-th"? Yes (recommended) / no.
- supervision r67 vs r98. Line (added):
  [supervision#r98] **When** a round of the kind `intake` that `work run` started gives a question on a line of a request, `work run` shall write the question in the request.
  r67 was "... start an `initiative-round` session of the kind `intake`, given the request, that writes each line's line outcome and passes the turn with `work turn`."; the draft changes it to "... that writes each line's line outcome or a question on it and passes the turn with `work turn`." A (recommended): the intake round gives the question in its result and `work run` writes it; r67 changes as drafted. B: both may write it; r67 stays and r98 would write it twice.
- supervision r98 Implementation line: "`work run` writes the question with `work`'s question command (requests r20), in the upstream's turn, before the round's `work turn`". Add? Yes (recommended) / no.
- supervision r99, "asker is this context". Line (added):
  [supervision#r99] **When** `work run` ends while a request whose asker is this context is in the asker's turn, `work run` shall exit with an error, printing the request with its open questions.
  A (recommended): asker is `internal` or this context's id (q3 is `internal`), with an Implementation line saying so. B: only this context's id.
- supervision r99, which requests: only those kept in this repository (recommended; the line becomes "a request kept in this context whose asker is this context") / also requests this context raised elsewhere.
- supervision r99 vs r9 and r82. r9 ("**When** no work-item can make a transition and every work-item is `green` or `withdrawn`, `work run` shall exit successfully, printing each work-item's status.") and r82 ("**When** `work run` was started with no initiative, no node of an initiative it took can make a transition and none is `awaiting-answer` or `failed`, `work run` shall exit successfully, printing the status of each initiative it took."): add to both "and no request whose asker is this context is in the asker's turn" (two changed lines)? Yes (recommended; r99 would otherwise contradict them) / no.
- supervision r99, "open questions": A (recommended): every question with no answer under `## Answers`, stated as an Implementation line. B: only those of the upstream's latest turn.

## Answers
- 2026-10-25: 1: B, lines as drafted; the commands stay Implementation (the coordinator under the person's delegation 2026-10-25)
- 2026-10-25: 2: yes, change r4 to add the asker's answers and r5 to add the upstream's questions (the coordinator under the person's delegation 2026-10-25)
- 2026-10-25: 3: yes, r12 covers the question and answer commands (the coordinator under the person's delegation 2026-10-25)
