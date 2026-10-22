# research of migration-rebind-4

Work-item: .shop/work/i8-model-in-consumers/migration-rebind-4.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 31e9ed37e6eeb352195be13c9a6470a6e680b1ba
Worktree: /tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-4-1-research
Branch: none (a detached checkout)
Work-item branch: work/migration-rebind-4
File set: scripts/migrate, scripts/migrate_*.py, tests/scenarios/*migration*.py, tests/scenarios/test_migration_tools.py
Accepted scenarios:
- features/migration-tools.feature: `migrate run` writes a qualified supersedes as the decisions' ids alone, the qualifier going to by, <case>
- features/migration-tools.feature: `migrate run` relocates adrs/ to .shop/records/decision-arguments/, with git
- features/migration-tools.feature: `migrate run` on a repository with <change> refuses, naming it, and changes no file
- features/migration-tools.feature: `migrate run` adds every file it wrote or relocated to git and writes spec/decisions/index.md

Read (paths in your worktree):
- .shop/work/i8-model-in-consumers/migration-rebind-4.md
- spec/capabilities/migration-tools.md

Run directory: /tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-4-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-4-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-4-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result. Write your notes, plan, report or findings in the run directory.
