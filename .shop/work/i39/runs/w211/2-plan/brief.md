# plan of w211

Work-item: .shop/work/i39/w211.md
Agent: bdd-planner
Scripts: /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts
Base: b4c4ad5e86f831f3aedb0695974552aed3ba6064
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w211-2-plan
Branch: none (a detached checkout)
Work-item branch: work/w211
Questions the researcher gave, for you to settle or ask:
- Carrier of 'sent' (r39-r43) and the upstream's asker-id allow list (decision 0071): no mechanism or list location in spec or code. Git transport of requests files, or a drop directory?
- work-queue r7 scenario (lines file missing, --source, asker ctx-a, features/work-queue.feature:304) conflicts with r30 if the origin check runs before the file check. Keep the order (test stays) or change the scenario?
- supervision raise (r135) writes requests into the upstream's checkout; under r28 read for every writer, features/supervision.feature:1445-1452 cannot pass. Does r28 bind supervision's raise?
- Work-item Retires cites requests @r44 and @r45 for the deprecated titles, but features/requests.feature tags those titles @r1 and @r3; @r44 and @r45 are the live scenarios. Which tags are meant?
- A request with an empty lines file is accepted with no lines (probe K). Refuse it, or accept it?

Read (paths in your worktree):
- .shop/work/i39/w211.md
- spec/capabilities/requests.md
- .shop/work/i39/runs/w211/1-research

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w211-2-plan/.shop/scratch/2-plan
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w211-2-plan/.shop/scratch/2-plan/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w211-2-plan: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
