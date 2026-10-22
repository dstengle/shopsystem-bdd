---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/migration-tools-1
kind: work-item
part_of: capability-proposal/upgrades
status: done
under: migration-tools
accepts: [migration-tools#r15, migration-tools#r18-r20, migration-tools#r22-r28]
fileset: [scripts/migrate, scripts/migrate_upgrade.py, scripts/migrate_upgrade_ids.py, scripts/migrate_write.py, hooks/hooks.json, .claude-plugin/plugin.json, CLAUDE.md, tests/scenarios/migration_upgrade_steps.py, tests/scenarios/test_migration_tools.py]
---

# migration-tools-1

Notes from the coordinator: r15 is checked before r27 (an upgrade with uncommitted changes refuses). The upgrade steps live in the plugin's scripts; the SessionStart hook is the plugin's `hooks/hooks.json`, running `migrate status` from `${CLAUDE_PLUGIN_ROOT}/scripts`. After this work-item the skill delivering-an-initiative must say `work add <initiative> <title>`.
