# intake of q13

Request: .shop/work/requests/q13.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts
Kind: intake
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/q13-1-intake
Branch: round/q13-1-intake
Lines of the request:
- 1. **When** `work run` writes the brief of a round of the kind `formulate`, `work run` shall tell the round that a round that has formulated every line with one reading and gives each other line as a question has done its work, with the outcome `DONE`.
- 2. **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question with the outcome `PARTIAL`, `work run` shall write each question its result gives under the proposal's `## Questions`.
- 3. **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question with the outcome `PARTIAL`, `work run` shall transition the proposal to `awaiting-answer`.

Read (paths in your worktree):
- .shop/work/requests/q13.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts/work outcome q13 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write no line outcome, and give a question on it in your result's `questions` as `<line>. <question>`, so each line has its line outcome or a question on it. Then pass the turn once with `python3 /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts/work turn q13`.

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/q13-1-intake/.shop/scratch/1-intake
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/q13-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/q13-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
