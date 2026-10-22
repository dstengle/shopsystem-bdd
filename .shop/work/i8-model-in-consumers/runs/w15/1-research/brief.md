# research of migration-rebind-2

Work-item: .shop/work/i8-model-in-consumers/migration-rebind-2.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 31e9ed37e6eeb352195be13c9a6470a6e680b1ba
Worktree: /tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-2-1-research
Branch: none (a detached checkout)
Work-item branch: work/migration-rebind-2
File set: scripts/migrate, scripts/migrate_*.py, tests/scenarios/*migration*.py, tests/scenarios/test_migration_tools.py
Accepted scenarios:
- features/migration-tools.feature: `migrate run` that finds <found> in spec/decisions.md names it, exits with an error and changes no file, the ledger included
- features/migration-tools.feature: `migrate run` whose ledger entry's decision file would land on <there> names it, exits with an error and changes no file
- features/migration-tools.feature: after `migrate run` on a repository with <what>, `model check` prints no unresolved reference or file problem
- features/migration-tools.feature: `migrate run` that cannot make two of its changes names both, exits with an error and changes no file
- features/migration-tools.feature: `migrate run` that would relocate a file onto an untracked file names the relocation, exits with an error and changes no file
- features/migration-tools.feature: `migrate run` relocates docs/superpowers/plans/, specs/ and requests/ under .shop/records/archive/, with git
- features/migration-tools.feature: `migrate run` gives a capability, a decision file, a plan, a request, a design note, an ADR and a test log the type-first id of its kind
- features/migration-tools.feature: `migrate run` gives a capability whose id is the short form capability/<name> its full id
- features/migration-tools.feature: `migrate run` gives a README.md it relocates to <new> no id, kind or about
- features/migration-tools.feature: `migrate run` gives a decision file whose id is decision/<nnnn>-<name> the type-first id
- features/migration-tools.feature: `migrate run` that would <what> names it, exits with an error and changes no file
- features/migration-tools.feature: `migrate run` outside a git repository says so, exits with an error and changes no file

Read (paths in your worktree):
- .shop/work/i8-model-in-consumers/migration-rebind-2.md
- spec/capabilities/migration-tools.md

Run directory: /tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-2-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-2-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-2-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result. Write your notes, plan, report or findings in the run directory.
