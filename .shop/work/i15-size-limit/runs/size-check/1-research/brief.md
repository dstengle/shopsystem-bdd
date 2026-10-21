# research of size-check

Work-item: .shop/work/i15-size-limit/size-check.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 2ea9b66fb6b40f0918de085a0ef8a4be38ac5130
Worktree: /tmp/work-run-i15-size-limit-l6t3hnm6/size-check-1-research
Branch: none (a detached checkout)
File set: scripts/tools, scripts/tools_*.py, features/analysis-tools.feature, tests/scenarios/*analysis_tools*.py, CLAUDE.md, agents/architecture-reviewer.md, agents/bdd-branch-reviewer.md, agents/bdd-task-reviewer.md, agents/bdd-implementer.md, agents/code-scout.md
Accepted scenarios:
- features/analysis-tools.feature: size prints each tracked Python file over the limit in the working tree, with its line count
- features/analysis-tools.feature: size fails when one tracked Python file is over the limit
- features/analysis-tools.feature: size uses the limit --limit gives, and 300 lines without it

Read (paths in your worktree):
- .shop/work/i15-size-limit/size-check.md
- spec/capabilities/analysis-tools.md

Run directory: /tmp/work-run-i15-size-limit-l6t3hnm6/size-check-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i15-size-limit-l6t3hnm6/size-check-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i15-size-limit-l6t3hnm6/size-check-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write your notes, plan, report or findings in the run directory and, last, the result file: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings).
