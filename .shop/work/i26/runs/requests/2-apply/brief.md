# apply of requests

Capability-proposal: .shop/work/i26/requests.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: apply
Base: f582b1bb522f819e5b2c7ff1d38707beafcc63fe
Worktree: /tmp/work-run-i26-oc_xbi0g/requests-2-apply
Branch: round/requests-2-apply
Answers the person gave, each with the question it answers:
- Question: Which command writes a question and which an answer (requests r20, r21)? Lines: [requests#r20] **When** the upstream asks a question on a line of a request in its turn, `work` shall write the question in the request. [requests#r21] **When** the asker answers a question on a request in its turn, `work` shall write the answer in the request. The note names no command. A: put new commands in the lines (`work question <request> <n> <text>`, `work answer <request> <text>`). B (recommended): lines as drafted; commands stay Implementation, named once known.
  Answer: 2026-10-25: 1: B, lines as drafted; the commands stay Implementation (the coordinator under the person's delegation 2026-10-25)
- Question: requests r4 (asker's part written only by `work request`) and r5 (upstream's part only by `work outcome`/`work resolve`) contradict r20/r21. Change r4 to add answers and r5 to add questions? Yes (recommended) / no, leaving a contradiction.
  Answer: 2026-10-25: 2: yes, change r4 to add the asker's answers and r5 to add the upstream's questions (the coordinator under the person's delegation 2026-10-25)
- Question: requests r12 (commit rule): should it cover the question and answer commands? Yes (recommended) / no.
  Answer: 2026-10-25: 3: yes, r12 covers the question and answer commands (the coordinator under the person's delegation 2026-10-25)
- Question: Is requests r16's refusal out of turn the intended refusal for a question in the asker's turn or an answer in the upstream's turn? Yes (recommended), nothing changes / no, a separate refusal line.
  Answer: 2026-10-25: 4: yes, r16 is the refusal; nothing changes (the coordinator under the person's delegation 2026-10-25)
- Question: requests Implementation: add "r20, r21: a question is written under `## Questions`, an answer under `## Answers`, the n-th answering the n-th"? Yes (recommended) / no.
  Answer: 2026-10-25: 5: yes, add the Implementation line (the coordinator under the person's delegation 2026-10-25)
- Question: supervision r67 vs r98. Line: [supervision#r98] **When** a round of the kind `intake` that `work run` started gives a question on a line of a request, `work run` shall write the question in the request. A (recommended): the intake round gives the question in its result and `work run` writes it; r67 changes to "... that writes each line's line outcome or gives a question on it, and passes the turn with `work turn`." (a changed line; it was: the intake round writes line outcomes and passes the turn). B: both may write it; r67 stays and r98 would write it twice.
  Answer: 2026-10-25: 6: A, the intake round gives the question in its result and work run writes it; r67 changes as drafted. The supervision lines this initiative adds take r100 (for r98) and r101 (for r99), since i25's drafts hold supervision r98 (the coordinator under the person's delegation 2026-10-25)
- Question: supervision r98 Implementation line: "`work run` writes the question with `work`'s question command (requests r20), in the upstream's turn, before the round's `work turn`". Add? Yes (recommended) / no.
  Answer: 2026-10-25: 7: yes, add the Implementation line (the coordinator under the person's delegation 2026-10-25)
- Question: supervision r99, "asker is this context". Line: [supervision#r99] **When** `work run` ends while a request whose asker is this context is in the asker's turn, `work run` shall exit with an error, printing the request with its open questions. A (recommended): asker is `internal` or this context's id (q3 is `internal`), with an Implementation line saying so. B: only this context's id.
  Answer: 2026-10-25: 8: A, asker internal or this context's id, with an Implementation line (the coordinator under the person's delegation 2026-10-25)
- Question: supervision r99, which requests: only those kept in this repository (recommended; line becomes "a request kept in this context whose asker is this context") / also requests this context raised elsewhere.
  Answer: 2026-10-25: 9: only requests kept in this repository (the coordinator under the person's delegation 2026-10-25)
- Question: supervision r99 vs r9 and r82 (exit successfully when all work-items green / no node awaiting): add to both "and no request whose asker is this context is in the asker's turn"? Yes (recommended; r99 would otherwise contradict them; two changed lines) / no.
  Answer: 2026-10-25: 10: yes, change r9 and r82 as recommended (the coordinator under the person's delegation 2026-10-25)
- Question: supervision r99, "open questions": A (recommended): every question with no answer under `## Answers`, stated as an Implementation line. B: only those of the upstream's latest turn.
  Answer: 2026-10-25: 11: A, every question with no answer under ## Answers, as an Implementation line (the coordinator under the person's delegation 2026-10-25)

Read (paths in your worktree):
- .shop/work/i26/requests.md
- .shop/work/i26/runs/requests/1-gate

Run directory: /tmp/work-run-i26-oc_xbi0g/requests-2-apply/.shop/scratch/2-apply
Result file: /tmp/work-run-i26-oc_xbi0g/requests-2-apply/.shop/scratch/2-apply/result.json

You start in your worktree, /tmp/work-run-i26-oc_xbi0g/requests-2-apply: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
