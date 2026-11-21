---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-71/review-2
kind: review
batch: batch-71
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/95
head: eff873b770c39220e2031fe5942cb9f931a8d9a2
range: 04fbfeb99d7f21f58391f8275202edf57df048ba..eff873b770c39220e2031fe5942cb9f931a8d9a2
result: clean
---

# batch-71 review 2

## Verdict

The fix takes the item-reference rule out of `Model.check_refs` and points superseded decision 0113's `source:` at quote-42, as finding f1 asked. f1 is fixed, and all five runs exit 0 at the head. One minor observation on how 0113 was edited.

## Findings

### f5 Minor observation: 0113's `source:` was edited by hand
- item: b516
- where: spec/decisions/0113-the-batch-agents.md:9
Commit 82cf29843 rewrites the frontmatter of a design-decision that is already committed and superseded. It changes `source: [item/missingmass.io/shopsystem/shopsystem-bdd/b34]` to `source: [quote-42]` in place. `CLAUDE.md` says a design-decision is written by `work decision`, never by hand. `work decision --amend` (scripts/decision_amend.py) only adds `enforced_by` and `rests_on`, so no command could have made this change. The new citation is valid: `.shop/quotes/42.md` exists in the tree, and 0114, which is accepted and restates 0113, cites the same quote. `spec decisions --check` says the index is current. The edit fixes a dangling reference rather than changing what the decision decides, so it need not hold the merge. If decisions should be able to correct their sources, an item could give `--amend` a `--source` (compare b522).

## Earlier findings
- f1: fixed
