---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/model-in-consumers-migration-tools
kind: capability-proposal
part_of: initiative/i8
status: approved
date: 2026-10-19
argues: [migration-tools]
adds: [migration-tools#r1-r7]
---

# Migration tools: scripts/migrate

A new script capability (group service), `capabilities/migration-tools.md`, fully described by its lines as
the plugin's scripts are. Three commands:

- `migrate status` (r2, r3): what is left of the old system, exit 0 when nothing is.
- `migrate run [--context <id>] [--dry-run] [--tests <dir>]` (r4-r29), four steps in order, all computed
  before any is written: **ids** (r11-r16: the Adding Ids numbering and id rewrites of 0.19.0, now a script),
  **layout** (r17-r21: the moves, record ids, moved paths rewritten in tracked text files, `.gitignore`), **decisions**
  (r22-r26: the ledger to decision files, `source` to ids and `by`, the index), **deprecated** (r27-r29:
  `@holding` to `@deprecated`, bindings rebound).
- `migrate plan [--plan <file>] [--drop <n,...>] [--leave <name,...>] [--dry-run]` (r30-r44): run after the
  scenarios are tagged; the living plan to work-items under `initiative/migrated-plan`, and its backlog and
  open log entries to observations.

Shared: r1, r7-r10 (dry run, printed changes, refusal before any write, nothing to do on the final layout),
r45 (exit statuses).

Shown on kb (records/measurements/fixture-runs, 2026-10-16 and 2026-10-17 trials, and a clone at `2eed357`):
21 capabilities with 371 lines and no ids, `spec/index.md` with no frontmatter, a ledger of 154
`## decision/...` entries (20 named `0001-` to `0020-` in ledger order, the rest unnumbered), 154 `source`
lines naming `docs/superpowers/specs/*.md`, `adrs/*.md` or words ("the person's delegation of 2026-10-10"),
31 ADRs and a README under `adrs/`, a living plan `docs/superpowers/plans/2026-09-24-kb-slices.md` with one enabling
slice (180.1, `blocked: done as slice 165.4`), 160 backlog entries and 45 log entries, 43 of them
`QUESTION FOR THE SPEC:`, `REQUEST` or `RE-FORMULATE`, 15 archived plans, 40-odd batch plans, 9 design notes and one request. No
`@holding` scenario, no glossary, no `work/` or `records/`. Each of those has a line here.

kb's `tests/slices.py` names the living plan by its path (`PLAN = "docs/superpowers/plans/2026-09-24-kb-slices.md"`)
and stops the run when it cannot read it; r20 rewrites that path so kb's suite gives the same answer after the
move. Removing kb's own slice machinery is kb's work, after its migration.

Re-synced 2026-10-19 to the EARS lines (initiative/i13, approved by the person): `capabilities/migration-tools.md` is now a walking skeleton (design-decision/behaviour-lines-are-ears), numbered from r1, which replaces the drafted lines wholesale; the drafted ids in the text above were never published. What the drafted lines said beyond the skeleton is in the initiative's "Ideas to test once the skeleton runs".
