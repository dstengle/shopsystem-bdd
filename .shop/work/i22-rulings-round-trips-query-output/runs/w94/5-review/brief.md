# review of w94

Work-item: .shop/work/i22-rulings-round-trips-query-output/w94.md
Agent: bdd-task-reviewer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: dc9ece7fda16edb90cfd3b8fed2c998b42017e0c
Worktree: /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w94-5-review
Branch: none (a detached checkout)
Work-item branch: work/w94
Answers the person gave, each with the question it answers:
- Question: r41 counts transitions 'to awaiting-answer', but every log written so far (this initiative's included, until w91 and decision 0064's upgrade step land) says awaiting-answer, and the deprecated r41 scenario, which w94 accepts and does not retire, expects '1 time to awaiting-answer'. What does measure count? Reading A, awaiting-answer only: a log with awaiting-answer transitions gives 0 to awaiting-answer; the deprecated r41 scenario goes red and w94 needs it retired (a Retires section). Reading B, awaiting-answer counted as the old name of awaiting-answer (0064: the status 'is' awaiting-answer): a log not yet upgraded gives its awaiting-answer transitions in the one awaiting-answer count; the deprecated scenario is kept, its step asserting that count is 1. Reading C, both counted apart: the measurement and show give an awaiting-answer count and an awaiting-answer count side by side; the deprecated scenario is kept as it reads.
  Answer: 2026-10-23: Reading A: measure counts awaiting-answer only; the r29 upgrade step renames old logs. w94 retires the deprecated r41 scenario (a Retires section).

Read (paths in your worktree):
- .shop/work/i22-rulings-round-trips-query-output/w94.md
- spec/capabilities/batch-measurement.md
- .shop/work/i22-rulings-round-trips-query-output/runs/w94/1-research
- .shop/work/i22-rulings-round-trips-query-output/runs/w94/2-plan
- .shop/work/i22-rulings-round-trips-query-output/runs/w94/3-plan
- .shop/work/i22-rulings-round-trips-query-output/runs/w94/4-implement

Run directory: /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w94-5-review/.shop/scratch/5-review
Result file: /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w94-5-review/.shop/scratch/5-review/result.json

You start in your worktree, /tmp/work-run-i22-rulings-round-trips-query-output-e455jsrc/w94-5-review: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
