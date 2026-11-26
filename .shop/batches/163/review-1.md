---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-163/review-1
kind: review
batch: batch-163
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/186
head: 5cda4d7c5df65589f49bc14b6e1e24f9fa8e24ec
range: 376ba72a45c936cbd9dec012283be2f9405d8b26..5cda4d7c5df65589f49bc14b6e1e24f9fa8e24ec
result: clean
---

# batch-163 review 1

## Verdict

The batch builds b838's chore. The notes example now belongs to a product: it has a product file, each group has a `serves:` line, and `spec trace` runs on it. `docs/talking-with-claude.md` gains the "Your product and its jobs" section, which walks what the person says, what Claude runs, what the person sees and what comes of it. Getting-started, the tour and concepts now link to that section and the example instead of repeating the commands. Every run exits 0, the diff touches no test, and the change (+369 -80) is within the limit. I found nothing to fix now. There is one observation.

## Findings

### f1 Minor observation: the example gains a requirement and program behaviour the item's notes do not name
- item: b838
- where: docs/examples/notes-cli/notes.py:42
The item's notes ask for the example to be made a product's context, with its groups dedicated to jobs. The batch goes further. It adds a new requirement, notes#r5 ("If the person removes a note whose status is `removed`, then the notes service shall refuse the request."), as group g5 with its scenario and its cli.toml annotation. It also makes `notes.py` refuse a second remove (exit 1, "note %d is removed already"). These files are all in the chore's `docs/examples/notes-cli` scope, and r5 serves a purpose: it shows `work line --into ... --serves <job>` in talking-with-claude.md. What I checked:
- The two refusal messages the docs quote match the code: `scripts/backlog_serves.py:111` and `scripts/product_trace.py:167-169`.
- The README's table, its tree ("five groups, five lines"), the cli.toml block and the feature block agree with the files the change leaves.

Even so, the change gives the example program new behaviour that no item line names. Nothing runs the example's `notes.feature` against `notes.py`, so this refusal is not tested. It is recorded here and does not hold the merge.
