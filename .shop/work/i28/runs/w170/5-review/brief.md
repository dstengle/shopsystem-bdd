# review of w170

Work-item: .shop/work/i28/w170.md
Agent: bdd-task-reviewer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 4b7dca6c200ffc64be3fe1887f1d08a62b311332
Worktree: /tmp/work-run-i28-ccl1nki_/w170-5-review
Branch: none (a detached checkout)
Work-item branch: work/w170
Answers the person gave, each with the question it answers:
- Question: Important, scripts/supervise_drafts.py:29: kept drafts are read from drafts/spec/capabilities/*.md, but integrate rounds keep them under drafts/round-<n>/spec/capabilities/, so r102 gives no ids on the real queue (i25's and i26's supervision r98 missed); the scenario's Given uses the same wrong layout
  Answer: 2026-10-25: Accepted as it is under the person's delegation (2026-10-25): the finding is real; r102's scenario is reformulated with the kept drafts' real layout (drafts/round-<n>/spec/capabilities/) and a fix work-item accepting supervision#r102 delivers it, because a reviewer's answer cannot yet return a work-item to implementation (q2, i25).

Read (paths in your worktree):
- .shop/work/i28/w170.md
- spec/capabilities/supervision.md
- .shop/work/i28/runs/w170/1-research
- .shop/work/i28/runs/w170/2-plan
- .shop/work/i28/runs/w170/3-implement
- .shop/work/i28/runs/w170/4-review

Run directory: /tmp/work-run-i28-ccl1nki_/w170-5-review/.shop/scratch/5-review
Result file: /tmp/work-run-i28-ccl1nki_/w170-5-review/.shop/scratch/5-review/result.json

You start in your worktree, /tmp/work-run-i28-ccl1nki_/w170-5-review: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
