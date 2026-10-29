# formulate of work-queue

Capability-proposal: .shop/work/i55/work-queue.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: formulate
Where the answers below change lines that are not in spec/, so that you formulate nothing, give in your result `nothing_formulated`, a sentence saying so, and no `questions`: `work run` then starts an integrate round for the proposal.
Base: c53a7c25e23bac68cae83b147c9dd66a2e6c6227
Worktree: /tmp/work-run-i55-kf283p9t/work-queue-9-formulate
Branch: round/work-queue-9-formulate
Answers the person gave, each with the question it answers:
- Question: Decision: r47 against work-queue r23 (done set with no condition on capability-proposals). Line concerned: [work-queue r47] **If** every work-item of an initiative is `green` or `withdrawn` while one of its capability-proposals is neither `formulated` nor `withdrawn`, **then** `work` shall keep the initiative `started`. (added; q21 line 11). Readings: (a, recommended) retire work-queue r23 for "[r48] **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn`, that every capability-proposal of it is `formulated` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`." and retire supervision r105 for the same condition; (b) keep r23 and r105, r47 the exception; (c) change only r23.
  Answer: 2026-10-29: Reading (a), under the person's delegation of 2026-10-27 ("Answer every question with its recommended reading"): retire work-queue r23 for r48 and retire supervision r105 for the same condition. by: work run, under the delegation "The person, 2026-10-27: "I'm delegating this to you. Please get the new version delivered without involving me." Lines 1-9 are i39's requests gate answers a formulate round could not draft (q14 lines 13-16 among them): line 1 replaces requests r13 (r14, an observation listing under work status, is retired with work status); lines 2-5 are q14 lines 13-16 naming work show; line 6 replaces r34; lines 7-9 replace r39, r41 and r43, a 'message' being an answer or a turn. Requirement lines are retired and replaced, never edited. Lines 10-13 fix the bugs i39 met. Answer every question with its recommended reading; where none is recommended, choose the one a test can check."
- Question: Decision: r47 and `merged` capability-proposals. Line concerned: [work-queue r47] **If** every work-item of an initiative is `green` or `withdrawn` while one of its capability-proposals is neither `formulated` nor `withdrawn`, **then** `work` shall keep the initiative `started`. (added; q21 line 11). Readings: (a, recommended) as drafted, word for word; (b) "neither `formulated`, `merged` nor `withdrawn`".
  Answer: 2026-10-29: Reading (a), as drafted word for word: r47 stays 'neither `formulated` nor `withdrawn`', per the delegation's instruction to use the recommended reading (The person, 2026-10-27). by: work run, under the delegation "The person, 2026-10-27: "I'm delegating this to you. Please get the new version delivered without involving me." Lines 1-9 are i39's requests gate answers a formulate round could not draft (q14 lines 13-16 among them): line 1 replaces requests r13 (r14, an observation listing under work status, is retired with work status); lines 2-5 are q14 lines 13-16 naming work show; line 6 replaces r34; lines 7-9 replace r39, r41 and r43, a 'message' being an answer or a turn. Requirement lines are retired and replaced, never edited. Lines 10-13 fix the bugs i39 met. Answer every question with its recommended reading; where none is recommended, choose the one a test can check."
- Question: Are the lines of work-queue approved as drafted? Readings: approve work-queue as drafted (recommended), or change its lines.
  Answer: 2026-10-29: Approve work-queue as drafted: the delegation (the person, 2026-10-27) says to answer every question with its recommended reading, and approving as drafted is the recommended one. by: work run, under the delegation "The person, 2026-10-27: "I'm delegating this to you. Please get the new version delivered without involving me." Lines 1-9 are i39's requests gate answers a formulate round could not draft (q14 lines 13-16 among them): line 1 replaces requests r13 (r14, an observation listing under work status, is retired with work status); lines 2-5 are q14 lines 13-16 naming work show; line 6 replaces r34; lines 7-9 replace r39, r41 and r43, a 'message' being an answer or a turn. Requirement lines are retired and replaced, never edited. Lines 10-13 fix the bugs i39 met. Answer every question with its recommended reading; where none is recommended, choose the one a test can check."

Read (paths in your worktree):
- .shop/work/i55/work-queue.md
- .shop/work/i55/runs/work-queue/1-gate
- .shop/work/i55/runs/work-queue/2-answer
- .shop/work/i55/runs/work-queue/3-answer
- .shop/work/i55/runs/work-queue/4-apply
- .shop/work/i55/runs/work-queue/5-integrate
- .shop/work/i55/runs/work-queue/6-gate
- .shop/work/i55/runs/work-queue/7-answer
- .shop/work/i55/runs/work-queue/8-apply

Run directory: /tmp/work-run-i55-kf283p9t/work-queue-9-formulate/.shop/scratch/9-formulate
Result file: /tmp/work-run-i55-kf283p9t/work-queue-9-formulate/.shop/scratch/9-formulate/result.json

You start in your worktree, /tmp/work-run-i55-kf283p9t/work-queue-9-formulate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
