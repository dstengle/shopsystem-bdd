# intake of q11

Request: .shop/work/requests/q11.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: intake
Worktree: /tmp/work-run-requests-3_ssuuj0/q11-1-intake
Branch: round/q11-1-intake
Lines of the request:
- 1. **When** `work run` checks a work-item against the whole suite, `work run` shall count as expected to fail each scenario whose requirement a capability-proposal that is neither `formulated` nor `withdrawn` adds or changes.

Read (paths in your worktree):
- .shop/work/requests/q11.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/shopsystem-bdd/scripts/work outcome q11 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write no line outcome, and give a question on it in your result's `questions` as `<line>. <question>`, so each line has its line outcome or a question on it. Then pass the turn once with `python3 /home/vscode/shopsystem-bdd/scripts/work turn q11`.

Run directory: /tmp/work-run-requests-3_ssuuj0/q11-1-intake/.shop/scratch/1-intake
Result file: /tmp/work-run-requests-3_ssuuj0/q11-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /tmp/work-run-requests-3_ssuuj0/q11-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
