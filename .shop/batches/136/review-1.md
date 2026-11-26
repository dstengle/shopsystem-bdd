---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-136/review-1
kind: review
batch: batch-136
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/159
head: d778f401319b44139ac2448a037aaed470d6eb02
range: 67dacacd65ae02a0c276d3d7d2c1e3ee7b296ebf..d778f401319b44139ac2448a037aaed470d6eb02
result: clean
---

# batch-136 review 1

## Verdict

The batch builds both items: product#r36 (b738) and checking#r141 (b739). All four checks exit 0 at the head, and the change is inside the size limit. One minor observation, about the module map.

## Findings

### f1 Minor observation: the module map row of contract_registry_github does not name the new refusal
- item: b739
- where: CLAUDE.md:1
`scripts/contract_registry_github.py` now refuses a second case as `bounded context unreachable` in `reached`. An upstream entry whose bullet names no `github:` is refused there, before any gh call (checking r141).

The module docstring says this, but the module map row in `.shop/worktrees/batch-136/CLAUDE.md` does not. The row still names only "a repository GitHub does not serve refused naming the bounded context and `bounded context unreachable` (`reached`)".

The change already rewrites the product_trace row in the same file, so this row could have been updated at the same time. Fix: add "or an upstream entry that holds no shared store (no `github:`), before any gh call (b739, r141)" to the row. The rest of the change follows the module map.

What I verified for b738:
- `own` keys each provider requirement with `key(provider, rid)` instead of dropping it when `r[0] in held`.
- `joined`'s dict now holds the provider ids apart from the local ones.
- `model_product.read_traces` and `product_coordination.coordination` read only `local` ids.
- `provided` is still kept and still called by `tests/scripts/test_adapter_uses.py`, so the test it serves is unchanged.
- r35's handler now expects the provider-keyed id. That matches the documented output, and no assertion was loosened.

What I verified for b739:
- `request_gh.bullets` and `REPO` exist.
- The bullet check returns `None` for this context's own id, so own-repo reads are untouched.
- `_unreachable` gives the `bounded context unreachable` reason and names the bounded context.
