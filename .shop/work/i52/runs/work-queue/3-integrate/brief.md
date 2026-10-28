# integrate of work-queue

Initiative: .shop/work/i52/work-queue.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q38
Accepted lines of the request:
- 1. **When** a round of the kind `integrate` gives terms for an initiative that already has a glossary-proposal, `work run` shall add them to that glossary-proposal, keeping its status, questions and answers.
- 2. **When** a question of an initiative is left for the person, `work run` shall start no further session under the delegation for that initiative's questions until the person has answered.
- 3. **When** `work withdraw` leaves every work-item of an initiative green or withdrawn, `work` shall leave the initiative's status for `work run` to set once its kept branch review lists nothing to fix now.
- 4. **When** `work` sets an initiative's status, `work` shall log the move in the initiative's log.
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3, supervision#r5, supervision#r16, supervision#r71, supervision#r77, supervision#r80, supervision#r92, supervision#r93, work-queue#r3, work-queue#r11, work-queue#r16, work-queue#r17, work-queue#r18, requests#r1, requests#r3, supervision#r99, supervision#r104, supervision#r112, supervision#r113, supervision#r114, review#r9, supervision#r125, supervision#r126, supervision#r127, design-model-check#r120, design-model-check#r121, requests#r26, requests#r27, requests#r35, requests#r36, requests#r37, requests#r38, spec-integration#r17, work-queue#r33, supervision#r137, supervision#r138, supervision#r139, supervision#r140, requests#r46, spec-integration#r47, spec-integration#r48, spec-integration#r49, spec-integration#r50, spec-integration#r51, spec-integration#r52, spec-integration#r53, requests#r47, requests#r48, supervision#r177, supervision#r178, supervision#r179, supervision#r174, supervision#r175, supervision#r176, spec-integration#r57, supervision#r187, work-queue#r48, work-queue#r49, requests#r50, requests#r51, requests#r52, requests#r53, requests#r54, requests#r55, requests#r56, requests#r57, requests#r58, supervision#r184, supervision#r185, supervision#r186, work-queue#r47, requests#r49, supervision#r183, work-queue#r46, backlog#r1, backlog#r2, backlog#r3, backlog#r4, backlog#r5, backlog#r6, backlog#r7, backlog#r8, migration-tools#r35, migration-tools#r36, spec-integration#r56, work-queue#r42, work-queue#r43, work-queue#r44, work-queue#r45
Drafts path: /tmp/work-run-i52-vjpigzqs/work-queue-3-integrate/.shop/scratch/3-integrate/drafts
Give your change list in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>`. Every term you add, change or remove goes in one entry for the glossary, `{"glossary": true, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `term/<term>`, and in no capability's entry.
Ledger: .shop/work/i52/ledger.md
Earlier drafts path (read only): .shop/work/i52/runs/i52/1-integrate/drafts/round-1/
Where an answer below asks for lines the request's accepted lines do not, draft those lines under the capabilities the answer names, each quoting the answer it comes from.
Base: 51bb24048825d03cf1e81728d51046a41b4c2ce0
Worktree: /tmp/work-run-i52-vjpigzqs/work-queue-3-integrate
Branch: round/work-queue-3-integrate
Answers the person gave, each with the question it answers:
- Question: work-queue r23 and r40: which `work` commands leave a finished initiative's `done` to `work run`? Lines: r23 CHANGED. Now: "**When** a `work` command other than `work withdraw` makes it true by its change that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`." Was: "**When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`." r40 ADDED: "**When** `work withdraw` leaves every work-item of an initiative `green` or `withdrawn`, `work` shall leave the initiative's status as it is, for `work run` to set once the initiative's kept branch review lists nothing to fix now." Readings: (a) only `work withdraw`, as drafted (the request names only it); (b) every `work` command: r23 removed (id retired) and r40 reads "**When** a `work` command's change leaves every work-item of an initiative `green` or `withdrawn`, `work` shall leave the initiative's status as it is, for `work run` to set once the initiative's kept branch review lists nothing to fix now." Recommended: (b), the writer's recommendation; (a) is the narrower reading, as the request names only `work withdraw`.
  Answer: 2026-10-28: Q1, r23 and r40: reading (b), every work command leaves a finished initiative's done to work run (r23 retired) (answered by the coordinator under the person's delegation, 2026-10-28)
- Question: work-queue r41: should the logged line also hold the time and who set the status, as r5's does? Line: r41 ADDED: "**When** `work` sets an initiative's status, `work` shall append a line to `.shop/work/<initiative>/log.jsonl` with the initiative and its status before and after the transition." Readings: (a) yes: "...with the time, the initiative, its status before and after, and who set it."; (b) only the initiative and the status before and after, as drafted. Recommended: (b), what the request asks; (a) if the log is to be an audit trail like r5's.
  Answer: 2026-10-28: Q2, r41's logged line: reading (a), with the time, the initiative, its status before and after, and who set it, as r5's lines do (answered by the coordinator under the person's delegation, 2026-10-28)
- Question: work-queue r41: does `work start` writing a `proposed` initiative count as setting its status? Line r41 as in the question above. Readings: (a) yes, a further line: "**When** `work start` writes an initiative, `work` shall append a line to `.shop/work/<initiative>/log.jsonl` with the initiative and its status `proposed`."; (b) no, as drafted (r41 covers only transitions). Recommended: (b).
  Answer: 2026-10-28: Q3, work start and r41: reading (b), r41 covers only transitions (answered by the coordinator under the person's delegation, 2026-10-28)
- Question: work-queue r41: should the `log.jsonl` line r41 writes be committed with the initiative's file (work-queue r9)? Readings: (a) yes, r9 changed or a new line: "**When** `work` sets an initiative's status, `work` shall commit on the current branch the initiative's file and the `log.jsonl` line it wrote."; (b) no line, as drafted. Recommended: (b), unless the log is to be kept in git, in which case (a).
  Answer: 2026-10-28: Q4, committing r41's line: reading (b), no line (answered by the coordinator under the person's delegation, 2026-10-28)

Read (paths in your worktree):
- .shop/work/i52/work-queue.md
- .shop/work/i52/runs/work-queue/1-gate
- .shop/work/i52/runs/work-queue/2-apply
- .shop/work/i52/ledger.md
- .shop/work/i52/runs/i52/1-integrate/drafts/round-1/

Run directory: /tmp/work-run-i52-vjpigzqs/work-queue-3-integrate/.shop/scratch/3-integrate
Result file: /tmp/work-run-i52-vjpigzqs/work-queue-3-integrate/.shop/scratch/3-integrate/result.json

You start in your worktree, /tmp/work-run-i52-vjpigzqs/work-queue-3-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
