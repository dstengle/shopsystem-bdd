# supervision, formulate round 1: reply

## Coverage

| id | line | scenario |
|---|---|---|
| r219 | "**If** a scenario fails in a run that `work run` makes before a merge and its failure would keep r4 from merging the work-item branch, **then** `work run` shall run that scenario again once, alone, before it refuses the merge." | none: returned as a question (below) |
| r220 | "**If** the second run of a scenario that r219 makes also fails, **then** `work run` shall give both runs of the scenario in the question r131 writes for the work-item." | a scenario that fails again on its second run, alone, has both its runs in the question written for the work-item |

## Questions

- r219: "**If** a scenario fails in a run that `work run` makes before a merge and its failure would keep r4 from merging the work-item branch, **then** `work run` shall run that scenario again once, alone, before it refuses the merge."
  - Reading 1: the merge is refused whatever the second run gives; the second run only adds evidence (for r220's question).
  - Reading 2: the merge is refused only if the second run also fails; a scenario that passes on its second run no longer keeps r4 from merging, and the branch is merged.

## Cases no line mentions

- A scenario that passes on its second run: whether anything is recorded of its first failure (in the work-item, the log or the implementer's stage directory).
- A test of the suite that fails and is not a scenario (r55 keeps such tests): whether it is run again too.
- A check that a work-item names in place of scenarios, failing before a merge: whether it is run again.
- Where `.shop/delivery.toml` gives `[tests]` (r29): how `work run` runs one scenario alone with the repository's commands.
- A second run that fails for a reason other than the first run's: whether the question says the two differ.
- Several scenarios failing in one run: whether each is run again alone, one after another, and whether one passing second run and one failing one merge nothing.

## Drafts

- /tmp/work-run-i62-2un7ny7b/supervision-9-formulate/.shop/scratch/9-formulate/drafts/round-1/supervision.feature
- /tmp/work-run-i62-2un7ny7b/supervision-9-formulate/.shop/scratch/9-formulate/drafts/round-1/supervision.reply.md
