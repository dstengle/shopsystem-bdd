# intake of q7

Request: .shop/work/requests/q7.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: intake
Worktree: /tmp/work-run-requests-ntx6b4zu/q7-1-intake
Branch: round/q7-1-intake
Lines of the request:
- 1. **When** a round of the kind `gate` that `work run` started for a capability-proposal gives no question, `work run` shall write under the proposal's `## Questions` one question asking for the approval of the proposal's lines as drafted.
- 2. **When** a work-item drafted for a kept branch review's findings turns `green`, `work run` shall start the next branch review of the initiative before it ends.
- 3. **When** `work run` starts a researcher, `work run` shall give the researcher a limit of 80 turns.
- 4. **When** `formulating-features` runs an old scenario alone, `formulating-features` shall run it with `python3 -m pytest`.

Read (paths in your worktree):
- .shop/work/requests/q7.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/shopsystem-bdd/scripts/work outcome q7 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write the line outcome `question` and give the question's text, with the number of its line, in your result's `questions`. Then pass the turn once with `python3 /home/vscode/shopsystem-bdd/scripts/work turn q7`.

Run directory: /tmp/work-run-requests-ntx6b4zu/q7-1-intake/.shop/scratch/1-intake
Result file: /tmp/work-run-requests-ntx6b4zu/q7-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /tmp/work-run-requests-ntx6b4zu/q7-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
