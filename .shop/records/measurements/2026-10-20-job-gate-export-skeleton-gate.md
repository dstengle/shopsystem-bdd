---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-20-job-gate-export-skeleton-gate
kind: measurement
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-20
---

# Skeleton Gate: the person's verdicts

The person's verdicts on the Skeleton Gate page (i10's walking skeleton, the proof run before release 0.21.0), exported from the page's review store and copied out of a job workspace on 2026-10-22. `at` is the save time in epoch milliseconds: 2026-10-20, 17:57-18:05 UTC. Each `question-<short>` file answers the card of that `short` in `skeleton-gate.html` (initiative-archive/2026-10-21-job-gate-pages): result, lines, python, haiku, migrate. The notes are the person's own words, kept exactly: both `change` verdicts ask that lines be written in EARS before committing.

Archived from git-ignored scratch; each file's text as it was.

## `.shop/scratch/gate-export/skeleton-gate/verdicts/question-haiku.json`

~~~~~~
{
  "at": 1792519360270,
  "note": "",
  "type": "initiative",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/skeleton-gate/verdicts/question-lines.json`

~~~~~~
{
  "at": 1792519476120,
  "note": "These lines do not appear to be written in EARS format. Please fix before committing ",
  "type": "initiative",
  "verdict": "change"
}
~~~~~~

## `.shop/scratch/gate-export/skeleton-gate/verdicts/question-migrate.json`

~~~~~~
{
  "at": 1792519491067,
  "note": "The lines do not appear to be written in the proper EARS syntax. Please fix before committing.",
  "type": "initiative",
  "verdict": "change"
}
~~~~~~

## `.shop/scratch/gate-export/skeleton-gate/verdicts/question-python.json`

~~~~~~
{
  "at": 1792519338918,
  "note": "",
  "type": "initiative",
  "verdict": "approve"
}
~~~~~~

## `.shop/scratch/gate-export/skeleton-gate/verdicts/question-result.json`

~~~~~~
{
  "at": 1792519022707,
  "note": "",
  "type": "initiative",
  "verdict": "approve"
}
~~~~~~
