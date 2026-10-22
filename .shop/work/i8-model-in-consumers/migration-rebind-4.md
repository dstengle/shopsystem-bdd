---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/migration-rebind-4
kind: work-item
part_of: capability-proposal/one-requirement-migration-tools
status: ready
wkind: capability
under: migration-tools
accepts: [migration-tools#r14, migration-tools#r15, migration-tools#r16, migration-tools#r17]
fileset: [tests/scenarios/migration_ledger_steps.py, tests/scenarios/test_migration_tools.py, scripts/migrate, scripts/migrate_layout.py, scripts/migrate_ledger.py, scripts/migrate_spec.py, scripts/migrate_write.py, scripts/model, scripts/model_report.py, scripts/model_facts.py, tests/scenarios/migration_old.py, tests/scenarios/migration_spec_steps.py, tests/scenarios/migration_safety_steps.py]
---

# migration-tools r14-r17: the reformulated scenarios bound

Goes green: the scenarios of the lines it accepts, as the blind formulator rewrote features/migration-tools.feature
for 0.22.0 (one requirement per scenario, exits in words), their step definitions following.
