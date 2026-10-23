# research of w108

Work-item: .shop/work/i23-faster-batches-and-a-clean-model-check/w108.md
Agent: code-scout
Scripts: /home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.24.0/scripts
Base: 1ad628182e2dd2eb91d1e0ed6e95ecb34f3bcc63
Worktree: /home/vscode/shopsystem-bdd/.shop/worktrees/w108-1-research
Branch: none (a detached checkout)
Work-item branch: work/w108
Accepted scenarios:
- features/migration-tools.feature: `migrate run` gives spec/index.md the id bounded-context/<path>
- features/migration-tools.feature: `migrate run` gives a capability, a decision file, a plan, a request, a design note, an ADR and a test log the type-first id of its kind
- features/migration-tools.feature: `migrate run` gives a capability whose id is the short form capability/<name> its full id
- features/migration-tools.feature: `migrate run` gives a README.md it relocates to <new> no id, kind or about
- features/migration-tools.feature: `migrate run` gives spec/index.md whose id is bounded-context/shop the id bounded-context/<path>, and rewrites what names the old id (deprecated)
- features/migration-tools.feature: `migrate run` gives spec/index.md whose id is bounded-context/shop the id bounded-context/<path>
- features/migration-tools.feature: `migrate run` gives a decision file whose id is decision/<nnnn>-<name> the type-first id, and rewrites what names the old id (deprecated)
- features/migration-tools.feature: `migrate run` gives a decision file whose id is decision/<nnnn>-<name> the type-first id
- features/migration-tools.feature: `migrate <command>` on a .shop/plugin-version that holds no version exits with an error, naming what it holds (deprecated)
- features/migration-tools.feature: `migrate <command>` on a .shop/plugin-version that holds no version exits with an error, naming that it is empty or what it holds
- features/migration-tools.feature: a session starting in a repository whose .shop/plugin-version holds no version is told to tell the person (deprecated)
- features/migration-tools.feature: a session starting in a repository whose .shop/plugin-version holds no version is told to tell the person that it is empty or what it holds

Read (paths in your worktree):
- .shop/work/i23-faster-batches-and-a-clean-model-check/w108.md
- spec/capabilities/migration-tools.md

Run directory: /home/vscode/shopsystem-bdd/.shop/worktrees/w108-1-research/.shop/scratch/1-research
Result file: /home/vscode/shopsystem-bdd/.shop/worktrees/w108-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /home/vscode/shopsystem-bdd/.shop/worktrees/w108-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
