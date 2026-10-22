# research of migration-tools-1

Work-item: .shop/work/i21-work-item-ids-and-upgrades/migration-tools-1.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 202c029c9774c00364b3bace8b0e99b529425e70
Worktree: /tmp/work-run-i21-work-item-ids-and-upgrades-gexbowe1/migration-tools-1-1-research
Branch: none (a detached checkout)
Work-item branch: work/migration-tools-1
Accepted scenarios:
- features/migration-tools.feature: `migrate run` on a repository with <change> refuses, naming it, exits non-zero and changes no file (deprecated)
- features/migration-tools.feature: `<command>` on a repository with <change> refuses, naming it, exits with an error and changes no file
- features/migration-tools.feature: `migrate status` prints the repository's plugin version, the plugin's version and each pending upgrade step with its version and description
- features/migration-tools.feature: a repository with .shop/ and no .shop/plugin-version is taken to be on 0.23.1
- features/migration-tools.feature: `migrate upgrade` applies the pending upgrade step, records the plugin's version and commits it all in one commit naming the step
- features/migration-tools.feature: a session starting in a repository with a pending upgrade step is told to offer the upgrade and run it only on the person's yes
- features/migration-tools.feature: a session starting in a repository on a plugin version above the plugin's is told to tell the person to update the plugin
- features/migration-tools.feature: a session starting in a repository on the plugin's version is told nothing
- features/migration-tools.feature: the upgrade step "work-items named by ids" numbers every work-item from 1, by its initiative's number and then its file name
- features/migration-tools.feature: the upgrade step "work-items named by ids" renames a work-item's file and stage directories and rewrites its name where its initiative names it
- features/migration-tools.feature: `migrate upgrade` with no pending upgrade step says so, exits successfully and changes nothing
- features/migration-tools.feature: a session starting in a repository without .shop/ is told nothing

Read (paths in your worktree):
- .shop/work/i21-work-item-ids-and-upgrades/migration-tools-1.md
- spec/capabilities/migration-tools.md

Run directory: /tmp/work-run-i21-work-item-ids-and-upgrades-gexbowe1/migration-tools-1-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i21-work-item-ids-and-upgrades-gexbowe1/migration-tools-1-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i21-work-item-ids-and-upgrades-gexbowe1/migration-tools-1-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
