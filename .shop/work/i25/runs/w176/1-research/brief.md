# research of w176

Work-item: .shop/work/i25/w176.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f582b1bb522f819e5b2c7ff1d38707beafcc63fe
Worktree: /tmp/work-run-i25-13i_gdaw/w176-1-research
Branch: none (a detached checkout)
Work-item branch: work/w176
Accepted scenarios:
- features/work-queue.feature: answer on an awaiting-answer work-item transitions it to the status the asking stage started from (deprecated)
- features/work-queue.feature: answer to a researcher's, a planner's or an implementer's question transitions the work-item to the status that stage started from
- features/work-queue.feature: answer that asks for a change, to a reviewer's question, transitions the work-item to ready
- features/work-queue.feature: answer that accepts the work-item as it is, to a reviewer's question, transitions the work-item to done
- features/work-queue.feature: answer to a reviewer's question that says neither whether it asks for a change nor whether it accepts the work-item is refused, and nothing changes

Read (paths in your worktree):
- .shop/work/i25/w176.md
- spec/capabilities/work-queue.md

Run directory: /tmp/work-run-i25-13i_gdaw/w176-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i25-13i_gdaw/w176-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i25-13i_gdaw/w176-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
