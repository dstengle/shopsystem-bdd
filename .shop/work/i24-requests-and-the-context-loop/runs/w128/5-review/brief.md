# review of w128

Work-item: .shop/work/i24-requests-and-the-context-loop/w128.md
Agent: bdd-task-reviewer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-31fe_luq/w128-5-review
Branch: none (a detached checkout)
Work-item branch: work/w128
Answers the person gave, each with the question it answers:
- Question: Important, scripts/workqueue_request.py:70-75: work turn from the upstream on a delivered request whose lines are all settled resets the status to accepted, losing r11's delivered (reproduced). r8 and r9 need a ruling that they hold only for a request not yet delivered.
  Answer: 2026-10-24: Accept the work-item as it stands (the coordinator, under the person's delegation): requests r8 and r9 are being changed to hold only for a request that is not delivered; that change and its scenario are delivered by their own fix work-item, drafted after the spec and formulate rounds.

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w128.md
- spec/capabilities/requests.md
- .shop/work/i24-requests-and-the-context-loop/runs/w128/1-research
- .shop/work/i24-requests-and-the-context-loop/runs/w128/2-plan
- .shop/work/i24-requests-and-the-context-loop/runs/w128/3-implement
- .shop/work/i24-requests-and-the-context-loop/runs/w128/4-review

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-31fe_luq/w128-5-review/.shop/scratch/5-review
Result file: /tmp/work-run-i24-requests-and-the-context-loop-31fe_luq/w128-5-review/.shop/scratch/5-review/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-31fe_luq/w128-5-review: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
