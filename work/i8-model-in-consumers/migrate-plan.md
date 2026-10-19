---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/migrate-plan
kind: work-item
part_of: capability-proposal/model-in-consumers-migration-tools
status: drafted
wkind: capability
under: migration-tools
accepts: [migration-tools#r30-r44]
blocked_by: [work-item/migrate-layout]
fileset: [scripts/migrate, tests/scenarios/test_migration_tools.py]
---

# The living plan to work-items and observations

Goes green: r30-r44 (design-decision/living-plan-to-work-items).

- Parse the plan as `scripts/plan`'s `--help` describes the format (read it before i10 removes the script, or
  from git history): `## Slice <n>: <name>` blocks, `- Kind:`, `- Scenarios:` (entries `<feature> /
  <title>` joined by `; `), `- Check:`, `- Status:` (the word before the colon), `## Backlog` and `## Log`
  entries `- <date> <text>` with indented continuation lines. A slice with a Status word not in planned,
  in progress, green, blocked is refused.
- Files written: `.shop/work/migrated-plan/initiative.md`, `migrated-<capability>.md` per capability,
  `slice-<n>.md` per work-item, in the forms of r33-r39 and `scripts/model --help`; observations appended to
  `.shop/records/observations.md` (created with `# Observations` and the line "Dated, never edited." when
  missing). Ids and file names must pass `model check`'s id rule (`[a-z0-9]+(-[a-z0-9]+)*` after the context).
- `--dry-run` (r43) prints `slice <n>: work-item | observation | drop` and `observation <name>: <first 80
  characters>` lines.
- A scenario test runs `model check` on the result (r42).
