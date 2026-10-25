# apply of review

Capability-proposal: .shop/work/i32/review.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: apply
Drafts path: .shop/work/i32/runs/i32/1-integrate/drafts/round-1/
Base: d3d3839d7347d73cc5e3d51f1761ba13875a4ae2
Worktree: /tmp/work-run-i32-_6c6pt8f/review-3-apply
Branch: round/review-3-apply
Answers the person gave, each with the question it answers:
- Question: Wording of the added line [review#r31] "**When** a branch review ends, the branch reviewer shall give in its result's questions only the findings it triages fix now." It names the result's `questions` field in the words of the request. Readings: (a, recommended) keep the wording as drafted, the request's own text; (b) reword to "shall give as questions in its result only the findings it triages fix now" and name the field `questions` under Implementation. Answer (a) leaves the line as above; answer (b) gives the reworded line.
  Answer: 2026-10-25: (a) Keep the line as drafted, the request's own text, per the delegation of 2026-10-25 to answer every question with its recommended reading: "When a branch review ends, the branch reviewer shall give in its result's questions only the findings it triages fix now." by: work run, under the delegation "The person, 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release". Answer every question with its recommended reading."

Read (paths in your worktree):
- .shop/work/i32/review.md
- .shop/work/i32/runs/review/1-gate
- .shop/work/i32/runs/review/2-answer
- .shop/work/i32/runs/i32/1-integrate/drafts/round-1/

Run directory: /tmp/work-run-i32-_6c6pt8f/review-3-apply/.shop/scratch/3-apply
Result file: /tmp/work-run-i32-_6c6pt8f/review-3-apply/.shop/scratch/3-apply/result.json

You start in your worktree, /tmp/work-run-i32-_6c6pt8f/review-3-apply: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
