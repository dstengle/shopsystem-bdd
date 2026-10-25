# answer

Agent: delegation-answerer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: none
Worktree: /tmp/work-run-i32-b539vdei/w190-4-answer
Branch: none (a detached checkout)
Question: r119 passes with no production change: `python3 -m pytest -q -n 0 --work-item w190` gives 1 failed, 144 passed; only the r118 test fails. Split the work-item (r118 only needs the code), or confirm r119 stays as a test pinning the existing behaviour?
Delegation: The person, 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release". Answer every question with its recommended reading.

Read (paths in your worktree):
Run directory: /tmp/work-run-i32-b539vdei/w190-4-answer/.shop/scratch/4-answer
Result file: /tmp/work-run-i32-b539vdei/w190-4-answer/.shop/scratch/4-answer/result.json

You start in your worktree, /tmp/work-run-i32-b539vdei/w190-4-answer: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings). When the delegation covers the question, give `DONE` with `answer`, the answer as one line; otherwise give `DONE` with no `answer`.
