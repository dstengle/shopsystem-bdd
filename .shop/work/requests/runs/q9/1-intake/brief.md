# intake of q9

Request: .shop/work/requests/q9.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: intake
Worktree: /tmp/work-run-requests-kyq34im2/q9-1-intake
Branch: round/q9-1-intake
Lines of the request:
- 1. **Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item, `work run` shall transition the work-item to `ready` for an answer that asks for a change and to `done` for one that accepts the work-item as it is.
- 2. **When** a branch review ends, the branch reviewer shall give in its result's questions only the findings it triages fix now.
- 3. **When** work-queue r26 and r27 change what decision 0063 decides for a reviewer's question, the spec shall hold a decision that supersedes the reviewer's row of decision 0063.

Read (paths in your worktree):
- .shop/work/requests/q9.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/shopsystem-bdd/scripts/work outcome q9 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write no line outcome, and give a question on it in your result's `questions` as `<line>. <question>`, so each line has its line outcome or a question on it. Then pass the turn once with `python3 /home/vscode/shopsystem-bdd/scripts/work turn q9`.

Run directory: /tmp/work-run-requests-kyq34im2/q9-1-intake/.shop/scratch/1-intake
Result file: /tmp/work-run-requests-kyq34im2/q9-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /tmp/work-run-requests-kyq34im2/q9-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
