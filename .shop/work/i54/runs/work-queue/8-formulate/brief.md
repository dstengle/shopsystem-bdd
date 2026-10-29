# formulate of work-queue

Capability-proposal: .shop/work/i54/work-queue.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: formulate
Where the answers below change lines that are not in spec/, so that you formulate nothing, give in your result `nothing_formulated`, a sentence saying so, and no `questions`: `work run` then starts an integrate round for the proposal.
Base: a2a53b36c02b74d046b7a490d802403f3f1828a9
Worktree: /tmp/work-run-i54-dk9g6cqa/work-queue-8-formulate
Branch: round/work-queue-8-formulate
Answers the person gave, each with the question it answers:
- Question: Decision on work-queue r49 (added): **When** `work list` is run, `work` shall print each initiative and each work-item under `.shop/work/` with its status. It replaces r34 (removed, retired; it was: **When** `work list` is run, `work` shall print each initiative, each request and each work-item under `.shop/work/` with its status.). Added r48 is: **When** `work show <request>` is run, `work` shall print the request's status, whose turn it is, its lines with their line outcomes, its questions, its answers and its resolution. The existing r35 (**Where** `--json` is given, `work list` shall print its result, each initiative, request and work-item with its status, as one JSON object.) then contradicts r49, because it still lists requests. Readings: (a) retire r35 and add r50 '**Where** `--json` is given, `work list` shall print its result, each initiative and work-item with its status, as one JSON object.', so the text and JSON outputs agree; (b) keep r35 as it is, so the text and JSON outputs differ. Recommended: (a).
  Answer: 2026-10-29: Reading (a): retire r35 and add r50 '**Where** `--json` is given, `work list` shall print its result, each initiative and work-item with its status, as one JSON object.', so the text and JSON outputs agree. This follows the person's 2026-10-27 delegation: answer every question with its recommended reading. by: work run, under the delegation "The person, 2026-10-27: "I'm delegating this to you. Please get the new version delivered without involving me." Lines 1 and 2 are i39's gate-round-7 answers that apply round 8 dropped (work-queue r48, and r34 retired for a list without requests, which requests r46 lists); line 2 replaces work-queue r34, retired, not edited. Line 3 states the merge w206 implemented (reading B). Answer every question with its recommended reading; where none is recommended, choose the one a test can check."
- Question: Are the lines of work-queue approved as drafted? Readings: approve work-queue as drafted (recommended), or change its lines.
  Answer: 2026-10-29: Approve work-queue as drafted (the recommended reading), under the person's 2026-10-27 delegation: "Please get the new version delivered without involving me." by: work run, under the delegation "The person, 2026-10-27: "I'm delegating this to you. Please get the new version delivered without involving me." Lines 1 and 2 are i39's gate-round-7 answers that apply round 8 dropped (work-queue r48, and r34 retired for a list without requests, which requests r46 lists); line 2 replaces work-queue r34, retired, not edited. Line 3 states the merge w206 implemented (reading B). Answer every question with its recommended reading; where none is recommended, choose the one a test can check."

Read (paths in your worktree):
- .shop/work/i54/work-queue.md
- .shop/work/i54/runs/work-queue/1-gate
- .shop/work/i54/runs/work-queue/2-answer
- .shop/work/i54/runs/work-queue/3-apply
- .shop/work/i54/runs/work-queue/4-integrate
- .shop/work/i54/runs/work-queue/5-gate
- .shop/work/i54/runs/work-queue/6-answer
- .shop/work/i54/runs/work-queue/7-apply

Run directory: /tmp/work-run-i54-dk9g6cqa/work-queue-8-formulate/.shop/scratch/8-formulate
Result file: /tmp/work-run-i54-dk9g6cqa/work-queue-8-formulate/.shop/scratch/8-formulate/result.json

You start in your worktree, /tmp/work-run-i54-dk9g6cqa/work-queue-8-formulate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
