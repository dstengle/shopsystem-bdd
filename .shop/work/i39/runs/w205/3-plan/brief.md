# plan of w205

Work-item: .shop/work/i39/w205.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts
Base: b4c4ad5e86f831f3aedb0695974552aed3ba6064
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w205-3-plan
Branch: none (a detached checkout)
Work-item branch: work/w205
Answers the person gave, each with the question it answers:
- Question: work-queue#r39: how does `work list` in this context know that a request an initiative raised into an upstream is not yet `delivered`? Requests are kept only in the upstream's repository (requests Implementation, decision 0067), and this context keeps no record of one it raised. Reading A: this context keeps its own record of each request it raised (which upstream, the request's id there, the initiative it was raised for, and its last known status). `work list` reads only that record. The narrator sees i1 as waiting on q1 until that record is updated, even after the upstream delivers, and `work list` never fails because the upstream cannot be reached. Reading B: `work list` reads each raised request where it is kept, in the upstream's repository, through a registered location of the upstream. The narrator sees the upstream's current status, so the waiting line goes as soon as the upstream delivers. But `work list` depends on reaching the upstream and exits with an error, or prints the status as unknown, when it cannot. Reading C: a request raised into an upstream is also kept in this context's .shop/work/requests/, with its asker as this context, its upstream named and `part_of`/`source` naming the initiative, as work-queue r23 reads requests. `work list` reads that copy. The narrator sees what reading A gives, and the copy's status follows the upstream only when `work` writes it there.
  Answer: 2026-10-27: Reading A: this context keeps its own record of each request it raised (the upstream, the request's id there, the initiative it was raised for, its last known status), and work list reads only that record; it never fails because the upstream cannot be reached. Chosen as the one a test can check without the upstream, matching q14 line 4 (the asker acts from its own repository, with no checkout of the upstream's) and decision 0067 (requests kept only in the upstream's repository), which reading C would contradict (answered by the coordinator under the person's delegation of 2026-10-27).

Read (paths in your worktree):
- .shop/work/i39/w205.md
- spec/capabilities/work-queue.md
- .shop/work/i39/runs/w205/1-research
- .shop/work/i39/runs/w205/2-plan

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w205-3-plan/.shop/scratch/3-plan
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w205-3-plan/.shop/scratch/3-plan/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w205-3-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
