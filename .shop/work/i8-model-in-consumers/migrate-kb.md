---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/migrate-kb
kind: work-item
part_of: capability-proposal/migrate-readings
status: ready
wkind: capability
under: migration-tools
accepts: [migration-tools#r1-r17]
fileset: [scripts/migrate, scripts/migrate_layout.py, scripts/migrate_ledger.py, scripts/migrate_spec.py, tests/scenarios/test_migration_tools.py, tests/scenarios/migration_ledger_steps.py, tests/scenarios/migration_spec_steps.py, tests/scenarios/migration_old.py]
---

# migrate run on kb as it is

Goes green: the rows the blind formulator wrote for the kb trial (measurement/2026-10-20-kb-migrate-trial-test-log):
the approved r2 (superseded status), r6 (narrowed), r8 (requests), r9 (ADRs, requests), r13 (unnumbered entries),
r14 (adrs/), and the trial's defects against existing lines: a dirty tree refused before any change and no
traceback (r7); a capability id in the short form rewritten to the full form (r9); `formulated_as` removed, new
decision files added to git and spec/decisions/index.md written (r6); a `supersedes` value with a qualifier keeps
only the id, its qualifier going to `by` (r2). Every module stays under 300 lines.
