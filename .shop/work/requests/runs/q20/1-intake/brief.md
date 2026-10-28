# intake of q20

Request: .shop/work/requests/q20.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: intake
Worktree: /tmp/work-run-requests-jju0e8j7/q20-1-intake
Branch: round/q20-1-intake
Lines of the request:
- 1. **When** `work show <request>` is run, `work` shall print the request's status, whose turn it is, its lines with their line outcomes, its questions, its answers and its resolution.
- 2. **When** `work list` is run, `work` shall print each initiative and each work-item under `.shop/work/` with its status.
- 3. **When** a round of the kind `integrate` started for a capability-proposal ends with a change list that names another capability for which the initiative holds a capability-proposal, `work run` shall add the round's ids for that capability to that proposal's `adds`, `changes` and `removes`, keeping the ids it holds.

Read (paths in your worktree):
- .shop/work/requests/q20.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/shopsystem-bdd/scripts/work outcome q20 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write no line outcome, and give a question on it in your result's `questions` as `<line>. <question>`, so each line has its line outcome or a question on it. Then pass the turn once with `python3 /home/vscode/shopsystem-bdd/scripts/work turn q20`.

Run directory: /tmp/work-run-requests-jju0e8j7/q20-1-intake/.shop/scratch/1-intake
Result file: /tmp/work-run-requests-jju0e8j7/q20-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /tmp/work-run-requests-jju0e8j7/q20-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
