# intake of q10

Request: .shop/work/requests/q10.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: intake
Worktree: /tmp/work-run-requests-l5ls6e_m/q10-1-intake
Branch: round/q10-1-intake
Lines of the request:
- 1. **If** every work-item of an initiative is `withdrawn`, **then** `work` shall leave the initiative's status as it is.
- 2. **If** `work add` is given an initiative that is `done` or `abandoned`, **then** `work add` shall refuse, naming the initiative's status, and change nothing.
- 3. **When** the delegation-answerer answers a reviewer's question on a work-item, the delegation-answerer shall give in its result whether its answer asks for a change or accepts the work-item as it is.
- 4. **When** a kept branch review's result gives no question, `work run` shall take the review as listing nothing to fix now, whatever its status.

Read (paths in your worktree):
- .shop/work/requests/q10.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/shopsystem-bdd/scripts/work outcome q10 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write no line outcome, and give a question on it in your result's `questions` as `<line>. <question>`, so each line has its line outcome or a question on it. Then pass the turn once with `python3 /home/vscode/shopsystem-bdd/scripts/work turn q10`.

Run directory: /tmp/work-run-requests-l5ls6e_m/q10-1-intake/.shop/scratch/1-intake
Result file: /tmp/work-run-requests-l5ls6e_m/q10-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /tmp/work-run-requests-l5ls6e_m/q10-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
