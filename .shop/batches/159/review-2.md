---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-159/review-2
kind: review
batch: batch-159
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/182
head: ad6c560b436c928f05326403cd61820f9c14c48f
range: c76c6b797c0b8b50acead5fc48056a0dbeac34b3..ad6c560b436c928f05326403cd61820f9c14c48f
result: clean
---

# batch-159 review 2

## Verdict

The fix rewords product#r68 on b814. The line's condition is now that no capability has a requirement group that serves the job. That is the one case where the code refuses: `product_trace.trace` refuses inside `if found is None:` at scripts/product_trace.py:165, and `found` is `None` only when no live group serves the job.

The other files follow the reworded line:
- The feature's Given was regenerated.
- The corpus block was written again, and its form now has `not [x4: capability, x5: requirement group] serve(x5, x3), of(x5, x4)`.
- The `cli.toml` annotation was updated.

`features generate --check` exits 0. The scenario's new Given opens with "no ", so `product_handlers_trace.given_does` reads it. The `item` branch of `build` still writes the item that holds the group and traces without `--item`, so the scenario checks the reworded line. The id is reworded in place, but r68 is a line of b814 that has never been on the base, so the rule against editing requirements is not broken.

I found nothing new to fix now. There is one observation.

## Findings

### f4 Minor observation: the amend on the batch branch dropped backlog_term_rules from grammar/rules.md, and a later commit put it back
- item: b810
- where: grammar/rules.md:1016
Commit 260c73b64 is the amend of b814 relaid on `batch-159`. It wrote `grammar/rules.md` again without `scripts/backlog_term_rules.py` in the `Implemented in:` lines of v_t4, v_t7, v_t11 and v_t19. That module is b810's, and it exists in the tree. Commit 219fd74df, citing b810, wrote the catalogue again with the module back. The range's net change to `grammar/rules.md` is empty, so nothing is wrong at `Head:`.

The amend's catalogue rewrite (batch_catalogues, run from the laying service's prepare) seems to have run where b810's module was not visible to it. The cause may be the generator's tree or the task's worktree, not the batch's. If so, every later `work batch amend` in a batch with another item's catalogue change will undo that change until someone writes the catalogue again by hand.

To reproduce: in a batch where one item adds a module that model.lp's rule catalogue names, amend another item and compare `grammar/rules.md` on `batch-<n>` before and after.

## Earlier findings
- f1: fixed
