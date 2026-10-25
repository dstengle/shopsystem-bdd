# research of w184

Work-item: .shop/work/i30/w184.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 4fbc25cd32843edb441abb8b04189f38edde1105
Worktree: /tmp/work-run-i30-owrwwozx/w184-1-research
Branch: none (a detached checkout)
Work-item branch: work/w184
Accepted scenarios:
- features/supervision.feature: a researcher is given the work-item's file set and accepted scenarios, and a limit of 40 turns (deprecated)
- features/supervision.feature: a researcher is given the work-item's file set and accepted scenarios, and a limit of 80 turns
- features/supervision.feature: when the gate round `work run` started for a capability-proposal gives no question, one question asking for the approval of the proposal's lines as drafted is written under its ## Questions
- features/supervision.feature: when the work-item drafted for a kept branch review's findings turns green, the next branch review of the initiative is started before `work run` exits

Read (paths in your worktree):
- .shop/work/i30/w184.md
- spec/capabilities/supervision.md

Run directory: /tmp/work-run-i30-owrwwozx/w184-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i30-owrwwozx/w184-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i30-owrwwozx/w184-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
