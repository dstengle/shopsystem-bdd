# intake of q41

Request: .shop/work/requests/q41.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: intake
Worktree: /tmp/work-run-requests-m91282fu/q41-1-intake
Branch: round/q41-1-intake
Lines of the request:
- 1. **When** a scenario's steps make a git repository for the scenario, the steps shall keep git from starting any maintenance of that repository that runs after the step that started it ends.
- 2. **If** a scenario's run fails for a reason that a rerun of that scenario alone does not repeat, **then** `work run` shall run that scenario again once before it refuses the merge, and give both runs in its question when the second also fails.

Read (paths in your worktree):
- .shop/work/requests/q41.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/shopsystem-bdd/scripts/work outcome q41 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write no line outcome, and give a question on it in your result's `questions` as `<line>. <question>`, so each line has its line outcome or a question on it. Then pass the turn once with `python3 /home/vscode/shopsystem-bdd/scripts/work turn q41`.

Run directory: /tmp/work-run-requests-m91282fu/q41-1-intake/.shop/scratch/1-intake
Result file: /tmp/work-run-requests-m91282fu/q41-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /tmp/work-run-requests-m91282fu/q41-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
