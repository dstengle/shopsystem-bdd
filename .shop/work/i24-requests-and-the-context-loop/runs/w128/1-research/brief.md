# research of w128

Work-item: .shop/work/i24-requests-and-the-context-loop/w128.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-p9l729v3/w128-1-research
Branch: none (a detached checkout)
Work-item branch: work/w128
Accepted scenarios:
- features/requests.feature: the upstream ending its turn with every line accepted, refused or withdrawn and one accepted sets the status to accepted
- features/requests.feature: the upstream ending its turn with every line refused or withdrawn sets the status to refused
- features/requests.feature: resolve on an accepted request in the asker's turn writes each accepted line's requirement id and version as the resolution
- features/requests.feature: resolve writing a request's resolution sets the request's status to delivered
- features/requests.feature: a command that changes a request commits the request on the current branch

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w128.md
- spec/capabilities/requests.md

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-p9l729v3/w128-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i24-requests-and-the-context-loop-p9l729v3/w128-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-p9l729v3/w128-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
