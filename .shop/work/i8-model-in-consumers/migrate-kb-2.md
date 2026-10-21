---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/migrate-kb-2
kind: work-item
part_of: capability-proposal/migrate-readings
status: claimed
wkind: capability
under: migration-tools
accepts: [migration-tools#r1-r17]
fileset: [scripts/migrate, scripts/migrate_layout.py, scripts/migrate_ledger.py, scripts/migrate_spec.py, tests/scenarios/test_migration_tools.py, tests/scenarios/migration_ledger_steps.py, tests/scenarios/migration_spec_steps.py, tests/scenarios/migration_old.py]
---

# migrate run on kb, second trial's defects

Goes green: the blind formulator's three rows from the second kb trial
(measurement/2026-10-20-kb-migrate-trial-test-log, "Trial 2"): a moved README.md gets no id, kind or about
(design-decision/references-are-ids); a decision's `by` naming a moved path names the new one (r5); a `supersedes`
naming two decisions keeps both (r2). Every module stays under 300 lines.
