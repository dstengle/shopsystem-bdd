---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-107/review-1
kind: review
batch: batch-107
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/130
head: 5d7fe97ceac464d5bf84e69872d7e0dd0b9f17d1
range: 14d07bc8777128d68d2a44b411ad1c3aed18e348..5d7fe97ceac464d5bf84e69872d7e0dd0b9f17d1
result: fix-now
---

# batch-107 review 1

## Verdict

Both items build their lines. b663 needed no code change, because batch_pick already checks the review limit before the bar, and it rebuilds r130 and r131 by retiring r101 and r107. b576 builds shop r1-r5, but it also refuses an id that is not in the context id form. That refusal is b650's line, not this batch's, so it is one finding to fix. Two observations go with it.

## Findings

### f1 Important fix now: work context keep refuses an id out of the context id form, which no line of the batch asks for
- item: b576
- where: scripts/shop_contexts.py:421
`keep` refuses an id that does not match migrate_init's `FORM` before it checks the product id:

```
if not FORM.fullmatch(ident):
    raise Refused("{names} is not in the context id form bounded-context/<domain>/<path>",
                  reason="id not in the context id form", names=names)
```

No line of this batch asks for this. b576's notes say "The id-form refusal line went to b650", and b650 is still `shaped`, with that line ("If the person entrusts a bounded context with an id that does not conform to the context id form, then the shop service shall refuse the request").

The refusal also cuts into a case r1 covers. The vocabulary defines `id` as "The `id` field of a file's frontmatter", not as an id in the context id form. Take an id such as `bounded-context/missingmass.io/shopsystem/A B`: the product id covers it (`covers` passes), so r2 and r3 do not refuse it, and r1 says the shop service keeps it and completes the request. The code refuses it instead.

Fix: take the form check out of `keep` and leave it to b650, along with:
- the `id not in the context id form` reason in the model line,
- the sentence in docs/reference/commands.md,
- the mention in the CLAUDE.md row.

The other fix is to bring b650's line into this batch with `work batch amend`.

### f2 Minor observation: CLAUDE.md's batch_pick row still says an item that fails the bar is returned `shaped` whatever its estimate
- item: b663
- where: CLAUDE.md
The `scripts/batch_pick.py` row says "one that fails the bar alone returned `shaped` whatever its estimate". That contradicts batches#r131, which this batch builds: an item past the review limit is not allocated, whether it meets the bar or not.

The code matches r131. batch_pick.py:68 checks `batch_estimate.exceeds` before `_alone` runs the bar, and its docstring says so. Only the module map row is out of date; it has been since b640, and b663 is the item that states this behaviour.

The `batches_handlers_limit.py` part of the batches_handlers4 row names r93 and r94 only. It does not mention that lines an earlier Given gave the item are now kept (r130).

### f3 Minor observation: r131's scenario covers only an item past the limit that meets the bar
- item: b663
- where: features/batches.feature:891
r131's group title says "whether or not it meets the bar". Its generated scenario gives no bar Given, though, and `exceeds` in tests/scenarios/batches_handlers_limit.py then gives the item `OWN` lines, which meet the bar. So nothing tests the case b663 was raised for: an item past the limit that fails the bar.

The code handles that case correctly (batch_pick.py:68-70 skips the bar for such an item). A script test of `batch_pick` with an item that is past the limit and fails the bar would pin it down.
