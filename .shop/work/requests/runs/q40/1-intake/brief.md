# intake of q40

Request: .shop/work/requests/q40.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: intake
Worktree: /tmp/work-run-requests-61tztsye/q40-1-intake
Branch: round/q40-1-intake
Lines of the request:
- 1. **When** a round of the kind `apply` gives the answers its drafts do not hold, `initiative-round` shall leave out each answer that a later answer of the same proposal replaces.
- 2. **If** a round of the kind `integrate` ends with a change list that adds, changes and removes nothing for a capability-proposal, **then** `work run` shall keep the proposal's status and its requirement ids and start no round of the kind `gate` for it.
- 3. **If** a round of the kind `integrate` ends with a change list that names the glossary and adds, changes and removes no term, **then** `work run` shall write no glossary-proposal.
- 4. **When** a round of the kind `gate` is started for a glossary-proposal, `initiative-round` shall ask only about the terms the glossary-proposal adds, changes and removes.

Read (paths in your worktree):
- .shop/work/requests/q40.md
- spec/index.md

Write the line outcome of each line with `python3 /home/vscode/shopsystem-bdd/scripts/work outcome q40 <line> <accepted|refused|withdrawn>`; for a line you cannot judge write no line outcome, and give a question on it in your result's `questions` as `<line>. <question>`, so each line has its line outcome or a question on it. Then pass the turn once with `python3 /home/vscode/shopsystem-bdd/scripts/work turn q40`.

Run directory: /tmp/work-run-requests-61tztsye/q40-1-intake/.shop/scratch/1-intake
Result file: /tmp/work-run-requests-61tztsye/q40-1-intake/.shop/scratch/1-intake/result.json

You start in your worktree, /tmp/work-run-requests-61tztsye/q40-1-intake: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done.
