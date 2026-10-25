# research of w178

Work-item: .shop/work/i26/w178.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f582b1bb522f819e5b2c7ff1d38707beafcc63fe
Worktree: /tmp/work-run-i26-esefo21v/w178-1-research
Branch: none (a detached checkout)
Work-item branch: work/w178
Accepted scenarios:
- features/supervision.feature: when every work-item is green or withdrawn, `work run` exits successfully, printing each work-item's status (deprecated)
- features/supervision.feature: when every work-item is green or withdrawn and no request whose asker is this context is in the asker's turn, `work run` exits successfully, printing each work-item's status
- features/supervision.feature: when `work run` ends while a request whose asker is this context is in the asker's turn, it exits with an error, printing the request with its open questions
- features/supervision.feature: a request this context is the upstream of that is <status> is given to an intake round (deprecated)
- features/supervision.feature: a request this context is the upstream of that is <status> is given to an intake round that writes each line's line outcome or a question on it
- features/supervision.feature: a question an intake round gives on a line of a request is written in the request
- features/supervision.feature: `work run` started with no initiative, ending with no node awaiting-answer or failed, exits successfully, printing the status of each initiative it took (deprecated)
- features/supervision.feature: `work run` started with no initiative, ending with no node awaiting-answer or failed and no request whose asker is this context in the asker's turn, exits successfully, printing the status of each initiative it took

Read (paths in your worktree):
- .shop/work/i26/w178.md
- spec/capabilities/supervision.md

Run directory: /tmp/work-run-i26-esefo21v/w178-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i26-esefo21v/w178-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i26-esefo21v/w178-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
