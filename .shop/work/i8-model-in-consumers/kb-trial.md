---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/kb-trial
kind: work-item
part_of: capability-proposal/model-in-consumers-migration-tools
status: withdrawn
wkind: capability
under: migration-tools
check: "a fresh clone of https://github.com/dstengle/shopsystem-kb under a scratch directory, migrate run alone (no skill, no gate): model check with no violation, unresolved reference or file problem but v_s3 for the lines that had no scenario before (10 at 2eed357), nothing pushed; recorded in .shop/records/measurements/fixture-runs/"
blocked_by: [work-item/migrate-decisions]
---

# migrate run on a clone of shopsystem-kb

The skeleton's proof for i8, not kb's migration: the clone is thrown away and nothing is pushed. Expect, from kb at
`2eed357`: 371 lines numbered, 154 decision files, kb's records moved, and `model check` passing but for the ten
lines with no scenario (`v_s3`). Record every refusal `migrate` gave.

Withdrawn 2026-10-20 (coordinator): the kb clone trial is the release's check, run by the coordinator after migrate-run is green, not a work-item for work run (it has no accepts).
