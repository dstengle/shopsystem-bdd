---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/migrate-status-and-ids
kind: work-item
part_of: capability-proposal/model-in-consumers-migration-tools
status: drafted
wkind: capability
under: migration-tools
accepts: [migration-tools#r1-r16, migration-tools#r45]
blocked_by: [work-item/final-layout-read, work-item/deprecated-and-sources]
fileset: [scripts/migrate, tests/scenarios/test_migration_tools.py, tests/scenarios/conftest.py]
---

# scripts/migrate: status, the run's frame, and the ids step

Goes green: the scenarios of migration-tools r1-r16 and r45, in `tests/scenarios/test_migration_tools.py`
bound by `scenarios("migration-tools.feature")` (the feature file is written at formulation); the other
steps' scenarios stay red for the work-items after this one.

- `scripts/migrate`, Python 3 standard library, `--help` its contract (CONTRACT text like `scripts/model`'s),
  argparse: `--root`; `status`; `run [--context ID] [--dry-run] [--tests DIR]`; `plan [--plan FILE]
  [--drop LIST] [--leave LIST] [--dry-run]`. Exit 0, 1 (refused, or `status` found something), 2 usage.
- The frame every step uses: a step returns a list of changes (move, write file, rewrite file) and a list of
  refusals; `run` computes all steps on an in-memory view of the tree, then refuses with every refusal or
  writes every change (r7-r10). Printing: `<step>: <change>` lines, then `<step>: <n> changes`.
- `status` (r2, r3): the checks in r2's order, one line each, naming the path.
- The ids step (r11-r16), the 0.19.0 Adding Ids step 2 as code (skills/migrating-to-capabilities, Adding
  Ids, step 2 has the rules): index id, `[r<n>]` numbering, `retired: []`, capability ids, `decision/` and
  `obs/` rewrites in frontmatter and headings, frontmatter ids in full, `formulated_as`. It works on the files
  wherever they are when it runs (before the layout step moves them): `decisions/`, `work/`, `records/`,
  `spec/decisions.md`. Reuse `scripts/model`'s frontmatter reader by importing it from the script's
  directory (`importlib` from `Path(__file__).with_name("model")`), so both read one YAML subset; write
  frontmatter by editing lines in place, never by re-serialising, so nothing else in a file changes.
- Step fixtures: a builder in `tests/scenarios/conftest.py` for an old-layout repository (a git repository
  in a temporary directory with `git init`, an identity, and an initial commit).
