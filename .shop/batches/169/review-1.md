---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-169/review-1
kind: review
batch: batch-169
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/192
head: e11b5fcad1072f86c5f10a633c24f7f0cc1dca9b
range: 2614ffe54c804717dc2ca48a77c7e6f6f50b5d9b..e11b5fcad1072f86c5f10a633c24f7f0cc1dca9b
result: clean
---

# batch-169 review 1

## Verdict

The batch builds b856's chore. The six files it changes are the six the chore names. Every gap in the item's notes is closed:

- getting-started §3 covers the purpose and the base pack, §4 the request-pack verb frame, step 7 the steps after the merge, and §8 the three jobs, g5 and the before-the-first-batch check labelled as such.
- concepts.md lists base and cli.
- commands.md fixes `spec job`'s synopsis, says the product commands commit, and gives `work line` its `--json`.
- shaping-items step 2 and building-a-batch step 7 are done.
- upgrading.md has its "From 0.44 to 0.45" section.

All runs exit 0, as they did at the base, and the change is well under the size limit. I checked these claims against the tree and each holds:

- The commit subject `spec job: <id>` is what `scripts/product_cli.py:29` writes.
- The synopsis showing `--actor` as required is right: argparse does not require it, but product_layer refuses a job with no product actor (product r62).
- The example's notes.md has g5 "A removed note is not removed again" serving `clear-notes`, and groups serving `find-notes` and `clear-notes`.
- The targets of the new references exist: talking-with-claude.md has "Your product and its jobs", recipes.md has "Add a word to the vocabulary" and its "A word a pack already has" paragraph, and shaping-items has "The product and its jobs".

One polish finding only.

## Findings

### f1 Minor drop: one rewrapped paragraph of getting-started runs past the page's line width
- item: b856
- where: docs/getting-started.md:183
The paragraph about the example's g5 has one line of about 190 characters, where the rest of the page wraps at 120. It renders the same, so this is source polish only. Fix: rewrap the paragraph.
