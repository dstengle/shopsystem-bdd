# research of w96

Work-item: .shop/work/i22-rulings-round-trips-query-output/w96.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: dc9ece7fda16edb90cfd3b8fed2c998b42017e0c
Worktree: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w96-1-research
Branch: none (a detached checkout)
Work-item branch: work/w96
Accepted scenarios:
- features/migration-tools.feature: `migrate run` that finds <found> in spec/decisions.md names it, exits non-zero and changes no file, the ledger included
- features/migration-tools.feature: `migrate run` whose ledger entry's decision file would land on <there> names it, exits non-zero and changes no file
- features/migration-tools.feature: `migrate run` that cannot make two of its changes names both, exits non-zero and changes no file
- features/migration-tools.feature: `migrate run` that would relocate a file onto an untracked file names the relocation, exits non-zero and changes no file
- features/migration-tools.feature: `migrate run` that would <what> names it, exits non-zero and changes no file
- features/migration-tools.feature: `migrate run` outside a git repository says so, exits non-zero and changes no file
- features/migration-tools.feature: `migrate status` prints the repository's plugin version, the plugin's version and each pending upgrade step with its version and description
- features/migration-tools.feature: the upgrade step "work-items named by ids" numbers every work-item from 1, by its initiative's number and then its file name
- features/migration-tools.feature: the upgrade step "work-items named by ids" renames a work-item's file and stage directories and rewrites its name where its initiative names it
- features/migration-tools.feature: the upgrade step "work-items named by ids" rewrites a reference from another initiative and a for: to the id of the work-item they name

Read (paths in your worktree):
- .shop/work/i22-rulings-round-trips-query-output/w96.md
- spec/capabilities/migration-tools.md

Run directory: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w96-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w96-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i22-rulings-round-trips-query-output-al5ntwjo/w96-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
