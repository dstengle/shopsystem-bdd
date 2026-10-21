# research of migrate-kb-2

Work-item: .shop/work/i8-model-in-consumers/migrate-kb-2.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: 31e9ed37e6eeb352195be13c9a6470a6e680b1ba
Worktree: /tmp/work-run-i8-model-in-consumers-v2zyal08/migrate-kb-2-1-research
Branch: none (a detached checkout)
File set: scripts/migrate, scripts/migrate_layout.py, scripts/migrate_ledger.py, scripts/migrate_spec.py, tests/scenarios/test_migration_tools.py, tests/scenarios/migration_ledger_steps.py, tests/scenarios/migration_spec_steps.py, tests/scenarios/migration_old.py
Accepted scenarios:
- features/migration-tools.feature: run moves decisions/ to spec/decisions/, work/ to .shop/work/ and each records/<x> to .shop/records/<x>, with git
- features/migration-tools.feature: run moves a file under records/ that is not text as it is
- features/migration-tools.feature: run replaces a ledger entry with a decision file named by its heading, with its first paragraph, accepted, with its date and source
- features/migration-tools.feature: run ends an entry's first paragraph at its date or source line, with or without a blank line before it
- features/migration-tools.feature: run writes a first paragraph and a source that hold <what> so that model reads them as they are
- features/migration-tools.feature: run puts an entry's whole text in its decision file's Decision, its first paragraph also being its summary
- features/migration-tools.feature: run gives a decision file its entry's supersedes and revisit_when, and the entry it supersedes the status `superseded`
- features/migration-tools.feature: run keeps both decisions an entry's supersedes names, each by its new id, and supersedes both
- features/migration-tools.feature: run writes a qualified supersedes as the decision's id alone, the qualifier going to by beside the source
- features/migration-tools.feature: run removes a ledger that holds nothing but <what> once it has replaced every entry
- features/migration-tools.feature: run numbers each ledger entry with no number, in ledger order, from one above the ledger's highest entry number, <case>
- features/migration-tools.feature: run that finds <found> in spec/decisions.md names it, exits non-zero and changes no file, the ledger included
- features/migration-tools.feature: run whose ledger entry's decision file would land on <there> names it, exits non-zero and changes no file
- features/migration-tools.feature: run deprecates a @holding scenario as `features deprecate` does
- features/migration-tools.feature: run gives spec/index.md the id bounded-context/<path>
- features/migration-tools.feature: run rewrites a repository-relative path, a relative Markdown link and a frontmatter id that name what it moved or renamed
- features/migration-tools.feature: run rewrites a frontmatter id and a supersedes that name a ledger entry it numbered
- features/migration-tools.feature: run rewrites a decision file's by that names <old>, a path it moved
- features/migration-tools.feature: after run on a repository with <what>, model check reports no unresolved reference or file problem
- features/migration-tools.feature: run that cannot make two of its changes names both, exits non-zero and changes no file
- features/migration-tools.feature: run that would move a file onto an untracked file names the move, exits non-zero and changes no file
- features/migration-tools.feature: run moves docs/superpowers/plans/, specs/ and requests/ under .shop/records/archive/, with git
- features/migration-tools.feature: run moves adrs/ to .shop/records/decision-arguments/, with git
- features/migration-tools.feature: run gives a capability, a decision file, a plan, a request, a design note, an ADR and a test log the type-first id of its kind
- features/migration-tools.feature: run gives a capability whose id is the short form capability/<name> its full id
- features/migration-tools.feature: run gives a moved README.md no id, kind or about
- features/migration-tools.feature: run numbers each Behaviour line with no id, in Behaviour order, from one above the highest id its capability has ever used
- features/migration-tools.feature: run gives each moved record kind with no about the context as its about
- features/migration-tools.feature: run on a repository with <change> refuses, naming it, exits non-zero and changes no file
- features/migration-tools.feature: run adds every file it wrote or moved to git and writes spec/decisions/index.md

Read (paths in your worktree):
- .shop/work/i8-model-in-consumers/migrate-kb-2.md
- spec/capabilities/migration-tools.md

Run directory: /tmp/work-run-i8-model-in-consumers-v2zyal08/migrate-kb-2-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i8-model-in-consumers-v2zyal08/migrate-kb-2-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i8-model-in-consumers-v2zyal08/migrate-kb-2-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write your notes, plan, report or findings in the run directory and, last, the result file: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings).
