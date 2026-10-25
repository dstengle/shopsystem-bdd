# integrate of i26

Initiative: .shop/work/i26/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q3
Accepted lines of the request:
- 1. **When** the upstream asks a question on a line of a request in its turn, `work` shall write the question in the request.
- 2. **When** the asker answers a question on a request in its turn, `work` shall write the answer in the request.
- 3. **When** an intake round that `work run` started gives a question on a line of a request, `work run` shall write the question in the request.
- 4. **When** `work run` ends while a request whose asker is this context is in the asker's turn, `work run` shall print the request with its open questions and exit with an error.
Base: f582b1bb522f819e5b2c7ff1d38707beafcc63fe
Worktree: /tmp/work-run-i26-5wp51p8m/i26-1-integrate
Branch: round/i26-1-integrate

Read (paths in your worktree):
- .shop/work/i26/initiative.md

Run directory: /tmp/work-run-i26-5wp51p8m/i26-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i26-5wp51p8m/i26-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i26-5wp51p8m/i26-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
