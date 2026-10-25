# review of w185

Work-item: .shop/work/i31/w185.md
Agent: bdd-task-reviewer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 9839b05ad9aad4b8f205963f9f056745069a2206
Worktree: /tmp/work-run-i31-02kb8i6n/w185-7-review
Branch: none (a detached checkout)
Work-item branch: work/w185
Answers the person gave, each with the question it answers:
- Question: supervision#r116: its Then (a formulate round was started for p1, given the answer) passes on today's apply-then-formulate chain (1 passed, no production code changed). Should the scenario also assert that no apply round is started, or is r116 met as is?
  Answer: 2026-10-25: r116 is met as is; that no apply round follows a formulate round's answered questions is r70's changed line, whose scenario w185 also accepts: implement r70 so that only a gate round's answered questions start an apply round (the coordinator under the person's delegation 2026-10-25)
- Question: Important, scripts/supervise_rounds.py:126-131 (rewrite_lists in supervise_change.py:52): an apply round's change list naming an unknown capability is silently dropped and work run exits successfully, against r107; a list naming only other capabilities empties the proposal's lists; Important, scripts/supervise.py:205-213 and supervise_rounds.py:62-67: a refused round stops rounds(), so the initiative's other due proposals get no round before the error, against r115 and r111 (the plan's D4 had them run)
  Answer: 2026-10-25: Fix both: an apply round's change list naming a capability spec/capabilities/ and its drafts do not have is refused as r107 says (no list emptied, work run exits with an error naming it); and a refused round of one proposal lets the initiative's other due proposals have their rounds before work run exits with an error (r111, r115), as the plan's D4 had it (the coordinator under the person's delegation 2026-10-25)

Read (paths in your worktree):
- .shop/work/i31/w185.md
- spec/capabilities/supervision.md
- .shop/work/i31/runs/w185/1-research
- .shop/work/i31/runs/w185/2-plan
- .shop/work/i31/runs/w185/3-implement
- .shop/work/i31/runs/w185/4-implement
- .shop/work/i31/runs/w185/5-review
- .shop/work/i31/runs/w185/6-implement

Run directory: /tmp/work-run-i31-02kb8i6n/w185-7-review/.shop/scratch/7-review
Result file: /tmp/work-run-i31-02kb8i6n/w185-7-review/.shop/scratch/7-review/result.json

You start in your worktree, /tmp/work-run-i31-02kb8i6n/w185-7-review: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
