# integrate of i25

Initiative: .shop/work/i25/initiative.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: integrate
Request: q2
Accepted lines of the request:
- 1. **When** a question a reviewer asked on a work-item is answered with a change to make, `work` shall return the work-item to `ready`.
- 2. **When** `work run` starts an implementer for a work-item that an answer to a reviewer's question returned to `ready`, `work run` shall give the implementer the reviewer's findings and the answer.
- 3. **When** a question a reviewer asked on a work-item is answered accepting the work-item as it is, `work` shall return the work-item to `done`.
Base: f582b1bb522f819e5b2c7ff1d38707beafcc63fe
Worktree: /tmp/work-run-i25-kj_6ua58/i25-1-integrate
Branch: round/i25-1-integrate

Read (paths in your worktree):
- .shop/work/i25/initiative.md

Run directory: /tmp/work-run-i25-kj_6ua58/i25-1-integrate/.shop/scratch/1-integrate
Result file: /tmp/work-run-i25-kj_6ua58/i25-1-integrate/.shop/scratch/1-integrate/result.json

You start in your worktree, /tmp/work-run-i25-kj_6ua58/i25-1-integrate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
