# intake of q31

Request: .shop/work/requests/q31.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: intake
Worktree: /tmp/work-run-requests-ycn8qyfc/q31-1-intake
Branch: round/q31-1-intake
Lines of the request:
- 1. The bounded context shall have a backlog of ideas and observations, kept in the repository.
- 2. **When** the person gives a session an idea or an observation outside an initiative, the session shall add it to the backlog in the same turn, with its date and the person's words.
- 3. The session-start hook's text shall give no item of the backlog.
- 4. **While** an item of the backlog has had no discovery discussion with the person, the plugin shall draft no request and no proposal from it.
- 5. **When** the person and a session have held a discovery discussion on an item of the backlog, the session shall raise a request from it, naming the item as its source.
- 6. The bounded context shall have a log of temporary rules that the person gives its sessions, kept in the repository.
- 7. **When** the person gives a session a rule outside an initiative, the session shall add it to the log of temporary rules in the same turn, with its date and the person's words.
- 8. The session-start hook's text shall give each rule of the log of temporary rules.
- 9. **When** the person rules that a rule of the log of temporary rules moves to the backlog, the session shall move it from the log to the backlog.
- 10. The session shall keep each rule, idea and observation of the bounded context in the repository.

Read (paths in your worktree):
- .shop/work/requests/q31.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/shopsystem-bdd/scripts/work outcome q31 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write no line outcome, and give a question on it in your result's `questions` as `<line>. <question>`, so each line has its line outcome or a question on it. Then pass the turn once with `python3 /home/vscode/shopsystem-bdd/scripts/work turn q31`.

Run directory: /tmp/work-run-requests-ycn8qyfc/q31-1-intake/.shop/scratch/1-intake
Result file: /tmp/work-run-requests-ycn8qyfc/q31-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /tmp/work-run-requests-ycn8qyfc/q31-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
