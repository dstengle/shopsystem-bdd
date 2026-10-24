# research of w125

Work-item: .shop/work/i24-requests-and-the-context-loop/w125.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-_5ujkx2k/w125-1-research
Branch: none (a detached checkout)
Work-item branch: work/w125
Accepted scenarios:
- features/supervision.feature: a worker's pytest run that collects scenarios, none of which its work-item accepts, is refused when a requirement the work-item accepts is not of a guarantees capability
- features/supervision.feature: a worker's pytest run that collects scenarios, for a work-item every requirement of which is of a guarantees capability, deselects each of them
- features/supervision.feature: a worker's pytest run for a work-item every requirement of which is of a guarantees capability, left with no test, exits successfully

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w125.md
- spec/capabilities/supervision.md

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-_5ujkx2k/w125-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i24-requests-and-the-context-loop-_5ujkx2k/w125-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-_5ujkx2k/w125-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
