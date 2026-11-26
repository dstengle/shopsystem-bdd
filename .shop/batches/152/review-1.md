---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-152/review-1
kind: review
batch: batch-152
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/175
head: 5ed3ac462ed3b8c05fe43dd2429a75e508ec2a2d
range: 219a6dd86714e77126c7621ab390bc44cc64573a..5ed3ac462ed3b8c05fe43dd2429a75e508ec2a2d
result: clean
---

# batch-152 review 1

## Verdict

The batch builds both chores and their checks hold. b766 moves the upgrades area's modules into the package `scripts/upgrades/` and keeps it apart with the `upgrades-apart` contract. b787 puts the poll loop on `shop work batch next` into the batch brief and into building-a-batch. There is nothing to fix now and one observation.

What I verified:
- **Importers of the moved modules:** none in the batch's tree (`scripts/`, `tests/`, `grammar/`) still names the old flat module names (`migrate_init`, `migrate_ledger`, `migrate_spec`, `migrate_upgrade*`) as a bare import, a dotted string or a `mock.patch`/`monkeypatch` target.
- **Paths from `__file__`:** the risk was that a moved module still works out the plugin's path one folder too shallow. `migrate_upgrade.SCRIPTS` is now `parents[1]`. The `parents[2]` in `migrate_init.py` sits inside `CONFTEST_TEXT`, the text written into a consumer's conftest, so it is right as it is.
- **Contracts:** the plumbing contract now forbids `upgrades`, and `scripts/migrate` stays the entry point outside the package. The `tools check` run shows both contracts kept.
- **Rule catalogue:** `model_rules.implemented` now searches subfolders with `rglob`, and the regenerated `grammar/rules.md` changes only the three `migrate_upgrade_frames.py` paths.
- **b787's test:** it covers every entry of `batch_next.INSTRUCTIONS`.
- **Tests:** none was removed or weakened. `test_kept_modules` swaps the glob `migrate*.py` for `upgrades/*.py` and keeps `migrate` in `KEPT_SCRIPTS`.
- **Size and runs:** the change is 42 files, +166 -99, well under the 1000-line limit. Every run exited 0, as at the base.

## Findings

### f1 Minor observation: the module map's batch_driver row does not mention the poll loop
- item: b787
- where: CLAUDE.md:293
`scripts/batch_driver.py` now gives the driver the loop on `shop work batch next` (`LOOP`, the section `## The loop`). Its row in the module map still lists only "the skill" among what the brief names. b787's chore files do not include `CLAUDE.md`, so the task could not change the row. The session can add "its poll loop on `work batch next` and what each step asks (b787)" to the row between batches, as directive-17 says.
