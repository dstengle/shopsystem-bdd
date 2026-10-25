# research of w185

Work-item: .shop/work/i31/w185.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 9839b05ad9aad4b8f205963f9f056745069a2206
Worktree: /tmp/work-run-i31-lkgnbfux/w185-1-research
Branch: none (a detached checkout)
Work-item branch: work/w185
Accepted scenarios:
- features/supervision.feature: an initiative that a work-item's transition leaves able to be done is set done before `work run` ends
- features/supervision.feature: a capability-proposal whose every question has an answer is given to an apply round with its answers
- features/supervision.feature: a capability-proposal whose every question from its formulate round has an answer is given to a formulate round with the answers
- features/supervision.feature: when the apply round `work run` started for a capability-proposal ends, the proposal's adds, changes and removes are written from the change list the round applied
- features/supervision.feature: when the formulate round `work run` started for a capability-proposal ends, the proposal is formulated (deprecated)
- features/supervision.feature: when the formulate round `work run` started for a capability-proposal ends without giving a question, the proposal is formulated
- features/supervision.feature: when the formulate round `work run` started for a capability-proposal gives questions, each is written under the proposal's ## Questions
- features/supervision.feature: when the formulate round `work run` started for a capability-proposal gives a question, the proposal is awaiting-answer
- features/supervision.feature: when the gate round of a capability-proposal <ending>, the initiative's other nodes are taken through their transitions before `work run` exits with an error

Read (paths in your worktree):
- .shop/work/i31/w185.md
- spec/capabilities/supervision.md

Run directory: /tmp/work-run-i31-lkgnbfux/w185-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i31-lkgnbfux/w185-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i31-lkgnbfux/w185-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
