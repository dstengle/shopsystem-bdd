# research of w177

Work-item: .shop/work/i26/w177.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f582b1bb522f819e5b2c7ff1d38707beafcc63fe
Worktree: /tmp/work-run-i26-esefo21v/w177-1-research
Branch: none (a detached checkout)
Work-item branch: work/w177
Accepted scenarios:
- features/requests.feature: outcome writing a line outcome leaves the request's lines as the asker wrote them (deprecated)
- features/requests.feature: outcome writing a line outcome leaves the request's lines and answers as the asker wrote them
- features/requests.feature: turn passing a request leaves its line outcomes as they were and writes no resolution (deprecated)
- features/requests.feature: the asker answering a question leaves the request's questions and line outcomes as they were and writes no resolution
- features/requests.feature: the upstream asking a question on a line in its turn writes the question in the request
- features/requests.feature: the asker answering a question in its turn writes the answer in the request
- features/requests.feature: a command that changes a request commits the request on the current branch (deprecated)
- features/requests.feature: a change to a request commits the request on the current branch

Read (paths in your worktree):
- .shop/work/i26/w177.md
- spec/capabilities/requests.md

Run directory: /tmp/work-run-i26-esefo21v/w177-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i26-esefo21v/w177-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i26-esefo21v/w177-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
