---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-133/review-1
kind: review
batch: batch-133
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/156
head: e7d637694e9100630e21ecf7ad6b14496f1b79c8
range: 6fceed41f55ab2a590865ff23033e6317a066a91..e7d637694e9100630e21ecf7ad6b14496f1b79c8
result: fix-now
---

# batch-133 review 1

## Verdict

The batch builds every line of b736 (r132-r134), b637 (checking r135, r136 and product r35), and b734's chore check. Every run exits 0, as it did at the base. No test was removed or weakened. The change is +819 -45, under the 1000-line limit. There is one finding to fix now, a module-map gap, plus two hardening observations.

## Findings

### f1 Minor fix now: the module map has no row for checking_handlers_uses.py, and product_handlers_trace's row leaves out r35
- item: b637
- where: CLAUDE.md:335
CLAUDE.md says "A new concern gets a new module and a row here", and the module map is binding.

- **Missing row:** b637 adds `tests/scenarios/checking_handlers_uses.py`, which holds the handlers of checking g135 and g136. It has no row. Every other `checking_handlers_*.py` has its own row, including b736's new `checking_handlers_upstream.py`. The generic `<capability>_handlers*.py` row does not list checking.
- **Stale row:** b637 also extends `tests/scenarios/product_handlers_trace.py` for r35. That adds the ledger's contract at `bounded-context/example.org/fixture/ledger@1.0.0`, its `ledger.post` listing `ledger#r1`, and `uses:` mapping `stock.reserve` to `ledger.post`. Its row at line 335 still says "r26-r30, b644" and does not describe this world.

Fix: add a row for `checking_handlers_uses.py` covering r135, r136 and b637 (the driven port, the nested `adapters/stock-inventory/` holding the inventory contract, `uses:` naming `inventory.debit` or nothing, and `spec --root adapters/stock-inventory check`). Extend product_handlers_trace's row with r35's world.

### f2 Minor observation: a provider requirement is keyed by its bare id, so it can be mistaken for a local one
- item: b637
- where: scripts/product_trace.py:112
A provider's requirement comes from a held contract's `requirements = ["<cap>#r<n>: <text>"]` entry. `provided` keys it by that id alone, without the provider.

- **Hidden:** `own` drops a provider requirement whose id equals one already in the trace (`if r[0] not in held`). If a provider and this context both have, say, `notebook#r1`, the provider's line never appears in `spec trace`.
- **Lost:** in `joined`, two providers' requirements with the same id are folded into one dict entry, so one of them is lost.
- **Misread:** `product_coordination.coordination(root, ctx, list(reqs))` and `model_product`'s text comparison (`local.get(rid) != text`) both look provider ids up in this context's facts. So a colliding id is read as the local line.

I checked `product_coordination.coordination`: it uses `uses.get(q, ())`, so a provider id that does not collide is harmless and nothing crashes. No client hits this today; the fixtures use distinct capability names (`holding`, `ledger`).

Hardening: qualify a provider requirement's key with its provider id, or keep provider requirements in a separate list from the context's own.

### f3 Minor observation: an upstream entry with no `github:` and no adapter spec is now refused with no reason
- item: b736
- where: scripts/contract_obtain.py:47
`_reach` now lets every `Refused` from `contract_registry.retrieve` through, which is what r132 and r133 need.

The risk: an upstream that is listed under `## Upstreams` but has no `github:`. `listed` passes it, and `request_gh.repo_of` then raises its own reasonless refusal ("names no GitHub repository ..."). Before this change, that case reached r103's "no adapter spec has the provider".

The item's notes say `reached` should give a reason in place of `repo_of`'s reasonless refusal. That is now done only for an unlisted upstream. No line names the unhosted-but-listed case, and nothing crashes.

Reproduction: an upstream bullet `- bounded-context/example.org/fixture/inventory: no repository`, no adapter spec, then run `spec obtain bounded-context/example.org/fixture/inventory`. It exits 1 naming no reason.
