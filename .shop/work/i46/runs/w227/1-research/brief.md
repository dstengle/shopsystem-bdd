# research of w227

Work-item: .shop/work/i46/w227.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 134745663cfa0a109b8564370c2464ef9ee9a7d5
Worktree: /tmp/work-run-i46-vz485uoj/w227-1-research
Branch: none (a detached checkout)
Work-item branch: work/w227
Accepted scenarios:
- features/supervision.feature: a drafted glossary-proposal is given to a gate round asked only for the questions on the terms it adds, changes or removes
- features/supervision.feature: the <kind> round of a glossary-proposal is given the path of the kept drafts of the integrate round that wrote the proposal
- features/supervision.feature: when the gate round `work run` started for a glossary-proposal ends, the proposal is awaiting-answer
- features/supervision.feature: a glossary-proposal whose every question from its gate round has an answer is given to an apply round with its answers
- features/supervision.feature: when the apply round `work run` started for a glossary-proposal ends having applied its drafts, the proposal is approved
- features/supervision.feature: when the apply round `work run` started for a glossary-proposal ends having applied its drafts, no formulate round is started for the proposal
- features/supervision.feature: an initiative that changes only the glossary, its glossary-proposal approved and its terms committed to spec/index.md, is set done

Read (paths in your worktree):
- .shop/work/i46/w227.md
- spec/capabilities/supervision.md

Run directory: /tmp/work-run-i46-vz485uoj/w227-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i46-vz485uoj/w227-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i46-vz485uoj/w227-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
