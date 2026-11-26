---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-131/review-1
kind: review
batch: batch-131
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/154
head: 51c1f499efd61c8a0df348a94432db0a1aaf43a1
range: 5189b42cf024f25456b1848d98a9099b3e4b8095..51c1f499efd61c8a0df348a94432db0a1aaf43a1
result: fix-now
---

# batch-131 review 1

## Verdict

The batch builds b636's nine lines: publish, fetch and obtain go through the contract registry and handle its three replies, and the shop-folder adapter keeps and finds the contracts. One finding to fix: when `spec publish` is given no version, it can now pick a version that is already kept and refuse. That breaks checking#r77, a live line. The other findings are observations.

## Findings

### f1 Important fix now: spec publish with no version can refuse its own default version
- item: b636
- where: scripts/contract_publish.py:52
The default version used to be one past the highest version kept, superseded ones included (`max(kept(root), key=_order)`). It is now one past the published version (`_next(_published(root))`). The published version is not always the highest. The person can publish a lower version explicitly after a higher one, and the higher one is then superseded.

Reproduction:
1. Run `spec publish --version 1.6`.
2. Run `spec publish --version 1.5`. 1.5 is now published and 1.6 is superseded.
3. Run `spec publish` with no version.

At the base, step 3 keeps `1.7`. At Head, `_next("1.5")` gives `1.6`, `_deposited` finds it, and the command refuses with "a contract is kept at the version 1.6 already". checking#r77 ("When the person publishes a contract, the specification service shall keep a contract whose status is `published` ...") names no state, so this is a wrong answer against a live line. No line of b636 asks for the change.

Fix: keep the default past every version deposited. With the port as it is, `_next` can be advanced until `_deposited(root, v)` is false. A test should cover the step 1 to 3 sequence.

### f2 Minor observation: obtain bypasses the port for where an obtained contract is kept, against decision 0139
- item: b636
- where: scripts/contract_obtain.py:18
Decision 0139 says that where a published or obtained contract is kept is an adapter's mechanism behind a driven port, and that no core code names a file location. The item's own technical call is that the core reaches the port through one module, contract_registry.

`contract_obtain` breaks both. It imports `place` straight from the adapter module `contract_registry_folder`, then writes `provider/<id>/<version>/contract.toml` into each adapter spec itself, through `shop_files.committed`. So if `$SHOPSYSTEM_CONTRACT_REGISTRY` names another adapter, retrieval goes through that adapter but the obtained copy is still placed by the shop folder's layout.

The registry model has no operation for keeping an obtained contract, so no line asks for more today. Fixing this needs either a port operation or a decision that the provider/ layout is the core's.

### f3 Minor observation: an unhosted upstream with no adapter spec now gets a different refusal
- item: b636
- where: scripts/contract_obtain.py:42
At the base, `obtain` called `reached` before `holders`. So an upstream with no `github:` under `## Upstreams` was refused by `request_gh.repo_of`, which names the missing `github:` entry.

Now, when no adapter spec holds the upstream, `_reach` re-raises only a refusal whose reason is `bounded context unreachable`. `repo_of`'s refusal has no reason set, so `_reach` swallows it. The command then refuses with `no adapter spec has the provider` (r94/r103), although r103 is written for an `available` provider. Gateway failures (`bounded context failing`) are swallowed the same way.

Reproduction: run `spec obtain bounded-context/x/y/z` where the index has no bullet for that id and no adapter spec names it. No test covers this case.

### f4 Minor observation: no test of a deposit the registry does not complete
- item: b636
- where: tests/scenarios/stand_in_registry.py:28
r128 is about keeping the contract only once the registry completes the deposit. But the stand-in's `deposit` always delegates to the shop-folder adapter and returns its done reply. So no scenario or script test covers a deposit that does not complete.

The branch at scripts/contract_publish.py:65 (refused naming the version, nothing reported) is never run. With the folder adapter, the file is written and committed inside the adapter before the reply. So g128's check that the contract is kept "only once completed" holds trivially.

A stand-in reply that refuses or fails the deposit would show that publish then keeps nothing and names the version.

### f5 Minor observation: the decisions the item's notes say the batch writes are not written
- item: b636
- where: -
The item's notes say the batch writes:
- a technical decision wiring in the shop-folder adapter, as decision 0125 asks;
- the requirement-tier successors of decisions 0139 and 0137, with `work decision --supersedes`, enforced by the new lines.

The Tree's spec/decisions/ holds no new decision. 0137 and 0139 are unchanged, and the code cites 0125 itself as the wiring. These are notes, not requirement lines, so this does not hold the merge.

### f6 Minor observation: the change is over the review size limit
- item: b636
- where: -
The range changes 26 files, +1126 -180, over the 1000-line limit. All of it is b636's. Most comes from the move of the GitHub reading into contract_registry_github and the folder layout into contract_registry_folder, the three new scenario handler modules with their stand-in, and the corpus and CLAUDE.md rows.
