# research of migration-rebind-1

Work-item: .shop/work/i8-model-in-consumers/migration-rebind-1.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 31e9ed37e6eeb352195be13c9a6470a6e680b1ba
Worktree: /tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-1-1-research
Branch: none (a detached checkout)
Work-item branch: work/migration-rebind-1
File set: scripts/migrate, scripts/migrate_*.py, tests/scenarios/*migration*.py, tests/scenarios/test_migration_tools.py
Accepted scenarios:
- features/migration-tools.feature: `migrate run` relocates decisions/ to spec/decisions/, work/ to .shop/work/ and each records/<x> to .shop/records/<x>, with git
- features/migration-tools.feature: `migrate run` relocates a file under records/ that is not text as it is
- features/migration-tools.feature: `migrate run` replaces a ledger entry with a decision file named by its heading, with its first paragraph, accepted, with its date and source
- features/migration-tools.feature: `migrate run` ends an entry's first paragraph at its date or source line, with or without a blank line before it
- features/migration-tools.feature: `migrate run` writes a first paragraph and a source that hold <what> so that model reads them as they are
- features/migration-tools.feature: `migrate run` puts an entry's whole text in its decision file's Decision, its first paragraph also being its summary
- features/migration-tools.feature: `migrate run` gives a decision file its entry's supersedes and revisit_when, and the entry it supersedes the status `superseded`
- features/migration-tools.feature: `migrate run` keeps both decisions an entry's supersedes names, each by its new id, and supersedes both
- features/migration-tools.feature: `migrate run` gives spec/index.md the id bounded-context/<path>
- features/migration-tools.feature: `migrate run` rewrites a repository-relative path, a relative Markdown link and a frontmatter id that name what it relocated or renamed
- features/migration-tools.feature: `migrate run` rewrites a frontmatter id and a supersedes that name a ledger entry it numbered
- features/migration-tools.feature: `migrate run` rewrites a decision file's by that names <old>, a path it relocated
- features/migration-tools.feature: `migrate run` from a subdirectory relocates the repository's top-level directories
- features/migration-tools.feature: `migrate run` gives spec/index.md whose id is bounded-context/shop the id bounded-context/<path>
- features/migration-tools.feature: `migrate run` rewrites a frontmatter id that names the context id it changed
- features/migration-tools.feature: `migrate run` rewrites a frontmatter id that names a decision file's old id
- features/migration-tools.feature: `migrate run` rewrites nothing through a tracked symbolic link, and leaves the file outside the repository it points to as it was
- features/migration-tools.feature: `migrate run` keeps the CRLF line endings of a file in which it rewrites a path

Read (paths in your worktree):
- .shop/work/i8-model-in-consumers/migration-rebind-1.md
- spec/capabilities/migration-tools.md

Run directory: /tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-1-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-1-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i8-model-in-consumers-dgjhnmfd/migration-rebind-1-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result. Write your notes, plan, report or findings in the run directory.
