# intake of q17

Request: .shop/work/requests/q17.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: intake
Worktree: /tmp/work-run-requests-21vc1iu2/q17-1-intake
Branch: round/q17-1-intake
Lines of the request:
- 1. **Where** `spec/index.md` names an upstream bounded-context, **when** a round of the kind `integrate` drafts a line that needs what the upstream does not yet give, `initiative-round` shall give in its result the lines of a request into that upstream, in whatever terms the round has.
- 2. **When** a round of the kind `intake` takes in a request whose lines use terms other than the context's glossary terms, `initiative-round` shall write the lines' outcomes in the context's glossary terms.

Read (paths in your worktree):
- .shop/work/requests/q17.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/shopsystem-bdd/scripts/work outcome q17 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write no line outcome, and give a question on it in your result's `questions` as `<line>. <question>`, so each line has its line outcome or a question on it. Then pass the turn once with `python3 /home/vscode/shopsystem-bdd/scripts/work turn q17`.

Run directory: /tmp/work-run-requests-21vc1iu2/q17-1-intake/.shop/scratch/1-intake
Result file: /tmp/work-run-requests-21vc1iu2/q17-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /tmp/work-run-requests-21vc1iu2/q17-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
