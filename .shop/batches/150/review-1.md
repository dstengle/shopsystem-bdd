---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-150/review-1
kind: review
batch: batch-150
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/173
head: 2c0c89ba56bf8632dc9c723ed16bbe2a40406f39
range: 632e7cb61ff30d792e2c0a22634b7c4860e6584d..2c0c89ba56bf8632dc9c723ed16bbe2a40406f39
result: clean
---

# batch-150 review 1

## Verdict

The batch builds b770's chore. `inputs` now also passes `spec/packs`, `spec/model`, `spec/vocabulary` or `spec/capabilities`, and the pathspec `provider/*/contract.toml` to `git status`, so taking out the last file of a folder, or a provider contract, is seen. The new parametrized test selected by `-k last_of_its_folder` covers both cases. The commits touch only the two chore files. Every run exits 0, as it did at the base. The change is 2 files, +23 -2. No test was removed or weakened, and no rule or judgement decision is broken. One hardening observation follows.

## Findings

### f1 Minor observation: the provider pathspec is tested only one folder deep, but real contracts sit deeper
- item: b770
- where: scripts/batch_reached.py:20
`contract_registry_folder.place` (scripts/contract_registry_folder.py:40) keeps a contract at `provider/<id's path>/<version>/contract.toml`, several folders below `provider/`. `PROVIDED` is `provider/*/contract.toml`, and its comment calls it "every provider contract". That is only true because git's default pathspec `*` also matches `/`. The new test uses `provider/stock/contract.toml`, which is one level deep, so it would still pass if the pathspec ever stopped matching across folders (for example under `:(glob)` magic, or if `GIT_GLOB_PATHSPECS` were set). The risk was a pathspec that misses the real layout. I checked `place` and the default meaning of a git pathspec, and the deeper layout is matched today.

Reproduction: add the case `provider/missingmass.io/shop/ctx/1.0.0/contract.toml` to the test's parametrize list. The fix is either that case, or writing the pathspec as `provider/**/contract.toml` with `:(glob)` magic so the depth is stated. Separately, `reached` now counts a provider contract change in a context that is not an adapter spec, where spec_held reads no such contract. The cost is an extra regeneration, not a wrong answer.
