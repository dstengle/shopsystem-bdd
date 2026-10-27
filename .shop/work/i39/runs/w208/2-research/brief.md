# research of w208

Work-item: .shop/work/i39/w208.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts
Base: b4c4ad5e86f831f3aedb0695974552aed3ba6064
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w208-2-research
Branch: none (a detached checkout)
Work-item branch: work/w208
Accepted scenarios:
- features/work-queue.feature: list prints each initiative, each request and each work-item under .shop/work/ with its status
- features/work-queue.feature: list with --json prints each initiative, request and work-item with its status as one JSON object
- features/work-queue.feature: list prints an initiative as waiting on a request it raised into an upstream while that request is not delivered
- features/work-queue.feature: show of an initiative prints where it stands, for a session to start from
- features/work-queue.feature: show of a work-item prints its status and its open questions
- features/work-queue.feature: show of <target> with --json prints its result as one JSON object
Answers the person gave, each with the question it answers:
- Question: the researcher's file set is missing: the researcher's result gave no question and does not give it
  Answer: 2026-10-27: Research again and give the file set in the result, as the researcher's stage requires (answered by the coordinator under the person's delegation of 2026-10-27).

Read (paths in your worktree):
- .shop/work/i39/w208.md
- spec/capabilities/work-queue.md
- .shop/work/i39/runs/w208/1-research

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w208-2-research/.shop/scratch/2-research
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w208-2-research/.shop/scratch/2-research/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w208-2-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
