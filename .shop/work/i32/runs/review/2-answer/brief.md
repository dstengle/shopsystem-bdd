# answer

Agent: delegation-answerer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: none
Worktree: /tmp/work-run-i32-_6c6pt8f/review-2-answer
Branch: none (a detached checkout)
Question: Wording of the added line [review#r31] "**When** a branch review ends, the branch reviewer shall give in its result's questions only the findings it triages fix now." It names the result's `questions` field in the words of the request. Readings: (a, recommended) keep the wording as drafted, the request's own text; (b) reword to "shall give as questions in its result only the findings it triages fix now" and name the field `questions` under Implementation. Answer (a) leaves the line as above; answer (b) gives the reworded line.
Delegation: The person, 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release". Answer every question with its recommended reading.

Read (paths in your worktree):
Run directory: /tmp/work-run-i32-_6c6pt8f/review-2-answer/.shop/scratch/2-answer
Result file: /tmp/work-run-i32-_6c6pt8f/review-2-answer/.shop/scratch/2-answer/result.json

You start in your worktree, /tmp/work-run-i32-_6c6pt8f/review-2-answer: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings). When the delegation covers the question, give `DONE` with `answer`, the answer as one line; otherwise give `DONE` with no `answer`.
