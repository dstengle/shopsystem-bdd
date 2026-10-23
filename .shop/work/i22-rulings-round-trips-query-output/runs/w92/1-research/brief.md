# research of w92

Work-item: .shop/work/i22-rulings-round-trips-query-output/w92.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: dc9ece7fda16edb90cfd3b8fed2c998b42017e0c
Worktree: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w92-1-research
Branch: none (a detached checkout)
Work-item branch: work/w92
Accepted scenarios:
- features/supervision.feature: an implementer's DONE whose <tests> fail makes the work-item's transition to awaiting-ruling (deprecated)
- features/supervision.feature: an implementer's DONE whose <tests> fail makes the work-item's transition to awaiting-answer
- features/supervision.feature: a researcher that gives <outcome> makes the work-item's transition to awaiting-ruling (deprecated)
- features/supervision.feature: a researcher that gives <outcome> makes the work-item's transition to awaiting-answer
- features/supervision.feature: when no work-item can make a transition and one is awaiting-ruling, `work run` exits with an error, printing each work-item's status and each open question (deprecated)
- features/supervision.feature: when no work-item can make a transition and one is awaiting-answer, `work run` exits with an error, printing each work-item's status and each open question
- features/supervision.feature: `work run` prints a question that has no ruling yet, and not one that has a ruling (deprecated)
- features/supervision.feature: `work run` prints a question that has no answer yet, and not one that has an answer
- features/supervision.feature: a work-item whose transition is to awaiting-ruling keeps its work-item branch (deprecated)
- features/supervision.feature: a work-item whose transition is to awaiting-answer keeps its work-item branch
- features/supervision.feature: a question goes into the work-item's ## Questions, before a section that follows it (deprecated)
- features/supervision.feature: a question goes into the work-item's ## Questions, before a section that follows it
- features/supervision.feature: no worker is started for a work-item that is <status> (deprecated)
- features/supervision.feature: no worker is started for a work-item that is <status>
- features/supervision.feature: no worker is started for a work-item after its transition to awaiting-answer
- features/supervision.feature: the brief of a worker for a work-item that has answers holds each answer with the question it answers
- features/supervision.feature: an implementer started for a work-item whose work-item branch was kept works in a worktree on that branch

Read (paths in your worktree):
- .shop/work/i22-rulings-round-trips-query-output/w92.md
- spec/capabilities/supervision.md

Run directory: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w92-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w92-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w92-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
