# intake of q27

Request: .shop/work/requests/q27.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: intake
Worktree: /tmp/work-run-requests-w1pw1a6c/q27-1-intake
Branch: round/q27-1-intake
Lines of the request:
- 1. **When** `work request` is given a title and a reason and no lines, `work request` shall keep the request with its reason and no lines.
- 2. **When** `work run` takes in a request that has a reason and no lines, `work run` shall start a round that drafts its lines from its reason and gives them to the person as a question.
- 3. **While** a request has no lines, `work start` shall start no initiative for it.

Read (paths in your worktree):
- .shop/work/requests/q27.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/shopsystem-bdd/scripts/work outcome q27 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write no line outcome, and give a question on it in your result's `questions` as `<line>. <question>`, so each line has its line outcome or a question on it. Then pass the turn once with `python3 /home/vscode/shopsystem-bdd/scripts/work turn q27`.

Run directory: /tmp/work-run-requests-w1pw1a6c/q27-1-intake/.shop/scratch/1-intake
Result file: /tmp/work-run-requests-w1pw1a6c/q27-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /tmp/work-run-requests-w1pw1a6c/q27-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
