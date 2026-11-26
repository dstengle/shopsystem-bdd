---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-121/review-1
kind: review
batch: batch-121
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/144
head: 78a31713f80748518b6c169d67a675a8d6e607a1
range: 3d21edea4901823219f355bbcfbf83a1aac0e7be..78a31713f80748518b6c169d67a675a8d6e607a1
result: fix-now
---

# batch-121 review 1

## Verdict

Both items are built: b697 builds review-guarantees#r13 and b666 builds shop#r6. There are two findings to fix on b666. When no product file is kept, the shop still refuses ids in the way the retired shop#r2 did, and no live line asks for that. The refusal's reason also no longer matches the reason the restated `shop.keep` operation declares.

## Findings

### f1 Important fix now: the shop still refuses as the retired r2 did when no product file is kept
- item: b666
- where: scripts/shop_contexts.py:26
b666 retires shop#r2. Its replacement, shop#r6, only refuses "while the product of the shop has an id". When no product file is kept, there is no product id, r6 does not apply, and shop#r1 ("the shop service shall keep the bounded context in the shop") is the only line on the request. But `product_id` falls back to this bounded context's id less its last part, and `keep` refuses any id outside that path.

```python
    if (Path(root) / product_store.REL).is_file():
        return product_store.read(root).get("id") or ""
    return shop_files.context_path(root).rpartition("/")[0]
```

So a refusal that no live line asks for remains, and it goes against r1. This is the case in this repository right now, which keeps no `.shop/product/product.toml` (I looked under the Tree), so r6 has no effect here and only the retired r2 behaviour runs. Fix: when no product file is kept, do not refuse an id for lying outside the product (r1 keeps it). If the refusal is wanted, give it a line of its own on the item instead (`work line` and `work batch amend`).

### f2 Minor fix now: the refusal's reason is not the reason the restated operation declares
- item: b666
- where: scripts/shop_contexts.py:59
b666 restates `shop.keep` in spec/model/execution.md:108 with the refusal reason `id outside the product`, but `keep` still refuses with `reason="id outside the product id"`. Under `--json`, the response envelope carries a reason the domain model does not declare. product_map's own refusal (scripts/product_map.py:40) already uses `id outside the product`. Fix: set the reason to `id outside the product`. Consider also changing the message's "outside the product id %s of this shop" to name the product.

### f3 Minor observation: the reference page still says the shop's product id is this context's id less its last part
- item: b666
- where: docs/reference/commands.md:668
The section on `shop work context keep` still reads: "The shop's product id is the id of this bounded context less `bounded-context/` and its last part". b666 makes the product id the product's id, read off the product file. The change touched CLAUDE.md and the module docstring but not this page.

### f4 Minor observation: ids without the `bounded-context/` prefix are now kept
- item: b666
- where: scripts/shop_contexts.py:57
The removed `shop_contexts.covers` required `ident.startswith("bounded-context/<product>/")`. `product_map.covers` calls `removeprefix("bounded-context/")` first, so `shop work context keep missingmass.io/shopsystem/x` is now kept as a bare id, where it was refused before. That id is not in the context id form the parser's help names (`bounded-context/<product id>/<name>`). No line names the form, so this is hardening. Reproduction: run `work context keep missingmass.io/shopsystem/x` in a context under `missingmass.io/shopsystem` with no product file; it prints `kept missingmass.io/shopsystem/x`.

### f5 Minor observation: product#r18 now reads differently with its text unchanged, and its new Then cannot fail
- item: b666
- where: grammar/corpus/spec/product.md:115
b666's model change gives a shop a product (`has → product`). As a result, R2 binds "the product" in the live line product#r18 to the image of the declared shop (`of(x7, x5)`), not to the indexical "the product this bounded context belongs to". The line's meaning changes while its id and text stay the same, which comes close to decision 0085 (requirements-retired-never-edited). The new generated Then "the shop s2 has the product p1" is checked by `shop_has` (tests/scenarios/product_handlers_map.py:99). That check asserts that the product's id covers the shop's id, but both values come from the scenario world (`example.org/...`, `example.org/shop-<s>`), so nothing the implementation does can make it fail. Consider retiring r18 for a line that says which product is meant, or making the handler read a relation the implementation actually keeps.

### f6 Minor observation: a commit citing b697 carries b666's regenerated product feature and its handler
- item: b697
- where: features/product.feature:180
Commit 4063b236b cites b697 but repeats b666's 6bdb49bb8 (product.feature and product_handlers_map.py), which no line of b697 asks for. The two branches merged cleanly because the changes are byte-identical. This was a workaround for the stale lay, and the net change is right. Recorded only so that the change is credited to b666.
