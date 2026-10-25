# research of w163

Work-item: .shop/work/i24-requests-and-the-context-loop/w163.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-85n5lsvr/w163-2-research
Branch: none (a detached checkout)
Work-item branch: work/w163
Accepted scenarios:
- features/supervision.feature: a proposed initiative is given to an integrate round with the accepted lines of the request it fulfils
- features/supervision.feature: a proposed initiative that fulfils no request is given no integrate round, stays proposed and leaves nothing behind
- features/supervision.feature: a proposed initiative whose fulfils names a request the queue does not hold is given no integrate round, and nothing changes
- features/supervision.feature: when `work run` starts the integrate round of a proposed initiative, the initiative is started

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w163.md
- spec/capabilities/supervision.md
- .shop/work/i24-requests-and-the-context-loop/runs/w163/1-research

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-85n5lsvr/w163-2-research/.shop/scratch/2-research
Result file: /tmp/work-run-i24-requests-and-the-context-loop-85n5lsvr/w163-2-research/.shop/scratch/2-research/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-85n5lsvr/w163-2-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
