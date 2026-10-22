---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/holding-renamed-and-rebound
kind: work-item
part_of: capability-proposal/release-gate-migration-tools
status: researched
wkind: capability
under: migration-tools
accepts: [migration-tools#r3]
fileset: [scripts/migrate, scripts/migrate_*.py, tests/scenarios/*migration*.py, tests/scenarios/test_migration_tools.py]
---

# A held scenario migrated to deprecated, renamed and rebound

Goes green: migration-tools r3 as changed: " (deprecated)" for " (held)" on the title, `Deprecated for:` for `Held for:`, each test naming it by title rebound, no `@holding` left. Today it gives "held one (held) (deprecated)" and the test loses its binding; migrating-to-capabilities does this by hand until then. For after the 0.21.0 release.

## Faults
- work run could not verify that it can push the initiative branch release-0.22.0 to origin before the research stage: fatal: could not read Username for 'https://github.com': No such device or address
