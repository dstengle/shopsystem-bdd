# intake of q2

Request: .shop/work/requests/q2.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: intake
Worktree: /tmp/work-run-requests-6b6d7p70/q2-1-intake
Branch: round/q2-1-intake
Lines of the request:
- 1. **When** a question a reviewer asked on a work-item is answered with a change to make, `work` shall return the work-item to `ready`.
- 2. **When** `work run` starts an implementer for a work-item that an answer to a reviewer's question returned to `ready`, `work run` shall give the implementer the reviewer's findings and the answer.
- 3. **When** a question a reviewer asked on a work-item is answered accepting the work-item as it is, `work` shall return the work-item to `done`.

Read (paths in your worktree):
- .shop/work/requests/q2.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/shopsystem-bdd/scripts/work outcome q2 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write the line outcome `question` and give the question's text, with the number of its line, in your result's `questions`. Then pass the turn once with `python3 /home/vscode/shopsystem-bdd/scripts/work turn q2`.

Run directory: /tmp/work-run-requests-6b6d7p70/q2-1-intake/.shop/scratch/1-intake
Result file: /tmp/work-run-requests-6b6d7p70/q2-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /tmp/work-run-requests-6b6d7p70/q2-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
