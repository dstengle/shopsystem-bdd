---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/migrate-decisions
kind: work-item
part_of: capability-proposal/model-in-consumers-migration-tools
status: drafted
wkind: capability
under: migration-tools
accepts: [migration-tools#r22-r26]
blocked_by: [work-item/migrate-layout]
fileset: [scripts/migrate, tests/scenarios/test_migration_tools.py]
---

# The decisions step

Goes green: r22-r26.

- Ledger entries are `## design-decision/<name>` or `## decision/<name>` headings up to the next `## `
  (after the ids step every one is `design-decision/`). File name and frontmatter as r22 and r23; the title
  is the name with any leading `nnnn-` dropped and hyphens as spaces, first letter upper case.
- `source` (r25), for ledger entries and for decision files already under `spec/decisions/` (this
  repository's form): split at `;`, strip; a part beginning with an old or new path of a moved file → that
  file's record id (from the layout step's map) and the rest of the part, if any, to `by`; a part matching
  `<kind>/...` with a node kind → kept; anything else → `by`. Write `source: [a, b]` and
  `by: "<parts joined with '; '>"`, omitting either when empty.
- r24's refusals. r26: run `scripts/model decisions --root <root>` after writing (or call its renderer
  through the same import as the ids step), and include the index in the step's changes.
