---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/migrate-status-and-ids
kind: work-item
part_of: capability-proposal/model-in-consumers-migration-tools
status: drafted
wkind: capability
under: migration-tools
accepts: [migration-tools#r1, migration-tools#r4-r5, migration-tools#r7-r10]
blocked_by: [work-item/final-layout-read, work-item/deprecated-and-sources]
fileset: [scripts/migrate, tests/scenarios/test_migration_tools.py, tests/scenarios/conftest.py]
---

# scripts/migrate: the run's frame, the moves and the ids

Goes green: the scenarios of migration-tools r1, r4, r5 and r7, in `tests/scenarios/test_migration_tools.py`
bound by `scenarios("migration-tools.feature")` (the feature file is written at formulation); r2, r3 and r6 stay
red for migrate-decisions.

- `scripts/migrate`, Python 3 standard library, `--help` its contract (CONTRACT text like `scripts/model`'s),
  argparse: `--root`; `run --context ID`.
- The frame every step uses: a step returns a list of changes (move, write file, rewrite file) and a list of
  refusals; `run` computes all steps on an in-memory view of the tree, then refuses with every refusal, changing no
  file, or writes every change (r7).
- The moves (r1) with `git mv`: the decisions to `spec/decisions/`, `work/` to `.shop/work/`, `records/` and
  `docs/superpowers/` to `.shop/records/`.
- The ids (r4), the 0.19.0 Adding Ids step 2 as code (skills/migrating-to-capabilities, Adding Ids, step 2 has the
  rules): the index id, `[r<n>]` numbering, capability ids, decision and record ids on the final layout. Reuse
  `scripts/model`'s frontmatter reader by importing it from the script's directory, so both read one YAML subset;
  write frontmatter by editing lines in place, never by re-serialising, so nothing else in a file changes.
- The references (r5): each moved path and changed id rewritten in the tracked text files.
- Step fixtures: a builder in `tests/scenarios/conftest.py` for an old-layout repository (a git repository in a
  temporary directory with `git init`, an identity, and an initial commit).

Takes what migrate-status-and-ids and migrate-layout had of the skeleton (initiative/i13, 2026-10-19); `migrate
status` leaves it, with the rest in the initiative's "Ideas to test once the skeleton runs".
