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
- Important, scripts/migrate:63-85,213-219: a ledger heading that is not in the <nnnn>-<slug> form is merged into the entry before it or lost, and spec/decisions.md is removed with exit 0 (r11 says to remove it only once every entry is replaced); Important, scripts/migrate:217,122,291: a ledger entry's new decision file overwrites a decision file moved from decisions/ or already tracked at that path, and its content is lost; Important, scripts/migrate:266-283: an untracked file at a move's destination passes the check, then git mv fails during the writes and leaves earlier moves staged with a traceback (r7: change no file); Important, tests/scenarios/test_migration_tools.py:336-340: r6 is green only because the fixture's old records already carry about:. migrate writes none, so model check reports v10b on a real old-system repository (the person decides: migrate writes about, or r6 is narrowed); Important, scripts/migrate:88-91: summary and by are written unquoted, so model reads a first paragraph with ' #' or a leading '[' wrongly (r2)
