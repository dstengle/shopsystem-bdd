# intake of q44

Request: .shop/work/requests/q44.md
Agent: initiative-round
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.3/scripts
Kind: intake
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/q44-1-intake
Branch: round/q44-1-intake
Lines of the request:
- 1. **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold for a glossary-proposal, `work run` shall start a new round of the kind `integrate` for the glossary-proposal.

Read (paths in your worktree):
- .shop/work/requests/q44.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.3/scripts/work outcome q44 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write no line outcome, and give a question on it in your result's `questions` as `<line>. <question>`, so each line has its line outcome or a question on it. Then pass the turn once with `python3 /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.28.3/scripts/work turn q44`.

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/q44-1-intake/.shop/scratch/1-intake
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/q44-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/q44-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
