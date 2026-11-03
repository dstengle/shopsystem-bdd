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
Ids drafted elsewhere (number added lines above each on the same capability): supervision#r3@0.29, supervision#r5@0.29, supervision#r16@0.29, supervision#r71@0.29, supervision#r77@0.29, supervision#r80@0.29, supervision#r92@0.29, supervision#r93@0.29, work-queue#r3@0.29, work-queue#r11@0.29, work-queue#r16@0.29, work-queue#r17@0.29, work-queue#r18@0.29, requests#r1@0.29, requests#r3@0.29, supervision#r99@0.29, supervision#r104@0.29, supervision#r112@0.29, supervision#r113@0.29, supervision#r114@0.29, review#r9@0.29, supervision#r125@0.29, supervision#r126@0.29, supervision#r127@0.29, design-model-check#r120@0.29, design-model-check#r121@0.29, requests#r26@0.29, requests#r27@0.29, requests#r35@0.29, requests#r36@0.29, requests#r37@0.29, requests#r38@0.29, spec-integration#r17@0.29, work-queue#r33@0.29, supervision#r137@0.29, supervision#r138@0.29, supervision#r139@0.29, supervision#r140@0.29, requests#r46@0.29, spec-integration#r47@0.29, spec-integration#r48@0.29, spec-integration#r49@0.29, spec-integration#r50@0.29, spec-integration#r51@0.29, spec-integration#r52@0.29, spec-integration#r53@0.29, requests#r47@0.29, requests#r48@0.29, supervision#r177@0.29, supervision#r178@0.29, supervision#r179@0.29, supervision#r174@0.29, supervision#r175@0.29, supervision#r176@0.29, spec-integration#r57@0.29, supervision#r187@0.29, work-queue#r48@0.29, work-queue#r49@0.29, requests#r50@0.29, requests#r51@0.29, requests#r52@0.29, requests#r53@0.29, requests#r54@0.29, requests#r55@0.29, requests#r56@0.29, requests#r57@0.29, requests#r58@0.29, supervision#r184@0.29, supervision#r185@0.29, supervision#r186@0.29, work-queue#r47@0.29, requests#r49@0.29, supervision#r183@0.29, work-queue#r46@0.29, backlog#r1, backlog#r2, backlog#r3, backlog#r4, backlog#r5, backlog#r6, backlog#r7, backlog#r8, migration-tools#r35@0.29, migration-tools#r36@0.29, spec-integration#r56@0.29, work-queue#r42@0.29, work-queue#r43@0.29, work-queue#r44@0.29, work-queue#r45@0.29
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
