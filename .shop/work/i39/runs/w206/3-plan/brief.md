# plan of w206

Work-item: .shop/work/i39/w206.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts
Base: b4c4ad5e86f831f3aedb0695974552aed3ba6064
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w206-3-plan
Branch: none (a detached checkout)
Work-item branch: work/w206
Answers the person gave, each with the question it answers:
- Question: Finding 1 of branch review 2 (fix now): scripts/supervise_change.py write_proposals rewrites the lists of a capability-proposal held for another capability that a redraft integrate round's change list names. w206 accepts only work-queue r34-r39, and supervision r142 and r148 do not say what becomes of that other proposal. Reading A: leave it out of w206 and give it its own work-item under supervision, after a line settles it; until then the narrator still sees the other proposal's adds and removes overwritten by the round's ids. Reading B: fix it in w206 by merging (union) the round's ids into the other proposal's lists, as the findings propose; the narrator sees that proposal keep its applied ids, with the round's ids added. Reading C: fix it in w206 by leaving the other proposal untouched; the narrator sees its lists unchanged and the round's ids for that capability written nowhere. Under B or C the file set gains scripts/supervise_change.py and tests/scripts/test_supervise_change.py.
  Answer: 2026-10-27: Reading B: fix it in w206 by merging (union) the round's ids into the other proposal's adds, changes and removes, as the coordinator restored i39-requests by hand (observation 2026-10-27-redraft-overwrites-other-proposal). Chosen as the one a test can check, and because i39's requests and supervision proposals are yet to be redrafted. The supervision line stating it is carried in the follow-up internal request after i39 (answered by the coordinator under the person's delegation of 2026-10-27).

Read (paths in your worktree):
- .shop/work/i39/w206.md
- spec/capabilities/work-queue.md
- .shop/work/i39/runs/w206/1-research
- .shop/work/i39/runs/w206/2-plan

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w206-3-plan/.shop/scratch/3-plan
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w206-3-plan/.shop/scratch/3-plan/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w206-3-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
