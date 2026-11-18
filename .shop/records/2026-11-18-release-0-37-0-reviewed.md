---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-18-release-0-37-0-reviewed
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-18
---

# Release 0.37.0 reviewed

One fresh reviewer read branch `plan-release-0.37.0` (head dc5355350) against `.shop/records/2026-11-18-release-0.37.0/plan.md` and what shipped since v0.36.0. Verdict: ready to merge; five Minor findings, no Critical or Important.

Verified: the version (0.37.0 by design-decision 0092: b333 retires readiness#r49 and `work ready` and `work batch start` refuse more); no upgrade step (a clone at 0.36.0: `migrate status` names none, `migrate upgrade` records 0.37.0); all fifteen delivered items of batches 43-46 in the notes with their PRs, nothing else; b175's refusal, b301's comma form, `work chore`'s refusals, `work promote --to` and `model forms --check` run in a throwaway clone; the new "Shape a chore" recipe reproduced byte for byte; docs, docs-lines, migrate-upgrade and retirement tests passed.

Findings and what was done (commit 653f740c2):

1. Minor, CHANGELOG.md: "two groups of different conditions, v15k and v15l" misdescribed the rules (v15k: a group's statements differ in trigger or condition; v15l: a group of more than one statement). Fixed: "a group holding statements of different conditions".
2. Minor, CHANGELOG.md and docs/upgrading.md: `work batch start` writes the corpus blocks and catalogues only where the repository keeps them (`spec_corpus_write.kept`, `batch_catalogues`). Fixed in both.
3. Minor, docs/upgrading.md: an item shaped before 0.37.0 has no `retires:` pairs, so `work line --remove` of its `--retires` line keeps the retired id under `retired:` (backlog_reword keeps an id no pair names). Fixed: a paragraph telling the reader to take the id out by hand after the removal.
4. Minor, CHANGELOG.md: bullets ordered by weight, b314/b315/b232 in one bullet, not grouped by batch as the plan asked. Kept: every item and PR is named.
5. Minor: b324's bullet leaves out that `work batch review` also takes parked lines out as laid; b324's title on main says the opposite of what was built. Kept: the notes follow the code; the title is the item's.
