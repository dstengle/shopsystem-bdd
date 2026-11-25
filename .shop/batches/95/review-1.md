---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-95/review-1
kind: review
batch: batch-95
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/118
head: 4cf9d17cb1f8d4fc04151dc18e238cea9e2afbcf
range: e373b1ba69de82c56b414fc6d237b01db859a7e9..4cf9d17cb1f8d4fc04151dc18e238cea9e2afbcf
result: fix-now
---

# batch-95 review 1

## Verdict

Both items are built. b595's two checks (r92, r93) do what their lines say, and each scenario fails before the fix. b593 keeps the contract inside each adapter spec of its provider, as r91 and decision 0136 ask. But it also adds a refusal that no line asks for, and that refusal breaks r81 and r89 when no adapter spec names the upstream. The module map also still describes the old place where a contract is kept. Two findings to fix and one observation.

## Findings

### f1 Important fix now: `spec obtain` refuses an upstream that no adapter spec names, which no line asks for and which breaks r81 and r89
- item: b593
- where: scripts/contract_obtain.py:139
r81 has no condition: "When the person obtains a contract from a bounded context, the specification service shall keep the contract and keep no context request." r91 only adds where the contract goes while an adapter spec has the provider. No line of the batch says what happens when no adapter spec has it. The change adds a new refusal, with the reason `no adapter spec has the provider`:

```python
    held = holders(root, context)
    if not held:
        raise Refused("the bounded context {names} is the provider of no adapter spec under %s/: no adapter spec has "
```

So in a context with no `adapters/<name>/` naming the upstream, r81's obtain is now refused instead of keeping the contract. The check also runs before `published` and `_reach`. For an unreachable upstream that no adapter spec names, the refusal therefore gives `no adapter spec has the provider`, not r89's `bounded context unreachable` reason. The scenario handlers hide this: `checking_handlers_obtain.build` always writes an adapter spec that names every bounded context obtained from, unless the scenario brings in an adapter spec of its own (`provides = w["provides"] or "adapter spec" not in w["kinds"].values()`). So r81 and r89's scenarios never reach the state where they would fail.

Fix, either way:
- Give the refusal a line. Retire r81 with `work line --retires checking#r81` for a line conditioned on an adapter spec that has the provider. Add an If line for the refusal, run `work batch amend b593`, and check the upstream's reach before looking for holders, so r89 keeps its reason.
- Or drop the refusal and the code path, keeping only what r91 asks.

### f2 Minor fix now: module-map rows of contract_obtain and its scenario handlers still describe the root `provider/`
- item: b593
- where: CLAUDE.md:157
The change edits `model_adapter.py`'s row but leaves three other rows stale:
- `scripts/contract_obtain.py`'s row still says the contract is "kept byte for byte as `provider/<id's path>/<version>/contract.toml`". It does not name `holders`, r91, b593, keeping the contract under each adapter spec's folder, or the new refusal.
- `tests/scenarios/checking_handlers_obtain.py`'s row still says the Thens read "the contract kept under `provider/example.org/fixture/inventory/1.2.0/`". It names neither g91 nor the nested adapter spec `ADAPTER`.
- `tests/scenarios/checking_handlers_adapter.py`'s row names only r84-r87. It leaves out r92 and r93, the `stock-elsewhere` id and the `1.*` version.

CLAUDE.md's module map is binding. Fix: rewrite those three rows to say what the modules now do.

### f3 Minor observation: an obtained version is written into every adapter spec of the provider, whatever version it pins
- item: -
- where: scripts/contract_obtain.py:220
`holders` matches a `providers:` entry at any version. So `spec obtain <ctx>` with no `--version` writes the published contract, say `1.3.0`, into an adapter spec that pins `<ctx>@1.2.0`. That spec's r86 check still fails, now next to a contract it does not read.

Reproduction:
1. An adapter spec whose `providers: [bounded-context/example.org/fixture/inventory@1.2.0]`.
2. The upstream publishes `1.3.0`.
3. `spec obtain bounded-context/example.org/fixture/inventory` writes `adapters/<name>/provider/example.org/fixture/inventory/1.3.0/contract.toml`.
4. `spec --root adapters/<name> check` still names the provider.

No line names this case. It could be settled later by a line, for example: obtain the pinned version for a spec that pins one.
