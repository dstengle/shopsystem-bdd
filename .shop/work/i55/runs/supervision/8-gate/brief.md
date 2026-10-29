# gate of supervision

Capability-proposal: .shop/work/i55/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: gate
Give the gate as questions in your result's `questions`, one string each: every question a decision, with its readings and the recommended reading marked.
Adds: supervision#r212
Changes: none
Removes: supervision#r149, supervision#r32, supervision#r9
Ask questions only on the lines and terms listed above as adds, changes or removes, and on no other line or term.
Drafts path: .shop/work/i55/runs/supervision/7-integrate/drafts/round-1/
Base: c53a7c25e23bac68cae83b147c9dd66a2e6c6227
Worktree: /tmp/work-run-i55-mwcb2_hn/supervision-8-gate
Branch: round/supervision-8-gate
Answers the person gave, each with the question it answers:
- Question: supervision r186 repeats r149 word for word. Line: [r186] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal. Readings: (a, recommended) retire r149 and keep r186, so a work-item is drafted for the fault i39 met; (b) drop r186 and keep r149; (c) keep both. r152 and r153 do not conflict and stay.
  Answer: 2026-10-29: Reading (a): retire r149 and keep r186, so a work-item is drafted for the fault i39 met (the delegation says to answer with the recommended reading, and r152 and r153 stay). by: work run, under the delegation "The person, 2026-10-27: "I'm delegating this to you. Please get the new version delivered without involving me." Lines 1-9 are i39's requests gate answers a formulate round could not draft (q14 lines 13-16 among them): line 1 replaces requests r13 (r14, an observation listing under work status, is retired with work status); lines 2-5 are q14 lines 13-16 naming work show; line 6 replaces r34; lines 7-9 replace r39, r41 and r43, a 'message' being an answer or a turn. Requirement lines are retired and replaced, never edited. Lines 10-13 fix the bugs i39 met. Answer every question with its recommended reading; where none is recommended, choose the one a test can check."
- Question: supervision r184 against r32, r81 and r9. Line: [r184] **When** `work run` ends with a capability-proposal or a work-item `awaiting-answer`, `work run` shall exit with an error, printing each with its open questions. It covers r32 and conflicts with r9 when every work-item is done while a capability-proposal is `awaiting-answer`. Readings: (a, recommended) retire r32 and r9 and add "[r187] **When** no node of the initiative can make a transition, every work-item is `green` or `withdrawn`, no capability-proposal is `awaiting-answer` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing each work-item's status."; (b) keep r32 and r9, r184 taking precedence; (c) keep r32 and r184, retire r9 only. r81 stays (recommended) or also prints each proposal's open questions.
  Answer: 2026-10-29: Reading (a), as the delegation says to use the recommended reading: retire r32 and r9 and add r187 ('When no node of the initiative can make a transition, every work-item is green or withdrawn, no capability-proposal is awaiting-answer and no request whose asker is this context is in the asker's turn, work run shall exit successfully, printing each work-item's status'); r184 stands as written, and r81 stays unchanged. by: work run, under the delegation "The person, 2026-10-27: "I'm delegating this to you. Please get the new version delivered without involving me." Lines 1-9 are i39's requests gate answers a formulate round could not draft (q14 lines 13-16 among them): line 1 replaces requests r13 (r14, an observation listing under work status, is retired with work status); lines 2-5 are q14 lines 13-16 naming work show; line 6 replaces r34; lines 7-9 replace r39, r41 and r43, a 'message' being an answer or a turn. Requirement lines are retired and replaced, never edited. Lines 10-13 fix the bugs i39 met. Answer every question with its recommended reading; where none is recommended, choose the one a test can check."
- Question: supervision r184, the exit code. Line: [r184] **When** `work run` ends with a capability-proposal or a work-item `awaiting-answer`, `work run` shall exit with an error, printing each with its open questions. (q21 asked for exit code 3; drafted as "an error" under design-decision/exits-are-successful-or-errors, the code held by Implementation: "3 awaiting an answer".) Readings: (a, recommended) as drafted, the code in Implementation only; (b) add an Implementation line "r184: the exit code is 3".
  Answer: 2026-10-29: Reading (a), as drafted: r184 stays 'an error' and the code 3 is held only in Implementation, with no new Implementation line. The person delegated on 2026-10-27 and said to answer every question with its recommended reading, and (a) is the recommended one. by: work run, under the delegation "The person, 2026-10-27: "I'm delegating this to you. Please get the new version delivered without involving me." Lines 1-9 are i39's requests gate answers a formulate round could not draft (q14 lines 13-16 among them): line 1 replaces requests r13 (r14, an observation listing under work status, is retired with work status); lines 2-5 are q14 lines 13-16 naming work show; line 6 replaces r34; lines 7-9 replace r39, r41 and r43, a 'message' being an answer or a turn. Requirement lines are retired and replaced, never edited. Lines 10-13 fix the bugs i39 met. Answer every question with its recommended reading; where none is recommended, choose the one a test can check."
- Question: supervision r185 against r132 and r131. Line: [r185] **When** a researcher's result gives an empty file set, `work run` shall take it as the researcher's file set. Readings: (a, recommended) keep r132 and r131 with r185 beside them; (b) retire r132 for "a researcher's file set, empty or not" and drop r185. For an empty planner's file set: (a, recommended) nothing drafted; (b) add "[r189] **When** a planner's result gives an empty file set, `work run` shall take it as the planner's file set."
  Answer: 2026-10-29: Reading (a) for both: keep r132 and r131 with r185 beside them, and for an empty planner's file set draft nothing, adding no r189. by: work run, under the delegation "The person, 2026-10-27: "I'm delegating this to you. Please get the new version delivered without involving me." Lines 1-9 are i39's requests gate answers a formulate round could not draft (q14 lines 13-16 among them): line 1 replaces requests r13 (r14, an observation listing under work status, is retired with work status); lines 2-5 are q14 lines 13-16 naming work show; line 6 replaces r34; lines 7-9 replace r39, r41 and r43, a 'message' being an answer or a turn. Requirement lines are retired and replaced, never edited. Lines 10-13 fix the bugs i39 met. Answer every question with its recommended reading; where none is recommended, choose the one a test can check."

Read (paths in your worktree):
- .shop/work/i55/supervision.md
- .shop/work/i55/runs/supervision/1-gate
- .shop/work/i55/runs/supervision/2-answer
- .shop/work/i55/runs/supervision/3-answer
- .shop/work/i55/runs/supervision/4-answer
- .shop/work/i55/runs/supervision/5-answer
- .shop/work/i55/runs/supervision/6-apply
- .shop/work/i55/runs/supervision/7-integrate
- .shop/work/i55/runs/supervision/7-integrate/drafts/round-1/

Run directory: /tmp/work-run-i55-mwcb2_hn/supervision-8-gate/.shop/scratch/8-gate
Result file: /tmp/work-run-i55-mwcb2_hn/supervision-8-gate/.shop/scratch/8-gate/result.json

You start in your worktree, /tmp/work-run-i55-mwcb2_hn/supervision-8-gate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
