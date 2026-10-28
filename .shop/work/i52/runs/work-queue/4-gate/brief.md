# gate of work-queue

Capability-proposal: .shop/work/i52/work-queue.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: gate
Give the gate as questions in your result's `questions`, one string each: every question a decision, with its readings and the recommended reading marked.
Adds: work-queue#r50, work-queue#r51
Changes: none
Removes: work-queue#r23
Ask questions only on the lines and terms listed above as adds, changes or removes, and on no other line or term.
Drafts path: .shop/work/i52/runs/work-queue/3-integrate/drafts/round-1/
Base: 51bb24048825d03cf1e81728d51046a41b4c2ce0
Worktree: /tmp/work-run-i52-vjpigzqs/work-queue-4-gate
Branch: round/work-queue-4-gate
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
- .shop/work/i52/runs/work-queue/3-integrate
- .shop/work/i52/runs/work-queue/3-integrate/drafts/round-1/

Run directory: /tmp/work-run-i52-vjpigzqs/work-queue-4-gate/.shop/scratch/4-gate
Result file: /tmp/work-run-i52-vjpigzqs/work-queue-4-gate/.shop/scratch/4-gate/result.json

You start in your worktree, /tmp/work-run-i52-vjpigzqs/work-queue-4-gate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
