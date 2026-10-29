# intake of q39

Request: .shop/work/requests/q39.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: intake
Worktree: /tmp/work-run-requests-pa82kop0/q39-1-intake
Branch: round/q39-1-intake
Lines of the request:
- 1. **When** `work delegate` is given a request and a delegation, `work` shall write the delegation in the request, replacing any delegation the request has, and commit the request.
- 2. **If** the delegation given to `work delegate` is empty, **then** `work delegate` shall refuse, because the delegation is empty, and change nothing.
- 3. **If** `work delegate` is given a request that is `delivered`, `refused` or `withdrawn`, **then** `work delegate` shall refuse, naming the request's status, and change nothing.
- 4. **When** the person gives a session a delegation for a request outside `work request`, the session shall write it in the request with `work delegate` in the same reply, in the person's words and with the date.
- 5. **When** `work run` reads the delegation of an initiative's request, `work run` shall read the delegation the request has at that moment, given before or after the initiative started.

Read (paths in your worktree):
- .shop/work/requests/q39.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/shopsystem-bdd/scripts/work outcome q39 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write no line outcome, and give a question on it in your result's `questions` as `<line>. <question>`, so each line has its line outcome or a question on it. Then pass the turn once with `python3 /home/vscode/shopsystem-bdd/scripts/work turn q39`.

Run directory: /tmp/work-run-requests-pa82kop0/q39-1-intake/.shop/scratch/1-intake
Result file: /tmp/work-run-requests-pa82kop0/q39-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /tmp/work-run-requests-pa82kop0/q39-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
