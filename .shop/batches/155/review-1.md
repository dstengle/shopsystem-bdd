---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-155/review-1
kind: review
batch: batch-155
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/178
head: c6330214e7448caf5306344423dfb90eb294fe66
range: 8b4b7fe67f5d392ac0f9d4acfb9bcfc33c164369..c6330214e7448caf5306344423dfb90eb294fe66
result: fix-now
---

# batch-155 review 1

## Verdict

The batch builds all thirteen of b795's lines, and the scenarios check each one. All five runs exit 0, as they do at the base. There is one finding to fix: every drop now refuses something the product does not hold, and no line asks for that refusal.

## Findings

### f1 Important fix now: a drop of something the product does not hold is refused, which no line asks for
- item: b795
- where: scripts/product_drop.py:15
`_held` refuses `drop_job`, `drop_subdomain` and `drop_context` when the product does not hold the thing (`job outside the product`, `subdomain outside the product`, `bounded context outside the product`). `drop_actor` does the same at scripts/product_drop.py:59 (`product actor outside the product`). No requirement of b795 asks for these refusals. r52, r46, r48 and r56 say only that the service does not keep the thing and completes the request. The product capability has no Implementation section that gives them either.

The domain model does not declare these reasons. The operations added at spec/model/specification.md:463-467 list only the reasons that r45, r47, r49 and r53-r57 state:

```
operation drop job(job)  outcomes: done → the job | refused: job a job needs, job a bounded context holds, job a subdomain serves
```

So the code has a refusal outcome that neither the lines nor the model carry, and the docs (docs/reference/commands.md, "A job the product does not hold is refused naming it") describe behaviour that is not specified.

Fix, on b795's branch, one of two ways:
- Add a line for each of these refusals to b795 (for example "If the person drops a job that is not in the product, then the product service shall refuse the request and name the job."), with the reason added to each drop operation's `refused:` in the model.
- Or take the four refusals out, so that dropping an id the product does not hold completes with the product unchanged.

### f2 Minor observation: the module map has no row for the new scenario handlers
- item: -
- where: CLAUDE.md:285
`tests/scenarios/product_handlers_drop.py` is a new module with its own concern: the Givens kept as relations, the product file written at the When, and the Thens of unassign and drop. Its sibling handlers each have their own row (product_handlers_trace, product_handlers_assign, product_handlers_coordination). This one is covered only by the generic `<capability>_handlers*.py` row. CLAUDE.md says "A new concern gets a new module and a row here."

### f3 Minor observation: the new groups sit in the capability file out of id order
- item: -
- where: spec/capabilities/product.md:194
The renumbered groups were laid as g50-g57 followed by g45-g49, and features/product.feature has them in its own order. Nothing breaks, but a reader of the capability file meets g45 after g57.
