# research of w155

Work-item: .shop/work/i24-requests-and-the-context-loop/w155.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-48xzxfbo/w155-1-research
Branch: none (a detached checkout)
Work-item branch: work/w155
Accepted scenarios:
- features/supervision.feature: when a session started under a delegation to answer a question ends at its turn limit, the question is left unanswered for the person
- features/supervision.feature: when a session started under a delegation to answer a question ends in an error, its stage directory and log lines are committed

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w155.md
- spec/capabilities/supervision.md

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-48xzxfbo/w155-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i24-requests-and-the-context-loop-48xzxfbo/w155-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-48xzxfbo/w155-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
