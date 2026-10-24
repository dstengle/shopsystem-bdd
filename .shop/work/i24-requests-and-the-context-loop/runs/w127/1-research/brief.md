# research of w127

Work-item: .shop/work/i24-requests-and-the-context-loop/w127.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-p9l729v3/w127-1-research
Branch: none (a detached checkout)
Work-item branch: work/w127
Accepted scenarios:
- features/requests.feature: outcome in the upstream's turn writes the outcome given as the line outcome of the line named
- features/requests.feature: a side writing a part of a request in the other side's turn is refused, and nothing changes
- features/requests.feature: turn passes the request's turn from the <side> to the <other side>
- features/requests.feature: turn passing a request to its asker with a line that has <line 2> sets the request's status to awaiting-asker
- features/requests.feature: turn passing a request to its upstream sets the request's status to awaiting-upstream

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w127.md
- spec/capabilities/requests.md

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-p9l729v3/w127-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i24-requests-and-the-context-loop-p9l729v3/w127-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-p9l729v3/w127-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
