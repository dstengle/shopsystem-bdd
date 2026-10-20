---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/migrate-run
kind: work-item
part_of: capability-proposal/migrate-readings
status: awaiting-ruling
wkind: capability
under: migration-tools
accepts: [migration-tools#r1-r12]
fileset: [scripts/migrate, tests/scenarios/test_migration_tools.py, tests/scripts/test_bound.py]
---

# migrate run takes a repository on the old system to the final layout

Goes green: features/migration-tools.feature (formulated by the blind formulator, 2026-10-20), every scenario,
bound by `scenarios("migration-tools.feature")` in tests/scenarios/test_migration_tools.py and listed in
tests/scripts/test_bound.py. `scripts/migrate run --context <owner/product/context>` does the transcription of
design-decision/migration-in-one-pass; it reuses scripts/model's reading of frontmatter and scripts/features'
deprecation (`features deprecate`) rather than a second reading of either. Built through `work run`.

## Questions
- Critical, features/migration-tools.feature:16-105,155-170,195-201: changed in fix commits 115e50c and 5eaf500 (new r1/r2/r7/r11/r12 scenarios, r8 Thens reworded) by the session that wrote the code. Confirm these as formulation or send them back to the formulator.; Important, scripts/migrate_layout.py:114-133: record_kind gives a kind to a non-.md plan or design note. A docs/superpowers/specs/*.png crashes migrate with a traceback, and a .json plan gets YAML frontmatter. Limit record_kind to .md files.
