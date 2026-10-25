# intake of q5

Request: .shop/work/requests/q5.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: intake
Worktree: /tmp/work-run-requests-82dyleze/q5-1-intake
Branch: round/q5-1-intake
Lines of the request:
- 1. **When** `work run` finds an initiative that is not `done`, whose every work-item is `green` or `withdrawn`, whose kept branch review lists nothing to fix now and whose every raised request is `delivered`, `work run` shall set the initiative to `done`.
- 2. **When** `work run` has written an initiative's measurement and its analysis, `work run` shall commit them on the initiative branch.
- 3. **If** a change list that `work run` reads names a capability that `spec/capabilities/` does not have, **then** `work run` shall write no capability-proposal for it and exit with an error naming the capability.
- 4. **When** `work run` starts a round of the kind `gate` or `apply` for a capability-proposal, `work run` shall give the round the path of the kept drafts of the integrate round that wrote the proposal.
- 5. **If** the delegation given to `work request` is empty, **then** `work request` shall refuse, because the delegation is empty, and change nothing.

Read (paths in your worktree):
- .shop/work/requests/q5.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/shopsystem-bdd/scripts/work outcome q5 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write the line outcome `question` and give the question's text, with the number of its line, in your result's `questions`. Then pass the turn once with `python3 /home/vscode/shopsystem-bdd/scripts/work turn q5`.

Run directory: /tmp/work-run-requests-82dyleze/q5-1-intake/.shop/scratch/1-intake
Result file: /tmp/work-run-requests-82dyleze/q5-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /tmp/work-run-requests-82dyleze/q5-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
