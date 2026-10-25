# intake of q3

Request: .shop/work/requests/q3.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: intake
Worktree: /tmp/work-run-requests-zt3zipbi/q3-1-intake
Branch: round/q3-1-intake
Lines of the request:
- 1. **When** the upstream asks a question on a line of a request in its turn, `work` shall write the question in the request.
- 2. **When** the asker answers a question on a request in its turn, `work` shall write the answer in the request.
- 3. **When** an intake round that `work run` started gives a question on a line of a request, `work run` shall write the question in the request.
- 4. **When** `work run` ends while a request whose asker is this context is in the asker's turn, `work run` shall print the request with its open questions and exit with an error.

Read (paths in your worktree):
- .shop/work/requests/q3.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/shopsystem-bdd/scripts/work outcome q3 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write the line outcome `question` and give the question's text, with the number of its line, in your result's `questions`. Then pass the turn once with `python3 /home/vscode/shopsystem-bdd/scripts/work turn q3`.

Run directory: /tmp/work-run-requests-zt3zipbi/q3-1-intake/.shop/scratch/1-intake
Result file: /tmp/work-run-requests-zt3zipbi/q3-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /tmp/work-run-requests-zt3zipbi/q3-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
