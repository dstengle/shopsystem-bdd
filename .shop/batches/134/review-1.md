---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-134/review-1
kind: review
batch: batch-134
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/157
head: 3ec52a8b90d6add5414038dbfd61ca3d0109a971
range: 09b98f032cac48fac3a6362e8ee508693d5ec2b7..3ec52a8b90d6add5414038dbfd61ca3d0109a971
result: fix-now
---

# batch-134 review 1

## Verdict

The batch builds b732's scenarios#r47 and b735's checking#r137 to r140 and contract-registry#r4. The b735 branch also changes how `spec check` reads decisions, and no requirement line asks for that: one finding to fix. Every run in `## Runs` exits 0, as it did at the base. The change is 939 changed lines, under the limit of 1000.

## Findings

### f1 Important fix now: spec check stops reporting a retired requirement that a superseded or rejected decision names, and no line asks for it
- item: b735
- where: scripts/model_work.py:66
Commit bd1b80f7c adds `retired_history`. It changes what `spec check` reports: a requirement id in a decision's `enforced_by` used to be an unresolved reference when its capability had retired it. Now it is silently accepted when the decision is `superseded` or `rejected`. Nothing in b735 asks for this:
- its lines are checking#r137 to r140 and contract-registry#r4, all about obtaining and registering a contract;
- no live requirement says that a decision no longer in force may name a retired requirement (searched spec/capabilities for `superseded` and `rejected`; decisions#r1 and review-guarantees#r12 are about other things);
- no capability's Implementation section gives it.

The change was made so that decision 0137 (now superseded, `enforced_by: [checking#r91]`) stops showing as dangling after r91 was retired. It is still a new behaviour of `spec check` that every context gets, it has its own test (tests/scripts/test_model_work.py), and no line traces to it.

Fix: give the item a requirement line for it, in the capability that owns `spec check`'s reference checks (for example, while a design-decision is `superseded` and names a retired requirement, `spec check` completes and does not name the requirement), then `work batch amend b735`. The other way is to drop the code and settle 0137's reference without changing the check.

### f2 Minor observation: a later refused registration leaves the earlier adapter specs' contracts committed
- item: b735
- where: scripts/contract_obtain.py:84
Before this batch, `obtain` wrote every adapter spec's contract in one `shop_files.committed`. Now it requests one `register` per adapter spec, and the shop-folder adapter commits each one separately (scripts/contract_registry_folder.py:56-65). When the provider has two adapter specs and the registry completes the first and refuses the second, the command exits 1 naming the second adapter spec, but the first contract is already committed.

r140's "change nothing" can be read as about the reply to that one refusal, so this does not hold the merge. Still, the command now refuses after it has changed the repository, which it did not do before. Related: tests/scripts/test_contract_obtain.py:149 was loosened from "both contracts in the HEAD commit" to "both somewhere in head..HEAD", to match the one-commit-per-adapter-spec behaviour.

Reproduction: two adapter specs naming the upstream, and `$STAND_IN_REGISTRY_REPLY=refuse` applied only to the second register call. `spec obtain` exits 1 and leaves the first contract's commit in place.

### f3 Minor observation: no counter-example at all when "no" boxes deny every other value
- item: b732
- where: scripts/spec_steps4_counter.py:71
`counter` now returns `[]` when `values(...) == []`, that is, when "no" boxes in the precondition deny every other value of the restriction's attribute. In that case the feature gets no counter-example. scenarios#r47 says the scenarios service "shall keep a counter-example that does not use the code", and its precondition does not rule this case out. No line names this edge and no consumer line produces it today (the `excluded` world keeps `high`), so it is hardening. Better options are to fall back to the negated atom (`r.cond(atom, False)`), as `unmet` already does for an atom with no attribute values, or to raise a TraceError naming the line.

### f4 Minor observation: the CLAUDE.md rows of the contract modules cite decision 0147, not the new decision 0149
- item: b735
- where: CLAUDE.md:12
The rows of `scripts/contract_obtain.py` and `scripts/contract_registry.py` were rewritten for b735. They cite "decision 0147", and the contract_obtain row dropped 0136. The decision that now governs `register` is 0149, which supersedes 0137, and neither row names it. The module docstring of contract_obtain likewise names 0147 only. Fix: add 0149 to both rows.
