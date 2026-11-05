# gate of requests-deda9fa6

Capability-proposal: .shop/work/i55/requests-deda9fa6.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: gate
Give the gate as questions in your result's `questions`, one string each: every question a decision, with its readings and the recommended reading marked.
Adds: requests#r73@0.29
Changes: none
Removes: requests#r52@0.29
Ask questions only on the lines and terms listed above as adds, changes or removes, and on no other line or term.
Drafts path: .shop/work/i55/runs/requests-deda9fa6/4-integrate/drafts/round-4/
Base: c53a7c25e23bac68cae83b147c9dd66a2e6c6227
Worktree: /tmp/work-run-i55-k2ut5f4r/requests-deda9fa6-5-gate
Branch: round/requests-deda9fa6-5-gate
Answers the person gave, each with the question it answers:
- Question: requests r52: "While an answer or a turn the asker has sent has not been taken in by the upstream, `work show <request>` shall print the request on either side as awaiting the upstream and not yet taken in." Reading 1: an answer sent alone, with the turn still the asker's, is enough, so show prints awaiting the upstream even in the asker's turn (clashes with r51). Reading 2: only a sent turn (with any answers sent with it) makes the request await the upstream; an answer sent alone leaves show printing the asker's turn under r51. Also: is 'awaiting the upstream' the status awaiting-upstream or only a description of who acts next?
  Answer: 2026-11-02: Reading 2: only a sent turn (with any answers sent with it) makes the request await the upstream, so an answer sent alone leaves `work show` printing the asker's turn under r51; and 'awaiting the upstream' is only the description printed of who acts next, not a new status named awaiting-upstream. (Under the delegation of The person, 2026-10-27: "I'm delegating this to you. Please get the new version delivered without involving me.") by: work run, under the delegation "The person, 2026-10-27: "I'm delegating this to you. Please get the new version delivered without involving me." Lines 1-9 are i39's requests gate answers a formulate round could not draft (q14 lines 13-16 among them): line 1 replaces requests r13 (r14, an observation listing under work status, is retired with work status); lines 2-5 are q14 lines 13-16 naming work show; line 6 replaces r34; lines 7-9 replace r39, r41 and r43, a 'message' being an answer or a turn. Requirement lines are retired and replaced, never edited. Lines 10-13 fix the bugs i39 met. Answer every question with its recommended reading; where none is recommended, choose the one a test can check." The drafts of this proposal are in .shop/work/i55/runs/requests-deda9fa6/4-integrate/drafts/round-4/.

Read (paths in your worktree):
- .shop/work/i55/requests-deda9fa6.md
- .shop/work/i55/runs/requests-deda9fa6/1-formulate
- .shop/work/i55/runs/requests-deda9fa6/2-answer
- .shop/work/i55/runs/requests-deda9fa6/3-formulate
- .shop/work/i55/runs/requests-deda9fa6/4-integrate
- .shop/work/i55/runs/requests-deda9fa6/4-integrate/drafts/round-4/

Run directory: /tmp/work-run-i55-k2ut5f4r/requests-deda9fa6-5-gate/.shop/scratch/5-gate
Result file: /tmp/work-run-i55-k2ut5f4r/requests-deda9fa6-5-gate/.shop/scratch/5-gate/result.json

You start in your worktree, /tmp/work-run-i55-k2ut5f4r/requests-deda9fa6-5-gate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
