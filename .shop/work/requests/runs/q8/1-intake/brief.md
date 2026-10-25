# intake of q8

Request: .shop/work/requests/q8.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: intake
Worktree: /tmp/work-run-requests-b73lf6jr/q8-1-intake
Branch: round/q8-1-intake
Lines of the request:
- 1. **When** a transition that `work run` makes leaves a node of an initiative able to make another transition, `work run` shall take the node through that transition before it ends.
- 2. **If** a round that `work run` started for one capability-proposal ends with an outcome other than `DONE`, **then** `work run` shall take the initiative's other nodes through their transitions before it exits with an error.
- 3. **When** a round of the kind `formulate` that `work run` started for a capability-proposal gives a question, `work run` shall write the question under the proposal's `## Questions` and transition the proposal to `awaiting-answer`.
- 4. **When** a round of the kind `apply` that `work run` started for a capability-proposal ends, `work run` shall write the proposal's `adds`, `changes` and `removes` from the change list the round applied.

Read (paths in your worktree):
- .shop/work/requests/q8.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/shopsystem-bdd/scripts/work outcome q8 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write the line outcome `question` and give the question's text, with the number of its line, in your result's `questions`. Then pass the turn once with `python3 /home/vscode/shopsystem-bdd/scripts/work turn q8`.

Run directory: /tmp/work-run-requests-b73lf6jr/q8-1-intake/.shop/scratch/1-intake
Result file: /tmp/work-run-requests-b73lf6jr/q8-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /tmp/work-run-requests-b73lf6jr/q8-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
